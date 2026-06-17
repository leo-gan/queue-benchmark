const fs = require('fs');
const path = require('path');
const { loadData } = require('../common/data_loader');
const { calculateStats, printStats } = require('../common/stats');
const fastq = require('fastq');

async function benchmarkArrayQueue(data, totalBytes) {
    const queue = [];
    const times_ns = [];

    // Producer
    for (const item of data) {
        queue.push(item);
    }

    // Consumer
    let received = 0;
    while (received < data.length) {
        const start = process.hrtime.bigint();
        const item = queue.shift();
        const end = process.hrtime.bigint();
        times_ns.push(Number(end - start));
        received++;
    }

    const stats = calculateStats(times_ns, totalBytes);
    printStats("Array.shift()", stats);
}

async function benchmarkFastq(data, totalBytes) {
    const times_ns = [];
    let received = 0;

    return new Promise((resolve) => {
        const q = fastq(function worker(item, cb) {
            const start = process.hrtime.bigint();
            // simulate work
            const end = process.hrtime.bigint();
            times_ns.push(Number(end - start));
            received++;
            cb(null);
        }, 1);

        q.drain = function() {
            if (received === data.length) {
                const stats = calculateStats(times_ns, totalBytes);
                printStats("fastq", stats);
                resolve();
            }
        };

        for (const item of data) {
            q.push(item);
        }
    });
}

async function main() {
    let dataPath = process.argv[2] || '../datasets/test_small.jsonl';
    if (!fs.existsSync(dataPath)) {
        dataPath = path.join(__dirname, '..', 'datasets', 'test_small.jsonl');
    }
    console.log(`Loading data from: ${dataPath}`);

    const data = loadData(dataPath);
    const totalBytes = data.reduce((acc, val) => acc + Buffer.byteLength(val, 'utf8'), 0);
    console.log(`Loaded ${data.length} records, total size: ${totalBytes} bytes`);

    await benchmarkArrayQueue(data, totalBytes);
    await benchmarkFastq(data, totalBytes);

    console.log("JavaScript benchmarks completed.");
}

main().catch(console.error);
