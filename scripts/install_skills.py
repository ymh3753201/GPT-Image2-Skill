#!/usr/bin/env python3
"""Install both skills from a full local package, without downloading source."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import tempfile


def install(source: Path, destination: Path, replace: bool = False) -> list[Path]:
    names = ("gpt-image", "get-prompt-from-image")
    for name in names:
        if not (source / "skills" / name / "SKILL.md").is_file():
            raise ValueError(f"Incomplete package: skills/{name}/SKILL.md is missing")
    backend = source / "src" / "gpt_image_cli"
    if not (backend / "cli.py").is_file():
        raise ValueError("Incomplete package: src/gpt_image_cli/cli.py is missing")
    destination.mkdir(parents=True, exist_ok=True)
    for name in names:
        target = destination / name
        if target.is_symlink():
            raise ValueError(f"Resolve this existing symlink before installing: {target}")
        if target.exists() and not replace:
            raise ValueError(f"Already installed: {target}. Use --replace for an authorized update.")
        if target.resolve() == (source / "skills" / name).resolve():
            raise ValueError("Installation destination must differ from the source skills directory")
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store", ".env", ".env.*")
    with tempfile.TemporaryDirectory(prefix=".gpt-image-install-", dir=destination) as staging:
        staged = Path(staging)
        for name in names:
            shutil.copytree(source / "skills" / name, staged / name, ignore=ignore)
        # Generated installation copy. The repository's src/ stays canonical.
        shutil.copytree(backend, staged / "gpt-image" / "scripts" / "gpt_image_cli", ignore=ignore)
        installed = []
        backups = []
        try:
            for name in names:
                target = destination / name
                if target.exists():
                    backup = staged / (name + ".previous")
                    target.rename(backup)
                    backups.append((backup, target))
                (staged / name).rename(target)
                installed.append(target)
        except OSError:
            for target in installed:
                shutil.rmtree(target)
            for backup, target in reversed(backups):
                backup.rename(target)
            raise
    return installed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path,
                        default=Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex") / "skills")
    parser.add_argument("--replace", action="store_true", help="Replace these two existing skills.")
    args = parser.parse_args()
    try:
        targets = install(Path(__file__).resolve().parents[1], args.skills_dir.expanduser(), args.replace)
    except (ValueError, OSError) as exc:
        parser.exit(2, f"error: {exc}\n")
    for target in targets:
        print(target)
    print("Skills installed. Start a new Codex chat to load the updated instructions.")
    print("Run the installed scripts/generate.py with uv run, or install the local CLI with uv tool install .")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
