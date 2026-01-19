# Skill 配置 Schema - 基础字段

用于 `generate_skill.py` 脚本的配置 JSON 基础字段说明。

## 必需字段

### name

- 类型：string
- 规范：小写字母、数字、连字符
- 最大长度：64 字符

```json
{
    "name": "financial-analyzer"
}
```

### description

- 类型：string
- 规范：包含"做什么"+"何时使用"
- 最大长度：1024 字符

```json
{
    "description": "Calculate financial ratios. Use when (1) analyzing performance, (2) evaluating investments."
}
```

## 可选字段

### title

- 类型：string
- 说明：显示标题，默认从 name 生成

```json
{
    "title": "Financial Analyzer"
}
```

## 最小配置示例

```json
{
    "name": "my-skill",
    "description": "Do something useful. Use when (1) scenario A, (2) scenario B.",
    "scenarios": [],
    "tasks": []
}
```
