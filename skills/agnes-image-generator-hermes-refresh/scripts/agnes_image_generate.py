#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


API_URL = "https://apihub.agnes-ai.com/v1/images/generations"
MODEL_NAME = "agnes-image-2.1-flash"
DEFAULT_TIMEOUT = 180
ENV_FILES = (".env.local", ".env")
HERMES_HOME = Path(os.getenv("HERMES_HOME", "~/.hermes")).expanduser()
HERMES_ENV = HERMES_HOME / ".env"
MASKED_SECRET_MARKERS = {"***", "<redacted>", "[redacted]", "redacted"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate images with Agnes Image 2.1 Flash."
    )
    parser.add_argument("--prompt", required=True, help="Prompt for image generation.")
    parser.add_argument(
        "--size",
        default="1024x768",
        help="Output size, for example 1024x768.",
    )
    parser.add_argument(
        "--image-url",
        action="append",
        default=[],
        help="Optional input image URL for image-to-image. Can be passed multiple times.",
    )
    parser.add_argument(
        "--output",
        help="Optional file path to download the first generated image.",
    )
    parser.add_argument(
        "--api-key",
        help="Agnes API key. Defaults to AGNES_API_KEY or AGNES_IMAGE_API_KEY.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="Request timeout in seconds.",
    )
    return parser.parse_args()


def load_env_files() -> None:
    script_root = Path(__file__).resolve().parent.parent
    for file_name in ENV_FILES:
        env_path = script_root / file_name
        if not env_path.exists():
            continue
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'\"")
            current_value = os.environ.get(key)
            if key and (
                key not in os.environ
                or (not is_usable_api_key(current_value) and is_usable_api_key(value))
            ):
                os.environ[key] = value
    if HERMES_ENV.exists():
        for raw_line in HERMES_ENV.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'\"")
            current_value = os.environ.get(key)
            if key and (
                key not in os.environ
                or (not is_usable_api_key(current_value) and is_usable_api_key(value))
            ):
                os.environ[key] = value


def normalize_api_key(value: str) -> str:
    token = value.strip()
    if token.lower().startswith("bearer "):
        token = token[7:].strip()
    return token


def is_usable_api_key(value: str | None) -> bool:
    if value is None:
        return False
    token = normalize_api_key(value)
    if not token:
        return False
    return token.lower() not in MASKED_SECRET_MARKERS


def resolve_api_key(cli_value: str | None) -> str:
    candidates = (
        cli_value,
        os.getenv("AGNES_API_KEY"),
        os.getenv("AGNES_IMAGE_API_KEY"),
    )
    for candidate in candidates:
        if is_usable_api_key(candidate):
            return normalize_api_key(candidate)
    raise SystemExit(
        "Missing valid API key. Pass --api-key or set AGNES_API_KEY / AGNES_IMAGE_API_KEY."
    )


def build_payload(args: argparse.Namespace) -> dict:
    payload = {
        "model": MODEL_NAME,
        "prompt": args.prompt,
        "size": args.size,
    }
    if args.image_url:
        payload["extra_body"] = {
            "image": args.image_url,
            "response_format": "url",
        }
    return payload


def post_json(url: str, payload: dict, api_key: str, timeout: int) -> dict:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(
            f"Agnes API request failed with HTTP {exc.code}: {error_body}"
        ) from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Agnes API request failed: {exc}") from exc


def extract_first_url(result: dict) -> str | None:
    if isinstance(result.get("data"), list) and result["data"]:
        first = result["data"][0]
        if isinstance(first, dict):
            return first.get("url")
    if isinstance(result.get("url"), str):
        return result["url"]
    return None


def download_file(url: str, output_path: str, timeout: int) -> None:
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            content = response.read()
    except urllib.error.URLError as exc:
        raise SystemExit(f"Failed to download generated image: {exc}") from exc
    target.write_bytes(content)


def main() -> int:
    args = parse_args()
    load_env_files()
    api_key = resolve_api_key(args.api_key)
    payload = build_payload(args)
    result = post_json(API_URL, payload, api_key, args.timeout)

    image_url = extract_first_url(result)
    output_path = None
    if args.output:
        if not image_url:
            raise SystemExit("No image URL found in Agnes response; cannot download.")
        output_path = str(Path(args.output).resolve())
        download_file(image_url, output_path, args.timeout)

    summary = {
        "model": MODEL_NAME,
        "size": args.size,
        "image_url": image_url,
        "output_path": output_path,
        "raw_response": result,
    }
    print(json.dumps(summary, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
