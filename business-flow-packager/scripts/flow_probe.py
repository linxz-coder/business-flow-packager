#!/usr/bin/env python3
"""Read-only probe for candidate business workflow folders."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


SCRIPT_SUFFIXES = {
    ".py",
    ".sh",
    ".command",
    ".js",
    ".ts",
    ".mjs",
    ".cjs",
    ".ps1",
    ".bat",
    ".applescript",
    ".sql",
    ".ipynb",
}
DOC_SUFFIXES = {".md", ".txt", ".pdf", ".doc", ".docx", ".pages", ".rtf"}
DATA_SUFFIXES = {".csv", ".tsv", ".xlsx", ".xls", ".json", ".jsonl", ".sqlite", ".db"}
CONFIG_SUFFIXES = {".env", ".ini", ".toml", ".yaml", ".yml", ".plist", ".conf", ".cfg"}
OUTPUT_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".pptx", ".pdf", ".zip", ".tar", ".gz"}
SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "Library",
}
SECRET_WORDS = ("secret", "token", "cookie", "credential", "password", "key", ".env")


@dataclass
class FileHit:
    path: str
    kind: str
    size: int
    modified: str


def iso_time(ts: float) -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S %z", time.localtime(ts))


def classify(path: Path) -> str | None:
    lower_name = path.name.lower()
    suffix = path.suffix.lower()
    if suffix in SCRIPT_SUFFIXES:
        return "script"
    if suffix in DOC_SUFFIXES:
        return "doc"
    if suffix in DATA_SUFFIXES:
        return "data"
    if suffix in CONFIG_SUFFIXES or lower_name in {"dockerfile", "makefile"}:
        return "config"
    if suffix in OUTPUT_SUFFIXES:
        return "output"
    if path.is_dir() and suffix in {".app"}:
        return "app"
    return None


def should_skip_dir(path: Path) -> bool:
    if path.name in SKIP_DIRS:
        return True
    if path.name.startswith(".") and path.name not in {".github"}:
        return True
    return False


def iter_files(root: Path, max_depth: int, max_files: int) -> Iterable[Path]:
    root = root.expanduser().resolve()
    if root.is_file():
        yield root
        return
    if not root.exists():
        return
    count = 0
    base_parts = len(root.parts)
    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        depth = len(current_path.parts) - base_parts
        dirs[:] = [d for d in dirs if not should_skip_dir(current_path / d)]
        if depth >= max_depth:
            dirs[:] = []
        for name in files:
            count += 1
            if count > max_files:
                return
            yield current_path / name


def collect(paths: list[Path], max_depth: int, max_files: int) -> dict:
    hits: list[FileHit] = []
    risk_flags: list[str] = []
    missing: list[str] = []
    by_kind: dict[str, int] = {}

    for root in paths:
        expanded = root.expanduser()
        if not expanded.exists():
            missing.append(str(expanded))
            continue
        for path in iter_files(expanded, max_depth=max_depth, max_files=max_files):
            try:
                stat = path.stat()
            except OSError:
                continue
            kind = classify(path)
            lower = str(path).lower()
            if any(word in lower for word in SECRET_WORDS):
                risk_flags.append(f"possible secret/config path: {path}")
            if kind is None:
                continue
            by_kind[kind] = by_kind.get(kind, 0) + 1
            hits.append(
                FileHit(
                    path=str(path),
                    kind=kind,
                    size=stat.st_size,
                    modified=iso_time(stat.st_mtime),
                )
            )

    hits.sort(key=lambda item: item.modified, reverse=True)
    return {
        "paths": [str(path.expanduser()) for path in paths],
        "missing_paths": missing,
        "counts": by_kind,
        "recent_files": [asdict(item) for item in hits[:80]],
        "risk_flags": sorted(set(risk_flags))[:80],
        "scriptability_signals": build_signals(by_kind, hits, risk_flags),
        "script_panel": probe_script_panel(),
    }


def build_signals(by_kind: dict[str, int], hits: list[FileHit], risk_flags: list[str]) -> list[str]:
    signals: list[str] = []
    if by_kind.get("script", 0):
        signals.append("existing scripts found; prefer reuse or wrapper over rewriting")
    if by_kind.get("config", 0):
        signals.append("config files found; inspect for env/config pattern before hardcoding")
    if by_kind.get("data", 0):
        signals.append("data/workbook files found; identify inputs and expected output files")
    if by_kind.get("doc", 0):
        signals.append("docs found; inspect for runbook or SOP details")
    if by_kind.get("output", 0):
        signals.append("output artifacts found; use them as verification targets")
    if risk_flags:
        signals.append("possible secrets or credential paths found; review before packaging or pushing")
    if not hits:
        signals.append("no candidate files found; ask for a path or concrete workflow evidence")
    return signals


def probe_script_panel() -> dict:
    commands_path = Path("~/script-manager/commands.json").expanduser()
    result: dict[str, object] = {
        "commands_json": str(commands_path),
        "commands_json_exists": commands_path.exists(),
        "api": "http://127.0.0.1:8787/api/commands",
    }
    if commands_path.exists():
        try:
            data = json.loads(commands_path.read_text(encoding="utf-8"))
            commands = data.get("commands", [])
            result["command_count"] = len(commands)
            result["command_ids"] = [cmd.get("id") for cmd in commands if isinstance(cmd, dict)][:80]
        except Exception as exc:  # noqa: BLE001 - diagnostic tool should not crash here.
            result["commands_json_error"] = str(exc)
    try:
        with urllib.request.urlopen("http://127.0.0.1:8787/api/commands", timeout=2) as response:
            result["api_status"] = response.status
    except urllib.error.URLError as exc:
        result["api_error"] = str(exc)
    except TimeoutError:
        result["api_error"] = "timeout"
    return result


def write_markdown(report: dict, markdown_path: Path) -> None:
    lines = [
        "# Flow Probe Report",
        "",
        "## Paths",
        "",
    ]
    for path in report["paths"]:
        lines.append(f"- `{path}`")
    if report["missing_paths"]:
        lines.extend(["", "## Missing Paths", ""])
        for path in report["missing_paths"]:
            lines.append(f"- `{path}`")
    lines.extend(["", "## Counts", ""])
    for key, value in sorted(report["counts"].items()):
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Scriptability Signals", ""])
    for signal in report["scriptability_signals"]:
        lines.append(f"- {signal}")
    if report["risk_flags"]:
        lines.extend(["", "## Risk Flags", ""])
        for flag in report["risk_flags"][:30]:
            lines.append(f"- {flag}")
    lines.extend(["", "## Recent Candidate Files", ""])
    for item in report["recent_files"][:40]:
        lines.append(f"- `{item['kind']}` `{item['path']}` ({item['modified']}, {item['size']} bytes)")
    lines.extend(["", "## Script Panel", ""])
    for key, value in report["script_panel"].items():
        lines.append(f"- `{key}`: `{value}`")
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paths", nargs="+", required=True, help="Files or directories to inspect")
    parser.add_argument("--output", help="Write JSON report to this path")
    parser.add_argument("--markdown", help="Write Markdown report to this path")
    parser.add_argument("--max-depth", type=int, default=4)
    parser.add_argument("--max-files", type=int, default=4000)
    args = parser.parse_args(argv)

    report = collect([Path(path) for path in args.paths], max_depth=args.max_depth, max_files=args.max_files)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        output_path = Path(args.output).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    if args.markdown:
        write_markdown(report, Path(args.markdown).expanduser())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
