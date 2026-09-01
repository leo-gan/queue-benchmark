# 05-wakeup

Times are not comparable across languages.

## python

Similar set (within 15% of fastest on this sample): queue.Queue, queue.SimpleQueue, asyncio.Queue, janus

See `python/results.md`.

## rust

Similar set (within 15% of fastest on this sample): async-channel, steal-deque, crossbeam-queue, flume, tokio-mpsc, std-mpsc, crossbeam-channel

See `rust/results.md`.

## javascript

Similar set (within 15% of fastest on this sample): yocto-queue, denque, p-queue, Array, steal-deque, fastq

See `javascript/results.md`.

## csharp

Similar set (within 15% of fastest on this sample): ConcurrentQueue, Channel, BlockingCollection, Queue+lock

See `csharp/results.md`.

## c

Similar set (within 15% of fastest on this sample): mutex-queue

See `c/results.md`.
