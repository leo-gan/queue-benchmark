#[path = "../../common/data_loader.rs"]
mod data_loader;

#[path = "../../common/stats.rs"]
mod stats;

use std::env;
use std::time::Instant;
use std::sync::mpsc;
use std::thread;

fn benchmark_std_mpsc(data: &[String], total_bytes: usize) {
    let (tx, rx) = mpsc::channel();
    let mut times_ns = Vec::with_capacity(data.len());

    let data_clone = data.to_vec();

    let producer = thread::spawn(move || {
        for item in data_clone {
            tx.send(item).unwrap();
        }
    });

    let expected = data.len();
    let consumer = thread::spawn(move || {
        let mut received = 0;
        while received < expected {
            let start = Instant::now();
            let _ = rx.recv().unwrap();
            times_ns.push(start.elapsed().as_nanos() as u64);
            received += 1;
        }
        times_ns
    });

    producer.join().unwrap();
    let times = consumer.join().unwrap();

    let stats = stats::calculate_stats(times, total_bytes);
    stats::print_stats("std::sync::mpsc", &stats);
}

fn benchmark_crossbeam(data: &[String], total_bytes: usize) {
    let (tx, rx) = crossbeam_channel::unbounded();
    let mut times_ns = Vec::with_capacity(data.len());

    let data_clone = data.to_vec();

    let producer = thread::spawn(move || {
        for item in data_clone {
            tx.send(item).unwrap();
        }
    });

    let expected = data.len();
    let consumer = thread::spawn(move || {
        let mut received = 0;
        while received < expected {
            let start = Instant::now();
            let _ = rx.recv().unwrap();
            times_ns.push(start.elapsed().as_nanos() as u64);
            received += 1;
        }
        times_ns
    });

    producer.join().unwrap();
    let times = consumer.join().unwrap();

    let stats = stats::calculate_stats(times, total_bytes);
    stats::print_stats("crossbeam-channel", &stats);
}

#[tokio::main]
async fn main() {
    let args: Vec<String> = env::args().collect();
    let data_path = if args.len() > 1 { &args[1] } else { "../datasets/test_small.jsonl" };

    println!("Loading data from: {}", data_path);
    let data = data_loader::load_data(data_path);
    let total_bytes: usize = data.iter().map(|s| s.len()).sum();
    println!("Loaded {} records, total size: {} bytes", data.len(), total_bytes);

    benchmark_std_mpsc(&data, total_bytes);
    benchmark_crossbeam(&data, total_bytes);

    println!("Rust benchmarks completed.");
}
