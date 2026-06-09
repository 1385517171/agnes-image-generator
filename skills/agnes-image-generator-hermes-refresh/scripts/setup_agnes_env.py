#!/usr/bin/env python3
import argparse
import os
import stat
import sys
from pathlib import Path


DEFAULT_ENV_FILE = ".env.local"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Persist Agnes Bearer Token to a local env file for later calls."
    )
    parser.add_argument(
        "--api-key",
        required=True,
        help="Agnes API key or a full 'Bearer <token>' string.",
    )
    parser.add_argument(
        "--env-file",
        default=DEFAULT_ENV_FILE,
        help="Target env file relative to the bundle root. Default: .env.local",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing AGNES_API_KEY entry.",
    )
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
        raise SystemExit("Empty Agnes API key.")

    bundle_root = Path(__file__).resolve().parent.parent
    if args.env_file == DEFAULT_ENV_FILE:
        env_path = get_default_env_path(bundle_root)
    else:
        candidate = Path(args.env_file).expanduser()
        env_path = candidate.resolve() if candidate.is_absolute() else (bundle_root / candidate).resolve()
    env_path.parent.mkdir(parents=True, exist_ok=True)

    existing_lines: list[str] = []
    replaced_keys: set[str] = set()
    if env_path.exists():
        existing_lines = env_path.read_text(encoding="utf-8").splitlines()

    new_lines: list[str] = []
    for line in existing_lines:
        if line.startswith("AGNES_API_KEY=") or line.startswith("AGNES_IMAGE_API_KEY="):
            if not args.force:
                raise SystemExit(
                    f"Agnes API key already exists in {env_path}. Re-run with --force to overwrite."
                )
            key_name = line.split("=", 1)[0]
            new_lines.append(f"{key_name}={api_key}")
            replaced_keys.add(key_name)
        else:
            new_lines.append(line)

    for key_name in ("AGNES_API_KEY", "AGNES_IMAGE_API_KEY"):
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

    print(f"Saved AGNES_API_KEY to {env_path}")
    print("Future calls to ./scripts/agnes_image_generate.py will auto-load this value.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
