import sys
import os
from typing import Any, Iterable
import pandas as pd

from fileStreams import getFileJsonStream

# Output JSONL file path
output_jsonl_file = "output_submissions_amateurroomporn_subreddits.jsonl"

def processRow(row: dict[str, Any]):
    global output_jsonl_file

    # Check if the 'subreddit' column contains the word 'amateurroomporn'
    if 'amateurroomporn' in row.get('subreddit', '').lower():
        # Save the row as a JSON line in the output file
        with open(output_jsonl_file, 'a') as file:
            json_line = pd.Series(row).to_json(orient='records')
            file.write(json_line + '\n')

def processFile(path: str):
    jsonStream = getFileJsonStream(path)
    if jsonStream is None:
        print(f"Skipping unknown file {path}")
        return
    for i, (lineLength, row) in enumerate(jsonStream):
        if i % 10_000 == 0:
            print(f"\rRow {i}", end="")
        
        # Use the processRow function to handle the row
        processRow(row)

    print(f"\rProcessing complete for {i+1} rows in file: {path}")

def processFolder(path: str, recursive: bool = False):
    fileIterator: Iterable[str]
    if recursive:
        def recursiveFileIterator():
            for root, dirs, files in os.walk(path):
                for file in files:
                    yield os.path.join(root, file)
        fileIterator = recursiveFileIterator()
    else:
        fileIterator = [os.path.join(path, 'RS_2023-03.zst')]

    for i, file in enumerate(fileIterator):
        print(f"Processing file {i+1: 3} {file}")
        processFile(file)

def main():
    # Replace <path to file or folder> with the actual path
    fileOrFolderPath = r"pushshift-reddit-2023-03"

    # Set recursive to True if you want to include subdirectories, False otherwise
    recursive = False

    if os.path.isdir(fileOrFolderPath):
        processFolder(fileOrFolderPath, recursive=recursive)
    else:
        processFile(fileOrFolderPath)

    print("Done :>")

if __name__ == "__main__":
    main()