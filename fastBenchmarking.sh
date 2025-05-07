#!/bin/bash

# Directory containing subfolders
RESULTS_DIR="results/scenario1"

# Loop through all subdirectories in the results directory
for dir in "$RESULTS_DIR"/*/; do
    # Remove trailing slash and extract subfolder name
    ID=$(basename "$dir")
    
    # Execute the Python program with the arguments
    python benchmarkMetrics.py --results_folder "$RESULTS_DIR" --verbose True --id "$ID"
done