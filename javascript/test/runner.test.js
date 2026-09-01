const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("fs");
const path = require("path");

test("runner source exists", () => {
  const p = path.join(__dirname, "..", "src", "runner.js");
  assert.ok(fs.existsSync(p));
  const src = fs.readFileSync(p, "utf8");
  assert.match(src, /SerializerName/);
  assert.match(src, /scheduler/);
  assert.match(src, /benchWakeup/);
  assert.match(src, /benchCancel/);
  assert.doesNotMatch(src, /Python-only/);
});
