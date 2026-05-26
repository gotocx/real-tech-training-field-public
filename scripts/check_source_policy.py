from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "assets" / "sources" / "source-registry.yaml"
INDEX = ROOT / "assets" / "question-bank" / "index.yaml"


def read_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    registry = read_yaml(REGISTRY)
    if registry.get("policy", {}).get("no_direct_copy") is not True:
        fail("registry must enforce no direct copy")
    sources = {item["id"]: item for item in registry.get("sources", [])}
    if len(sources) < 6:
        fail("source registry is too small")

    index = read_yaml(INDEX)
    for entry in index["assets"]:
        data = read_yaml(ROOT / entry["path"])
        for ref in data["source_refs"]:
            source_id = ref.get("source_id")
            if source_id not in sources:
                fail(f"{data['id']} references unknown source {source_id}")
            for field in ["repo", "url", "path", "license", "usage"]:
                if not ref.get(field):
                    fail(f"{data['id']} source ref missing {field}")
            if ref["usage"] != "reference_only":
                fail(f"{data['id']} source usage must be reference_only")
            if sources[source_id]["copy_policy"].lower().find("do not copy") < 0:
                fail(f"{source_id} must state no-copy policy")

    print("OK: source registry and reference-only policy validated")


if __name__ == "__main__":
    main()
