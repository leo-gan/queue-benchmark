use std::fs;
use std::path::Path;
use serde::Deserialize;

#[derive(Deserialize)]
struct Record {
    payload: String,
}

pub fn load_data(path: &str) -> Vec<String> {
    let mut data = Vec::new();
    let p = Path::new(path);

    if p.is_dir() {
        for entry in fs::read_dir(p).unwrap() {
            let entry = entry.unwrap();
            let content = fs::read_to_string(entry.path()).unwrap();
            data.push(content);
        }
    } else if path.ends_with(".jsonl") {
        let content = fs::read_to_string(path).unwrap();
        for line in content.lines() {
            let record: Record = serde_json::from_str(line).unwrap();
            data.push(record.payload);
        }
    } else if path.ends_with(".csv") {
        let content = fs::read_to_string(path).unwrap();
        for line in content.lines().skip(1) { // skip header
            data.push(line.to_string());
        }
    }
    data
}
