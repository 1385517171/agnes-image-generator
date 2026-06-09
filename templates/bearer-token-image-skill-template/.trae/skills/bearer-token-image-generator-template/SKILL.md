---
name: "bearer-token-image-generator-template"
description: "Template for bearer-token image generation skills. Invoke when you need a reusable image-generation skill for a provider with a bearer-token API."
---

# Bearer Token Image Generator Template

Use this template to build a reusable image-generation skill for providers that expose an OpenAI-style image endpoint and require bearer-token authentication.

## Customize before use

1. Rename this skill directory.
2. Update the `name` field above.
3. Replace provider-specific constants in `scripts/generic_image_generate.py`.
4. Update `manifest.json` and `.env.example`.
5. Adjust examples below to match your provider and model.

## Default capabilities

- text-to-image
- image-to-image by image URL
- one-time bearer-token setup
- Hermes-safe env resolution
- JSON output for downstream tools

## One-time setup

```bash
python3 ./scripts/setup_bearer_env.py --api-key "Bearer YOUR_TOKEN"
```

## Execution

```bash
python3 ./scripts/generic_image_generate.py \
  --prompt "your prompt" \
  --size 1024x1024 \
  --output /tmp/generated-image.png
```

## Hermes safety rules

- Do not use `write_file` to modify `~/.hermes/.env`.
- Do not trust masked placeholder secrets such as `***`.
- Prefer a real shell for initial token setup.
- Treat a fresh API call as the source of truth for auth validation.
