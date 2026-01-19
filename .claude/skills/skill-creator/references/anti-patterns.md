# 反模式警告

**CRITICAL**: 避免以下错误做法。

## 1. 确定性逻辑写在指令中

### ❌ 错误

```markdown
Step 1: 计算 ROE = 净利润 / 股东权益
Step 2: 计算 ROA = 净利润 / 总资产
```

### ✅ 正确

```markdown
Step 1: 执行财务比率计算
- 调用脚本：`echo '{"net_income": 1000, "equity": 5000}' | python scripts/calculate_ratios.py`
```

## 2. Agent 执行批量操作

### ❌ 错误

```markdown
Step 1: 循环处理每个视频
Step 2: 下载视频文件
Step 3: 保存结果统计
```

### ✅ 正确

```markdown
Step 1: Agent 解析录制列表为 JSON（需要理解用户输入）
Step 2: 脚本执行批量下载（确定性逻辑）
   - 执行脚本：`python download.py --json_file down_list.json`
```

## 3. 独立章节列出资源

### ❌ 错误

```markdown
## References
- references/api.md
```

### ✅ 正确

```markdown
2. **执行计算**: 调用 `python scripts/calc.py`
```

## 4. 其他反模式

- ❌ 创建辅助文档（README.md, CHANGELOG.md）
- ❌ Windows 路径格式（`references\api.md`）
- ✅ 使用正斜杠（`references/api-reference.md`）
