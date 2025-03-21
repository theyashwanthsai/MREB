#!/bin/bash

echo "Running evaluation script..."
python ./scripts/evaluate.py

echo "Running benchmark script..."
python ./scripts/benchmark.py

echo "Running plot script..."
python ./scripts/plots.py

echo "All scripts completed."