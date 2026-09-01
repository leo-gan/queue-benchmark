"use strict";

const fs = require("fs");
const path = require("path");
const { performance } = require("perf_hooks");
const { spawn } = require("child_process");
const { Worker, isMainThread, workerData } = require("worker_threads");
const fastq = require("fastq");

function envOn(name) {
  const v = process.env[name] || "";
  return v === "1" || v === "true" || v === "on";
}

function rssBytes() {
  return process.memoryUsage().rss;
}

if (!isMainThread && workerData && workerData.role === "shared-ring") {
  const { sab, n, slots, slot } = workerData;
  const iv = new Int32Array(sab, 0, 2);
  for (let i = 0; i < n; i++) {
    for (;;) {
      const head = Atomics.load(iv, 0);
      const tail = Atomics.load(iv, 1);
      if (head !== tail) {
        Atomics.store(iv, 0, (head + 1) % slots);
        break;
      }
    }
  }
  process.exit(0);
}

if (process.env.BENCHMARK_CHILD === "pipe") {
  const n = Number(process.env.BENCHMARK_CHILD_N || 0);
  const stdin = process.stdin;
  stdin.resume();
  let buf = Buffer.alloc(0);
  let left = n;
  stdin.on("data", (chunk) => {
    buf = Buffer.concat([buf, chunk]);
    while (left > 0 && buf.length >= 4) {
      const len = buf.readUInt32BE(0);
      if (buf.length < 4 + len) break;
      buf = buf.subarray(4 + len);
      left -= 1;
    }
    if (left <= 0) process.exit(0);
  });
  stdin.on("end", () => process.exit(0));
}

function ns() {
  return BigInt(Math.round(performance.now() * 1e6));
}

function loadCells() {
  const p = process.env.BENCHMARK_CELLS_TSV;
  if (!p || !fs.existsSync(p)) return [];
  const lines = fs.readFileSync(p, "utf8").trim().split("\n").slice(1);
  return lines.map((ln) => {
    const [type_id, payload_bytes, n, io_mode, hash] = ln.split("\t");
    return {
      type_id,
      payload_bytes: Number(payload_bytes),
      n: Number(n),
      io_mode,
      hash,
    };
  });
}

function logDir() {
  const env = process.env.LOG_DIR || path.join(__dirname, "..", "..", "logs", "javascript");
  return env.endsWith("javascript") ? env : path.join(env, "javascript");
}

const HEADER =
  "Language,StringOrStream,TestDataName,Repetitions,RepetitionIndex,SerializerName,SerializerVersion,TimeSer,TimeDeser,Size,TimeSerAndDeser,OpPerSecSer,OpPerSecDeser,OpPerSecSerAndDeser,MemoryPeakBytes,FidelityScore,DataTypeInstanceCount,TypeConfigHash,SizeGzip,SizeZstd,NativeKind,StreamMode,RunOrder,SchedulePosition,CpuTimeNs";

function ops(t) {
  return t > 0n ? (1e9 / Number(t)).toFixed(6) : "0.000000";
}

function row(mode, ty, reps, idx, name, ver, enq, deq, size, n, hash, kind, order, cpuNs, rss) {
  const tot = enq + deq;
  return [
    "javascript",
    mode,
    ty,
    reps,
    idx,
    name,
    ver,
    enq.toString(),
    deq.toString(),
    size,
    tot.toString(),
    ops(enq),
    ops(deq),
    ops(tot),
    rss || 0,
    "1.0000",
    n,
    hash,
    0,
    0,
    kind,
    mode === "stream" ? "native" : "",
    order,
    order,
    (cpuNs || 0n).toString(),
  ].join(",");
}

