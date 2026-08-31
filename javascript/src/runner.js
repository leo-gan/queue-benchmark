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
  "Language,StringOrStream,TestDataName,Repetitions,RepetitionIndex,SerializerName,SerializerVersion,TimeSer,TimeDeser,Size,TimeSerAndDeser,OpPerSecSer,OpPerSecDeser,OpPerSecSerAndDeser,MemoryPeakBytes,FidelityScore,DataTypeInstanceCount,TypeConfigHash,SizeGzip,SizeZstd,NativeKind,StreamMode,RunOrder,SchedulePosition";

function ops(t) {
  return t > 0n ? (1e9 / Number(t)).toFixed(6) : "0.000000";
}

function row(mode, ty, reps, idx, name, ver, enq, deq, size, n, hash, kind, order) {
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
  ].join(",");
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
    { name: "p-queue", kind: "async" },
  ];
  const pkg = require("../package.json");
  for (const cell of cells) {
    if (df && !cell.type_id.includes(df)) continue;
    const item = Buffer.alloc(cell.payload_bytes, 0x61);
    const items = Array.from({ length: cell.n }, () => item);
    const size = cell.payload_bytes * cell.n;
    for (const q of queues) {
      if (qf && !q.name.toLowerCase().includes(qf.toLowerCase())) continue;
      if (cell.io_mode === "stream" && q.name === "Array") continue;
      for (let i = 0; i < reps; i++) {
        let enq, deq;
        if (q.name === "Array") [enq, deq] = benchArray(items);
        else if (q.name === "fastq") [enq, deq] = await benchFastq(items);
        else [enq, deq] = await benchPQueue(items);
        const ver = q.name === "Array" ? process.version.replace(/^v/, "") : pkg.dependencies[q.name] || "0";
        lines.push(
          row(cell.io_mode, cell.type_id, reps, i, q.name, ver, enq, deq, size, cell.n, cell.hash, q.kind, order)
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
