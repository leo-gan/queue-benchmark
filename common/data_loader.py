import json
import csv
import os

def load_data(path):
    data = []
    if os.path.isdir(path):
        for filename in os.listdir(path):
            with open(os.path.join(path, filename), 'r') as f:
                data.append(f.read())
    elif path.endswith('.jsonl'):
        with open(path, 'r') as f:
            for line in f:
                data.append(json.loads(line)['payload'])
    elif path.endswith('.csv'):
        with open(path, 'r') as f:
            reader = csv.reader(f)
            next(reader) # skip header
            for row in reader:
                data.append(row[0])
    return data
