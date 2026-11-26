#!/usr/bin/env python3
"""Entrypoint for the 26 November 2026 news-image entry.

The entry image is committed in this repository as entry.png; this
program simply places a copy of it at the output path, exactly as
the brief suggests. Standard library only, no network, no
randomness: every run writes the same bytes. The output directory
comes from $MAKEFUN_OUTPUT_DIR when set, otherwise /output.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
DEST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DEST = os.path.join(DEST_DIR, "entry.png")


def main():
    os.makedirs(DEST_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    print("wrote " + DEST)


if __name__ == "__main__":
    main()
