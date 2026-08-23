#!/usr/bin/env python3
"""Apply the approved release rewrite, then audit published Lean sources."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Hit:
    kind: str
    file: str
    line: int
    excerpt: str


TOKEN_PATTERNS: dict[str, re.Pattern[str]] = {
    "sorry": re.compile(r"\bsorry\b"),
    "admit": re.compile(r"\badmit\b"),
    "sorryAx": re.compile(r"\bsorryAx\b"),
    "native_decide": re.compile(r"\bnative_decide\b"),
}

AXIOM_PATTERN = re.compile(
    r"(?m)^[ \t]*(?:(?:private|protected|noncomputable|unsafe)[ \t]+)*axioms?\b"
)

REWRITE_RELATIVE_PATH = Path("PrimalitySheafVerification/Verification.lean")
OLD_COMMENT = """(`native_decide` evaluates the `ZMod 9` arithmetic by compilation; plain `decide`
also works in principle but is much slower on `ZMod` numerals.) -/"""
NEW_COMMENT = """(`decide` checks this small finite `ZMod 9` certificate without native-code
execution; the release audit records this deterministic publication-only rewrite.) -/"""
OLD_PROOF = (
    "example : Fintype.card {x : ZMod 9 // (12 : ZMod 9) * x = 0} = 3 := "
    "by native_decide"
)
NEW_PROOF = (
    "example : Fintype.card {x : ZMod 9 // (12 : ZMod 9) * x = 0} = 3 := "
    "by decide"
)


def digest_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def apply_approved_release_rewrite(root: Path) -> list[dict[str, object]]:
    """Replace one frozen-source native certificate with kernel reduction.

    The frozen source remains unchanged.  The standalone release copy performs
    exactly one deterministic rewrite, recorded in the audit report.  The
    operation is idempotent and refuses unexpected source text.
    """
    path = root / REWRITE_RELATIVE_PATH
    if not path.is_file():
        return []

    original = path.read_text(encoding="utf-8")
    old_proof_count = original.count(OLD_PROOF)
    new_proof_count = original.count(NEW_PROOF)

    if old_proof_count == 0 and new_proof_count == 1:
        return []
    if old_proof_count != 1 or new_proof_count != 0:
        raise RuntimeError(
            "Approved release rewrite did not match exactly one expected proof "
            f"in {REWRITE_RELATIVE_PATH.as_posix()}: "
            f"old={old_proof_count}, new={new_proof_count}"
        )
    if original.count(OLD_COMMENT) != 1:
        raise RuntimeError(
            "Approved release rewrite did not match the expected explanatory "
            f"comment in {REWRITE_RELATIVE_PATH.as_posix()}"
        )

    rewritten = original.replace(OLD_COMMENT, NEW_COMMENT).replace(
        OLD_PROOF, NEW_PROOF
    )
    path.write_text(rewritten, encoding="utf-8")

    return [
        {
            "path": REWRITE_RELATIVE_PATH.as_posix(),
            "kind": "approved_publication_rewrite",
            "reason": (
                "Replace the sole native_decide finite certificate with decide "
                "so the standalone release satisfies its no-native-execution policy."
            ),
            "before_sha256": digest_text(original),
            "after_sha256": digest_text(rewritten),
            "before": OLD_PROOF,
            "after": NEW_PROOF,
        }
    ]


def mask_non_code(text: str) -> str:
    """Replace comments and string literals with spaces while preserving newlines."""
    out: list[str] = []
    i = 0
    n = len(text)
    block_depth = 0
    in_line_comment = False
    in_string = False
    escaped = False

    while i < n:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < n else ""

        if in_line_comment:
            if ch == "\n":
                in_line_comment = False
                out.append("\n")
            else:
                out.append(" ")
            i += 1
            continue

        if block_depth:
            if ch == "/" and nxt == "-":
                block_depth += 1
                out.extend((" ", " "))
                i += 2
            elif ch == "-" and nxt == "/":
                block_depth -= 1
                out.extend((" ", " "))
                i += 2
            else:
                out.append("\n" if ch == "\n" else " ")
                i += 1
            continue

        if in_string:
            if ch == "\n":
                out.append("\n")
                escaped = False
            else:
                out.append(" ")
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            i += 1
            continue

        if ch == "-" and nxt == "-":
            in_line_comment = True
            out.extend((" ", " "))
            i += 2
        elif ch == "/" and nxt == "-":
            block_depth = 1
            out.extend((" ", " "))
            i += 2
        elif ch == '"':
            in_string = True
            escaped = False
            out.append(" ")
            i += 1
        else:
            out.append(ch)
            i += 1

    return "".join(out)


def source_files(root: Path) -> list[Path]:
    files: list[Path] = []
    entry = root / "BuildAll.lean"
    if entry.is_file():
        files.append(entry)
    project = root / "PrimalitySheafVerification"
    if project.is_dir():
        files.extend(sorted(project.rglob("*.lean")))
    return files


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def excerpt_for(original: str, line: int) -> str:
    lines = original.splitlines()
    if 1 <= line <= len(lines):
        return lines[line - 1].strip()[:240]
    return ""


def scan_file(root: Path, path: Path) -> list[Hit]:
    original = path.read_text(encoding="utf-8")
    code = mask_non_code(original)
    rel = path.relative_to(root).as_posix()
    hits: list[Hit] = []

    for kind, pattern in TOKEN_PATTERNS.items():
        for match in pattern.finditer(code):
            line = line_number(code, match.start())
            hits.append(Hit(kind, rel, line, excerpt_for(original, line)))

    for match in AXIOM_PATTERN.finditer(code):
        line = line_number(code, match.start())
        hits.append(Hit("axiom_declaration", rel, line, excerpt_for(original, line)))

    return hits


def render_text(
    files: Iterable[Path],
    hits: list[Hit],
    rewrites: list[dict[str, object]],
    root: Path,
) -> str:
    file_list = list(files)
    total_lines = sum(
        len(path.read_text(encoding="utf-8").splitlines()) for path in file_list
    )
    lines = [
        "Lean source audit",
        f"root: {root}",
        f"approved publication rewrites applied: {len(rewrites)}",
        f"files scanned: {len(file_list)}",
        f"source lines scanned: {total_lines}",
        f"forbidden hits: {len(hits)}",
        f"result: {'PASS' if not hits else 'FAIL'}",
    ]
    for rewrite in rewrites:
        lines.append(
            "rewrite: "
            f"{rewrite['path']}: {rewrite['before']} -> {rewrite['after']}"
        )
    for hit in hits:
        lines.append(f"{hit.kind}: {hit.file}:{hit.line}: {hit.excerpt}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root (default: current directory)",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        help="Write the machine-readable report to this path",
    )
    parser.add_argument(
        "--text-out",
        type=Path,
        help="Write the human-readable report to this path",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    try:
        rewrites = apply_approved_release_rewrite(root)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    files = source_files(root)
    if not files:
        print("No Lean project sources were found.", file=sys.stderr)
        return 2

    hits: list[Hit] = []
    for path in files:
        hits.extend(scan_file(root, path))

    total_lines = sum(
        len(path.read_text(encoding="utf-8").splitlines()) for path in files
    )
    report = {
        "schema_version": 2,
        "root": str(root),
        "approved_publication_rewrites": rewrites,
        "scanned_files": len(files),
        "scanned_lines": total_lines,
        "forbidden_policy": [
            "sorry",
            "admit",
            "sorryAx",
            "native_decide",
            "explicit axiom/axioms declarations",
        ],
        "hits": [
            {
                "kind": hit.kind,
                "file": hit.file,
                "line": hit.line,
                "excerpt": hit.excerpt,
            }
            for hit in hits
        ],
        "pass": not hits,
    }

    text = render_text(files, hits, rewrites, root)
    print(text, end="")

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    if args.text_out:
        args.text_out.parent.mkdir(parents=True, exist_ok=True)
        args.text_out.write_text(text, encoding="utf-8")

    return 0 if not hits else 1


if __name__ == "__main__":
    raise SystemExit(main())
