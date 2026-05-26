from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "assets" / "question-bank" / "index.yaml"


def read_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def read_json(path: Path) -> list:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def run_js(solution_path: Path, cases_path: Path, expect_pass: bool = True) -> None:
    runner = f'''
const solve = require({json.dumps(str(solution_path))});
const cases = require({json.dumps(str(cases_path))});
function stable(value) {{ return JSON.stringify(value); }}
for (let i = 0; i < cases.length; i += 1) {{
  const actual = solve(cases[i].input);
  const expected = cases[i].expected;
  if (stable(actual) !== stable(expected)) {{
    console.error(`case ${{i}} failed: expected ${{stable(expected)}} got ${{stable(actual)}}`);
    process.exit(1);
  }}
}}
'''
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as handle:
        handle.write(runner)
        runner_path = Path(handle.name)
    try:
        completed = subprocess.run(["node", str(runner_path)], capture_output=True, text=True, timeout=10)
    finally:
        runner_path.unlink(missing_ok=True)
    if expect_pass and completed.returncode != 0:
        fail(f"{solution_path.relative_to(ROOT)} failed: {completed.stderr.strip()}")
    if not expect_pass and completed.returncode == 0:
        fail(f"{solution_path.relative_to(ROOT)} should fail at least one debug test")


def main() -> None:
    index = read_yaml(INDEX)
    tested = 0
    for entry in index["assets"]:
        data = read_yaml(ROOT / entry["path"])
        tests = data.get("tests", {})
        if tests.get("kind") != "executable":
            continue
        solution_file = data["standard_solution"]["file"]
        cases_file = tests["file"]
        solution_path = ROOT / solution_file
        cases_path = ROOT / cases_file
        if not solution_path.exists():
            fail(f"{data['id']} missing solution file")
        if not cases_path.exists():
            fail(f"{data['id']} missing test file")
        cases = read_json(cases_path)
        if len(cases) < 4:
            fail(f"{data['id']} must have at least 4 test cases")
        run_js(solution_path, cases_path)
        if data["type"] == "debug_review":
            buggy_file = tests.get("buggy_file")
            if not buggy_file or not (ROOT / buggy_file).exists():
                fail(f"{data['id']} missing buggy file")
            run_js(ROOT / buggy_file, cases_path, expect_pass=False)
        tested += 1
    if tested != 150:
        fail(f"expected 150 executable assets, got {tested}")
    print("OK: executable code tests passed for 150 assets")


if __name__ == "__main__":
    main()
