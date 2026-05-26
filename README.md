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
- 用户粘贴答案后要先过回答真实性门禁，识别模板化、浅层、过度像生成内容的答案。
- 主 `SKILL.md` 只负责训练路由，题库事实源来自 `assets/`。
