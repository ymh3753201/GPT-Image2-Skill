# OpenAI and compatible providers

The CLI accepts the endpoint and exact model name chosen by the user. It uses the official OpenAI Python SDK with `base_url`; this does not restrict it to the OpenAI host.

## Configuration

Set values in the process environment, working-directory `.env`, or home `.env`, in that priority order. Load all three settings before resolving defaults. Do not display secret values.

```dotenv
OPENAI_API_KEY=YOUR_PROVIDER_KEY
OPENAI_BASE_URL=https://images.example.com/v1
OPENAI_IMAGE_MODEL=provider-model-id
```

`OPENAI_IMAGE_MODEL` is optional. Without it or `--model`, this distribution sends `gpt-image-2.6-sunburst`. `--base-url` and `--model` override their environment settings for that request. Use the base URL supplied by the provider, including any `/v1` or custom path prefix. For OpenAI, omit `OPENAI_BASE_URL` or use `https://api.openai.com/v1`.

Credentials, URL and model should belong to the same intended service. Existing process variables win over `.env`; a stale exported variable can explain unexpected routing. Check presence and source without exposing the key. Updating the skill does not alter credentials.

## API contract

- Text only uses `POST <base-url>/images/generations` with JSON.
- One or more `-i` inputs use `POST <base-url>/images/edits` with multipart files, preserving their supplied order. Provider support for multiple references and masks must match the task.
- Returned `data[].b64_json` is saved directly. `data[].url` is downloaded without attaching the API credential to the download request.
- Provider aliases are passed unchanged. With a custom host the CLI also permits provider aliases for `max`/`xhigh` or GIF rather than demanding OpenAI's model spelling. Other argument and file-format checks remain active.
- A service offering only a proprietary task API, `/chat/completions`, or asynchronous polling needs its documented adapter. Changing the base URL alone does not translate those protocols. Report that compatibility gap without substituting another vendor.
- The SDK's automatic retries are disabled. A timeout may follow a completed paid request; check provider task history before any authorized resubmission.

Official SDK configuration reference: https://github.com/openai/openai-python#configuring-the-http-client
