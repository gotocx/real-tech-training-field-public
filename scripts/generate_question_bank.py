from __future__ import annotations

import json
import shutil
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]

QUESTION_TYPES = {
    "algorithm": {"prefix": "ALG", "count": 120, "dir": "algorithm"},
    "frontend": {"prefix": "FE", "count": 60, "dir": "frontend"},
    "backend": {"prefix": "BE", "count": 40, "dir": "backend"},
    "system_design": {"prefix": "SD", "count": 30, "dir": "system-design"},
    "debug_review": {"prefix": "DBG", "count": 30, "dir": "debug-review"},
    "project_vibe": {"prefix": "PRJ", "count": 20, "dir": "project-vibe"},
}


SOURCES = [
    {
        "id": "the-algorithms-typescript",
        "repo": "TheAlgorithms/TypeScript",
        "url": "https://github.com/TheAlgorithms/TypeScript",
        "license": "MIT",
        "usage": "reference_only",
        "priority": "high",
        "usable_for": ["algorithm", "debug_review"],
        "copy_policy": "Do not copy source files. Use as implementation-pattern reference only.",
        "notes": "算法分类和复杂度基线参考。",
    },
    {
        "id": "interactive-coding-challenges",
        "repo": "donnemartin/interactive-coding-challenges",
        "url": "https://github.com/donnemartin/interactive-coding-challenges",
        "license": "Apache-2.0",
        "usage": "reference_only",
        "priority": "high",
        "usable_for": ["algorithm", "debug_review"],
        "copy_policy": "Do not copy prompts or tests. Rebuild internal tasks and cases.",
        "notes": "编码挑战、约束、测试思路参考。",
    },
    {
        "id": "system-design-primer",
        "repo": "donnemartin/system-design-primer",
        "url": "https://github.com/donnemartin/system-design-primer",
        "license": "CC-BY-4.0",
        "usage": "reference_only",
        "priority": "high",
        "usable_for": ["system_design", "project_vibe"],
        "copy_policy": "Do not copy answers. Keep attribution and rewrite internal rubrics.",
        "notes": "系统设计主题和追问角度参考。",
    },
    {
        "id": "greatfrontend-react-questions",
        "repo": "greatfrontend/top-reactjs-interview-questions",
        "url": "https://github.com/greatfrontend/top-reactjs-interview-questions",
        "license": "unconfirmed-2026-05-26",
        "usage": "reference_only",
        "priority": "high",
        "usable_for": ["frontend"],
        "copy_policy": "Do not copy explanations or wording. Use topic path only.",
        "notes": "React 题目主题和覆盖矩阵参考。",
    },
    {
        "id": "sudheerj-react-questions",
        "repo": "sudheerj/reactjs-interview-questions",
        "url": "https://github.com/sudheerj/reactjs-interview-questions",
        "license": "MIT",
        "usage": "reference_only",
        "priority": "medium",
        "usable_for": ["frontend"],
        "copy_policy": "Do not copy answer cards. Use as topic inventory and rewrite all content.",
        "notes": "React 大规模问题清单参考。",
    },
    {
        "id": "sudheerj-javascript-questions",
        "repo": "sudheerj/javascript-interview-questions",
        "url": "https://github.com/sudheerj/javascript-interview-questions",
        "license": "unconfirmed-2026-05-26",
        "usage": "reference_only",
        "priority": "medium",
        "usable_for": ["frontend", "backend"],
        "copy_policy": "Do not copy answer cards. Use as topic inventory and rewrite all content.",
        "notes": "JavaScript 机制题主题参考。",
    },
    {
        "id": "devinterview-node-questions",
        "repo": "Devinterview-io/node-interview-questions",
        "url": "https://github.com/Devinterview-io/node-interview-questions",
        "license": "unconfirmed-2026-05-26",
        "usage": "reference_only",
        "priority": "medium",
        "usable_for": ["backend"],
        "copy_policy": "Do not copy answers. Use topic path only and rewrite all content.",
        "notes": "Node.js 后端题目主题参考。",
    },
    {
        "id": "ajay-jagtap-node-questions",
        "repo": "ajay-jagtap/nodejs-interview-questions",
        "url": "https://github.com/ajay-jagtap/nodejs-interview-questions",
        "license": "unconfirmed-2026-05-26",
        "usage": "reference_only",
        "priority": "low",
        "usable_for": ["backend"],
        "copy_policy": "Do not copy answers. Use topic path only and rewrite all content.",
        "notes": "Node.js 补充题目主题参考。",
    },
]


