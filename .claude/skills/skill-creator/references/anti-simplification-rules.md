# 不缺省原则 (Anti-Simplification)

**CRITICAL**: 严禁在没有用户授权的情况下缺省或删减用户提供的内容。

## 内容分工

| SKILL.md (核心层) | Infrastructure (资源层) |
|-------------------|------------------------|
| 用户提供的核心逻辑 | 非核心的详细支撑信息 |
| 业务规则与工作流 | 长篇 API 参考 |
| 任务节点与步骤 | 静态模板 |
| 判定标准与约束 | 冗长示例数据 |

## 资源引用原则

| ✅ 正确：内嵌在步骤中 | ❌ 错误：独立章节 |
|----------------------|------------------|
| `调用脚本：python scripts/calc.py` | `## Scripts` 独立列出 |
| `参考：references/benchmarks.md` | `## References` 独立列出 |

## 逻辑保留底线

- Application 层每个非末端节点必须在 Domain 层有对应 Task
- 严禁删减执行步骤、关键约束或判定标准
- 外部引用仅作辅助，不能替代核心工作流

## 违规示例

### ❌ 过度简化核心逻辑

```markdown
Step 1: 遵循 references/rules.md 执行
```

### ✅ 正确做法

```markdown
Step 1: 执行数据验证
   - 检查必需字段完整性
   - 验证数值范围合理性
   - **CRITICAL**: 分母为零时必须报错
   - 详细规则参考：`references/validation-rules.md`
```
