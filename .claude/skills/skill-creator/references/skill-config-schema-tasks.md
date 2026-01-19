# Skill 配置 Schema - Tasks 定义

任务列表配置，定义 Domain 层的 Task。

## 字段说明

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| node_id | string | 是 | 对应 scenario.id |
| name | string | 是 | 任务名称 |
| description | string | 是 | 场景说明 |
| steps | array | 是 | 步骤列表 |
| output | string | 否 | 输出确认模板 |

## steps 格式

### 简单格式

```json
"steps": ["步骤1", "步骤2", "步骤3"]
```

### 详细格式

```json
"steps": [
    {
        "type": "step",
        "content": "执行操作",
        "script": "process.py",
        "reference": "guide.md"
    },
    {
        "type": "critical",
        "content": "核心约束"
    },
    {
        "type": "mandatory",
        "content": "必需操作"
    }
]
```

## 完整示例

```json
{
    "tasks": [
        {
            "node_id": "S1",
            "name": "比率计算",
            "description": "当用户需要计算财务比率时使用",
            "steps": [
                {"type": "step", "content": "收集财务数据"},
                {"type": "step", "content": "执行计算", "script": "calculate_ratios.py"},
                {"type": "critical", "content": "验证计算结果合理性"}
            ],
            "output": "🔍 **比率计算完成**\n- ROE: {roe}%\n✅ 可以进行分析"
        }
    ]
}
```