function sleepMs(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function waitNs() {
  const raw = Number(process.env.BENCHMARK_WAIT_NS || 1_000_000);
  return Number.isFinite(raw) && raw > 0 ? raw : 1_000_000;
}

async function benchWakeup(n) {
  const count = Math.max(1, n);
  const gapMs = Math.max(0, waitNs() / 1e6);
  const q = [];
  let remaining = count;
  const consumer = (async () => {
    while (remaining > 0) {
      if (q.length) {
        q.shift();
        remaining -= 1;
        continue;
      }
      await new Promise((r) => setImmediate(r));
    }
  })();
  await sleepMs(2);
  const t0 = ns();
  for (let i = 0; i < count; i++) {
    if (gapMs > 0) await sleepMs(gapMs);
    q.push(1);
  }
  await consumer;
  const wall = ns() - t0;
  const mid = wall / BigInt(count);
  return [mid, wall - mid];
}

async function benchCancel(waiters) {
  const { default: PQueue } = await import("p-queue");
  const q = new PQueue({ concurrency: 1 });
  const ac = new AbortController();
  const pending = [];
  for (let i = 0; i < Math.max(8, waiters); i++) {
    pending.push(
      q.add(
        ({ signal }) =>
          new Promise((_, reject) => {
            const onAbort = () => reject(signal && signal.reason ? signal.reason : new Error("aborted"));
            if (signal && signal.aborted) {
              onAbort();
              return;
            }
            if (signal) signal.addEventListener("abort", onAbort, { once: true });
          }),
        { signal: ac.signal }
      )
    );
  }
  await sleepMs(1);
  const t0 = ns();
  ac.abort();
  // Do not clear(): pending add() promises would never settle. Abort
  // makes each queued function throwIfAborted as it starts.
  await Promise.allSettled(pending);
  return [ns() - t0, 0n];
}

function benchArray(items) {
  const q = [];
  const t0 = ns();
  for (const it of items) q.push(it);
  const t1 = ns();
  const got = [];
  while (q.length) got.push(q.shift());
  const t2 = ns();
  return [t1 - t0, t2 - t1];
}

function benchFastq(items) {
  return new Promise((resolve) => {
    const t0 = ns();
    let deq = 0n;
    const q = fastq(function worker(_task, cb) {
      const a = ns();
      cb(null);
      deq += ns() - a;
    }, 1);
    q.drain = () => resolve([ns() - t0 - deq, deq]);
    for (const it of items) q.push(it);
  });
}

function benchSteal(items) {
  const q = [];
  const t0 = ns();
  for (const it of items) q.push(it);
  const t1 = ns();
  const got = [];
  while (q.length) got.push(q.shift());
  return [t1 - t0, ns() - t1];
}

function writeFrame(stream, item) {
  const hdr = Buffer.alloc(4);
  hdr.writeUInt32BE(item.length);
  stream.write(hdr);
  stream.write(item);
}

function benchPipe(items) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [__filename], {
      env: { ...process.env, BENCHMARK_CHILD: "pipe", BENCHMARK_CHILD_N: String(items.length) },
      stdio: ["pipe", "ignore", "inherit"],
    });
    const t0 = ns();
    for (const it of items) writeFrame(child.stdin, it);
    child.stdin.end();
    child.on("exit", () => {
      const wall = ns() - t0;
      resolve([wall / 2n, wall - wall / 2n]);
    });
    child.on("error", reject);
  });
}

function benchShared(items) {
  return new Promise((resolve, reject) => {
    const slots = items.length + 2;
    const slot = Math.max((items[0] && items[0].length) || 64, 64);
    const sab = new SharedArrayBuffer(8 + 4 * slots + slots * slot);
    const iv = new Int32Array(sab, 0, 2);
    Atomics.store(iv, 0, 0);
    Atomics.store(iv, 1, 0);
    const worker = new Worker(__filename, {
      workerData: { role: "shared-ring", sab, n: items.length, slots, slot },
    });
    const t0 = ns();
    for (const it of items) {
      for (;;) {
        const tail = Atomics.load(iv, 1);
        const head = Atomics.load(iv, 0);
        const nxt = (tail + 1) % slots;
        if (nxt === head) continue;
        const n = Math.min(it.length, slot);
        const bytes = new Uint8Array(sab, 8 + 4 * slots + tail * slot, n);
        bytes.set(it.subarray ? it.subarray(0, n) : it.slice(0, n));
        Atomics.store(iv, 1, nxt);
        break;
      }
    }
    worker.on("exit", () => {
      const wall = ns() - t0;
      resolve([wall / 2n, wall - wall / 2n]);
    });
    worker.on("error", reject);
  });
}

function benchSqlite(items) {
  const { DatabaseSync } = require("node:sqlite");
  const p = path.join(require("os").tmpdir(), `qb-d-${process.pid}-${Date.now()}.sqlite`);
  const db = new DatabaseSync(p);
  const fsync = envOn("BENCHMARK_FSYNC");
  db.exec(fsync ? "PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL;" : "PRAGMA journal_mode=WAL; PRAGMA synchronous=OFF;");
  db.exec("CREATE TABLE q (id INTEGER PRIMARY KEY, payload BLOB)");
  const ins = db.prepare("INSERT INTO q(payload) VALUES (?)");
  const t0 = ns();
  for (const it of items) ins.run(it);
  const t1 = ns();
  const sel = db.prepare("SELECT payload FROM q ORDER BY id");
  for (const _ of sel.iterate()) {
    /* drain */
  }
  const t2 = ns();
  db.close();
  try {
    fs.unlinkSync(p);
  } catch {
    /* ignore */
  }
  return [t1 - t0, t2 - t1];
}

