#!/usr/bin/env python3
"""Generate reproducibility evidence for the standalone release."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence


STATIC_HASH_PATHS = (
    "README.md",
    "CITATION.cff",
    "CITATION.md",
    "PROVENANCE.md",
    "RELEASE_NOTES.md",
    "LICENSE",
    "BuildAll.lean",
    "lakefile.lean",
    "lake-manifest.json",
    "lean-toolchain",
    ".github/repository-metadata.json",
    ".github/workflows/publish.yml",
    ".github/workflows/verify.yml",
    "scripts/audit_lean.py",
    "scripts/generate_evidence.py",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(command: Sequence[str], cwd: Path) -> dict[str, object]:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        return {
            "command": list(command),
            "exit_code": completed.returncode,
            "output": completed.stdout.strip(),
        }
    except OSError as exc:
        return {
            "command": list(command),
            "exit_code": None,
            "output": f"{type(exc).__name__}: {exc}",
        }


def lean_sources(root: Path) -> list[Path]:
    files: list[Path] = []
    entry = root / "BuildAll.lean"
    if entry.is_file():
        files.append(entry)
    project = root / "PrimalitySheafVerification"
    if project.is_dir():
        files.extend(sorted(project.rglob("*.lean")))
    return files


def hash_targets(root: Path, sources: list[Path]) -> list[Path]:
    result: set[Path] = set(sources)
    for relative in STATIC_HASH_PATHS:
        path = root / relative
        if path.is_file():
            result.add(path)
    return sorted(result, key=lambda path: path.relative_to(root).as_posix())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--evidence-dir", type=Path, required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--release-repository", required=True)
    parser.add_argument("--source-repository", required=True)
    parser.add_argument("--source-ref", required=True)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--mathlib-sha", required=True)
    parser.add_argument("--manuscript-sha256", required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    evidence_dir = args.evidence_dir
    if not evidence_dir.is_absolute():
        evidence_dir = root / evidence_dir
    evidence_dir.mkdir(parents=True, exist_ok=True)

    sources = lean_sources(root)
    if not sources:
        raise SystemExit("No published Lean source files were found.")

    source_rows = []
    total_lines = 0
    total_bytes = 0
    for path in sources:
        data = path.read_bytes()
        lines = len(data.decode("utf-8").splitlines())
        total_lines += lines
        total_bytes += len(data)
        source_rows.append(
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": len(data),
                "lines": lines,
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )

    source_identity = {
        "schema_version": 1,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "release_repository": args.release_repository,
        "release_version": args.version,
        "source_repository": args.source_repository,
        "source_ref": args.source_ref,
        "source_commit": args.source_sha,
        "upstream_mathlib_commit": args.mathlib_sha,
        "lean_toolchain": (root / "lean-toolchain").read_text(
            encoding="utf-8"
        ).strip(),
        "manuscript_bundle": {
            "filename": "overleaf_bundle (Copy)(20260812-034123).pdf",
            "physical_pages": 507,
            "bytes": 4304556,
            "sha256": args.manuscript_sha256,
        },
        "github_actions": {
            "repository": os.environ.get("GITHUB_REPOSITORY"),
            "run_id": os.environ.get("GITHUB_RUN_ID"),
            "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
            "workflow": os.environ.get("GITHUB_WORKFLOW"),
            "runner_os": os.environ.get("RUNNER_OS"),
            "runner_arch": os.environ.get("RUNNER_ARCH"),
        },
    }
    (evidence_dir / "source.json").write_text(
        json.dumps(source_identity, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    inventory = {
        "schema_version": 1,
        "lean_file_count": len(sources),
        "lean_source_lines": total_lines,
        "lean_source_bytes": total_bytes,
        "files": source_rows,
    }
    (evidence_dir / "inventory.json").write_text(
        json.dumps(inventory, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    targets = hash_targets(root, sources)
    hash_lines = [
        f"{sha256(path)}  {path.relative_to(root).as_posix()}" for path in targets
    ]
    (evidence_dir / "hashes.sha256").write_text(
        "\n".join(hash_lines) + "\n", encoding="utf-8"
    )

    environment = {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "git": run(["git", "--version"], root),
        "lean": run(["lake", "env", "lean", "--version"], root),
        "lake": run(["lake", "--version"], root),
        "elan": run(["elan", "--version"], root),
        "git_head_before_release_commit": run(["git", "rev-parse", "HEAD"], root),
        "git_status": run(["git", "status", "--short"], root),
    }
    (evidence_dir / "environment.json").write_text(
        json.dumps(environment, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    summary = [
        "Standalone release evidence",
        f"release repository: {args.release_repository}",
        f"version: {args.version}",
        f"source repository: {args.source_repository}",
        f"source ref: {args.source_ref}",
        f"source commit: {args.source_sha}",
        f"upstream Mathlib commit: {args.mathlib_sha}",
        f"Lean files: {len(sources)}",
        f"Lean source lines: {total_lines}",
        f"Lean source bytes: {total_bytes}",
        f"hashed release inputs: {len(targets)}",
    ]
    (evidence_dir / "SUMMARY.txt").write_text(
        "\n".join(summary) + "\n", encoding="utf-8"
    )

    print("\n".join(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
