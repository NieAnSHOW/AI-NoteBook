# 脚本测试清单

**CRITICAL**: 脚本必须在包含到 Skill 前进行测试。

## 手动测试命令

### 测试正常输入

```bash
echo '{"field1": "value1", "field2": "value2"}' | python scripts/my_script.py
```

### 测试错误处理

```bash
echo '{"invalid": "data"}' | python scripts/my_script.py
```

### 测试边界情况

```bash
# 空输入
echo '{}' | python scripts/my_script.py

# 空值
echo '{"field1": null}' | python scripts/my_script.py

# 极端值
echo '{"value": 999999999}' | python scripts/my_script.py
```

## 验证清单

- [ ] 脚本无错误运行
- [ ] 输出符合预期格式（JSON）
- [ ] 错误情况处理优雅（输出到 stderr）
- [ ] 边界情况已考虑
- [ ] 无硬编码路径或值
- [ ] 必需字段验证正确
- [ ] 返回码正确（成功 0，失败 1）

## 常见问题排查

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| JSON 解析错误 | 输入格式不正确 | 检查 JSON 语法 |
| 字段缺失错误 | 必需字段未提供 | 添加字段验证 |
| 编码错误 | 非 ASCII 字符 | 使用 `ensure_ascii=False` |
| 路径错误 | 硬编码路径 | 使用相对路径或参数 |
