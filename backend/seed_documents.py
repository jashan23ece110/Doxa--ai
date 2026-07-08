#!/usr/bin/env python3
"""
Seed script: reads all files from sample_docs/ and ingests them into the
RAG knowledge base via rag.add_document().
"""

import os
import sys

# Ensure the backend directory is on the path
sys.path.insert(0, os.path.dirname(__file__))

from rag import add_document


SAMPLE_DOCS_DIR = os.path.join(os.path.dirname(__file__), "sample_docs")


def main():
    if not os.path.isdir(SAMPLE_DOCS_DIR):
        print(f"ERROR: sample_docs directory not found at {SAMPLE_DOCS_DIR}")
        sys.exit(1)

    files = sorted(
        f
        for f in os.listdir(SAMPLE_DOCS_DIR)
        if os.path.isfile(os.path.join(SAMPLE_DOCS_DIR, f))
    )

    if not files:
        print("No files found in sample_docs/")
        sys.exit(0)

    print(f"Found {len(files)} file(s) in sample_docs/\n")

    for filename in files:
        filepath = os.path.join(SAMPLE_DOCS_DIR, filename)
        print(f"Processing: {filename} ... ", end="", flush=True)

        with open(filepath, "rb") as f:
            content_bytes = f.read()

        try:
            result = add_document(filename, content_bytes)
            print(
                f"OK — doc_id={result['doc_id']}, "
                f"chunks={result['chunks_count']}"
            )
        except Exception as e:
            print(f"FAILED — {e}")

    print("\nSeeding complete.")


if __name__ == "__main__":
    main()
