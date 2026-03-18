# n8n Workflow Builder

`n8n-workflow-builder` 是一个给 Codex 使用的技能，用来把自然语言的业务逻辑、流程链路、需求说明或现有 `n8n` 工作流 JSON，转换成更完整、更清晰、可导入的 `n8n workflow JSON`。

它不只是“拼节点”，而是会主动做这些事情：

- 识别合适的触发器、路由、分支和返回路径
- 优先选择内置节点，而不是滥用 `Code`
- 补充校验、重试、批处理、失败通知和可维护性设计
- 优化节点命名、连接关系和画布结构
- 尽量输出可直接导入的完整 JSON

## 适用场景

- 你只有思维逻辑链，想直接生成完整 `n8n` 工作流
- 你已有一份 `n8n` JSON，想让它更稳定、更清晰
- 你需要把一个业务 SOP、自动化想法、接口串联流程落地成 `n8n`
- 你希望让 AI 帮你减少无意义节点、理顺分支和异常处理

## 核心能力

- 从零生成新工作流
- 重构已有工作流 JSON
- 修复断链、错误分支、Webhook 返回不完整等结构问题
- 用更合理的节点替代不必要的 `Code` 节点
- 为复杂流程补齐失败路径、节流、审批和监控思路

## 目录结构

```text
n8n-workflow-builder/
├─ SKILL.md
├─ README.md
├─ agents/
│  └─ openai.yaml
├─ references/
│  ├─ n8n-workflow-patterns.md
│  ├─ request-template.md
│  └─ review-checklist.md
├─ scripts/
│  └─ validate_workflow.py
└─ docs/
   ├─ usage-guide.zh-CN.md
   └─ whitepaper.zh-CN.md
```

## 如何安装

把整个 `n8n-workflow-builder` 文件夹放到你的 `$CODEX_HOME/skills/` 目录下即可。

在当前机器上，它的位置是：

`C:\Users\62940\.codex\skills\n8n-workflow-builder`

## 如何使用

最简单的调用方式：

```text
使用 $n8n-workflow-builder 根据下面的业务逻辑生成完整可导入的 n8n workflow JSON，并优化节点关系、异常处理和可维护性：
1. ...
2. ...
3. ...
要求：
- ...
- ...
```

更完整的调用方式见：

- [docs/usage-guide.zh-CN.md](./docs/usage-guide.zh-CN.md)
- [references/request-template.md](./references/request-template.md)

## 校验生成结果

如果你把 JSON 保存成文件，可以用内置脚本做基础结构校验：

```powershell
python .\scripts\validate_workflow.py .\your-workflow.json
```

它会检查：

- 顶层字段是否完整
- 节点名称是否重复
- 连接引用的节点是否存在
- 节点是否具备基础必需字段
- 是否存在孤立节点或非触发器的悬空入口

## 输出原则

这个技能默认会让结果尽量满足这些目标：

- 完整
- 可读
- 可导入
- 易维护
- 少写无意义 `Code`
- 不伪造凭证 ID

## 文档

- 使用说明: [docs/usage-guide.zh-CN.md](./docs/usage-guide.zh-CN.md)
- 技术白皮书: [docs/whitepaper.zh-CN.md](./docs/whitepaper.zh-CN.md)
