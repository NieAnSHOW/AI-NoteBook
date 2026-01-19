# 顺序工作流模式

适用于需要按步骤执行的复杂任务。

## 模式说明

顺序工作流按固定顺序执行步骤，每个步骤依赖前一步骤的输出。

## 模板

```markdown
[任务名称]流程：

1. [步骤1名称] (运行 script1.py)
2. [步骤2名称] (编辑 config.json)
3. [步骤3名称] (运行 script2.py)
4. [步骤4名称] (运行 script3.py)
5. [步骤5名称] (运行 verify.py)
```

## 示例

### PDF 表单填写流程

```markdown
PDF 表单填写流程：

1. 分析表单 (运行 analyze_form.py)
2. 创建字段映射 (编辑 fields.json)
3. 验证映射 (运行 validate_fields.py)
4. 填充表单 (运行 fill_form.py)
5. 验证输出 (运行 verify_output.py)
```

### 数据处理流程

```markdown
数据处理流程：

1. 读取原始数据 (运行 read_data.py)
2. 数据清洗 (运行 clean_data.py)
3. 数据转换 (运行 transform_data.py)
4. 数据验证 (运行 validate_data.py)
5. 输出结果 (运行 export_data.py)
```

## 适用场景

- 数据处理管道
- 文件转换流程
- 多步骤验证
- 构建和部署流程
