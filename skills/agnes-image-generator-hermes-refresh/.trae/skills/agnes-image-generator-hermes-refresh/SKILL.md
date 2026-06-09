---
name: "agnes-image-generator-hermes-refresh"
description: "Generates images with Agnes Image 2.1 Flash. Invoke when users ask for text-to-image or image-to-image generation through Agnes or compatible tools."
---

# Agnes Image Generator Hermes Refresh

Use this skill when the user wants to generate or transform images with **Agnes Image 2.1 Flash**.

This skill is implemented with a portable local CLI script so it can be reused by Trae and other agent frameworks that can run terminal commands.

## What this skill does

- Calls the Agnes image API endpoint: `https://apihub.agnes-ai.com/v1/images/generations`
- Uses model ID: `agnes-image-2.1-flash`
- Supports:
  - text-to-image
  - image-to-image by passing input image URLs
  - optional local download of the first generated result

## When to invoke

Invoke this skill when the user:

- asks to generate an image with Agnes Image 2.1 Flash
- asks for text-to-image using Agnes
- asks to edit or restyle an existing image with Agnes
- wants a reusable CLI-based image generation flow that other agents can call

## Required setup

Provide the API key in one of these ways:

- environment variable `AGNES_API_KEY`
- environment variable `AGNES_IMAGE_API_KEY`
- CLI argument `--api-key`

Recommended one-time setup:

```bash
python3 ./scripts/setup_agnes_env.py --api-key "Bearer YOUR_TOKEN"
```

This saves the token into `.env.local` in a generic bundle. When the same skill runs inside Hermes, the setup helper instead writes to `HERMES_HOME/.env` (usually `~/.hermes/.env`) because Hermes skill directories may be read-only. Future calls to `./scripts/agnes_image_generate.py` automatically load `.env.local`, `.env`, and Hermes global env.

The setup script accepts both:

- raw token
- full `Bearer <token>` string

Do not hardcode real keys into project files tracked by version control.

When installed under Hermes:

- do not use `write_file` to edit `~/.hermes/.env`, because Hermes may protect credential files
- do not inline the token into ad-hoc shell or Python snippets inside chat, because secret redaction can corrupt the value
- prefer asking the user to run the setup helper from a real shell, or let the user edit `HERMES_HOME/.env` manually

## Execution

Primary script:

`python3 ./scripts/agnes_image_generate.py`

Setup script:

`python3 ./scripts/setup_agnes_env.py --api-key "Bearer YOUR_TOKEN"`

### Text-to-image example

```bash
python3 ./scripts/agnes_image_generate.py \
  --prompt "Ink wash painting of Shanghai Bund skyline by the Huangpu River, misty morning, traditional Chinese ink style, rice paper texture, wide composition" \
  --size 1024x768 \
  --output /tmp/agnes-bund.png
```

### Image-to-image example

```bash
python3 ./scripts/agnes_image_generate.py \
  --prompt "Transform the input image into a monochrome ink wash painting while preserving the original composition" \
  --size 1024x768 \
  --image-url "https://example.com/input-image.png" \
  --output /tmp/agnes-restyled.png
```

## Working rules

1. If the user has not provided a prompt, ask for one.
2. If the task is image-to-image and no input image URL is available, ask for the image URL.
3. Prefer saving the output file when the user wants a deliverable image file.
4. After execution, report:
   - the effective prompt
   - size
   - returned image URL
   - local output path if downloaded
5. If no API key is configured, prefer guiding the user to run `python3 ./scripts/setup_agnes_env.py --api-key "Bearer YOUR_TOKEN"` once.
6. If the API returns an auth error, tell the user to provide a valid Agnes API key or overwrite the saved value with `--force`.

## Output contract

The script prints JSON with:

- `model`
- `size`
- `image_url`
- `output_path`
- `raw_response`

Other agents can parse this JSON and continue downstream workflows.

## Portable bundle layout

Recommended bundle layout:

- `.trae/skills/agnes-image-generator-hermes-refresh/SKILL.md`
- `scripts/agnes_image_generate.py`
- `scripts/setup_agnes_env.py`
- `.env.example`
- `manifest.json`

If a framework does not understand Trae skills, it can still call the CLI script directly.
