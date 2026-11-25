#!/usr/bin/env python3
"""Deliver the 2026-11-25 news-image entry.

The finished picture lives beside this file as entry.png. This script
only moves those bytes into the grading folder. Nothing is drawn,
fetched, or randomised here, so the result is identical on every run.
"""

import os
import shutil
import sys
from pathlib import Path

ENTRY_NAME = "entry.png"
DEFAULT_OUT = "/output"


def bundled_picture() -> Path:
    folder = Path(__file__).resolve().parent
    picture = folder / ENTRY_NAME
    if not picture.is_file():
        raise FileNotFoundError(
            f"bundled picture {picture} is missing; "
            "the entry cannot be built without it"
        )
    return picture


def out_folder() -> Path:
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUT
    return Path(wanted).expanduser()


def deliver() -> Path:
    origin = bundled_picture()
    folder = out_folder()
    folder.mkdir(parents=True, exist_ok=True)
    result = folder / ENTRY_NAME
    shutil.copyfile(origin, result)
    # Confirm the copy is complete before reporting success: a short
    # or truncated write must fail loudly instead of shipping a
    # corrupt entry to the grader.
    if result.stat().st_size != origin.stat().st_size:
        raise OSError(
            f"copied {result} has {result.stat().st_size} bytes, "
            f"expected {origin.stat().st_size}"
        )
    return result


def run() -> int:
    try:
        placed = deliver()
    except FileNotFoundError as problem:
        print(f"error: {problem}", file=sys.stderr)
        return 1
    except OSError as problem:
        print(f"error: failed to write the entry: {problem}", file=sys.stderr)
        return 1
    print(f"Wrote {placed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
