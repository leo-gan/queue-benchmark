# 05-wakeup

Times are not comparable across languages.

## python

Similar set (within 15% of fastest on this sample): queue.SimpleQueue, queue.Queue, asyncio.Queue

See `python/results.md`.

## rust

Similar set (within 15% of fastest on this sample): flume, crossbeam-channel, std-mpsc, crossbeam-queue, tokio-mpsc, async-channel, steal-deque

See `rust/results.md`.

## javascript

Similar set (within 15% of fastest on this sample): steal-deque, fastq, yocto-queue, denque, p-queue, Array

See `javascript/results.md`.

## csharp

Similar set (within 15% of fastest on this sample): Queue+lock, Channel, ConcurrentQueue

See `csharp/results.md`.

## c

Similar set (within 15% of fastest on this sample): mutex-queue

See `c/results.md`.
