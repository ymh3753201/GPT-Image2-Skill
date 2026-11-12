---
name: gpt-image
description: "Generate and edit images in Codex using GPT Image 2.6 Sunburst by default. Use for posters, Chinese typography, short-drama character sheets and keyframes, ecommerce images, uploaded references, inpainting and GIFs. Supports OpenAI-compatible third-party APIs and exact provider model IDs."
metadata: {"openclaw":{"primaryEnv":"OPENAI_API_KEY","homepage":"https://github.com/ymh3753201/GPT-Image2-Skill"}}
---

# GPT Image

Requires Python 3.11+ and the packaged CLI or uv. Requests use the chosen provider and credentials and may incur API charges.

Create finished images from a brief and optional references through the packaged CLI. Read only the references relevant to the task. Keep the user's exact copy, subject identity, intended deliverables and chosen provider.

## Choose the model and API

- Default to **`gpt-image-2.6-sunburst`**, with `quality=high`, one image and PNG. This distribution prioritizes detailed posters, character continuity and product fidelity. This is a skill default, not an OpenAI server default.
- Honor an explicit model or a previously selected model. `OPENAI_IMAGE_MODEL` is the user's configured default and takes precedence over the built-in default. Send the selected value explicitly via `--model`.
- For speed-first drafts, select `gpt-image-2.6-flare` when the user asks for speed or chooses it. Do not change an explicitly selected model based on the task category.
- For an unspecified “2.6” request, use the default directly. On OpenAI the documented IDs are `gpt-image-2.6-sunburst` and `gpt-image-2.6-flare`. A third-party service may use another alias, including `gpt-image-2.6`; preserve its documented model ID exactly.
- Respect `OPENAI_BASE_URL` or the user's `--base-url`. The default is OpenAI; the CLI supports providers with compatible Images API endpoints. Do not hard-code a vendor, replace the user's base URL, reject an unfamiliar provider model, or use an unrelated chat API key. See [providers.md](references/providers.md) for configuration and compatibility.
- If the user explicitly wants Codex's native image tool, use that available tool. Its model routing is platform-managed; this CLI's `--model` setting does not select the native tool's backend.
- Consult [models.md](references/models.md) for official IDs, API defaults, parameters and verification boundaries. Leave `input_fidelity` and `complexity` unset unless the task or provider calls for them. `complexity` controls planning independently of rendering `quality`.

## Execute the request

1. Identify the deliverables, exact text, aspect ratio, size and references. For a clear request, proceed. For a multi-image campaign or short-drama sequence, state a compact per-image plan and shared visual identity. Ask only for information that materially affects the result; do not require repeated confirmation of choices already made.
2. Inspect every reference with the available image-viewing tool. Assign each a role: product identity, character identity, style, composition or edit target. Do not infer unseen product specifications or hidden views as facts. Read [production-workflows.md](references/production-workflows.md) for posters, short-drama imagery and ecommerce work.
3. Write a complete prompt preserving exact text and edit invariants. Include the page/shot purpose, subject identity and count, composition, camera/light, text hierarchy and unwanted changes. For long or Chinese prompts, save a UTF-8 text file and pass `--prompt-file` to avoid shell escaping errors. Gallery/craft references are optional inspiration, not a mandatory bundle.
4. Check the existing installation and effective configuration without printing keys. Use the installed `gpt-image` CLI, or `uv run "$SKILL_DIR/scripts/generate.py"`. Full local packages and installed skills include the Python source. If dependencies are missing, use the local installation guide; the launcher never downloads a repository automatically. Installation authorization does not authorize a paid test image.
5. With **any image reference**, pass the actual local image files using repeatable `-i`. This selects `/images/edits`; do not merely describe the uploaded image in a text-only `/images/generations` request. If an attachment has no readable local path, obtain the file through the host's supported attachment access, or ask for the file. Never substitute a guessed path.
6. Pass the resolved model, size, quality and output path. Use one request per distinct page or shot. `-n` requests variants of one prompt, not a sequence with different briefs. Produce the requested count; request further paid variants only when the user's scope does not already include them.
7. Inspect each output at full size. Verify exact text, subject identity, product structure/count/color, character face/clothing, layout and requested size. For corrections, use the original references plus the latest accepted image when helpful, with a precise change and preserved-region description. Stay within authorized revision scope. On timeout, invalid-model, access, quota or policy error, report the error and stop; do not blindly retry, change providers or switch models.
8. Deliver the images inline where possible and provide absolute local paths, requested model and useful settings. State any visible defects or unverified points. For short-drama work, these outputs are images/keyframes; report separately if video production was requested and remains outstanding.

## CLI examples

```bash
# Poster: full Chinese copy in a UTF-8 file
gpt-image --model gpt-image-2.6-sunburst --prompt-file poster.txt --size portrait --quality high -f poster.png

# Product identity from front and back references
gpt-image --model gpt-image-2.6-sunburst --prompt-file product.txt -i front.png -i back.png --size 1024x1536 -f product.png

# Character identity and prior accepted frame
gpt-image --model gpt-image-2.6-sunburst --prompt-file shot-02.txt -i character.png -i shot-01.png --size 1536x1024 -f shot-02.png

# Provider-defined endpoint/model; credentials come from the environment
gpt-image --base-url https://images.example.com/v1 --model provider-model-id --prompt-file poster.txt -i reference.png -f result.png

# Source or locally installed skill launcher
uv run "$SKILL_DIR/scripts/generate.py" --model gpt-image-2.6-sunburst --prompt-file poster.txt -f poster.png
```

`--model` > `OPENAI_IMAGE_MODEL` > Sunburst. `--base-url` > `OPENAI_BASE_URL` > OpenAI. Environment variables override working-directory `.env`, which overrides home `.env`. Do not edit keys or shared configuration unless the user requested setup. Never print secrets.

## Parameters and references

- `--size`: `square`, `portrait`, `landscape`, `wide`, `tall`, `1k`, `2k`, `4k`, `auto` or provider-supported `WIDTHxHEIGHT`. Choose dimensions for the actual placement; do not claim a design suggestion is a platform rule.
- `--quality`: `auto`, `low`, `medium`, `high`, `xhigh`, `max`. Default `high`; explain cost implications before increasing an agreed setting. Provider capabilities can differ.
- `--complexity`: optional `low`, `medium`, `high`. Omit for ordinary requests; supported OpenAI 2.6 models default to high planning effort.
- `-i`: repeatable local reference image, up to 16. `-m`: optional alpha PNG mask with the first reference, same dimensions; transparent regions are edited.
- `--format`: `png`, `jpeg`, `webp`, `gif`. Transparent output requires PNG/WebP. `--compression` applies to JPEG/WebP. The CLI preserves provider base64 or URL outputs.
- GIF: `--format gif`, optional `--frames` 2–16 and `--frame-duration` 20–2000 ms. Size defaults to `auto`. Inspect all frames and playback. Provider/model access is required.
- Local sprite animation: `gpt-image animate --help`. This assembles an existing sprite sheet without an API call.
- Image 2 requests: [gallery.md](references/gallery.md), then one relevant category. Image 2.6: [models.md](references/models.md) plus the needed production workflow. Historical 2.5 task guides may inform prompts, with their original provenance retained.

Run `gpt-image --help` for all flags. Exit codes are 0 success, 1 API/output failure, 2 bad arguments or missing configuration. A successful request still requires visual review.
