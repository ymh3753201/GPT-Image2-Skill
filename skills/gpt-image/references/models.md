# GPT Image model IDs and API contract

Checked against official documentation on **2026-11-12**. This file owns current API selection. Historical gallery and 2.5 reference examples retain their original models.

## IDs and defaults

| Choice | Exact OpenAI ID | Purpose |
|---|---|---|
| Sunburst, this distribution's default | `gpt-image-2.6-sunburst` | Detailed compositions and reference-sensitive editing |
| Flare | `gpt-image-2.6-flare` | Fast iteration and generation/editing |
| Older explicit choices | `gpt-image-2.5-sunburst`, `gpt-image-2.5-flare`, `gpt-image-2` | User-selected compatibility |

OpenAI documents the two 2.6 IDs separately, without a bare `gpt-image-2.6` alias. The upstream v0.3.0 skill defaults to Flare. This distribution chooses Sunburst for posters, character continuity and ecommerce reference work, following OpenAI's description of its detail and editing consistency. This is a task-driven choice, not a claim that every image requires Sunburst. Flare remains selectable. [Official announcement](https://openai.com/index/introducing-images-2-6/) · [Sunburst](https://developers.openai.com/api/docs/models/gpt-image-2.6-sunburst) · [Flare](https://developers.openai.com/api/docs/models/gpt-image-2.6-flare)

The generation reference requires an explicit `model`. The editing reference still documents `gpt-image-2.5-sunburst` when it is omitted. Both CLI paths therefore send an explicit model. Priority is `--model`, then `OPENAI_IMAGE_MODEL`, then `gpt-image-2.6-sunburst`. A provider's documented alias is accepted unchanged; consult [providers.md](providers.md). [Generation reference](https://developers.openai.com/api/reference/resources/images/methods/generate) · [Edit reference](https://developers.openai.com/api/reference/resources/images/methods/edit)

## Requests

- Text only: `POST /v1/images/generations`.
- Any reference: `POST /v1/images/edits`. The CLI uploads one or more files through `image`, using multipart form data. Official reference inputs support up to 16 PNG/JPEG/WebP images, each under 50 MB. Masked edits use an alpha PNG matching the first reference's dimensions.
- A request has no previous-shot memory. Include the relevant source images each time.
- Save `data[].b64_json` or a compatible provider's `data[].url`. A successful HTTP response still requires visual inspection.

## Parameters

| Setting | CLI behavior |
|---|---|
| `quality` | Default `high`. `low`, `medium`, `high`, `auto`, `xhigh`, `max` are exposed. Preserve the user's cost/quality selection and check provider support. |
| `complexity` | Optional `low`, `medium`, `high`. Official 2.6 models use `high` when omitted. Independent of rendering quality. |
| `size` | Default `1024x1024`; GIF defaults to `auto`. Use a shortcut or provider-supported `WIDTHxHEIGHT`. |
| `input_fidelity` | Omitted by default. Explicit Image 2 values are dropped because its API rejects the field. Explicit 2.5/2.6/provider values are forwarded as opt-in, with support checked against that service. |
| `background` | Optional `auto`, `opaque`, `transparent`. Transparency requires PNG/WebP. |
| `output_format` | PNG by default; JPEG, WebP and GIF exposed. SVG is not implemented by this CLI. |
| `n` | 1–10, default 1. Each distinct page/shot needs a distinct prompt. |
| `moderation` | Retains upstream generation default `low`, with `auto` selectable. Edits omit it by default. |
| `output_compression` | Optional 0–100 for JPEG/WebP. |

The official 2.6 guide separates planning complexity from rendering quality. More planning can help dense composition but can also alter details, so leave it at the API default unless the task benefits from a specific choice. [Image generation guide](https://developers.openai.com/api/docs/guides/image-generation#gpt-image-26)

For Image 2/2.5, the CLI retains its existing custom-size validation. For 2.6, standard square/portrait/landscape sizes are supported; do not copy an older model's full size limits onto 2.6. Let the provider validate unusual resolutions. A size written in prose does not set the API request dimensions.

GIF accepts `--frames` 2–16 and `--frame-duration` 20–2000 ms. The API checks access and GIF pixel limits. Masks/compression are incompatible with GIF. Local `gpt-image animate` assembles existing frames with no API request. Still images or GIFs do not supply dialogue, audio or complete short-drama video production.

## Verification boundaries

This distribution's v0.4.0 tests cover both default endpoints, explicit models, custom base URLs/model aliases, multiple reference files, prompt-file Unicode, complexity, error handling without automatic retries and local installation. They use mock HTTP responses and do not establish paid API access or visual quality.

Upstream v0.3.0 records live Flare checks in [its sample report](../../../docs/image-2.6-samples.md). These are upstream evidence, not new Sunburst runs performed for this distribution. Its older [2.5 results](../../../docs/sunburst-samples.md) retain their historical model/version boundaries.

Use an authorized real generation/edit request to assess a particular provider and model, then inspect text, character/product identity, changes and size. Do not treat model-list membership as proof of generation availability. A timeout or output download failure is not authorization to resubmit a potentially completed paid generation.
