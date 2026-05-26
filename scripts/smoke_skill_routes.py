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
    for marker in ["wf-answer-authenticity-gate", "wf-vibe-engineering-transfer-gate", "happy path", "TypeScript", "Supabase", "Vercel"]:
        if marker not in skill_text:
            raise SystemExit(f"FAIL: missing skill marker: {marker}")
    transfer_text = (ROOT / "references" / "vibe-engineering-transfer-gate.md").read_text(encoding="utf-8")
    for marker in ["Q1:", "Q2:", "Q3:", "TypeScript", "React", "Node.js", "Supabase", "Nginx", "Vercel"]:
        if marker not in transfer_text:
            raise SystemExit(f"FAIL: missing transfer marker: {marker}")
    if "version: 0.1.2" not in skill_text or "v0.1.2" not in skill_text:
        raise SystemExit("FAIL: skill version metadata must match v0.1.2")
    alg001 = read_yaml(ROOT / "assets" / "question-bank" / "algorithm" / "ALG001.yaml")
    if "动态规划" in alg001["standard_solution"]["summary"]:
        raise SystemExit("FAIL: ALG001 summary must not imply dynamic programming")
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
    for item in rendered:
        data = read_yaml(ROOT / next(entry["path"] for entry in assets if entry["id"] == item["id"]))
        if not data.get("project_transfer"):
            raise SystemExit(f"FAIL: {data['id']} missing project_transfer")
        if data["type"] == "algorithm":
            questions = "\n".join(data.get("follow_up_questions", []))
            for marker in ["100", "100 万", "边界测试", "AI 助手"]:
                if marker not in questions:
                    raise SystemExit(f"FAIL: {data['id']} missing algorithm transfer follow-up marker: {marker}")
    if len(rendered) != 10:
        raise SystemExit("FAIL: smoke route did not render 10 tasks")
    if not any(item["mode"] == "cold" for item in rendered):
        raise SystemExit("FAIL: no cold mode task rendered")
    print("OK: smoke route rendered startup/training/cold tasks")


if __name__ == "__main__":
    main()
