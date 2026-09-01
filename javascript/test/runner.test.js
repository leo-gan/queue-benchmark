const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("fs");
const path = require("path");

test("runner source exists", () => {
  const p = path.join(__dirname, "..", "src", "runner.js");
  assert.ok(fs.existsSync(p));
  const src = fs.readFileSync(p, "utf8");
  assert.match(src, /LibraryName/);
  assert.match(src, /scheduler/);
  assert.match(src, /benchWakeup/);
  assert.match(src, /benchCancel/);
  assert.match(src, /steal-deque/);
  assert.match(src, /pipe-ipc/);
  assert.match(src, /sqlite-queue/);
  assert.match(src, /denque/);
  assert.match(src, /yocto-queue/);
  assert.doesNotMatch(src, /Python-only/);
});

test("denque FIFO roundtrip", () => {
  const Denque = require("denque");
  const q = new Denque();
  q.push(Buffer.from("a"));
  q.push(Buffer.from("b"));
  assert.equal(q.shift().toString(), "a");
  assert.equal(q.shift().toString(), "b");
});

test("yocto-queue FIFO roundtrip", async () => {
  const { default: Queue } = await import("yocto-queue");
  const q = new Queue();
  q.enqueue(Buffer.from("a"));
  q.enqueue(Buffer.from("b"));
  assert.equal(q.dequeue().toString(), "a");
  assert.equal(q.dequeue().toString(), "b");
});
