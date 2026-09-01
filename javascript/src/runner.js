"use strict";

const fs = require("fs");
const path = require("path");
const { performance } = require("perf_hooks");
const fastq = require("fastq");

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

function row(mode, ty, reps, idx, name, ver, enq, deq, size, n, hash, kind, order, cpuNs) {
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
    0,
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
  const special = process.env.BENCHMARK_SPECIAL || "";
  const reps = Number(process.argv[2] || 10);
  const qf = process.argv[3] || "";
  const df = process.argv[4] || "";
  const cells = loadCells();
  const dir = logDir();
  fs.mkdirSync(dir, { recursive: true });
  const stamp = process.env.BENCHMARK_TS || "run";
  const out = path.join(dir, `${stamp}.csv`);
  const lines = [HEADER];
  let order = 0;
  const queues = [
    { name: "Array", kind: "locked" },
    { name: "fastq", kind: "concurrent" },
    { name: "p-queue", kind: "scheduler" },
  ];
  const pkg = require("../package.json");
  for (const cell of cells) {
    if (df && !cell.type_id.includes(df)) continue;
    const item = Buffer.alloc(cell.payload_bytes, 0x61);
    const items = Array.from({ length: cell.n }, () => item);
    const size = cell.payload_bytes * cell.n;
    for (const q of queues) {
      if (qf && !q.name.toLowerCase().includes(qf.toLowerCase())) continue;
      const multi = cell.io_mode !== "bytes" && cell.io_mode !== "spsc";
      if (multi && (q.name === "Array" || q.name === "p-queue")) continue;
      if (special === "cancel" && q.name !== "p-queue") continue;
      for (let i = 0; i < reps; i++) {
        const cpu0 = process.cpuUsage();
        let enq, deq;
        if (special === "wakeup") {
          [enq, deq] = await benchWakeup(cell.n);
        } else if (special === "burst") {
          if (q.name === "Array") [enq, deq] = benchArray(items);
          else if (q.name === "fastq") [enq, deq] = await benchFastq(items);
          else [enq, deq] = await benchPQueue(items);
        } else if (special === "cancel") {
          [enq, deq] = await benchCancel(cell.n);
        } else if (q.name === "Array") {
          [enq, deq] = benchArray(items);
        } else if (q.name === "fastq") {
          [enq, deq] = await benchFastq(items);
        } else {
          [enq, deq] = await benchPQueue(items);
        }
        const used = process.cpuUsage(cpu0);
        const cpuNs = BigInt(used.user + used.system) * 1000n;
        const ver = q.name === "Array" ? process.version.replace(/^v/, "") : pkg.dependencies[q.name] || "0";
        lines.push(
          row(cell.io_mode, cell.type_id, reps, i, q.name, ver, enq, deq, size, cell.n, cell.hash, q.kind, order, cpuNs)
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
