#!/bin/bash
set -e

echo "Installing global dependencies..."
sudo apt-get update
sudo apt-get install -y build-essential libzmq3-dev

echo "Installing Python dependencies..."
pip3 install -r python/requirements.txt
pip3 install mkdocs mkdocs-material

echo "Installing JavaScript dependencies..."
cd javascript && npm install && cd ..

echo "Installing Rust dependencies..."
cd rust_benchmark && cargo build --release && cd ..

echo "Building C benchmarks..."
cd c_benchmark && make clean && make && cd ..

echo "Restoring C# dependencies..."
cd csharp && dotnet restore && dotnet build -c Release && cd ..

echo "All dependencies installed successfully!"
