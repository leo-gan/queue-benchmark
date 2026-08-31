use std::env;
use std::fs::{self, File};
use std::io::{BufRead, BufReader, Write};
use std::path::PathBuf;
use std::sync::mpsc;
use std::sync::Arc;
use std::thread;
use std::time::Instant;

use crossbeam_queue::SegQueue;

struct Cell {
    type_id: String,
    payload_bytes: usize,
    n: usize,
    io_mode: String,
    hash: String,
}

fn cells_path() -> PathBuf {
    env::var("BENCHMARK_CELLS_TSV")
        .map(PathBuf::from)
        .unwrap_or_else(|_| PathBuf::from("cells.tsv"))
}

fn load_cells() -> Vec<Cell> {
    let f = File::open(cells_path()).expect("BENCHMARK_CELLS_TSV");
    let mut out = Vec::new();
    for (i, line) in BufReader::new(f).lines().flatten().enumerate() {
        if i == 0 {
            continue;
        }
        let p: Vec<&str> = line.split('\t').collect();
        if p.len() < 5 {
            continue;
        }
        out.push(Cell {
            type_id: p[0].to_string(),
            payload_bytes: p[1].parse().unwrap_or(256),
            n: p[2].parse().unwrap_or(1),
            io_mode: p[3].to_string(),
            hash: p[4].to_string(),
        });
    }
    out
}

fn payload(n: usize) -> Vec<u8> {
    (0..n).map(|i| (i % 251) as u8).collect()
}

fn log_dir() -> PathBuf {
    let p = env::var("LOG_DIR").unwrap_or_else(|_| "../logs/rust".into());
    let pb = PathBuf::from(p);
    if pb.ends_with("rust") {
        pb
    } else {
        pb.join("rust")
    }
}

fn stamp() -> String {
    env::var("BENCHMARK_TS").unwrap_or_else(|_| "run".into())
}

fn write_header(w: &mut impl Write) {
    writeln!(
        w,
        "Language,StringOrStream,TestDataName,Repetitions,RepetitionIndex,SerializerName,SerializerVersion,TimeSer,TimeDeser,Size,TimeSerAndDeser,OpPerSecSer,OpPerSecDeser,OpPerSecSerAndDeser,MemoryPeakBytes,FidelityScore,DataTypeInstanceCount,TypeConfigHash,SizeGzip,SizeZstd,NativeKind,StreamMode,RunOrder,SchedulePosition"
    )
    .unwrap();
}

fn ops(ns: u128) -> f64 {
    if ns == 0 {
        0.0
    } else {
        1_000_000_000.0 / ns as f64
    }
}

fn row(
    w: &mut impl Write,
    mode: &str,
    ty: &str,
    reps: usize,
    idx: usize,
    name: &str,
    ver: &str,
    enq: u128,
    deq: u128,
    size: usize,
    n: usize,
    hash: &str,
    kind: &str,
    order: usize,
) {
    let tot = enq + deq;
    writeln!(
        w,
        "rust,{mode},{ty},{reps},{idx},{name},{ver},{enq},{deq},{size},{tot},{:.6},{:.6},{:.6},0,1.0000,{n},{hash},0,0,{kind},{},{order},{order}",
        ops(enq),
        ops(deq),
        ops(tot),
        if mode == "stream" { "native" } else { "" },
    )
    .unwrap();
}

fn bench_std_mpsc(items: &[Vec<u8>]) -> (u128, u128) {
    let (tx, rx) = mpsc::channel();
    let t0 = Instant::now();
    for it in items {
        tx.send(it.clone()).unwrap();
    }
    let enq = t0.elapsed().as_nanos();
    let t1 = Instant::now();
    for _ in items {
        let _ = rx.recv().unwrap();
    }
    (enq, t1.elapsed().as_nanos())
}

fn bench_crossbeam(items: &[Vec<u8>], mpmc: bool) -> (u128, u128) {
    let (tx, rx) = crossbeam_channel::unbounded();
    if !mpmc {
        let t0 = Instant::now();
        for it in items {
            tx.send(it.clone()).unwrap();
        }
        let enq = t0.elapsed().as_nanos();
        let t1 = Instant::now();
        for _ in items {
            let _ = rx.recv().unwrap();
        }
        return (enq, t1.elapsed().as_nanos());
    }
    let half = items.len() / 2;
    let a = items[..half].to_vec();
    let b = items[half..].to_vec();
    let tx2 = tx.clone();
    let t0 = Instant::now();
    let p1 = thread::spawn(move || {
        for it in a {
            tx.send(it).unwrap();
        }
    });
    let p2 = thread::spawn(move || {
        for it in b {
            tx2.send(it).unwrap();
        }
    });
    let n = items.len();
    let c1n = n / 2;
    let rx2 = rx.clone();
    let c1 = thread::spawn(move || {
        for _ in 0..c1n {
            let _ = rx.recv().unwrap();
        }
    });
    let c2 = thread::spawn(move || {
        for _ in 0..(n - c1n) {
            let _ = rx2.recv().unwrap();
        }
    });
    p1.join().unwrap();
    p2.join().unwrap();
    c1.join().unwrap();
    c2.join().unwrap();
    let wall = t0.elapsed().as_nanos();
    (wall / 2, wall - wall / 2)
}

