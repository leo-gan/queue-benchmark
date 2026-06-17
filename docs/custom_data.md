# Custom Data

You can benchmark queues with your own payloads. We support datasets formatted as:
1. `.jsonl` files (where each line is `{"payload": "data"}`)
2. `.csv` files (where the first row is `payload` header)
3. A folder of text files (each file is one payload)

Simply pass the dataset path as an argument to the benchmark runner.
