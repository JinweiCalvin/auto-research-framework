#!/usr/bin/env python3
"""Create an immutable, minimal Idea2Paper handoff packet for an ARIS project."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
I2P_ROOT = ROOT / "idea2paper"
OUTPUT = I2P_ROOT / "Paper-KG-Pipeline" / "output"
FILES = ("final_story.json", "pipeline_result.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_commit(path: Path) -> str | None:
    try:
        return subprocess.run(
            ["git", "-C", str(path), "rev-parse", "HEAD"],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def safe_slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return slug[:48].strip("-") or "idea2paper"


def package(project: Path, idea: str | None, run_id: str | None) -> Path:
    project = project.expanduser().resolve()
    if not project.is_dir() or not (project / "RESEARCH_BRIEF.md").is_file():
        raise ValueError(f"not a research project (RESEARCH_BRIEF.md missing): {project}")
    sources = {name: OUTPUT / name for name in FILES}
    missing = [str(path) for path in sources.values() if not path.is_file()]
    if missing:
        raise ValueError("missing Idea2Paper outputs: " + ", ".join(missing))

    parsed: dict[str, object] = {}
    for name, path in sources.items():
        try:
            parsed[name] = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"invalid JSON in {path}: {exc}") from exc
    story = parsed["final_story.json"]
    if not isinstance(story, dict) or not any(story.get(key) for key in ("title", "abstract", "problem_framing")):
        raise ValueError("final_story.json has no recognizable story fields")

    title = str(story.get("title") or "idea2paper")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    name = run_id or f"{stamp}_{safe_slug(title)}"
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,100}", name):
        raise ValueError("run id may contain only letters, numbers, dot, underscore and hyphen")
    destination = project / "idea2paper_runs" / name
    if destination.exists():
        raise ValueError(f"refusing to overwrite existing run: {destination}")
    destination.mkdir(parents=True)
    for filename, source in sources.items():
        shutil.copy2(source, destination / filename)

    manifest = {
        "schema_version": 1,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "run_id": name,
        "idea": idea,
        "title": title,
        "source_repository": "idea2paper",
        "source_commit": git_commit(I2P_ROOT),
        "artifacts": {filename: {"sha256": sha256(destination / filename)} for filename in FILES},
        "limits": [
            "Idea2Paper scores and local novelty checks are screening signals, not external verification.",
            "Proposed experiments and numerical outcomes are unverified unless supported by execution artifacts.",
            "This packet contains only final_story.json and pipeline_result.json; inspect logs separately when needed.",
        ],
    }
    (destination / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prompt = f"""# ARIS handoff: {title}

Read `manifest.json`, `final_story.json`, and `pipeline_result.json`. Treat this as a candidate research narrative and machine review record, not as established evidence. Do not repeat proposed or generated metrics as measured results.

1. Extract the research question, method, atomic claims, assumptions, risks, and unresolved questions.
2. Verify novelty claims against external literature and attach stable paper identifiers and source locators.
3. Populate the project-level `CLAIMS_AND_EVIDENCE.md`; identify what is unsupported or contradicted.
4. Produce a minimal falsifiable experiment plan in `EXPERIMENT_PLAN.md`, including datasets, versions, strongest feasible baselines, metrics, ablations, failure criteria, commands, and resource estimates.
5. Do not launch costly or remote experiments until the plan and resource requirements have been reviewed by the user.

Idea supplied for this run: {idea or '(not recorded)'}
"""
    (destination / "ARIS_HANDOFF.md").write_text(prompt, encoding="utf-8")
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir", type=Path, help="existing research project directory")
    parser.add_argument("--idea", help="original idea text; do not include secrets")
    parser.add_argument("--run-id", help="optional unique run id")
    args = parser.parse_args()
    try:
        destination = package(args.project_dir, args.idea, args.run_id)
    except ValueError as exc:
        parser.error(str(exc))
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
