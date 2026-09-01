# Adding a queue

1. Implement the language adapter (see the language README).
2. Register the name **exactly** as it will appear in `LibraryName`.
3. Report the installed package/crate version in `LibraryVersion`.
4. Implement **SPSC**. Implement **MPMC** only if the library is actually MPMC;
   otherwise skip MPMC cells (CSV `io_mode=stream`). Set `communication` to
   `thread` or `async` in `config/benchmark_config.yaml`. If the library cannot
   bound (`maxsize`), set `supports_bounded = False` so backpressure cells are
   skipped. Do not register a concurrency limiter as an async handoff queue.
5. Add the inventory row under `languages.<id>.queues` in
   `config/benchmark_config.yaml`.
6. Add a dependency pin (uv / cargo / npm / csproj / cmake).
7. Document it on `docs/<lang>/index.md`.
8. Smoke, then `all-single`, then `analyze-benchmarks -l <lang>`.
