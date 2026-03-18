# 商业顾问与行业分析报告示例

## 示例目标

这个示例工作流演示如何在 `n8n` 中搭一个更稳的“商业顾问”流程：

- 接收用户查询
- 校验请求参数
- 先检索证据，而不是直接让模型裸生成
- 支持知识库、行业数据库、Web 搜索三类信息源开关
- 对证据做置信度门控
- 只在证据足够时生成正式分析报告
- 证据不足时，返回低置信度结果并要求人工复核

## 为什么这个例子更稳

它不是“用户一问，模型直接答”，而是采用了更适合商业咨询场景的结构：

1. 输入校验
   - 避免无效问题直接进入下游流程。
2. 证据优先
   - 先从知识库或外部行业源检索资料，再组织报告。
3. 置信度门控
   - 如果可信来源数量不够，直接降级，不输出看似完整但不可靠的结论。
4. 引用约束
   - 报告节点明确要求基于证据、列出引用、缺信息时说明不足。

## 可配置能力

这个示例预留了以下选项：

- `useKnowledgeBase`
- `useIndustryApi`
- `useWebSearch`
- `knowledgeBaseId`
- `maxSources`
- `minTrustedSources`
- `minConfidence`

因此它既能做：

- 企业内知识库顾问
- 行业情报问答
- 研究型商业报告生成
- 投前/项目初筛辅助分析

## 依赖的环境变量

你需要按自己的系统填这些环境变量：

- `KNOWLEDGE_ORCHESTRATOR_URL`
- `KNOWLEDGE_ORCHESTRATOR_TOKEN`
- `REPORT_LLM_URL`
- `REPORT_LLM_TOKEN`
- `REPORT_LLM_MODEL`

建议做法：

- `KNOWLEDGE_ORCHESTRATOR_URL` 指向你自己的检索编排服务
- 它内部再去接企业知识库、向量库、行业数据库或搜索接口
- `REPORT_LLM_URL` 指向你的报告生成模型接口

## 输入示例

```json
{
  "query": "分析中国智能家居行业在未来12个月的渠道机会与竞争风险",
  "industry": "smart-home",
  "geography": "CN",
  "reportType": "industry-opportunity-report",
  "useKnowledgeBase": true,
  "useIndustryApi": true,
  "useWebSearch": false,
  "knowledgeBaseId": "china-industry-kb",
  "maxSources": 8,
  "minTrustedSources": 2,
  "minConfidence": 0.72,
  "responseLanguage": "zh-CN"
}
```

## 输出特点

成功时，工作流会返回：

- 请求摘要
- 证据统计
- 结构化商业分析报告
- 参考来源列表
- 置信度提示

证据不足时，工作流会返回：

- `needs_human_review`
- 证据不足原因
- 建议补充的数据源或知识库

## 文件位置

- 示例 JSON: [examples/business-consultant-industry-report.json](../examples/business-consultant-industry-report.json)
