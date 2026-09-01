/**
 * Communication category for each logged library name.
 * T = thread, A = async, scheduler = not a handoff queue.
 * P / S / D have no runners yet.
 */
export const QUEUE_CATALOG = {
  'Queue+lock': { communication: 'thread', family: 'locked' },
  ConcurrentQueue: { communication: 'thread', family: 'concurrent' },
  BlockingCollection: { communication: 'thread', family: 'concurrent' },
  Channel: { communication: 'async', family: 'async' },
  'deque-lock': { communication: 'thread', family: 'locked' },
  'queue.Queue': { communication: 'thread', family: 'concurrent' },
  'queue.SimpleQueue': { communication: 'thread', family: 'concurrent' },
  'asyncio.Queue': { communication: 'async', family: 'async' },
  janus: { communication: 'async', family: 'async' },
  'spsc-ring': { communication: 'thread', family: 'spsc' },
  'mutex-queue': { communication: 'thread', family: 'locked' },
  lfqueue: { communication: 'thread', family: 'concurrent' },
  'std-mpsc': { communication: 'thread', family: 'concurrent' },
  'crossbeam-channel': { communication: 'thread', family: 'concurrent' },
  flume: { communication: 'thread', family: 'concurrent' },
  'crossbeam-queue': { communication: 'thread', family: 'concurrent' },
  'tokio-mpsc': { communication: 'async', family: 'async' },
  'async-channel': { communication: 'async', family: 'async' },
  Array: { communication: 'thread', family: 'locked' },
  denque: { communication: 'thread', family: 'locked' },
  'yocto-queue': { communication: 'thread', family: 'locked' },
  fastq: { communication: 'thread', family: 'concurrent' },
  'p-queue': { communication: 'scheduler', family: 'scheduler' },
  'multiprocessing.Queue': { communication: 'process', family: 'concurrent' },
  'multiprocessing.SimpleQueue': { communication: 'process', family: 'concurrent' },
  'shared-ring': { communication: 'shared', family: 'spsc' },
  'sqlite-queue': { communication: 'durable', family: 'durable' },
};

export const COMMUNICATION_ORDER = [
  'all',
  'thread',
  'async',
  'process',
  'shared',
  'durable',
  'other',
];

export function communicationOf(name) {
  return QUEUE_CATALOG[name]?.communication || 'unknown';
}

export function communicationBucket(name) {
  const c = communicationOf(name);
  if (c === 'thread' || c === 'async' || c === 'process' || c === 'shared' || c === 'durable') {
    return c;
  }
  return 'other';
}

export function communicationLabel(id) {
  if (id === 'all') return 'All';
  if (id === 'thread') return 'Thread (T)';
  if (id === 'async') return 'Async (A)';
  if (id === 'process') return 'Process (P)';
  if (id === 'shared') return 'Shared (S)';
  if (id === 'durable') return 'Durable (D)';
  if (id === 'other') return 'Other';
  return id;
}
