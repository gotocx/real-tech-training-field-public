# Source Conversion Workflow

1. 在 `assets/sources/source-registry.yaml` 登记来源、许可、用途和复制策略。
2. 从来源中提取主题，不复制题面、答案或代码。
3. 重新编写内部训练题卡，补齐训练动作、评分点、追问和项目迁移。
4. 代码类题目补齐标准实现、错误实现或测试数据。
5. 运行来源检查、schema 检查和代码测试。
6. 只有通过检查的题卡才能保持 `accepted` 状态。
