# 统一强调标记

在 SKILL.md 和输出中使用的标准化标记体系。

## 标记定义

| 标记 | 用途 | 使用场景 |
|------|------|----------|
| **CRITICAL** | 必须严格遵守的红线规则 | 分母为零时必须报错 |
| **MANDATORY** | 必需执行的操作步骤 | 必须先执行场景识别 |
| **IMPORTANT** | 关键的质量建议 | 建议添加单元测试 |
| **WARNING** | 潜在的错误或风险 | 此操作不可逆 |

## 使用示例

### CRITICAL - 红线规则

```markdown
- **CRITICAL**: 验证计算结果合理性
- **CRITICAL**: 分母为零时必须报错
- **CRITICAL**: 脚本必须实际运行测试
```

### MANDATORY - 必需操作

```markdown
- **MANDATORY**: 每次任务必须先执行场景识别
- **MANDATORY**: 必须使用此模板结构
- **MANDATORY**: 验证输出文件
```

### IMPORTANT - 质量建议

```markdown
- **IMPORTANT**: 建议添加单元测试
- **IMPORTANT**: 考虑边界情况
```

### WARNING - 风险提示

```markdown
- **WARNING**: 此操作不可逆
- **WARNING**: 可能覆盖现有文件
```
