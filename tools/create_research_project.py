#!/usr/bin/env python3
"""Create a research project from the shared workspace template."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "research-project"


def create(destination: Path) -> Path:
    target = destination.expanduser().resolve()
    if target.exists():
        raise ValueError(f"refusing to overwrite existing path: {target}")
    if not TEMPLATE.is_dir():
        raise ValueError(f"project template is missing: {TEMPLATE}")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(TEMPLATE, target)
    for folder in ("idea2paper_runs", "claims", "experiments", "paper", "decisions", "literature"):
        (target / folder).mkdir(exist_ok=True)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="new project directory")
    args = parser.parse_args()
    try:
        target = create(args.destination)
    except ValueError as exc:
        parser.error(str(exc))
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