ALGORITHM_PATTERNS = [
    {
        "topic": "数组双指针",
        "prompt": "给定整数数组和目标值，返回任意一组相加等于目标值的下标。要求先写测试，再实现。",
        "points": ["哈希表换时间", "重复值处理", "不存在结果时返回空数组"],
        "complexity": "O(n) time, O(n) space",
        "source_path": "src/data_structures/hash_table",
        "code": """module.exports = function solve(input) {
  const nums = input.nums;
  const target = input.target;
  const seen = new Map();
  for (let i = 0; i < nums.length; i += 1) {
    const need = target - nums[i];
    if (seen.has(need)) return [seen.get(need), i];
    if (!seen.has(nums[i])) seen.set(nums[i], i);
  }
  return [];
};
""",
        "tests": [
            {"input": {"nums": [2, 7, 11, 15], "target": 9}, "expected": [0, 1]},
            {"input": {"nums": [3, 3], "target": 6}, "expected": [0, 1]},
            {"input": {"nums": [1, 2, 4], "target": 8}, "expected": []},
            {"input": {"nums": [-1, 4, 6], "target": 3}, "expected": [0, 1]},
        ],
    },
    {
        "topic": "滑动窗口",
        "prompt": "给定整数数组和窗口长度，返回所有固定长度窗口中的最大元素和。要求解释空数组和窗口越界。",
        "points": ["窗口初始化", "增量更新", "非法窗口返回 0"],
        "complexity": "O(n) time, O(1) space",
        "source_path": "src/algorithms/sliding_window",
        "code": """module.exports = function solve(input) {
  const nums = input.nums;
  const k = input.k;
  if (!Array.isArray(nums) || k <= 0 || k > nums.length) return 0;
  let sum = 0;
  for (let i = 0; i < k; i += 1) sum += nums[i];
  let best = sum;
  for (let i = k; i < nums.length; i += 1) {
    sum += nums[i] - nums[i - k];
    if (sum > best) best = sum;
  }
  return best;
};
""",
        "tests": [
            {"input": {"nums": [1, 3, -1, 5, 2], "k": 3}, "expected": 7},
            {"input": {"nums": [4, 2], "k": 2}, "expected": 6},
            {"input": {"nums": [4, 2], "k": 3}, "expected": 0},
            {"input": {"nums": [-5, -2, -8], "k": 2}, "expected": -7},
        ],
    },
    {
        "topic": "最长无重复子串",
        "prompt": "给定字符串，返回不含重复字符的最长连续子串长度。要求说明左右指针移动条件。",
        "points": ["字符最后位置", "左边界单调右移", "空字符串处理"],
        "complexity": "O(n) time, O(min(n, alphabet)) space",
        "source_path": "src/algorithms/strings",
        "code": """module.exports = function solve(input) {
  const s = input.s || "";
  const last = new Map();
  let left = 0;
  let best = 0;
  for (let right = 0; right < s.length; right += 1) {
    const ch = s[right];
    if (last.has(ch) && last.get(ch) >= left) left = last.get(ch) + 1;
    last.set(ch, right);
    best = Math.max(best, right - left + 1);
  }
  return best;
};
""",
        "tests": [
            {"input": {"s": "abcabcbb"}, "expected": 3},
            {"input": {"s": "bbbbb"}, "expected": 1},
            {"input": {"s": ""}, "expected": 0},
            {"input": {"s": "pwwkew"}, "expected": 3},
        ],
    },
    {
        "topic": "括号栈判断",
        "prompt": "判断只包含括号字符的字符串是否有效。要求设计能暴露栈空弹出的测试。",
        "points": ["入栈与匹配", "提前失败", "结束后栈必须为空"],
        "complexity": "O(n) time, O(n) space",
        "source_path": "src/data_structures/stack",
        "code": """module.exports = function solve(input) {
  const s = input.s || "";
  const pairs = { ")": "(", "]": "[", "}": "{" };
  const stack = [];
  for (const ch of s) {
    if (ch === "(" || ch === "[" || ch === "{") stack.push(ch);
    else if (pairs[ch]) {
      if (stack.pop() !== pairs[ch]) return false;
    }
  }
  return stack.length === 0;
};
""",
        "tests": [
            {"input": {"s": "()[]{}"}, "expected": True},
            {"input": {"s": "([)]"}, "expected": False},
            {"input": {"s": "]"}, "expected": False},
            {"input": {"s": "((("}, "expected": False},
        ],
    },
    {
        "topic": "区间合并",
        "prompt": "合并所有重叠区间，输入可能无序。要求说明排序依据和闭区间边界。",
        "points": ["按起点排序", "相邻重叠合并", "不修改输入假设"],
        "complexity": "O(n log n) time, O(n) space",
        "source_path": "src/algorithms/sorting",
        "code": """module.exports = function solve(input) {
  const intervals = (input.intervals || []).map((item) => [item[0], item[1]]);
  intervals.sort((a, b) => a[0] - b[0]);
  const merged = [];
  for (const current of intervals) {
    if (merged.length === 0 || merged[merged.length - 1][1] < current[0]) {
      merged.push(current);
    } else {
      merged[merged.length - 1][1] = Math.max(merged[merged.length - 1][1], current[1]);
    }
  }
  return merged;
};
""",
        "tests": [
            {"input": {"intervals": [[1, 3], [2, 6], [8, 10]]}, "expected": [[1, 6], [8, 10]]},
            {"input": {"intervals": []}, "expected": []},
            {"input": {"intervals": [[1, 4], [4, 5]]}, "expected": [[1, 5]]},
            {"input": {"intervals": [[5, 7], [1, 2]]}, "expected": [[1, 2], [5, 7]]},
        ],
    },
    {
        "topic": "二分查找",
        "prompt": "在升序数组中查找目标值下标，找不到返回 -1。要求说明循环不变量。",
        "points": ["左右边界收缩", "中点计算", "找不到返回 -1"],
        "complexity": "O(log n) time, O(1) space",
        "source_path": "src/algorithms/searching",
        "code": """module.exports = function solve(input) {
  const nums = input.nums || [];
  const target = input.target;
  let left = 0;
  let right = nums.length - 1;
  while (left <= right) {
    const mid = left + Math.floor((right - left) / 2);
    if (nums[mid] === target) return mid;
    if (nums[mid] < target) left = mid + 1;
    else right = mid - 1;
  }
  return -1;
};
""",
        "tests": [
            {"input": {"nums": [-1, 0, 3, 5, 9], "target": 9}, "expected": 4},
            {"input": {"nums": [-1, 0, 3, 5, 9], "target": 2}, "expected": -1},
            {"input": {"nums": [], "target": 1}, "expected": -1},
            {"input": {"nums": [7], "target": 7}, "expected": 0},
        ],
    },
    {
        "topic": "动态规划路径",
        "prompt": "给定非负整数网格，返回从左上到右下、只能向右或向下移动的最小路径和。",
        "points": ["状态定义", "第一行第一列初始化", "原地或滚动数组优化"],
        "complexity": "O(mn) time, O(n) space",
        "source_path": "src/algorithms/dynamic_programming",
        "code": """module.exports = function solve(input) {
  const grid = input.grid || [];
  if (grid.length === 0 || grid[0].length === 0) return 0;
  const dp = Array(grid[0].length).fill(Infinity);
  dp[0] = 0;
  for (let r = 0; r < grid.length; r += 1) {
    for (let c = 0; c < grid[r].length; c += 1) {
      if (c === 0) dp[c] = dp[c] + grid[r][c];
      else dp[c] = Math.min(dp[c], dp[c - 1]) + grid[r][c];
    }
  }
  return dp[dp.length - 1];
};
""",
        "tests": [
            {"input": {"grid": [[1, 3, 1], [1, 5, 1], [4, 2, 1]]}, "expected": 7},
            {"input": {"grid": [[5]]}, "expected": 5},
            {"input": {"grid": []}, "expected": 0},
            {"input": {"grid": [[1, 2, 3], [4, 5, 6]]}, "expected": 12},
        ],
    },
    {
        "topic": "频次统计",
        "prompt": "返回数组中出现频次最高的 k 个数字，结果按频次降序、数字升序稳定输出。",
        "points": ["频次表", "排序规则", "k 大于种类数处理"],
        "complexity": "O(n log n) time, O(n) space",
        "source_path": "src/data_structures/heap",
        "code": """module.exports = function solve(input) {
  const nums = input.nums || [];
  const k = input.k || 0;
  const count = new Map();
  for (const num of nums) count.set(num, (count.get(num) || 0) + 1);
  return [...count.entries()]
    .sort((a, b) => b[1] - a[1] || a[0] - b[0])
    .slice(0, k)
    .map((item) => item[0]);
};
""",
        "tests": [
            {"input": {"nums": [1, 1, 1, 2, 2, 3], "k": 2}, "expected": [1, 2]},
            {"input": {"nums": [4], "k": 1}, "expected": [4]},
            {"input": {"nums": [2, 1], "k": 5}, "expected": [1, 2]},
            {"input": {"nums": [], "k": 2}, "expected": []},
        ],
    },
    {
        "topic": "零钱兑换",
        "prompt": "给定硬币面额和金额，返回凑成金额所需最少硬币数；无法凑成返回 -1。",
        "points": ["完全背包", "无解哨兵值", "金额 0 返回 0"],
        "complexity": "O(amount * coin_count) time, O(amount) space",
        "source_path": "src/algorithms/dynamic_programming",
        "code": """module.exports = function solve(input) {
  const coins = input.coins || [];
  const amount = input.amount || 0;
  const dp = Array(amount + 1).fill(Infinity);
  dp[0] = 0;
  for (let value = 1; value <= amount; value += 1) {
    for (const coin of coins) {
      if (value >= coin) dp[value] = Math.min(dp[value], dp[value - coin] + 1);
    }
  }
  return Number.isFinite(dp[amount]) ? dp[amount] : -1;
};
""",
        "tests": [
            {"input": {"coins": [1, 2, 5], "amount": 11}, "expected": 3},
            {"input": {"coins": [2], "amount": 3}, "expected": -1},
            {"input": {"coins": [1], "amount": 0}, "expected": 0},
            {"input": {"coins": [2, 5], "amount": 10}, "expected": 2},
        ],
    },
    {
        "topic": "除自身以外乘积",
        "prompt": "返回数组中每个位置除自身以外其他元素的乘积，不能使用除法。",
        "points": ["前缀积", "后缀积", "包含 0 的情况"],
        "complexity": "O(n) time, O(1) extra space",
        "source_path": "src/algorithms/arrays",
        "code": """module.exports = function solve(input) {
  const nums = input.nums || [];
  const result = Array(nums.length).fill(1);
  let prefix = 1;
  for (let i = 0; i < nums.length; i += 1) {
    result[i] = prefix;
    prefix *= nums[i];
  }
  let suffix = 1;
  for (let i = nums.length - 1; i >= 0; i -= 1) {
    result[i] *= suffix;
    suffix *= nums[i];
  }
  return result;
};
""",
        "tests": [
            {"input": {"nums": [1, 2, 3, 4]}, "expected": [24, 12, 8, 6]},
            {"input": {"nums": [0, 1, 2]}, "expected": [2, 0, 0]},
            {"input": {"nums": [0, 0, 2]}, "expected": [0, 0, 0]},
            {"input": {"nums": [-1, 2, -3]}, "expected": [-6, 3, -2]},
        ],
    },
    {
        "topic": "字母异位词",
        "prompt": "判断两个字符串是否由相同字符和相同次数组成。要求说明 Unicode 或小写字母假设。",
        "points": ["长度剪枝", "计数抵消", "负数提前失败"],
        "complexity": "O(n) time, O(k) space",
        "source_path": "src/algorithms/strings",
        "code": """module.exports = function solve(input) {
  const s = input.s || "";
  const t = input.t || "";
  if (s.length !== t.length) return false;
  const count = new Map();
  for (const ch of s) count.set(ch, (count.get(ch) || 0) + 1);
  for (const ch of t) {
    const next = (count.get(ch) || 0) - 1;
    if (next < 0) return false;
    count.set(ch, next);
  }
  return true;
};
""",
        "tests": [
            {"input": {"s": "listen", "t": "silent"}, "expected": True},
            {"input": {"s": "rat", "t": "car"}, "expected": False},
            {"input": {"s": "", "t": ""}, "expected": True},
            {"input": {"s": "aacc", "t": "ccac"}, "expected": False},
        ],
    },
    {
        "topic": "课程依赖拓扑",
        "prompt": "给定课程数和先修关系，判断是否能完成全部课程。要求说明如何发现环。",
        "points": ["入度表", "队列拓扑排序", "处理孤立节点"],
        "complexity": "O(V + E) time, O(V + E) space",
        "source_path": "src/algorithms/graphs",
        "code": """module.exports = function solve(input) {
  const n = input.n || 0;
  const edges = input.prerequisites || [];
  const graph = Array.from({ length: n }, () => []);
  const indegree = Array(n).fill(0);
  for (const [course, pre] of edges) {
    graph[pre].push(course);
    indegree[course] += 1;
  }
  const queue = [];
  for (let i = 0; i < n; i += 1) if (indegree[i] === 0) queue.push(i);
  let visited = 0;
  while (queue.length > 0) {
    const node = queue.shift();
    visited += 1;
    for (const next of graph[node]) {
      indegree[next] -= 1;
      if (indegree[next] === 0) queue.push(next);
    }
  }
  return visited === n;
};
""",
        "tests": [
            {"input": {"n": 2, "prerequisites": [[1, 0]]}, "expected": True},
            {"input": {"n": 2, "prerequisites": [[1, 0], [0, 1]]}, "expected": False},
            {"input": {"n": 3, "prerequisites": []}, "expected": True},
            {"input": {"n": 4, "prerequisites": [[1, 0], [2, 1], [3, 2]]}, "expected": True},
        ],
    },
]


