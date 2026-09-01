use std::env;
use std::fs::{self, File, OpenOptions};
use std::io::{BufRead, BufReader, Read, Write};
use std::path::PathBuf;
use std::process::{Command, Stdio};
use std::sync::mpsc;
use std::sync::Arc;
use std::thread;
use std::time::Instant;

use crossbeam_deque::{Injector, Steal};
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
        "Language,Pattern,TestDataName,Repetitions,RepetitionIndex,LibraryName,LibraryVersion,TimeEnq,TimeDeq,Size,TimeHandoff,OpPerSecEnq,OpPerSecDeq,OpPerSecHandoff,MemoryPeakBytes,FidelityScore,DataTypeInstanceCount,TypeConfigHash,SizeGzip,SizeZstd,NativeKind,StreamMode,RunOrder,SchedulePosition,CpuTimeNs"
    )
    .unwrap();
}

fn cpu_ns() -> u128 {
    unsafe {
        let mut ts = libc::timespec {
            tv_sec: 0,
            tv_nsec: 0,
        };
        if libc::clock_gettime(libc::CLOCK_PROCESS_CPUTIME_ID, &mut ts) != 0 {
            return 0;
        }
        ts.tv_sec as u128 * 1_000_000_000 + ts.tv_nsec as u128
    }
}

fn rss_bytes() -> u64 {
    unsafe {
        let mut ru: libc::rusage = std::mem::zeroed();
        if libc::getrusage(libc::RUSAGE_SELF, &mut ru) != 0 {
            return 0;
        }
        ru.ru_maxrss as u64 * 1024
    }
}

