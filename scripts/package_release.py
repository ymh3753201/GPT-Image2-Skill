#!/usr/bin/env python3
"""Build the full redistributable ZIP from tracked repository files."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import tomllib
import zipfile


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=root).strip():
        raise ValueError("Commit release changes before building the full ZIP")
    version = tomllib.loads((root / "pyproject.toml").read_text())["project"]["version"]
    # Tracked files only: commit the release source before packaging.
    names = subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode().split("\0")
    names = sorted(name for name in names if name)
    forbidden = {".env", ".DS_Store", "__pycache__", ".git", ".venv"}
    for name in names:
        if any(part in forbidden or part.startswith(".env.") or part.endswith(".pyc")
               for part in Path(name).parts):
            raise ValueError(f"Forbidden release file: {name}")
        if (root / name).is_symlink():
            raise ValueError(f"Release files must be regular files: {name}")
    output = root / "dist" / f"GPT-Image2-Skill-v{version}-full.zip"
    output.parent.mkdir(exist_ok=True)
    manifest = {"version": version, "commit": subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(), "files": {}}
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in names:
            data = (root / name).read_bytes()
            manifest["files"][name] = hashlib.sha256(data).hexdigest()
            archive.writestr("GPT-Image2-Skill/" + name, data)
        archive.writestr("GPT-Image2-Skill/RELEASE-MANIFEST.json",
                         json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    with output.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    checksum = output.with_suffix(".zip.sha256")
    checksum.write_text(f"{digest}  {output.name}\n")
    print(output)
    print(checksum)


if __name__ == "__main__":
    main()
