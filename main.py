"""News-image entry for 25 November 2026.

This program ships the finished collage, ``entry.png``, to the directory
the grader reads from. It performs no drawing, no downloading and no
random work: it copies one fixed file, byte for byte, so every run
produces exactly the same output.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

IMAGE_FILENAME = "entry.png"


def locate_collage() -> Path:
    """Return the collage bundled next to this script."""
    here = Path(__file__).resolve().parent
    candidate = here / IMAGE_FILENAME
    if not candidate.is_file():
        raise FileNotFoundError(
            f"Missing bundled image: expected {candidate} next to main.py, "
            "but no such file was found. The entry cannot be produced "
            "without it."
        )
    return candidate


def locate_target_dir() -> Path:
    """Return the grader output directory from the environment."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = Path(raw).expanduser()
    return target


def publish_collage() -> Path:
    """Copy the bundled collage to the output directory and return its path."""
    source = locate_collage()
    destination_dir = locate_target_dir()
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / IMAGE_FILENAME
    # copyfile moves bytes only: no timestamps, metadata or randomness
    # leak into the result, so repeated runs stay identical. The output
    # is deterministic because the source file is fixed and nothing in
    # this program depends on the clock, the network or random data.
    shutil.copyfile(source, destination)
    return destination


def main() -> int:
    try:
        written = publish_collage()
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"error: could not write the entry image: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote {written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
