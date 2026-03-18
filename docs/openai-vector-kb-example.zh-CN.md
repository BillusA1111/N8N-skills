# OpenAI + 向量知识库商业顾问示例

## 示例目标

这个示例工作流展示如何直接在 `n8n` 里调用 OpenAI 的 `Responses API`，配合 `file_search` 和 `vector stores` 做一个更稳的商业顾问与行业分析报告流程。

它的核心思路是：

- 用 OpenAI 托管的 `file_search` 检索企业知识库
- 只基于知识库检索结果生成报告
- 把检索结果一并返回出来，便于做置信度门控
- 当命中文档过少或分数过低时，不直接给“看起来完整”的结论

## 为什么这个版本更适合 OpenAI

这个示例直接遵循官方推荐方向：

- 使用 `Responses API`
- 使用内置工具 `file_search`
- 使用 `vector stores` 承载知识库
- 使用 `include=["file_search_call.results"]` 让响应里带上检索结果

官方文档说明：

- `file_search` 是 `Responses API` 中可用的工具，用于在知识库文件中检索相关内容
- 在把文件加入 `vector store` 后，OpenAI 会自动分块、嵌入和索引
- `Responses API` 支持在一次请求中调用内置工具
- 如果要提升一致性，建议在生产环境中使用固定模型快照

## 工作流结构

```text
Webhook
-> Normalize Request
-> Validate Request
-> Is Request Valid?
-> OpenAI Grounded Report
-> Parse OpenAI Response
-> Score Retrieval Quality
-> Is Grounding Sufficient?
-> Respond Low Confidence / Respond Success
```

## 可配置选项

请求体里可以传这些字段：

- `query`
- `industry`
- `geography`
- `reportType`
- `vectorStoreIds`
- `knowledgeCategories`
- `maxSources`
- `minAcceptedResults`
- `minSearchScore`
- `responseLanguage`
- `model`

说明：

- `vectorStoreIds` 可以是数组，也可以是逗号分隔字符串
- `knowledgeCategories` 可以是数组，也可以是逗号分隔字符串，会映射到 `file_search.filters`
- `model` 推荐你在生产中传固定快照版本
- 如果不传 `model`，工作流会读取环境变量 `OPENAI_RESPONSES_MODEL`

## 必需环境变量

- `OPENAI_API_KEY`
- `OPENAI_RESPONSES_MODEL`

可选环境变量：

- `OPENAI_PROJECT_ID`
- `OPENAI_ORG_ID`
- `OPENAI_VECTOR_STORE_IDS`

说明：

- `OPENAI_VECTOR_STORE_IDS` 可作为默认知识库 ID 列表
- 请求体中的 `vectorStoreIds` 会覆盖默认值

## 输入示例

```json
{
  "query": "请基于知识库分析中国智能家居行业未来12个月的渠道机会、价格带变化与主要竞争风险",
  "industry": "smart-home",
  "geography": "CN",
  "reportType": "industry-opportunity-report",
  "vectorStoreIds": ["vs_abc123", "vs_xyz789"],
  "knowledgeCategories": ["industry-report", "channel-research", "pricing-study"],
  "maxSources": 8,
  "minAcceptedResults": 2,
  "minSearchScore": 0.72,
  "responseLanguage": "zh-CN",
  "model": "gpt-4.1"
}
```

## 输出特点

成功时返回：

- 结构化商业分析报告
- grounding 统计
- 检索命中的文件结果
- citations
- requestId

如果你在向量库文件里设置了 `category` 等 attributes，这个示例就可以按类别约束检索范围。

证据不足时返回：

- `needs_human_review`
- 命中数量与得分统计
- 建议提高知识库质量或补充文档

## 官方参考

- [Responses API 概览](https://developers.openai.com/api/docs/guides/migrate-to-responses)
- [File search 指南](https://developers.openai.com/api/docs/guides/tools-file-search)
- [Retrieval / Vector stores 指南](https://developers.openai.com/api/docs/guides/retrieval)
- [API 概览与请求 ID 说明](https://developers.openai.com/api/reference/overview)

## 文件位置

- 示例 JSON: [examples/business-consultant-openai-vector-kb.json](../examples/business-consultant-openai-vector-kb.json)
