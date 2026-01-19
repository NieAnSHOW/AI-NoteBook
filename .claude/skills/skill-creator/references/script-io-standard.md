# 脚本输入输出标准

**CRITICAL**: 所有脚本必须使用 stdin/stdout JSON 格式进行输入输出。

## 输入标准 (stdin JSON)

```python
import sys
import json

# 从 stdin 读取 JSON
input_data = json.loads(sys.stdin.read())
```

## 输出标准 (stdout JSON)

### 成功输出

```python
result = {
    "status": "success",
    "data": {
        # 处理结果
    }
}
print(json.dumps(result, indent=2))
```

### 错误输出 (to stderr)

```python
error = {
    "status": "error",
    "error_type": "ValueError",
    "message": "错误描述"
}
print(json.dumps(error, indent=2), file=sys.stderr)
sys.exit(1)
```

## 调用示例

### 命令行调用

```bash
echo '{"net_income": 1000000, "equity": 5000000}' | python scripts/calculate_roe.py
```

### 在 SKILL.md 中引用

```markdown
2. **Step 2**: 执行计算
   - 调用脚本：`echo '{"data": 100}' | python scripts/calculate.py`
   - 预期输出：`{"result": <number>, "status": "success"}`
```

## 输出格式规范

| 字段 | 类型 | 说明 |
|------|------|------|
| status | string | "success" 或 "error" |
| data | object | 成功时的处理结果 |
| error_type | string | 错误时的异常类型 |
| message | string | 错误时的描述信息 |
