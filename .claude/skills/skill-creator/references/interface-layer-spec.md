# Interface 层规范

YAML Frontmatter 的编写规范。

## name 字段

- 最大 64 字符
- 小写字母、数字、连字符
- 推荐动名词形式：`analyzing-financial-statements`

**正确示例**:
- `financial-analyzer`
- `pdf-editor`
- `code-reviewer`

**错误示例**:
- `FinancialAnalyzer`（大写字母）
- `financial_analyzer`（下划线）
- `my skill`（空格）

## description 字段

- 最大 1024 字符
- **CRITICAL**: 必须包含"做什么"和所有"何时使用"场景
- 使用第三人称
- 禁止 XML 标签

**模板**:
```
[做什么的简短描述]. Use when (1) [场景1], (2) [场景2], (3) [场景3].
```

**示例**:
```yaml
description: Calculate and interpret financial ratios (ROE, ROA, P/E) from financial statements. Use when (1) analyzing company performance, (2) evaluating investments, (3) comparing financial metrics.
```

## 完整 Frontmatter 示例

```yaml
---
name: financial-analyzer
description: Calculate and interpret financial ratios (ROE, ROA, P/E) from financial statements. Use when (1) analyzing company performance, (2) evaluating investments, (3) comparing financial metrics.
---
```
