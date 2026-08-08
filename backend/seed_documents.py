#!/usr/bin/env python3
"""
Seed script: reads all files from sample_docs/ and ingests them into the
RAG knowledge base via document_service.add_document().
"""

import os
import sys

# Ensure the backend directory is on Python path
sys.path.insert(0, os.path.dirname(__file__))

from app.services.document_service import document_service
from app.core.logging import logger

SAMPLE_DOCS_DIR = os.path.join(os.path.dirname(__file__), "sample_docs")


def main():
    if not os.path.isdir(SAMPLE_DOCS_DIR):
        logger.error(f"sample_docs directory not found at {SAMPLE_DOCS_DIR}")
        sys.exit(1)

    files = sorted(
        f
        for f in os.listdir(SAMPLE_DOCS_DIR)
        if os.path.isfile(os.path.join(SAMPLE_DOCS_DIR, f))
    )

    if not files:
        logger.info("No files found in sample_docs/")
        sys.exit(0)

    logger.info(f"Found {len(files)} file(s) in sample_docs/\n")

    for filename in files:
        filepath = os.path.join(SAMPLE_DOCS_DIR, filename)
        logger.info(f"Processing: {filename} ... ")

        with open(filepath, "rb") as f:
            content_bytes = f.read()

        try:
            result = document_service.add_document(filename, content_bytes)
            logger.info(
                f"OK — doc_id={result['doc_id']}, "
                f"chunks={result['chunks_count']}"
            )
        except Exception as e:
            logger.error(f"FAILED processing {filename} — {e}")

    logger.info("Seeding complete.")


if __name__ == "__main__":
    main()
