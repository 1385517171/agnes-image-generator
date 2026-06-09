# Agnes Image Generator Hermes Refresh

Portable release bundle for using **Agnes Image 2.1 Flash** from Trae and other agent frameworks.

## Bundle layout

- `manifest.json`: package metadata and entrypoints
- `.trae/skills/agnes-image-generator-hermes-refresh/SKILL.md`: Trae skill definition
- `scripts/agnes_image_generate.py`: reusable CLI entrypoint
- `scripts/setup_agnes_env.py`: one-time token setup helper
- `.env.example`: environment variable template

## One-time Bearer Token setup

Run once:

```bash
python3 ./scripts/setup_agnes_env.py --api-key "Bearer YOUR_TOKEN"
```

This writes `AGNES_API_KEY` into `.env.local` for a generic bundle. If the bundle is installed under Hermes, the same helper writes to `HERMES_HOME/.env` (usually `~/.hermes/.env`) because skill directories may be read-only. Future calls automatically load `.env.local`, `.env`, and Hermes global env.

The setup helper accepts either:

- raw token
- full `Bearer <token>` string

## Quick start

After setup, run:

```bash
python3 ./scripts/agnes_image_generate.py \
  --prompt "Ink wash painting of Shanghai Bund skyline, misty morning, rice paper texture" \
  --size 1024x768 \
  --output /tmp/agnes-bund.png
```

## Trae

Place `.trae/skills/agnes-image-generator-hermes-refresh/SKILL.md` and `scripts/agnes_image_generate.py` in the target workspace root.

## Other agent frameworks

If the framework supports shell or Python tool execution, call:

```bash
python3 ./scripts/agnes_image_generate.py --prompt "your prompt"
```

If the framework supports an initialization step, call:

```bash
python3 ./scripts/setup_agnes_env.py --api-key "Bearer YOUR_TOKEN"
```

Hermes-specific note:

- do not use agent-side `write_file` to modify `~/.hermes/.env`
- do not paste the token into ad-hoc inline Python or shell snippets inside chat
- prefer running the setup helper in a real shell, or manually editing `HERMES_HOME/.env`

The script prints JSON so downstream tools can parse:

- `model`
- `size`
- `image_url`
- `output_path`
- `raw_response`
