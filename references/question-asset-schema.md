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
