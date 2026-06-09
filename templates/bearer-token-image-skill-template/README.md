# Bearer Token Image Skill Template

Reusable template for bearer-token image generation skills across Trae, Hermes, and similar agent frameworks.

## What to customize

Edit these files before first use:

- `manifest.json`
- `.trae/skills/bearer-token-image-generator-template/SKILL.md`
- `scripts/generic_image_generate.py`
- `scripts/setup_bearer_env.py` only if you want different default env key names
- `.env.example`

## Required replacements

Update the placeholders in `scripts/generic_image_generate.py`:

- `PROVIDER_NAME`
- `MODEL_NAME`
- `API_URL`
- `PRIMARY_ENV_KEY`
- `SECONDARY_ENV_KEY`

Then rename the skill directory and the `name:` field in `SKILL.md`.

## One-time token setup

```bash
python3 ./scripts/setup_bearer_env.py --api-key "Bearer YOUR_TOKEN"
```

Generic bundle behavior:

- writes to `.env.local` in a normal workspace
- writes to `HERMES_HOME/.env` when running under Hermes
- persists both primary and secondary env keys to avoid split-brain config
- ignores masked placeholder values such as `***` during runtime resolution

## Runtime behavior

The generator script:

- supports text-to-image and image-to-image by URL
- loads `.env.local`, `.env`, and `HERMES_HOME/.env`
- prefers real keys over masked placeholders or empty env values
- prints JSON for downstream agent consumption

## Hermes notes

- do not use agent-side `write_file` to edit `~/.hermes/.env`
- prefer running the setup helper in a real shell
- if Hermes redacts secrets into `***`, the runtime script skips those placeholder values
