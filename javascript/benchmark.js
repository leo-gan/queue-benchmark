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
        queue.push({ item, start: process.hrtime.bigint() });
    }

    // Consumer
    let received = 0;
    while (received < data.length) {
        const task = queue.shift();
        const end = process.hrtime.bigint();
        times_ns.push(Number(end - task.start));
        received++;
    }

    const stats = calculateStats(times_ns, totalBytes);
    printStats("Array.shift()", stats);
}

async function benchmarkFastq(data, totalBytes) {
    const times_ns = [];
    let received = 0;

    return new Promise((resolve) => {
        const q = fastq(function worker(task, cb) {
            const end = process.hrtime.bigint();
            times_ns.push(Number(end - task.start));
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
            const start = process.hrtime.bigint();
            q.push({ item, start });
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
    await benchmarkPQueue(data, totalBytes);
    await benchmarkNpmQueue(data, totalBytes);
    await benchmarkRxjs(data, totalBytes);
    // Skipping bullmq, bee-queue, better-queue, workerpool, Node.js MessageChannel as they require
    // external services like Redis or process forks which are beyond simple micro-benchmark scope here.

    console.log("JavaScript benchmarks completed.");
}


main().catch(console.error);

const { default: PQueue } = require('p-queue');
async function benchmarkPQueue(data, totalBytes) {
    const queue = new PQueue({ concurrency: 1 });
    const times_ns = [];

    for (const item of data) {
        const start = process.hrtime.bigint();
        queue.add(async () => {
            const end = process.hrtime.bigint();
            times_ns.push(Number(end - start));
        });
    }

    await queue.onIdle();
    const stats = calculateStats(times_ns, totalBytes);
    printStats("p-queue", stats);
}



const { default: Queue } = require('queue');
async function benchmarkNpmQueue(data, totalBytes) {
    const q = new Queue({ concurrency: 1, autostart: true });
    const times_ns = [];

    return new Promise((resolve) => {
        let received = 0;

        q.addEventListener('end', () => {
            const stats = calculateStats(times_ns, totalBytes);
            printStats("queue (npm)", stats);
            resolve();
        });

        for (const item of data) {
            const start = process.hrtime.bigint();
            q.push((cb) => {
                const end = process.hrtime.bigint();
                times_ns.push(Number(end - start));
                received++;
                if (cb) cb();
            });
        }

        // if autostart doesn't emit end when empty
        if(data.length === 0) resolve();
    });
}

const { Subject, concatMap, of } = require('rxjs');
async function benchmarkRxjs(data, totalBytes) {
    const subject = new Subject();
    const times_ns = [];

    return new Promise((resolve) => {
        let received = 0;
        const sub = subject.pipe(
            concatMap((task) => of(task))
        ).subscribe((task) => {
            const end = process.hrtime.bigint();
            times_ns.push(Number(end - task.start));
            received++;
            if (received === data.length) {
                const stats = calculateStats(times_ns, totalBytes);
                printStats("rxjs Subject + concatMap", stats);
                sub.unsubscribe();
                resolve();
            }
        });

        for (const item of data) {
            subject.next({ item, start: process.hrtime.bigint() });
        }
    });
}
