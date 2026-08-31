# Timing honesty

**Prepare is not timed. The loop is timed. Warmup stays in the raw CSV.**

1. Construct the queue, allocate payloads, spawn threads **before** the clock.
2. Do not enqueue items during prepare “to warm the queue.”
3. Write every repetition, including index `0`. Analysis drops warmup.
4. A failed fidelity check is an error row, not a fast time.
5. Label must match work: if the cell is **MPMC** (CSV `stream`), two producers
   and two consumers actually ran. Otherwise skip the cell. Do not call this
   a stream API.
