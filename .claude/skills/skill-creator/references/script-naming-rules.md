# 脚本命名规范

## 命名规则

- 使用 `snake_case`（下划线连接）
- 描述性命名，表明功能
- Python 文件使用 `.py` 扩展名

## 示例

### ✅ 正确示例

| 文件名 | 功能 |
|--------|------|
| `calculate_ratios.py` | 计算财务比率 |
| `validate_input.py` | 验证输入数据 |
| `generate_report.py` | 生成报告 |
| `parse_pdf.py` | 解析 PDF 文件 |
| `merge_files.py` | 合并文件 |

### ❌ 错误示例

| 文件名 | 问题 |
|--------|------|
| `script1.py` | 不具描述性 |
| `CalculateRatios.py` | 错误大小写（PascalCase） |
| `calculate-ratios.py` | 错误分隔符（kebab-case） |
| `calc.py` | 过于简短，不清晰 |

## 命名建议

1. 使用动词开头：`calculate_`, `validate_`, `generate_`, `parse_`, `merge_`
2. 描述处理对象：`_ratios`, `_input`, `_report`, `_pdf`, `_files`
3. 保持简洁但清晰
