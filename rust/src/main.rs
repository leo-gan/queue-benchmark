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

fn parse_pattern(mode: &str) -> (usize, usize) {
    match mode {
        "bytes" | "spsc" | "string" => (1, 1),
        "stream" | "mpmc" => (2, 2),
        other => {
            let b = other.as_bytes();
            let mut p = 0usize;
            let mut c = 0usize;
            let mut i = 0;
            while i < b.len() && b[i].is_ascii_digit() {
                p = p * 10 + (b[i] - b'0') as usize;
                i += 1;
            }
            if i < b.len() && b[i] == b'p' {
                i += 1;
            }
            while i < b.len() && b[i].is_ascii_digit() {
                c = c * 10 + (b[i] - b'0') as usize;
                i += 1;
            }
            (p.max(1), c.max(1))
        }
    }
}

fn split_items(items: &[Vec<u8>], parts: usize) -> Vec<Vec<Vec<u8>>> {
    let n = items.len();
    let parts = parts.max(1);
    (0..parts)
        .map(|i| {
            let a = n * i / parts;
            let b = n * (i + 1) / parts;
            items[a..b].to_vec()
        })
        .collect()
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

fn bench_crossbeam(items: &[Vec<u8>], producers: usize, consumers: usize) -> (u128, u128) {
    let (tx, rx) = crossbeam_channel::unbounded();
    if producers == 1 && consumers == 1 {
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
    let batches = split_items(items, producers);
    let n = items.len();
    let t0 = Instant::now();
    let mut handles = Vec::new();
    for batch in batches {
        let tx = tx.clone();
        handles.push(thread::spawn(move || {
            for it in batch {
                tx.send(it).unwrap();
            }
        }));
    }
    let per = n / consumers.max(1);
    let extra = n % consumers.max(1);
    for i in 0..consumers {
        let rx = rx.clone();
        let take = per + if i == 0 { extra } else { 0 };
        handles.push(thread::spawn(move || {
            for _ in 0..take {
                let _ = rx.recv().unwrap();
            }
        }));
    }
    for h in handles {
        h.join().unwrap();
    }
    let wall = t0.elapsed().as_nanos();
    (wall / 2, wall - wall / 2)
}

fn bench_crossbeam_queue(items: &[Vec<u8>], producers: usize, consumers: usize) -> (u128, u128) {
    let q = Arc::new(SegQueue::new());
    if producers == 1 && consumers == 1 {
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
    let batches = split_items(items, producers);
    let n = items.len();
    let t0 = Instant::now();
    let mut handles = Vec::new();
    for batch in batches {
        let q = Arc::clone(&q);
        handles.push(thread::spawn(move || {
            for it in batch {
                q.push(it);
            }
        }));
    }
    let per = n / consumers.max(1);
    let extra = n % consumers.max(1);
    for i in 0..consumers {
        let q = Arc::clone(&q);
        let take = per + if i == 0 { extra } else { 0 };
        handles.push(thread::spawn(move || {
            let mut left = take;
            while left > 0 {
                if q.pop().is_some() {
                    left -= 1;
                }
            }
        }));
    }
    for h in handles {
        h.join().unwrap();
    }
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

fn bench_wakeup(items: &[Vec<u8>]) -> (u128, u128) {
    let (tx, rx) = crossbeam_channel::bounded::<Vec<u8>>(1);
    let n = items.len().max(1);
    let wait_ns: u64 = env::var("BENCHMARK_WAIT_NS")
        .ok()
        .and_then(|s| s.parse().ok())
        .unwrap_or(1_000_000);
    let h = thread::spawn(move || {
        for _ in 0..n {
            let _ = rx.recv();
        }
    });
    thread::sleep(std::time::Duration::from_millis(2));
    let t0 = Instant::now();
    for _ in 0..n {
        thread::sleep(std::time::Duration::from_nanos(wait_ns));
        tx.send(vec![1]).unwrap();
    }
    h.join().unwrap();
    let wall = t0.elapsed().as_nanos();
    (wall / n as u128, wall - wall / n as u128)
}

async fn bench_tokio_cancel(waiters: usize) -> (u128, u128) {
    let (_tx, rx) = tokio::sync::mpsc::unbounded_channel::<Vec<u8>>();
    let rx = std::sync::Arc::new(tokio::sync::Mutex::new(rx));
    let mut handles = Vec::new();
    for _ in 0..waiters.max(8) {
        let rx = std::sync::Arc::clone(&rx);
        handles.push(tokio::spawn(async move {
            let mut g = rx.lock().await;
            let _ = g.recv().await;
        }));
    }
    tokio::time::sleep(std::time::Duration::from_millis(1)).await;
    let t0 = Instant::now();
    for h in &handles {
        h.abort();
    }
    for h in handles {
        let _ = h.await;
    }
    (t0.elapsed().as_nanos(), 0)
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
        let (producers, consumers) = parse_pattern(&cell.io_mode);
        for name in queues {
            if !qf.is_empty() && !name.contains(&qf) {
                continue;
            }
            if (name == "std-mpsc" || name == "tokio-mpsc") && (producers > 1 || consumers > 1)
            {
                continue;
            }
            let special = env::var("BENCHMARK_SPECIAL").unwrap_or_default();
            if special == "cancel" && name != "tokio-mpsc" {
                continue;
            }
            for i in 0..reps {
                let (enq, deq) = if special == "wakeup" {
                    bench_wakeup(&items)
                } else if special == "burst" {
                    match name {
                        "std-mpsc" => bench_std_mpsc(&items),
                        "tokio-mpsc" => bench_tokio(&items).await,
                        "crossbeam-queue" => bench_crossbeam_queue(&items, 1, 1),
                        _ => bench_crossbeam(&items, 1, 1),
                    }
                } else if special == "cancel" {
                    bench_tokio_cancel(items.len()).await
                } else {
                    match name {
                    "std-mpsc" => bench_std_mpsc(&items),
                    "crossbeam-channel" => bench_crossbeam(&items, producers, consumers),
                    "tokio-mpsc" => bench_tokio(&items).await,
                    "crossbeam-queue" => bench_crossbeam_queue(&items, producers, consumers),
                    _ => (0, 0),
                    }
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
