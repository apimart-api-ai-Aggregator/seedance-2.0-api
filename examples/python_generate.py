#!/usr/bin/env python3
"""Generate one video with Seedance 2.0 (seedance-2.0) and download the MP4."""

import argparse, os, pathlib, time
import requests

BASE = os.environ.get("APIMART_BASE_URL", "https://api.apimart.ai/v1")
HEADERS = {"Authorization": f"Bearer {os.environ['APIMART_API_KEY']}", "Content-Type": "application/json"}


def generate(prompt: str, size: str = "16:9", resolution: str = "720p", duration: int = 5,
             audio: bool = False, references: list[str] | None = None) -> dict:
    body = {"model": "seedance-2.0", "prompt": prompt, "size": size, "resolution": resolution,
            "duration": duration, "generate_audio": audio}
    if references:
        body["image_urls"] = references
    created = requests.post(f"{BASE}/videos/generations", headers=HEADERS, json=body, timeout=60)
    created.raise_for_status()
    data = created.json()["data"]
    task_id = data["id"] if isinstance(data, dict) else data[0]["task_id"]
    delay = 10
    for _ in range(120):
        task = requests.get(f"{BASE}/tasks/{task_id}", headers=HEADERS, timeout=60).json()["data"]
        if task["status"] in ("completed", "failed"):
            return task
        time.sleep(delay)
        delay = min(delay + 5, 20)
    raise TimeoutError(task_id)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Seedance 2.0 video generation")
    ap.add_argument("--prompt", default="A kitten yawning at the camera")
    ap.add_argument("--size", default="16:9", help="`16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9` and adaptive ratios")
    ap.add_argument("--resolution", default="720p", help="480p, 720p, 1080p, 4k")
    ap.add_argument("--duration", type=int, default=5, help="4–15 seconds (default 5)")
    ap.add_argument("--audio", action="store_true", help="generate audio (billed the same per second)")
    ap.add_argument("--out", default="out")
    args = ap.parse_args()

    task = generate(args.prompt, args.size, args.resolution, args.duration, args.audio)
    print(f"status={task['status']} cost={task.get('cost')} credits={task.get('credits_cost')} seconds={args.duration}")
    pathlib.Path(args.out).mkdir(parents=True, exist_ok=True)
    for url in (task.get("result", {}).get("videos", [{}])[0].get("url") or []):
        dest = pathlib.Path(args.out) / url.rsplit("/", 1)[-1]
        dest.write_bytes(requests.get(url, timeout=300).content)
        print("saved", dest)
