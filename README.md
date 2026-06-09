# Bearer Token Image Skills

Reusable image-generation skills for Trae, Hermes, and other agent frameworks that can execute Python CLI commands.

This repository contains:

- a production-ready Agnes Image 2.1 Flash skill bundle
- a reusable bearer-token image skill template for other providers

## Repository Layout

- `skills/agnes-image-generator-hermes-refresh/`
  - production bundle for `agnes-image-2.1-flash`
  - includes Trae skill definition, CLI generator, and one-time token setup helper
- `templates/bearer-token-image-skill-template/`
  - reusable template for other bearer-token image APIs
  - includes placeholder constants for provider name, model, endpoint, and env key names

## Included Projects

### 1) Agnes Image Generator Hermes Refresh

Path: `skills/agnes-image-generator-hermes-refresh/`

Highlights:

- model: `agnes-image-2.1-flash`
- endpoint: `https://apihub.agnes-ai.com/v1/images/generations`
- supports text-to-image and image-to-image by URL
- supports one-time bearer-token setup
- handles Hermes-specific env resolution
- skips masked placeholder secrets such as `***`

Quick start:

```bash
cd skills/agnes-image-generator-hermes-refresh
python3 ./scripts/setup_agnes_env.py --api-key "Bearer YOUR_TOKEN"
python3 ./scripts/agnes_image_generate.py \
  --prompt "Ink wash painting of Shanghai Bund skyline, misty morning" \
  --size 1024x768 \
  --output /tmp/agnes-bund.png
```

### 2) Bearer Token Image Skill Template

Path: `templates/bearer-token-image-skill-template/`

Use this when you want to adapt the same structure to another provider.

Customize:

- `PROVIDER_NAME`
- `MODEL_NAME`
- `API_URL`
- `PRIMARY_ENV_KEY`
- `SECONDARY_ENV_KEY`

Then rename the skill directory and the `name` field in `SKILL.md`.

## Why This Repository Exists

This repository packages a working image-generation skill and a reusable template in one place so you can:

- install the Agnes bundle directly
- fork and adapt the template for other providers
- reuse the same Hermes-safe bearer-token flow across multiple image models

## Hermes Notes

- Do not use agent-side `write_file` to modify `~/.hermes/.env`
- Prefer running setup helpers in a real shell
- Some Hermes flows may surface masked placeholder secrets such as `***`
- The included scripts treat masked placeholders as invalid and prefer real file-based keys

## Compatibility

- Trae
- Hermes-compatible agents
- Any agent framework that can execute Python CLI commands

## Versioning

- Repository release tag: `v1.0.1`
- Agnes bundle version: `1.1.1`
- Template bundle version: `1.0.0`

## License

See [LICENSE](./LICENSE).
