import os
import json
import random
import string
import csv

def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_jsonl(filename, num_records, size_bytes):
    with open(filename, 'w') as f:
        for _ in range(num_records):
            payload = random_string(size_bytes)
            record = {"payload": payload}
            f.write(json.dumps(record) + '\n')

def generate_csv(filename, num_records, size_bytes):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["payload"])
        for _ in range(num_records):
            payload = random_string(size_bytes)
            writer.writerow([payload])

def generate_folder(folder, num_records, size_bytes):
    os.makedirs(folder, exist_ok=True)
    for i in range(num_records):
        payload = random_string(size_bytes)
        with open(os.path.join(folder, f"{i}.txt"), "w") as f:
            f.write(payload)

if __name__ == '__main__':
    # Generate small subset for testing the benchmark suite
    generate_jsonl('datasets/test_small.jsonl', 10, 64)
    generate_csv('datasets/test_small.csv', 10, 64)
    generate_folder('datasets/test_folder', 10, 64)
    print("Test data generated in datasets/")