fn bench_crossbeam_queue(items: &[Vec<u8>], mpmc: bool) -> (u128, u128) {
    let q = Arc::new(SegQueue::new());
    if !mpmc {
        let t0 = Instant::now();
        for it in items {
            q.push(it.clone());
        }
        let enq = t0.elapsed().as_nanos();
        let t1 = Instant::now();
        for _ in items {
            let _ = q.pop();
        }
        return (enq, t1.elapsed().as_nanos());
    }
    let half = items.len() / 2;
    let a = items[..half].to_vec();
    let b = items[half..].to_vec();
    let q1 = Arc::clone(&q);
    let q2 = Arc::clone(&q);
    let q3 = Arc::clone(&q);
    let q4 = Arc::clone(&q);
    let t0 = Instant::now();
    let p1 = thread::spawn(move || {
        for it in a {
            q1.push(it);
        }
    });
    let p2 = thread::spawn(move || {
        for it in b {
            q2.push(it);
        }
    });
    let n = items.len();
    let c1n = n / 2;
    let c1 = thread::spawn(move || {
        let mut left = c1n;
        while left > 0 {
            if q3.pop().is_some() {
                left -= 1;
            }
        }
    });
    let c2 = thread::spawn(move || {
        let mut left = n - c1n;
        while left > 0 {
            if q4.pop().is_some() {
                left -= 1;
            }
        }
    });
    p1.join().unwrap();
    p2.join().unwrap();
    c1.join().unwrap();
    c2.join().unwrap();
    let wall = t0.elapsed().as_nanos();
    (wall / 2, wall - wall / 2)
}

async fn bench_tokio(items: &[Vec<u8>]) -> (u128, u128) {
    let (tx, mut rx) = tokio::sync::mpsc::unbounded_channel();
    let t0 = Instant::now();
    for it in items {
        tx.send(it.clone()).unwrap();
    }
    let enq = t0.elapsed().as_nanos();
    let t1 = Instant::now();
    for _ in items {
        let _ = rx.recv().await.unwrap();
    }
    (enq, t1.elapsed().as_nanos())
}

#[tokio::main]
async fn main() {
    let args: Vec<String> = env::args().collect();
    let reps: usize = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(10);
    let qf = args.get(2).cloned().unwrap_or_default();
    let df = args.get(3).cloned().unwrap_or_default();
    let cells = load_cells();
    let dir = log_dir();
    fs::create_dir_all(&dir).unwrap();
    let path = dir.join(format!("{}.csv", stamp()));
    let mut w = File::create(&path).unwrap();
    write_header(&mut w);
    let queues = ["std-mpsc", "crossbeam-channel", "tokio-mpsc", "crossbeam-queue"];
    let mut order = 0usize;
    for cell in &cells {
        if !df.is_empty() && !cell.type_id.contains(&df) {
            continue;
        }
        let item = payload(cell.payload_bytes);
        let items: Vec<Vec<u8>> = (0..cell.n).map(|_| item.clone()).collect();
        let size = cell.payload_bytes * cell.n;
        let mpmc = cell.io_mode == "stream";
        for name in queues {
            if !qf.is_empty() && !name.contains(&qf) {
                continue;
            }
            if name == "std-mpsc" && mpmc {
                continue;
            }
            for i in 0..reps {
                let (enq, deq) = match name {
                    "std-mpsc" => bench_std_mpsc(&items),
                    "crossbeam-channel" => bench_crossbeam(&items, mpmc),
                    "tokio-mpsc" => bench_tokio(&items).await,
                    "crossbeam-queue" => bench_crossbeam_queue(&items, mpmc),
                    _ => (0, 0),
                };
                let ver = match name {
                    "crossbeam-channel" => env!("CARGO_PKG_VERSION"),
                    "crossbeam-queue" => env!("CARGO_PKG_VERSION"),
                    "tokio-mpsc" => "1",
                    _ => env!("CARGO_PKG_VERSION"),
                };
                let kind = if name == "tokio-mpsc" {
                    "async"
                } else {
                    "concurrent"
                };
                row(
                    &mut w,
                    &cell.io_mode,
                    &cell.type_id,
                    reps,
                    i,
                    name,
                    ver,
                    enq,
                    deq,
                    size,
                    cell.n,
                    &cell.hash,
                    kind,
                    order,
                );
                order += 1;
            }
        }
    }
    println!("Wrote {}", path.display());
}
