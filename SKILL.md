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
