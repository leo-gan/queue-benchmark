# 08-async-backpressure

Times are not comparable across languages.

## python

Similar set (within 15% of fastest on this sample): deque-lock

See `python/results.md`.

## rust

Similar set (within 15% of fastest on this sample): steal-deque, crossbeam-queue, std-mpsc

See `rust/results.md`.

## javascript

Similar set (within 15% of fastest on this sample): fastq

See `javascript/results.md`.

## csharp

Similar set (within 15% of fastest on this sample): ConcurrentQueue

See `csharp/results.md`.

## c

Similar set (within 15% of fastest on this sample): spsc-ring

See `c/results.md`.
