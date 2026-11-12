# Install or update this distribution

This is the ymh3753201 distribution based on wuyoscar/GPT-Image2-Skill. Default model: `gpt-image-2.6-sunburst`. Read [the Chinese package guide](../COURSE_INSTALL_ZH.md) for a ready-to-use Codex installation prompt.

## Full local package (Codex)

Check Python 3.11+, uv, the existing CLI and the intended skills directory. Preserve unrelated configuration. The extracted package must contain `pyproject.toml`, `src`, `skills` and `scripts`. Run from that root:

```bash
uv tool install .
python scripts/install_skills.py
gpt-image --version
gpt-image --help
```

Use `python3` or `py -3` if appropriate to the OS. For an authorized update, use `uv tool install --force .` and `python scripts/install_skills.py --replace`. `--skills-dir PATH` chooses an explicit install directory. The default uses `$CODEX_HOME/skills`, falling back to `~/.codex/skills`.

The installer copies both complete skills and generates a bundled `gpt_image_cli` source copy inside `gpt-image/scripts/`. This permits `uv run <installed-skill>/scripts/generate.py` to work even without a separately installed command on PATH. The repository's `src/` is the canonical source. No GitHub download is performed by the launcher or installer. Python dependencies may still need downloading from the user's approved package index.

For users who can access GitHub, clone https://github.com/ymh3753201/GPT-Image2-Skill and follow the same local commands. The Release full ZIP contains the same source and reference assets, without Git history, caches or credentials.

## Configure when requested

Use the intended image provider's `OPENAI_API_KEY` and optional `OPENAI_BASE_URL`, `OPENAI_IMAGE_MODEL`. Prefer a `.env` in the user's chosen image working directory, or process environment. Do not overwrite global chat credentials or display secrets. Existing process variables override `.env`; working-directory `.env` precedes home `.env`.

With no model override, both generation and editing explicitly send `gpt-image-2.6-sunburst`. The provider and model remain configurable. See [provider compatibility](../skills/gpt-image/references/providers.md).

## Verify and report

Check `gpt-image --version`, `gpt-image --help`, and `uv run <installed-skill>/scripts/generate.py --help`. Both the installed CLI and skill copy should be from this distribution. Start a new Codex chat or restart it to refresh skill instructions.

Installation and help checks do not require a key or paid request. Generate only when the user requests it, within their selected scope. Report source, installed version and paths, checks performed and whether actual image generation was tested. Other installation routes are in [install-update.md](install-update.md).
