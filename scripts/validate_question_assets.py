from __future__ import annotations

from collections import Counter
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "assets" / "question-bank" / "index.yaml"
REQUIRED_FIELDS = [
    "id",
    "type",
    "status",
    "difficulty",
    "time_limit_minutes",
    "title",
    "source_refs",
    "training_action",
    "prompt",
    "knowledge_points",
    "standard_solution",
    "bruteforce_solution",
    "common_mistakes",
    "edge_cases",
    "follow_up_questions",
    "scoring_points",
    "ai_ide_tasks",
    "project_transfer",
    "interview_transfer",
    "tests",
]
EXPECTED_COUNTS = {
    "algorithm": 120,
    "frontend": 60,
    "backend": 40,
    "system_design": 30,
    "debug_review": 30,
    "project_vibe": 20,
}
ALLOWED_DIFFICULTY = {"easy", "medium", "hard"}


def read_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    index = read_yaml(INDEX)
    assets = index.get("assets", [])
    if index.get("total") != 300:
        fail(f"index total should be 300, got {index.get('total')}")
    if len(assets) != 300:
        fail(f"index asset count should be 300, got {len(assets)}")

    ids = set()
    counts = Counter()
    for entry in assets:
        asset_path = ROOT / entry["path"]
        if not asset_path.exists():
            fail(f"missing asset file: {entry['path']}")
        data = read_yaml(asset_path)
        missing = [field for field in REQUIRED_FIELDS if field not in data or data[field] in (None, "", [], {})]
        if missing:
            fail(f"{data.get('id', asset_path.name)} missing fields: {missing}")
        if data["id"] in ids:
            fail(f"duplicate id: {data['id']}")
        ids.add(data["id"])
        if data["status"] != "accepted":
            fail(f"{data['id']} status must be accepted")
        if data["difficulty"] not in ALLOWED_DIFFICULTY:
            fail(f"{data['id']} invalid difficulty: {data['difficulty']}")
        if data["type"] not in EXPECTED_COUNTS:
            fail(f"{data['id']} invalid type: {data['type']}")
        if data["type"] != entry["type"]:
            fail(f"{data['id']} type mismatch between index and asset")
        if not isinstance(data["time_limit_minutes"], int) or data["time_limit_minutes"] <= 0:
            fail(f"{data['id']} invalid time limit")
        if not isinstance(data["source_refs"], list) or not data["source_refs"]:
            fail(f"{data['id']} must have source_refs")
        if not isinstance(data["scoring_points"], dict) or sum(data["scoring_points"].values()) != 100:
            fail(f"{data['id']} scoring_points must sum to 100")
        counts[data["type"]] += 1

    for question_type, expected in EXPECTED_COUNTS.items():
        if counts[question_type] != expected:
            fail(f"{question_type} should have {expected}, got {counts[question_type]}")

    print("OK: 300 accepted question assets validated")


if __name__ == "__main__":
    main()
