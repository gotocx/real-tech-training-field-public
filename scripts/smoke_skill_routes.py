from __future__ import annotations

import random
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "assets" / "question-bank" / "index.yaml"


def read_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def main() -> None:
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    for marker in ["回答真实性门禁", "真实面试中过不了", "happy path"]:
        if marker not in skill_text:
            raise SystemExit(f"FAIL: missing authenticity gate marker: {marker}")
    index = read_yaml(INDEX)
    assets = index["assets"]
    sample = random.Random(7).sample(assets, 10)
    modes = ["startup", "training", "cold"]
    rendered = []
    for mode, entry in zip(modes * 4, sample):
        data = read_yaml(ROOT / entry["path"])
        rendered.append(
            {
                "mode": mode,
                "id": data["id"],
                "title": data["title"],
                "time_limit_minutes": 3 if mode == "startup" else data["time_limit_minutes"],
                "prompt": data["prompt"],
                "scoring_points": data["scoring_points"],
            }
        )
    if len(rendered) != 10:
        raise SystemExit("FAIL: smoke route did not render 10 tasks")
    if not any(item["mode"] == "cold" for item in rendered):
        raise SystemExit("FAIL: no cold mode task rendered")
    print("OK: smoke route rendered startup/training/cold tasks")


if __name__ == "__main__":
    main()
