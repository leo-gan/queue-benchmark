# Experiment plan

One question per folder. Never compare times across languages. Group libraries
by Cliff’s δ vs the fastest (similar / close / slower). Do not crown a winner.

| # | Folder | Status | Question |
|---|--------|--------|----------|
| 1 | [01-spsc-handoff](01-spsc-handoff/) | Ready | Which in-process queue is fastest for a single producer handing a small message to a single consumer? |
| 2 | [02-payload-size](02-payload-size/) | Ready | Does that ranking stay the same when the payload grows from 256 B to 4 KiB? |

Run 1, then 2. Later experiments can add bounded vs unbounded, or more
producers, without changing these two questions.