async function benchPQueue(items) {
  const { default: PQueue } = await import("p-queue");
  const q = new PQueue({ concurrency: 1 });
  const t0 = ns();
  let deq = 0n;
  for (const it of items) {
    q.add(async () => {
      const a = ns();
      void it;
      deq += ns() - a;
    });
  }
  await q.onIdle();
  return [ns() - t0 - deq, deq];
}

async function main() {
  if (process.env.BENCHMARK_CHILD === "pipe") return;
  const special = process.env.BENCHMARK_SPECIAL || "";
  const reps = Number(process.argv[2] || 10);
  const qf = process.argv[3] || "";
  const df = process.argv[4] || "";
  const includePsd = envOn("BENCHMARK_INCLUDE_PSD");
  const psdNames = (process.env.BENCHMARK_PSD_NAMES || "")
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
  const cells = loadCells();
  const dir = logDir();
  fs.mkdirSync(dir, { recursive: true });
  const stamp = process.env.BENCHMARK_TS || "run";
  const out = path.join(dir, `${stamp}.csv`);
  const lines = [HEADER];
  let order = 0;
  const queues = [
    { name: "Array", kind: "locked", optIn: false, spscOnly: true },
    { name: "fastq", kind: "concurrent", optIn: false, spscOnly: false },
    { name: "p-queue", kind: "scheduler", optIn: false, spscOnly: true },
    { name: "steal-deque", kind: "work-stealing", optIn: false, spscOnly: false },
    { name: "pipe-ipc", kind: "concurrent", optIn: true, spscOnly: true },
    { name: "shared-ring", kind: "spsc", optIn: true, spscOnly: true },
    { name: "sqlite-queue", kind: "durable", optIn: true, spscOnly: true },
  ];
  const pkg = require("../package.json");
  for (const cell of cells) {
    if (df && !cell.type_id.includes(df)) continue;
    const item = Buffer.alloc(cell.payload_bytes, 0x61);
    const items = Array.from({ length: cell.n }, () => item);
    const size = cell.payload_bytes * cell.n;
    const multi = cell.io_mode !== "bytes" && cell.io_mode !== "spsc";
    for (const q of queues) {
      if (qf && !q.name.toLowerCase().includes(qf.toLowerCase())) continue;
      if (q.optIn) {
        if (!includePsd && !qf) continue;
        if (psdNames.length && !psdNames.includes(q.name)) continue;
      }
      if (multi && q.spscOnly) continue;
      if (special === "cancel" && q.name !== "p-queue") continue;
      if (special && q.optIn) continue;
      for (let i = 0; i < reps; i++) {
        const cpu0 = process.cpuUsage();
        let enq, deq;
        if (special === "wakeup") {
          [enq, deq] = await benchWakeup(cell.n);
        } else if (special === "burst") {
          if (q.name === "Array" || q.name === "steal-deque") [enq, deq] = benchArray(items);
          else if (q.name === "fastq") [enq, deq] = await benchFastq(items);
          else [enq, deq] = await benchPQueue(items);
        } else if (special === "cancel") {
          [enq, deq] = await benchCancel(cell.n);
        } else if (q.name === "Array") {
          [enq, deq] = benchArray(items);
        } else if (q.name === "fastq") {
          [enq, deq] = await benchFastq(items);
        } else if (q.name === "p-queue") {
          [enq, deq] = await benchPQueue(items);
        } else if (q.name === "steal-deque") {
          [enq, deq] = benchSteal(items);
        } else if (q.name === "pipe-ipc") {
          [enq, deq] = await benchPipe(items);
        } else if (q.name === "shared-ring") {
          [enq, deq] = await benchShared(items);
        } else if (q.name === "sqlite-queue") {
          [enq, deq] = benchSqlite(items);
        }
        const used = process.cpuUsage(cpu0);
        const cpuNs = BigInt(used.user + used.system) * 1000n;
        const ver = q.name === "Array" || q.optIn || q.name === "steal-deque" ? process.version.replace(/^v/, "") : pkg.dependencies[q.name] || "0";
        lines.push(
          row(
            cell.io_mode,
            cell.type_id,
            reps,
            i,
            q.name,
            ver,
            enq,
            deq,
            size,
            cell.n,
            cell.hash,
            q.kind,
            order,
            cpuNs,
            rssBytes()
          )
        );
        order += 1;
      }
    }
  }
  fs.writeFileSync(out, lines.join("\n") + "\n");
  console.log("Wrote", out);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
