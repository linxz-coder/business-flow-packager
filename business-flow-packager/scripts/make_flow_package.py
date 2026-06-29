#!/usr/bin/env python3
"""Scaffold a reusable business workflow automation package."""

from __future__ import annotations

import argparse
import re
import textwrap
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "business-flow"


def write(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip() + "\n", encoding="utf-8")


def scaffold(root: Path, title: str, platform: str, panel: bool, force: bool) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for folder in [
        "sources",
        "scripts",
        "config",
        "docs",
        "tests",
        "exports",
        "logs",
        "notes",
        "panel",
        "release",
        "backup",
    ]:
        (root / folder).mkdir(parents=True, exist_ok=True)
        write(root / folder / ".gitkeep", "", force=False)

    write(
        root / "README.md",
        f"""
        # {title}

        One-click business workflow package.

        ## What It Does

        TODO: Describe the business process, source systems, and final output.

        ## Quick Start

        ```bash
        python3 scripts/run.py --help
        python3 scripts/run.py --dry-run
        ```

        ## Configuration

        Copy `config/example.env` to a private local `.env` file if needed. Do not commit real secrets.

        ## Verification

        TODO: List the files, logs, dashboards, API responses, or workbook sheets that prove a run succeeded.

        ## Launcher

        - Target platform: `{platform}`
        - Script panel candidate: `{str(panel).lower()}`
        """,
        force=force,
    )
    write(
        root / "flow_spec.md",
        f"""
        # Flow Spec: {title}

        ## Session Evidence

        - Source session/thread:
        - Successful run summary:
        - Commands actually run:
        - Files touched:
        - Outputs verified:
        - Manual decisions:
        - Known gaps:

        ## Workflow

        - Purpose:
        - Operator:
        - Trigger:
        - Inputs:
        - Source systems:
        - Outputs:
        - Manual assumptions:
        - Data sensitivity:
        - Non-goals:
        """,
        force=force,
    )
    write(
        root / "run_contract.md",
        """
        # Run Contract

        ## Session Evidence

        TODO: Link or summarize the successful AI session this contract is based on.

        ## Command

        ```bash
        python3 scripts/run.py --dry-run
        ```

        ## Working Directory

        TODO

        ## Runtime Dependencies

        TODO

        ## Environment / Config

        TODO

        ## Idempotency

        TODO

        ## Locks

        TODO

        ## Logs

        TODO

        ## Verification

        TODO

        ## Rollback / Cleanup

        TODO
        """,
        force=force,
    )
    write(
        root / "config" / "example.env",
        """
        # Copy to a private .env if the workflow needs local configuration.
        # Never commit real credentials.
        OUTPUT_DIR=./exports
        """,
        force=force,
    )
    write(
        root / "scripts" / "run.py",
        f'''#!/usr/bin/env python3
"""Runner for {title}."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Validate inputs without changing external systems")
    parser.add_argument("--output-dir", default="exports")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        print("dry-run ok")
        return 0

    raise SystemExit("TODO: implement workflow body after flow_spec.md and run_contract.md are complete")


if __name__ == "__main__":
    raise SystemExit(main())
''',
        force=force,
    )
    write(
        root / "tests" / "smoke_test.py",
        """
        #!/usr/bin/env python3
        import subprocess
        import sys


        def main() -> int:
            result = subprocess.run(
                [sys.executable, "scripts/run.py", "--dry-run"],
                check=False,
                text=True,
                capture_output=True,
            )
            print(result.stdout, end="")
            print(result.stderr, end="", file=sys.stderr)
            return result.returncode


        if __name__ == "__main__":
            raise SystemExit(main())
        """,
        force=force,
    )
    write(
        root / ".gitignore",
        """
        .DS_Store
        __pycache__/
        *.pyc
        .env
        *.log
        logs/*
        !logs/.gitkeep
        exports/*
        !exports/.gitkeep
        backup/*
        !backup/.gitkeep
        release/*
        !release/.gitkeep
        """,
        force=force,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Package directory to create")
    parser.add_argument("--name", help="Slug name; defaults to root folder name")
    parser.add_argument("--title", help="Human title; defaults to name")
    parser.add_argument("--platform", choices=["mac", "windows", "cross-platform"], default="cross-platform")
    parser.add_argument("--panel", action="store_true", help="Mark as a script-panel candidate")
    parser.add_argument("--force", action="store_true", help="Overwrite scaffold files")
    args = parser.parse_args()

    root = Path(args.root).expanduser()
    name = args.name or root.name
    title = args.title or slugify(name).replace("-", " ").title()
    scaffold(root=root, title=title, platform=args.platform, panel=args.panel, force=args.force)
    print(f"created package scaffold: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
