#!/usr/bin/env python3
import argparse
import os
import stat
import sys
from pathlib import Path

DEFAULT_ENV_FILE = ".env.local"
DEFAULT_PRIMARY_ENV_KEY = "IMAGE_API_KEY"
DEFAULT_SECONDARY_ENV_KEY = "IMAGE_IMAGE_API_KEY"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Persist bearer-token image API keys to an env file.")
    parser.add_argument("--api-key", required=True, help="API key or full 'Bearer <token>' string.")
    parser.add_argument("--env-file", default=DEFAULT_ENV_FILE, help="Target env file relative to bundle root.")
    parser.add_argument("--primary-env-key", default=DEFAULT_PRIMARY_ENV_KEY, help="Primary env key name.")
    parser.add_argument("--secondary-env-key", default=DEFAULT_SECONDARY_ENV_KEY, help="Secondary env key name.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing key entries.")
    return parser.parse_args()


def normalize_api_key(value: str) -> str:
    token = value.strip()
    if token.lower().startswith("bearer "):
        token = token[7:].strip()
    return token


def get_default_env_path(bundle_root: Path) -> Path:
    hermes_home = Path(os.getenv("HERMES_HOME", "~/.hermes")).expanduser()
    try:
        script_path = Path(__file__).resolve()
        if script_path.is_relative_to(hermes_home / "skills"):
            return hermes_home / ".env"
    except AttributeError:
        pass
    return (bundle_root / DEFAULT_ENV_FILE).resolve()


def main() -> int:
    args = parse_args()
    api_key = normalize_api_key(args.api_key)
    if not api_key:
        raise SystemExit("Empty API key.")
    bundle_root = Path(__file__).resolve().parent.parent
    if args.env_file == DEFAULT_ENV_FILE:
        env_path = get_default_env_path(bundle_root)
    else:
        candidate = Path(args.env_file).expanduser()
        env_path = candidate.resolve() if candidate.is_absolute() else (bundle_root / candidate).resolve()
    env_path.parent.mkdir(parents=True, exist_ok=True)

    target_keys = (args.primary_env_key, args.secondary_env_key)
    existing_lines = env_path.read_text(encoding="utf-8").splitlines() if env_path.exists() else []
    new_lines = []
    replaced_keys = set()
    for line in existing_lines:
        if any(line.startswith(f"{key_name}=") for key_name in target_keys):
            if not args.force:
                raise SystemExit(f"API key already exists in {env_path}. Re-run with --force to overwrite.")
            key_name = line.split("=", 1)[0]
            new_lines.append(f"{key_name}={api_key}")
            replaced_keys.add(key_name)
        else:
            new_lines.append(line)
    for key_name in target_keys:
        if key_name in replaced_keys:
            continue
        if new_lines and new_lines[-1] != "":
            new_lines.append("")
        new_lines.append(f"{key_name}={api_key}")

    env_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    try:
        os.chmod(env_path, stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass
    print(f"Saved {args.primary_env_key} and {args.secondary_env_key} to {env_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
