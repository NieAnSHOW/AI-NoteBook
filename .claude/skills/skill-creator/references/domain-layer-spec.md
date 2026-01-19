# Domain 层规范

Task 定义与执行的编写规范。

## 核心执行模型

```
Task (任务) - 与 Application 层节点 1:1 对应
├── Dimensions (维度) - 多角度分析
│   ├── Dimension 1
│   └── Dimension 2
└── Workflows (工作流) - 顺序执行
    ├── Step 1
    └── Step 2
```

## Task 标准结构模板

```markdown
### NodeID[任务名称]

**场景说明**: [描述任务目标与触发条件]

#### 1. 执行维度/工作流

1. **维度/步骤 1**: [原子动作描述]
   - 具体操作
   - **CRITICAL**: [核心约束]

2. **维度/步骤 2**: [逻辑加工步骤]
   - 执行计算：`python scripts/xxx.py`
   - 参考资料：`references/xxx.md`

#### 2. 输出确认

🔍 **[任务名称]完成**
- 处理项目：{项目说明}
✅ [下一步说明]
```

## 节点对应规则

**CRITICAL**: Application 层每个非末端节点必须在 Domain 层有对应 Task。

| Application 节点 | Domain Task |
|-----------------|-------------|
| `S1[创建流程]` | `### S1[创建流程]` |
| `S2[编辑流程]` | `### S2[编辑流程]` |
| `Common[通用处理]` | `### Common[通用处理]` |

## 资源引用规则

**CRITICAL**: Infrastructure 资源引用必须内嵌在步骤中。

✅ 正确：
```markdown
2. **Step 2**: 执行计算
   - 调用脚本：`python scripts/calc.py`
   - 参考资料：`references/guide.md`
```

❌ 错误：
```markdown
## Scripts
- scripts/calc.py

## References
- references/guide.md
```
