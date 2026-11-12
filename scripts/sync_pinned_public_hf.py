#!/usr/bin/env python3
"""Import ONLY allowlisted, SHA256-pinned public Hugging Face artifacts.

Runs in GitHub Actions; no model/private data access, authentication, or training.
Never execute downloaded remote scripts. Network failure or SHA mismatch stops release.
"""
from pathlib import Path
from urllib.request import Request, urlopen
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]
SPACE_REPO = "ibtihalalkhayyat/medicare-exclusion-risk-synthetic-demo"
DATA_REPO = "ibtihalalkhayyat/medicare-l5-synthetic-schema-demo"
SPACE_COMMIT = "848236eed6da5aed4ac82b495c9a0dd23b41c2dd"

# Source path, destination path, exact SHA-256 of bytes already audited locally.
SPACE_FILES = {
    "README.md": ("demo/README.md", "f54929750eec43becb9502e8a170c7db6e886a32980389ac6df09b8fbc21e17d"),
    "index.html": ("demo/index.html", "1b076039c5050be4691eb2498751d44d25aacf4b7927f879a1bf1c3740f98e26"),
    "data/scenarios.json": ("demo/data/scenarios.json", "cc65b9097a1b9fb5667dd17655001ed0fbd3b5910e6c3cbce550b580f467a78f"),
    "data/inference_grid.json": ("demo/data/inference_grid.json", "911c0278519464f744d48c48d62330c362606db29b1c26e33903c4fee2e9ba1d"),
    "data/synthetic_examples.csv": ("demo/data/synthetic_examples.csv", "18f093efb4c0845a60e7bc19b70625432517b46b345b79bb20edc0cb44c60425"),
    "data/model_output_provenance.json": ("demo/data/model_output_provenance.json", "123d5db918cae225d3bc835c803d1948b2df66fd77b0fdaea9d374b05ff99abe"),
}
DATA_SCHEMA_SHA = "007e3317a6c47a2ab66e2ee52205cd1955893f7dd6301cc369d75ba110f5368e"
INFERENCE_CODE_SHA = "60eb019ae5daba6a82bac60ec778555c66b8c016687971d2bcb574f342e15654"

def digest(contents):
    return hashlib.sha256(contents).hexdigest()

def download(url, max_bytes=250_000):
    request = Request(url, headers={"User-Agent": "Medicare-Stage23B-scientific-release/1.0"})
    with urlopen(request, timeout=60) as res:
        contents = res.read(max_bytes + 1)
        if len(contents) > max_bytes:
            raise RuntimeError("Remote public file larger than approved bound: " + url)
    return contents

def save_pinned(contents, destination, expected_sha):
    observed = digest(contents)
    if observed != expected_sha:
        raise RuntimeError("Pinned SHA-256 mismatch for " + destination + ": " + observed)
    target = ROOT / destination
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(contents)
    print("PASS", destination, len(contents), observed)
    return observed

def main():
    pinned = {}
    for path, (destination, expected) in SPACE_FILES.items():
        url = "https://huggingface.co/spaces/" + SPACE_REPO + "/resolve/" + SPACE_COMMIT + "/" + path
        pinned[destination] = save_pinned(download(url), destination, expected)
    url = "https://huggingface.co/datasets/" + DATA_REPO + "/resolve/main/schema.json"
    pinned["schema.json"] = save_pinned(download(url), "schema.json", DATA_SCHEMA_SHA)
    original = (ROOT / "src/frozen_stage8_inference.py").read_bytes()
    pinned["src/frozen_stage8_inference.py"] = save_pinned(original, "src/frozen_stage8_inference.py", INFERENCE_CODE_SHA)
    metadata = {
        "release_kind": "PUBLIC_SYNTHETIC_RESEARCH_SOURCE_ONLY",
        "release_label": "Stage23-B pinned public demo and source",
        "source_space_repo": SPACE_REPO,
        "source_space_commit": SPACE_COMMIT,
        "source_dataset_repo": DATA_REPO,
        "public_files_sha256": dict(sorted(pinned.items())),
        "research_checkpoint_is_private": True,
        "final_2023_outcomes_included": False
    }
    (ROOT / "PUBLIC_RELEASE_SHA256.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf8"
    )
    print("PASS: manifest", len(pinned), "SHA-pinned public files")

if __name__ == "__main__":
    main()