FRONTEND_TOPICS = [
    "React reconciliation 与 key 稳定性",
    "useEffect 依赖数组与闭包陷阱",
    "受控组件和非受控组件边界",
    "React 事件批处理与状态更新",
    "Context 过度渲染与拆分策略",
    "memo/useMemo/useCallback 的真实收益",
    "Suspense 数据加载边界",
    "服务端渲染 hydration 错误定位",
    "TypeScript 泛型组件约束",
    "JS 事件循环和微任务顺序",
    "Promise 错误传播",
    "原型链与对象创建",
    "闭包内存保留",
    "模块边界和副作用",
    "CSS 布局中的包含块",
]

BACKEND_TOPICS = [
    "Node.js 事件循环与阻塞任务",
    "Express 中间件顺序",
    "REST API 幂等性",
    "分页一致性和游标方案",
    "鉴权中间件边界",
    "输入校验与错误响应",
    "数据库事务和重试",
    "连接池耗尽排查",
    "缓存击穿和雪崩保护",
    "队列消费幂等",
]

SYSTEM_TOPICS = [
    "短链接系统",
    "消息通知系统",
    "实时聊天系统",
    "文件上传服务",
    "秒杀库存系统",
    "搜索建议服务",
    "评论系统",
    "任务调度平台",
    "指标监控平台",
    "多人协作文档",
]