fn env_on(name: &str) -> bool {
    matches!(
        env::var(name).unwrap_or_default().as_str(),
        "1" | "true" | "on"
    )
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
    cpu: u128,
) {
    let tot = enq + deq;
    writeln!(
        w,
        "rust,{mode},{ty},{reps},{idx},{name},{ver},{enq},{deq},{size},{tot},{:.6},{:.6},{:.6},{},1.0000,{n},{hash},0,0,{kind},{},{order},{order},{cpu}",
        ops(enq),
        ops(deq),
        ops(tot),
        rss_bytes(),
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

fn bench_steal(items: &[Vec<u8>], producers: usize, consumers: usize) -> (u128, u128) {
    let inj = Arc::new(Injector::new());
    if producers == 1 && consumers == 1 {
        let t0 = Instant::now();
        for it in items {
            inj.push(it.clone());
        }
        let enq = t0.elapsed().as_nanos();
        let t1 = Instant::now();
        for _ in items {
            loop {
                match inj.steal() {
                    Steal::Success(_) => break,
                    Steal::Empty | Steal::Retry => {}
                }
            }
        }
        return (enq, t1.elapsed().as_nanos());
    }
    let batches = split_items(items, producers);
    let n = items.len();
    let t0 = Instant::now();
    let mut handles = Vec::new();
    for batch in batches {
        let inj = Arc::clone(&inj);
        handles.push(thread::spawn(move || {
            for it in batch {
                inj.push(it);
            }
        }));
    }
    let per = n / consumers.max(1);
    let extra = n % consumers.max(1);
    for i in 0..consumers {
        let inj = Arc::clone(&inj);
        let take = per + if i == 0 { extra } else { 0 };
        handles.push(thread::spawn(move || {
            for _ in 0..take {
                loop {
                    match inj.steal() {
                        Steal::Success(_) => break,
                        Steal::Empty | Steal::Retry => {}
                    }
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

fn write_frame(w: &mut impl Write, item: &[u8]) {
    let len = (item.len() as u32).to_be_bytes();
    w.write_all(&len).unwrap();
    w.write_all(item).unwrap();
}

fn read_frame(r: &mut impl Read) -> Vec<u8> {
    let mut lenb = [0u8; 4];
    r.read_exact(&mut lenb).unwrap();
    let len = u32::from_be_bytes(lenb) as usize;
    let mut buf = vec![0u8; len];
    r.read_exact(&mut buf).unwrap();
    buf
}

fn child_pipe() {
    let n: usize = env::var("BENCHMARK_CHILD_N")
        .ok()
        .and_then(|s| s.parse().ok())
        .unwrap_or(0);
    let mut stdin = std::io::stdin().lock();
    for _ in 0..n {
        let _ = read_frame(&mut stdin);
    }
}

fn bench_pipe(items: &[Vec<u8>]) -> (u128, u128) {
    let exe = env::current_exe().unwrap();
    let mut child = Command::new(exe)
        .env("BENCHMARK_CHILD", "pipe")
        .env("BENCHMARK_CHILD_N", items.len().to_string())
        .stdin(Stdio::piped())
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .spawn()
        .unwrap();
    let mut stdin = child.stdin.take().unwrap();
    let t0 = Instant::now();
    for it in items {
        write_frame(&mut stdin, it);
    }
    drop(stdin);
    let _ = child.wait();
    let wall = t0.elapsed().as_nanos();
    (wall / 2, wall - wall / 2)
}

fn child_shared() {
    let n: usize = env::var("BENCHMARK_CHILD_N")
        .ok()
        .and_then(|s| s.parse().ok())
        .unwrap_or(0);
    let path = env::var("BENCHMARK_MMAP").unwrap();
    let slots: u32 = env::var("BENCHMARK_SLOTS").unwrap().parse().unwrap();
    let slot: u32 = env::var("BENCHMARK_SLOT").unwrap().parse().unwrap();
    let file = OpenOptions::new().read(true).write(true).open(path).unwrap();
    let mmap = unsafe { memmap2::MmapMut::map_mut(&file).unwrap() };
    let head = mmap.as_ptr() as *const std::sync::atomic::AtomicU32;
    let tail = unsafe { mmap.as_ptr().add(4) } as *const std::sync::atomic::AtomicU32;
    for _ in 0..n {
        loop {
            let h = unsafe { (*head).load(std::sync::atomic::Ordering::Relaxed) };
            let t = unsafe { (*tail).load(std::sync::atomic::Ordering::Acquire) };
            if h != t {
                unsafe {
                    (*head).store((h + 1) % slots, std::sync::atomic::Ordering::Release);
                }
                break;
            }
        }
    }
    let _ = slot;
}

fn bench_shared(items: &[Vec<u8>]) -> (u128, u128) {
    let slots = (items.len() as u32) + 2;
    let slot = items.first().map(|i| i.len().max(64) as u32).unwrap_or(64);
    let bytes = 8 + 4 * slots as usize + slots as usize * slot as usize;
    let path = env::temp_dir().join(format!("qb-ring-{}", std::process::id()));
    {
        let f = OpenOptions::new()
            .create(true)
            .read(true)
            .write(true)
            .truncate(true)
            .open(&path)
            .unwrap();
        f.set_len(bytes as u64).unwrap();
    }
    let file = OpenOptions::new().read(true).write(true).open(&path).unwrap();
    let mut mmap = unsafe { memmap2::MmapMut::map_mut(&file).unwrap() };
    mmap.fill(0);
    let exe = env::current_exe().unwrap();
    let child = Command::new(exe)
        .env("BENCHMARK_CHILD", "shared")
        .env("BENCHMARK_CHILD_N", items.len().to_string())
        .env("BENCHMARK_MMAP", path.display().to_string())
        .env("BENCHMARK_SLOTS", slots.to_string())
        .env("BENCHMARK_SLOT", slot.to_string())
        .stdin(Stdio::null())
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .spawn()
        .unwrap();
    let head = mmap.as_ptr() as *const std::sync::atomic::AtomicU32;
    let tail = unsafe { mmap.as_ptr().add(4) } as *const std::sync::atomic::AtomicU32;
    let t0 = Instant::now();
    for it in items {
        loop {
            let t = unsafe { (*tail).load(std::sync::atomic::Ordering::Relaxed) };
            let h = unsafe { (*head).load(std::sync::atomic::Ordering::Acquire) };
            let nxt = (t + 1) % slots;
            if nxt != h {
                let n = it.len().min(slot as usize);
                let off = 8 + 4 * slots as usize + t as usize * slot as usize;
                mmap[off..off + n].copy_from_slice(&it[..n]);
                unsafe {
                    (*tail).store(nxt, std::sync::atomic::Ordering::Release);
                }
                break;
            }
        }
    }
    let mut child = child;
    let _ = child.wait();
    let wall = t0.elapsed().as_nanos();
    let _ = fs::remove_file(&path);
    (wall / 2, wall - wall / 2)
}

fn bench_sqlite(items: &[Vec<u8>]) -> (u128, u128) {
    let path = env::temp_dir().join(format!("qb-d-{}-{}.sqlite", std::process::id(), items.len()));
    let _ = fs::remove_file(&path);
    let db = rusqlite::Connection::open(&path).unwrap();
    let fsync = env_on("BENCHMARK_FSYNC");
    db.execute_batch(if fsync {
        "PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL;"
    } else {
        "PRAGMA journal_mode=WAL; PRAGMA synchronous=OFF;"
    })
    .unwrap();
    db.execute("CREATE TABLE q (id INTEGER PRIMARY KEY, payload BLOB)", [])
        .unwrap();
    let t0 = Instant::now();
    {
        let mut ins = db
            .prepare("INSERT INTO q(payload) VALUES (?1)")
            .unwrap();
        for it in items {
            ins.execute(rusqlite::params![it.as_slice()]).unwrap();
        }
    }
    let enq = t0.elapsed().as_nanos();
    let t1 = Instant::now();
    {
        let mut sel = db.prepare("SELECT payload FROM q ORDER BY id").unwrap();
        let mut rows = sel.query([]).unwrap();
        while let Some(_) = rows.next().unwrap() {}
    }
    let deq = t1.elapsed().as_nanos();
    drop(db);
    let _ = fs::remove_file(&path);
    (enq, deq)
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

fn maybe_child() -> bool {
    match env::var("BENCHMARK_CHILD").unwrap_or_default().as_str() {
        "pipe" => {
            child_pipe();
            true
        }
        "shared" => {
            child_shared();
            true
        }
        _ => false,
    }
}

fn kind_of(name: &str) -> &'static str {
    match name {
        "tokio-mpsc" => "async",
        "steal-deque" => "work-stealing",
        "shared-ring" => "spsc",
        "sqlite-queue" => "durable",
        _ => "concurrent",
    }
}

fn opt_in(name: &str) -> bool {
    matches!(name, "pipe-ipc" | "shared-ring" | "sqlite-queue")
}

fn spsc_only(name: &str) -> bool {
    matches!(
        name,
        "std-mpsc" | "tokio-mpsc" | "pipe-ipc" | "shared-ring" | "sqlite-queue"
    )
}

fn include_queue(name: &str, qf: &str) -> bool {
    if !qf.is_empty() && !name.contains(qf) {
        return false;
    }
    if opt_in(name) {
        let include_psd = env_on("BENCHMARK_INCLUDE_PSD");
        if !include_psd && qf.is_empty() {
            return false;
        }
        let names = env::var("BENCHMARK_PSD_NAMES").unwrap_or_default();
        if !names.is_empty() && !names.split(',').any(|s| s.trim() == name) {
            return false;
        }
    }
    true
}

fn main() {
    if maybe_child() {
        return;
    }
    tokio_main();
}

#[tokio::main]
async fn tokio_main() {
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
    let queues = [
        "std-mpsc",
        "crossbeam-channel",
        "tokio-mpsc",
        "crossbeam-queue",
        "steal-deque",
        "pipe-ipc",
        "shared-ring",
        "sqlite-queue",
    ];
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
            if !include_queue(name, &qf) {
                continue;
            }
            if spsc_only(name) && (producers > 1 || consumers > 1) {
                continue;
            }
            let special = env::var("BENCHMARK_SPECIAL").unwrap_or_default();
            if special == "cancel" && name != "tokio-mpsc" {
                continue;
            }
            if !special.is_empty() && opt_in(name) {
                continue;
            }
            for i in 0..reps {
                let cpu0 = cpu_ns();
                let (enq, deq) = if special == "wakeup" {
                    bench_wakeup(&items)
                } else if special == "burst" {
                    match name {
                        "std-mpsc" => bench_std_mpsc(&items),
                        "tokio-mpsc" => bench_tokio(&items).await,
                        "crossbeam-queue" => bench_crossbeam_queue(&items, 1, 1),
                        "steal-deque" => bench_steal(&items, 1, 1),
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
                        "steal-deque" => bench_steal(&items, producers, consumers),
                        "pipe-ipc" => bench_pipe(&items),
                        "shared-ring" => bench_shared(&items),
                        "sqlite-queue" => bench_sqlite(&items),
                        _ => (0, 0),
                    }
                };
                let cpu = cpu_ns().saturating_sub(cpu0);
                row(
                    &mut w,
                    &cell.io_mode,
                    &cell.type_id,
                    reps,
                    i,
                    name,
                    env!("CARGO_PKG_VERSION"),
                    enq,
                    deq,
                    size,
                    cell.n,
                    &cell.hash,
                    kind_of(name),
                    order,
                    cpu,
                );
                order += 1;
            }
        }
    }
    println!("Wrote {}", path.display());
}
