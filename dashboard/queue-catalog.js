/**
 * Communication category for each logged library name.
 * T = thread, A = async, scheduler = not a handoff queue.
 * P / S / D have no runners yet.
 */
export const QUEUE_CATALOG = {
  'Queue+lock': { communication: 'thread', family: 'locked' },
  ConcurrentQueue: { communication: 'thread', family: 'concurrent' },
  Channel: { communication: 'async', family: 'async' },
  'deque-lock': { communication: 'thread', family: 'locked' },
  'queue.Queue': { communication: 'thread', family: 'concurrent' },
  'asyncio.Queue': { communication: 'async', family: 'async' },
  'spsc-ring': { communication: 'thread', family: 'spsc' },
  'mutex-queue': { communication: 'thread', family: 'locked' },
  'std-mpsc': { communication: 'thread', family: 'concurrent' },
  'crossbeam-channel': { communication: 'thread', family: 'concurrent' },
  'crossbeam-queue': { communication: 'thread', family: 'concurrent' },
  'tokio-mpsc': { communication: 'async', family: 'async' },
  Array: { communication: 'thread', family: 'locked' },
  fastq: { communication: 'thread', family: 'concurrent' },
  'p-queue': { communication: 'scheduler', family: 'scheduler' },
};

export const COMMUNICATION_ORDER = ['all', 'thread', 'async', 'other'];

export function communicationOf(name) {
  return QUEUE_CATALOG[name]?.communication || 'unknown';
}

export function communicationBucket(name) {
  const c = communicationOf(name);
  if (c === 'thread' || c === 'async') return c;
  return 'other';
}

export function communicationLabel(id) {
  if (id === 'all') return 'All';
  if (id === 'thread') return 'Thread (T)';
  if (id === 'async') return 'Async (A)';
  if (id === 'other') return 'Other';
  return id;
}