PROJECT_TOPICS = [
    "全栈任务看板",
    "小型电商后台",
    "实时聊天室",
    "博客发布系统",
    "日志检索面板",
    "用户反馈平台",
    "权限管理后台",
    "预约排期系统",
    "文件协作空间",
    "数据看板服务",
]

DIFFICULTIES = ["easy", "medium", "medium", "hard"]


def clean() -> None:
    for path in [
        ROOT / "assets",
        ROOT / "references",
    ]:
        if path.exists():
            shutil.rmtree(path)
    for file_name in ["README.md", "SKILL.md", ".gitignore"]:
        target = ROOT / file_name
        if target.exists():
            target.unlink()


def ensure_dirs() -> None:
    for question_type in QUESTION_TYPES.values():
        (ROOT / "assets" / "question-bank" / question_type["dir"]).mkdir(parents=True, exist_ok=True)
    for name in ["standard", "buggy", "slow", "boundary-bug", "tests"]:
        (ROOT / "assets" / "code-bank" / name).mkdir(parents=True, exist_ok=True)
    (ROOT / "assets" / "sources").mkdir(parents=True, exist_ok=True)
    (ROOT / "references").mkdir(parents=True, exist_ok=True)


def dump_yaml(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def source_ref(source_id: str, path: str) -> dict:
    source = next(item for item in SOURCES if item["id"] == source_id)
    return {
        "source_id": source["id"],
        "repo": source["repo"],
        "url": source["url"],
        "path": path,
        "license": source["license"],
        "usage": "reference_only",
    }


def common_asset(
    asset_id: str,
    question_type: str,
    title: str,
    difficulty: str,
    minutes: int,
    refs: list[dict],
    training_action: str,
    prompt: str,
    knowledge_points: list[str],
    standard_solution: dict | str,
    bruteforce_solution: dict | str,
    common_mistakes: list[str],
    edge_cases: list[str],
    follow_up_questions: list[str],
    scoring_points: dict,
    ai_ide_tasks: list[str],
    project_transfer: str,
    interview_transfer: str,
    tests: dict,
) -> dict:
    return {
        "id": asset_id,
        "type": question_type,
        "status": "accepted",
        "difficulty": difficulty,
        "time_limit_minutes": minutes,
        "title": title,
        "source_refs": refs,
        "training_action": training_action,
        "prompt": prompt,
        "knowledge_points": knowledge_points,
        "standard_solution": standard_solution,
        "bruteforce_solution": bruteforce_solution,
        "common_mistakes": common_mistakes,
        "edge_cases": edge_cases,
        "follow_up_questions": follow_up_questions,
        "scoring_points": scoring_points,
        "ai_ide_tasks": ai_ide_tasks,
        "project_transfer": project_transfer,
        "interview_transfer": interview_transfer,
        "tests": tests,
    }


def make_buggy_code(code: str) -> str:
    replacements = [
        ("return [seen.get(need), i];", "return [i, seen.get(need)];"),
        ("if (sum > best) best = sum;", "if (sum < best) best = sum;"),
        ("left = last.get(ch) + 1;", "left = last.get(ch);"),
        ("return stack.length === 0;", "return true;"),
        ("merged[merged.length - 1][1] < current[0]", "merged[merged.length - 1][1] <= current[0]"),
        ("while (left <= right)", "while (left < right)"),
        ("Math.min(dp[c], dp[c - 1])", "Math.max(dp[c], dp[c - 1])"),
        ("b[1] - a[1] || a[0] - b[0]", "a[1] - b[1] || a[0] - b[0]"),
        ("Math.min(dp[value], dp[value - coin] + 1)", "Math.max(dp[value], dp[value - coin] + 1)"),
        ("result[i] *= suffix;", "result[i] += suffix;"),
        ("if (next < 0) return false;", "if (next < 0) return true;"),
        ("return visited === n;", "return visited !== n;"),
    ]
    for old, new in replacements:
        if old in code:
            return code.replace(old, new, 1)
    return """module.exports = function solve(input) {
  return null;
};
"""


def write_code_artifacts(asset_id: str, code: str, tests: list[dict], buggy: bool = False) -> None:
    write_text(ROOT / "assets" / "code-bank" / "standard" / f"{asset_id}.js", code)
    if buggy:
        write_text(ROOT / "assets" / "code-bank" / "buggy" / f"{asset_id}.js", make_buggy_code(code))
    (ROOT / "assets" / "code-bank" / "tests" / f"{asset_id}.json").write_text(
        json.dumps(tests, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def build_algorithm_assets(index: list[dict]) -> None:
    for i in range(1, QUESTION_TYPES["algorithm"]["count"] + 1):
        asset_id = f"ALG{i:03d}"
        pattern = ALGORITHM_PATTERNS[(i - 1) % len(ALGORITHM_PATTERNS)]
        variant = ((i - 1) // len(ALGORITHM_PATTERNS)) + 1
        write_code_artifacts(asset_id, pattern["code"], pattern["tests"])
        asset = common_asset(
            asset_id=asset_id,
            question_type="algorithm",
            title=f"{pattern['topic']}训练 {variant}: 先测后写",
            difficulty=DIFFICULTIES[i % len(DIFFICULTIES)],
            minutes=18 if i % 4 else 25,
            refs=[
                source_ref("the-algorithms-typescript", pattern["source_path"]),
                source_ref("interactive-coding-challenges", f"questions/{pattern['topic']}"),
            ],
            training_action="先让智能编程助手给出实现计划，再由用户补测试、审复杂度、运行标准样例。",
            prompt=pattern["prompt"],
            knowledge_points=pattern["points"],
            standard_solution={
                "summary": "使用可解释的数据结构或动态规划状态，先覆盖边界，再提交实现。",
                "file": f"assets/code-bank/standard/{asset_id}.js",
                "expected_complexity": pattern["complexity"],
            },
            bruteforce_solution={
                "summary": "用直接枚举或完整扫描得到答案，用于校验小输入。",
                "risk": "大输入下会超时，必须说明为什么正式方案更稳。",
            },
            common_mistakes=[
                "只让工具生成代码但不补边界测试。",
                "能跑通样例但说不清复杂度。",
                "忽略空输入、重复值或非法参数。",
            ],
            edge_cases=["空输入", "单元素", "重复值", "负数或极端边界"],
            follow_up_questions=[
                "如果输入规模扩大 100 倍，瓶颈在哪里？",
                "你会增加哪一个测试来证明边界可靠？",
                "如果智能助手给出的实现错了，你先看哪一段？",
            ],
            scoring_points={
                "correctness": 40,
                "tests": 25,
                "complexity": 20,
                "explanation": 15,
            },
            ai_ide_tasks=[
                "把题面改写成实现约束清单。",
                "要求助手生成三组边界测试，然后手动补一组反例。",
                "对生成代码做复杂度和边界审查。",
            ],
            project_transfer="把局部算法能力迁移到列表过滤、搜索、调度或数据聚合模块。",
            interview_transfer="用 90 秒说清思路、复杂度、边界和失败样例。",
            tests={
                "kind": "executable",
                "file": f"assets/code-bank/tests/{asset_id}.json",
                "runner": "scripts/run_code_tests.py",
            },
        )
        dump_yaml(ROOT / "assets" / "question-bank" / "algorithm" / f"{asset_id}.yaml", asset)
        index.append({"id": asset_id, "type": "algorithm", "path": f"assets/question-bank/algorithm/{asset_id}.yaml", "status": "accepted"})


def build_frontend_assets(index: list[dict]) -> None:
    for i in range(1, QUESTION_TYPES["frontend"]["count"] + 1):
        asset_id = f"FE{i:03d}"
        topic = FRONTEND_TOPICS[(i - 1) % len(FRONTEND_TOPICS)]
        source_id = "greatfrontend-react-questions" if i <= 30 else ("sudheerj-react-questions" if i <= 45 else "sudheerj-javascript-questions")
        asset = common_asset(
            asset_id=asset_id,
            question_type="frontend",
            title=f"{topic}: 机制判断与工程迁移",
            difficulty=DIFFICULTIES[i % len(DIFFICULTIES)],
            minutes=12,
            refs=[source_ref(source_id, f"topics/{topic}")],
            training_action="先回答机制，再判断一个错误回答，最后落到真实组件或页面场景。",
            prompt=f"围绕「{topic}」给出标准解释、工程场景、常见误判和一个能验证理解的小例子。",
            knowledge_points=[topic, "机制边界", "工程副作用", "错误回答识别"],
            standard_solution={
                "key_points": [
                    "先定义概念，再说明触发条件和边界。",
                    "必须给出真实组件、状态流或构建场景。",
                    "要能指出错误回答为什么会在项目中造成问题。",
                ],
                "answer_shape": "定义 -> 机制 -> 例子 -> 风险 -> 追问",
            },
            bruteforce_solution="只背定义但不能说明工程影响，真实面试中会被追问击穿。",
            common_mistakes=[
                "把工具生成的解释当成事实，不核对机制。",
                "只说概念，不说触发条件。",
                "不能把答案迁移到组件设计或性能问题。",
            ],
            edge_cases=["异步更新", "重复渲染", "异常输入", "服务端与客户端状态不一致"],
            follow_up_questions=[
                "这个机制在真实项目里什么时候会出问题？",
                "如果生成代码看起来可用，你怎么验证它没有隐藏渲染问题？",
                "请给一个最小复现。",
            ],
            scoring_points={"definition": 25, "mechanism": 30, "engineering_case": 25, "follow_up": 20},
            ai_ide_tasks=[
                "要求助手写一个最小示例。",
                "审查示例是否真的覆盖该机制。",
                "补一个会失败的边界场景。",
            ],
            project_transfer="迁移到 React/TypeScript 页面、组件库、表单或数据加载模块。",
            interview_transfer="用结构化回答抵抗追问，不把背诵答案当成理解。",
            tests={"kind": "rubric", "checklist": ["概念准确", "机制完整", "有工程例子", "能指出错误回答"]},
        )
        dump_yaml(ROOT / "assets" / "question-bank" / "frontend" / f"{asset_id}.yaml", asset)
        index.append({"id": asset_id, "type": "frontend", "path": f"assets/question-bank/frontend/{asset_id}.yaml", "status": "accepted"})


def build_backend_assets(index: list[dict]) -> None:
    for i in range(1, QUESTION_TYPES["backend"]["count"] + 1):
        asset_id = f"BE{i:03d}"
        topic = BACKEND_TOPICS[(i - 1) % len(BACKEND_TOPICS)]
        source_id = "devinterview-node-questions" if i <= 25 else "ajay-jagtap-node-questions"
        asset = common_asset(
            asset_id=asset_id,
            question_type="backend",
            title=f"{topic}: 服务端可靠性判断",
            difficulty=DIFFICULTIES[(i + 1) % len(DIFFICULTIES)],
            minutes=14,
            refs=[source_ref(source_id, f"topics/{topic}")],
            training_action="把后端知识点变成接口、错误处理、测试和可观测性判断。",
            prompt=f"围绕「{topic}」设计一个小型服务场景，说明风险、测试、失败响应和修复策略。",
            knowledge_points=[topic, "接口边界", "失败模式", "可观测性"],
            standard_solution={
                "key_points": [
                    "明确请求输入、状态变化和失败输出。",
                    "说明并发、重试、超时或数据一致性风险。",
                    "给出至少一个测试或日志指标。",
                ],
                "answer_shape": "场景 -> 风险 -> 约束 -> 测试 -> 修复",
            },
            bruteforce_solution="只给框架 API 用法，不讨论失败路径和数据边界。",
            common_mistakes=[
                "忽略超时、重试和幂等。",
                "把异常全部吞掉。",
                "没有说明如何验证服务真的可靠。",
            ],
            edge_cases=["重复请求", "空输入", "并发写入", "下游失败"],
            follow_up_questions=[
                "如果请求被重放两次会发生什么？",
                "如何观测这个问题已经发生？",
                "你会让智能助手先生成哪一类测试？",
            ],
            scoring_points={"api_boundary": 25, "failure_modes": 30, "tests": 25, "explanation": 20},
            ai_ide_tasks=[
                "把需求整理成接口契约。",
                "要求助手生成失败路径测试。",
                "审查生成代码是否丢失幂等或错误响应。",
            ],
            project_transfer="迁移到 Node 服务、API 网关、任务队列或数据访问层。",
            interview_transfer="用服务边界和失败模式回答，而不是只背框架概念。",
            tests={"kind": "rubric", "checklist": ["接口边界明确", "失败模式完整", "有测试策略", "有可观测性"]},
        )
        dump_yaml(ROOT / "assets" / "question-bank" / "backend" / f"{asset_id}.yaml", asset)
        index.append({"id": asset_id, "type": "backend", "path": f"assets/question-bank/backend/{asset_id}.yaml", "status": "accepted"})


def build_system_assets(index: list[dict]) -> None:
    for i in range(1, QUESTION_TYPES["system_design"]["count"] + 1):
        asset_id = f"SD{i:03d}"
        topic = SYSTEM_TOPICS[(i - 1) % len(SYSTEM_TOPICS)]
        asset = common_asset(
            asset_id=asset_id,
            question_type="system_design",
            title=f"{topic}: 需求拆解与冷面追问",
            difficulty="hard" if i % 3 == 0 else "medium",
            minutes=25,
            refs=[source_ref("system-design-primer", f"solutions/{topic}")],
            training_action="限时拆需求、列约束、画核心数据流，再接受追问。",
            prompt=f"设计一个「{topic}」。先问清需求，再给出核心模块、数据流、瓶颈和降级方案。",
            knowledge_points=[topic, "需求澄清", "容量估算", "一致性权衡", "降级策略"],
            standard_solution={
                "key_points": [
                    "先澄清用户规模、读写比例、SLO 和约束。",
                    "给出核心模块和数据流。",
                    "明确一个主要瓶颈及其取舍。",
                    "说明失败降级和观测指标。",
                ],
                "answer_shape": "澄清 -> 规模 -> 架构 -> 数据 -> 瓶颈 -> 追问",
            },
            bruteforce_solution="直接堆组件名，不说明为什么需要，也不说明失败时怎么处理。",
            common_mistakes=[
                "没有澄清需求就画方案。",
                "只说缓存、队列、分库，不讲取舍。",
                "不能承受一致性或容量追问。",
            ],
            edge_cases=["热点用户", "下游服务失败", "数据重复", "读写峰值突增"],
            follow_up_questions=[
                "如果写入量扩大 10 倍，第一处瓶颈在哪里？",
                "你选择强一致还是最终一致，代价是什么？",
                "如何证明这个方案上线后能被观测？",
            ],
            scoring_points={"clarification": 20, "architecture": 30, "tradeoff": 30, "pressure_response": 20},
            ai_ide_tasks=[
                "让助手生成需求澄清清单。",
                "审查架构是否只是堆名词。",
                "把追问整理成下一次修补任务。",
            ],
            project_transfer="迁移到端到端项目设计、后端模块拆分和可观测性方案。",
            interview_transfer="在高压环境下保持结构化表达和取舍意识。",
            tests={"kind": "rubric", "checklist": ["先澄清", "有数据流", "有瓶颈", "有取舍", "能抗追问"]},
        )
        dump_yaml(ROOT / "assets" / "question-bank" / "system-design" / f"{asset_id}.yaml", asset)
        index.append({"id": asset_id, "type": "system_design", "path": f"assets/question-bank/system-design/{asset_id}.yaml", "status": "accepted"})


def build_debug_assets(index: list[dict]) -> None:
    for i in range(1, QUESTION_TYPES["debug_review"]["count"] + 1):
        asset_id = f"DBG{i:03d}"
        pattern = ALGORITHM_PATTERNS[(i - 1) % len(ALGORITHM_PATTERNS)]
        write_code_artifacts(asset_id, pattern["code"], pattern["tests"], buggy=True)
        asset = common_asset(
            asset_id=asset_id,
            question_type="debug_review",
            title=f"{pattern['topic']}: 接管错误实现",
            difficulty=DIFFICULTIES[(i + 2) % len(DIFFICULTIES)],
            minutes=20,
            refs=[
                source_ref("the-algorithms-typescript", pattern["source_path"]),
                source_ref("interactive-coding-challenges", f"debug/{pattern['topic']}"),
            ],
            training_action="先运行错误代码，再用测试定位缺陷，最后修复并解释根因。",
            prompt=f"给你一段看起来合理但会失败的「{pattern['topic']}」实现。不要先重写，先找最小失败用例。",
            knowledge_points=[pattern["topic"], "测试设计", "根因定位", "修复验证"],
            standard_solution={
                "summary": "通过失败用例定位边界或状态更新错误，再做最小修复。",
                "file": f"assets/code-bank/standard/{asset_id}.js",
                "expected_complexity": pattern["complexity"],
            },
            bruteforce_solution={
                "summary": "直接替换成全新实现。",
                "risk": "可能掩盖根因，无法证明自己识别了错误代码的失败点。",
            },
            common_mistakes=[
                "不运行测试就凭感觉修。",
                "只修样例，不补反例。",
                "不能说明错误来自边界、状态还是复杂度。",
            ],
            edge_cases=["最小输入", "重复值", "非法参数", "边界窗口"],
            follow_up_questions=[
                "哪个测试最先暴露错误？",
                "这个错误如果进项目会造成什么用户影响？",
                "你如何防止助手下次生成同类错误？",
            ],
            scoring_points={"failure_case": 30, "root_cause": 30, "repair": 25, "explanation": 15},
            ai_ide_tasks=[
                "要求助手先解释错误代码意图。",
                "手动补一个失败测试。",
                "让助手修复后再次审查复杂度和边界。",
            ],
            project_transfer="迁移到接管生成代码、审查 PR、修复线上边界问题。",
            interview_transfer="展示调试顺序，而不是只给最终答案。",
            tests={
                "kind": "executable",
                "file": f"assets/code-bank/tests/{asset_id}.json",
                "runner": "scripts/run_code_tests.py",
                "buggy_file": f"assets/code-bank/buggy/{asset_id}.js",
            },
        )
        dump_yaml(ROOT / "assets" / "question-bank" / "debug-review" / f"{asset_id}.yaml", asset)
        index.append({"id": asset_id, "type": "debug_review", "path": f"assets/question-bank/debug-review/{asset_id}.yaml", "status": "accepted"})


def build_project_assets(index: list[dict]) -> None:
    for i in range(1, QUESTION_TYPES["project_vibe"]["count"] + 1):
        asset_id = f"PRJ{i:03d}"
        topic = PROJECT_TOPICS[(i - 1) % len(PROJECT_TOPICS)]
        asset = common_asset(
            asset_id=asset_id,
            question_type="project_vibe",
            title=f"{topic}: 从需求聊天到可执行 md",
            difficulty="medium" if i % 4 else "hard",
            minutes=30,
            refs=[source_ref("system-design-primer", f"project-practice/{topic}")],
            training_action="用 AI IDE 做需求澄清、约束整理、任务拆分、测试计划和实现审查。",
            prompt=f"你要做一个「{topic}」。先和助手聊清楚需求，再输出一份可执行开发 md，并设计验收测试。",
            knowledge_points=["需求澄清", "任务拆解", "测试优先", "生成代码审查", "项目迁移"],
            standard_solution={
                "key_points": [
                    "需求 md 必须有目标、非目标、用户流、接口或组件边界。",
                    "必须列出测试计划和风险清单。",
                    "必须说明哪些代码可以让助手生成，哪些必须人工审查。",
                ],
                "answer_shape": "聊天摘要 -> 需求 md -> 任务拆分 -> 测试 -> 审查点",
            },
            bruteforce_solution="只让工具直接生成完整项目，不写约束、不写测试、不审查输出。",
            common_mistakes=[
                "没有先把需求说清楚。",
                "没有定义完成标准。",
                "把生成结果当成可交付成品。",
            ],
            edge_cases=["用户需求变更", "接口遗漏", "状态不同步", "测试无法覆盖关键路径"],
            follow_up_questions=[
                "这份 md 中哪个需求最模糊？",
                "你会要求助手先写哪一组测试？",
                "如果生成项目能跑但结构混乱，你如何接管？",
            ],
            scoring_points={"clarity": 25, "task_breakdown": 25, "tests": 25, "review": 25},
            ai_ide_tasks=[
                "进行 5 轮需求澄清。",
                "生成开发 md 后人工删掉含糊表述。",
                "根据 md 生成测试清单，再审查实现计划。",
            ],
            project_transfer="直接服务于真实全栈、服务器、TypeScript 和 React 项目训练。",
            interview_transfer="把项目经历表达成需求、取舍、验证和复盘，而不是堆功能名。",
            tests={"kind": "rubric", "checklist": ["需求清楚", "任务可执行", "测试可验收", "审查点明确"]},
        )
        dump_yaml(ROOT / "assets" / "question-bank" / "project-vibe" / f"{asset_id}.yaml", asset)
        index.append({"id": asset_id, "type": "project_vibe", "path": f"assets/question-bank/project-vibe/{asset_id}.yaml", "status": "accepted"})


def write_registry() -> None:
    registry = {
        "version": "0.1.0",
        "policy": {
            "default_usage": "reference_only",
            "no_direct_copy": True,
            "accepted_asset_rule": "Asset content must be internally authored and independently reviewable.",
        },
        "sources": SOURCES,
    }
    dump_yaml(ROOT / "assets" / "sources" / "source-registry.yaml", registry)


def write_docs(index: list[dict]) -> None:
    counts = {key: 0 for key in QUESTION_TYPES}
    for item in index:
        counts[item["type"]] += 1
    dump_yaml(
        ROOT / "assets" / "question-bank" / "index.yaml",
        {
            "version": "0.1.0",
            "total": len(index),
            "required_status": "accepted",
            "counts": counts,
            "assets": index,
        },
    )
    write_text(
        ROOT / "README.md",
        """
# Real Tech Training Field

这是一个面向 AI IDE 的真实技术筛选训练资产库。第一阶段只交付题库资产体系：300 道正式训练题、来源登记、代码样例、测试数据和校验脚本。

## 快速验证

```bash
python scripts/validate_question_assets.py
python scripts/check_source_policy.py
python scripts/run_code_tests.py
python scripts/smoke_skill_routes.py
```

## 资产原则

- 外部仓库只作为主题和来源路径参考，不直接搬运题面、答案或代码。
- 每道正式题必须是 `accepted` 状态，并具备来源、训练动作、评分点、追问和迁移场景。
- 代码类题目必须有可运行测试数据；非代码类题目必须有明确评分清单。
- 主 `SKILL.md` 只负责训练路由，题库事实源来自 `assets/`。
""",
    )
    write_text(
        ROOT / ".gitignore",
        """
__pycache__/
*.pyc
.pytest_cache/
node_modules/
""",
    )
    write_text(
        ROOT / "SKILL.md",
        """
---
name: real-tech-training-field
description: 面向 AI IDE 的真实技术筛选训练场，基于结构化题库、代码样例、评分点和来源登记来分发每日训练、冷面模拟和项目迁移任务。
version: 0.1.0
---

# Real Tech Training Field

<!-- @类型: 运行期训练 Skill -->
<!-- @目的: 从 accepted 训练资产中分发任务，让用户完成真实能力动作 -->
<!-- @场景: 用户在 AI IDE 中练习算法、八股、Debug、系统设计和项目拆解 -->

> **一句话**: 这不是普通刷题工具，而是把题库、代码、测试、评分点和追问绑定起来的真实训练场。
> **版本**: v0.1.0

## @工作流: 选择训练模式

<!-- @类型: 主工作流 -->
<!-- @验证点: 每次只从 accepted 资产中抽题，不让讲解层临场编事实 -->
<!-- @验证方式: 运行 scripts/validate_question_assets.py 和 scripts/smoke_skill_routes.py -->
<!-- @ID: wf-select-training-mode -->

### @步骤1: 判断用户状态

- @动作: 用户低能量时进入启动模式，只要求完成一个判断动作。
- @动作: 用户有训练状态时进入训练模式，完成一题或一个知识点闭环。
- @动作: 用户状态较好或到每周模拟时进入冷面模式，限时、少提示、强追问、直接判错。

### @步骤2: 从资产库取题

- @动作: 读取 `assets/question-bank/index.yaml`。
- @动作: 只选择 `status: accepted` 的资产。
- @动作: 根据 `type`、`difficulty`、`knowledge_points` 和历史薄弱点选择任务。

### @步骤3: 执行训练并生成证据

- @动作: 使用题卡中的 `prompt`、`ai_ide_tasks`、`tests` 和 `scoring_points`。
- @动作: 代码题必须运行测试；非代码题必须按评分清单判定。
- @动作: 训练结束输出今日证据：做了什么判断、错在哪里、下一次修补什么、如何迁移到项目和面试表达。

## @工作流: 冷面模拟

<!-- @类型: 子工作流 -->
<!-- @验证点: 冷面模式能明确判定答案是否真实可用 -->
<!-- @验证方式: 抽取 10 道题，检查是否包含限时、追问和评分点 -->
<!-- @ID: wf-cold-interview -->

- @动作: 限时输出，不提前给答案。
- @动作: 根据 `follow_up_questions` 连续追问。
- @动作: 根据 `scoring_points` 直接判定，不把失败包装成成功。
- @动作: 若未通过，记录失败点并生成下一次修补任务。

## 事实源

- 题库事实源: `assets/question-bank/`
- 来源登记: `assets/sources/source-registry.yaml`
- 代码样例: `assets/code-bank/`
- 校验入口: `scripts/`

## 版本历史

- v0.1.0: 建立 300 道正式训练资产、来源登记、代码测试和校验脚本。
""",
    )
    write_text(
        ROOT / "references" / "question-asset-schema.md",
        """
# Question Asset Schema v0.1.0

每个正式题卡都是 YAML 文件，必须包含以下字段：

```yaml
id:
type:
status: accepted
difficulty:
time_limit_minutes:
title:
source_refs:
training_action:
prompt:
knowledge_points:
standard_solution:
bruteforce_solution:
common_mistakes:
edge_cases:
follow_up_questions:
scoring_points:
ai_ide_tasks:
project_transfer:
interview_transfer:
tests:
```

状态流转：

`candidate -> normalized -> test_verified/reviewed -> accepted`

本仓库第一阶段只把通过格式、来源和测试检查的资产写入正式题库。
""",
    )
    write_text(
        ROOT / "references" / "source-conversion-workflow.md",
        """
# Source Conversion Workflow

1. 在 `assets/sources/source-registry.yaml` 登记来源、许可、用途和复制策略。
2. 从来源中提取主题，不复制题面、答案或代码。
3. 重新编写内部训练题卡，补齐训练动作、评分点、追问和项目迁移。
4. 代码类题目补齐标准实现、错误实现或测试数据。
5. 运行来源检查、schema 检查和代码测试。
6. 只有通过检查的题卡才能保持 `accepted` 状态。
""",
    )
    write_text(
        ROOT / "references" / "scoring-rubric.md",
        """
# Scoring Rubric

## 启动模式

完成一个真实判断动作即可通过，例如指出一个边界、写一个测试、识别一个错误回答。

## 训练模式

必须完成闭环：题目理解、实现或回答、测试或评分、复盘。

## 冷面模式

限时输出，少提示，强追问。答案不满足真实可用标准时，应明确判定未通过，并记录修补任务。

## 通用评分

- 正确性：答案或代码是否解决目标问题。
- 验证能力：是否能设计测试或评分清单。
- 表达能力：是否能结构化讲清楚。
- 迁移能力：是否能连接到真实项目和协作场景。
""",
    )


def write_validation_scripts() -> None:
    write_text(
        ROOT / "scripts" / "validate_question_assets.py",
        r"""
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
""",
    )
    write_text(
        ROOT / "scripts" / "check_source_policy.py",
        r"""
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
""",
    )
    write_text(
        ROOT / "scripts" / "run_code_tests.py",
        r"""
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
""",
    )
    write_text(
        ROOT / "scripts" / "smoke_skill_routes.py",
        r"""
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
""",
    )

def main() -> None:
    clean()
    ensure_dirs()
    write_registry()
    index: list[dict] = []
    build_algorithm_assets(index)
    build_frontend_assets(index)
    build_backend_assets(index)
    build_system_assets(index)
    build_debug_assets(index)
    build_project_assets(index)
    write_docs(index)
    write_validation_scripts()
    print(f"generated {len(index)} accepted assets")


if __name__ == "__main__":
    main()
