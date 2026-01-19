# 核心生成原则

## 1. 可追溯性原则（最高优先级）

### 核心要求
所有结论、图表、示例必须标注来源。

### 来源标注格式

#### 模块引用
```
来源：`{module_path}.{ComponentName}` ({file_path}:{line_number})
```

#### 函数引用
```
来源：`{ComponentName}.{functionName}()` ({file_path}:{line_number})
```

#### 接口引用
```
来源：`{InterfaceName}` ({file_path}:{line_number})
```

#### 配置引用
```
来源：配置文件 `{config_file}` ({line_number} 行)
```

### 标注示例

**Java**
```
来源：`com.example.UserService` (src/main/java/com/example/UserService.java:25)
```

**Python**
```
来源：`app.services.user_service.UserService` (app/services/user_service.py:25)
```

**JavaScript**
```
来源：`UserService.createUser()` (src/services/userService.js:45-60)
```

**Go**
```
来源：`userservice.CreateUser()` (internal/service/user_service.go:45-60)
```

**Rust**
```
来源：`user_service::UserService::create_user()` (src/services/user_service.rs:45-60)
```

**C#**
```
来源：`UserService.CreateUser()` (Services/UserService.cs:45-60)
```

**配置**
```
来源：配置文件 `application.yml` (15-20 行)
```

### 强制标注场景
- 描述类/模块/组件时
- 描述方法/函数时
- 引用配置参数时
- 描述数据模型时
- 展示代码示例时
- 绘制流程图的每个节点

---

## 2. 使用示例驱动原则

### 核心要求
所有类、方法、接口描述必须补充使用场景示例。

### 示例结构
1. **使用场景说明**
2. **具体代码示例**
3. **预期结果说明**

### 示例模板

```markdown
**使用场景**：{场景描述}

```{language}
// 示例代码
{code_snippet}
```

**预期结果**：{结果说明}

来源：`{ComponentName}.{functionName}()` ({file_path}:{line_number})
```

### 强制补充场景
- API/接口层说明
- 服务层方法说明
- 数据访问层方法说明
- 工具函数说明
- 外部集成接口说明

---

## 3. 内容预估原则

### 核心要求
每个章节必须标注预估行数。

### 标注格式
```markdown
## 章节标题 (预估约 X 行)
```

### 预估时机
1. 文档规划阶段预估
2. 文档生成后验证
3. 如实际行数与预估相差>30%，需说明原因

### 复杂度拆分规则
- **阈值**: 2000行
- **操作**: 单模块预估超过2000行时拆分
- **拆分策略**:
  - 模块概述文档
  - 核心流程详解文档
  - 规则逻辑详解文档

---

## 4. 零推测原则

### 绝对约束
严禁任何形式的推测、臆测或理论化描述。

### 禁止行为
- ❌ 描述不存在的功能
- ❌ 臆造接口或方法
- ❌ 推测设计意图
- ❌ 凭经验描述
- ❌ 使用"可能"、"应该"、"大概"等模糊词汇

### 必需行为
- ✅ 所有内容必须基于实际代码
- ✅ 所有描述必须标注来源
- ✅ 不确定时向用户询问
- ✅ 使用确定性语言

---

## 5. HIL (Human in the Loop) 机制

### 强制停止点

#### 规划后确认
- **触发**: 生成文档规划后
- **操作**: MUST STOP - 等待用户确认规划
- **提示模板**:
  ```markdown
  ## 📋 知识库生成规划确认
  
  **文档清单**：
  {document_list_with_estimated_lines}
  
  **总文档数**: {document_count}
  **预估总行数**: {total_lines}
  
  **⚠️ 强制确认点**：继续执行将开始生成知识库
  
  **确认选项**：
  - 输入 "确认继续" 开始生成
  - 输入 "修改规划" 调整规划  
  - 输入 "取消" 终止操作
  ```

- **违规预防**: 如果AI未等待用户确认就继续，立即停止并道歉

### 动态确认

#### 触发条件
生成过程中遇到不明确内容时

#### 场景
- 业务逻辑理解不确定
- 技术实现细节模糊
- 架构设计意图不明
- 模块职责边界不清

#### 响应策略
1. 明确说明困惑的具体点
2. 提供当前理解
3. 请求用户澄清或补充
4. 避免自主臆测

---

## 6. 图表可视化设计

### 配色方案

#### 文字可见性优先级
1. 所有文字使用黑色或深灰色 (`#000000` 或 `#333333`)
2. 节点背景使用浅色调，确保高对比度
3. 边框使用中等深度颜色增强结构感
4. 避免高饱和度颜色影响文字可读性

#### 通用样式

**流程节点**
```
fill:#e3f2fd,stroke:#1976d2,stroke-width:2px,color:#000000
```

**决策节点**
```
fill:#fff3e0,stroke:#f57c00,stroke-width:2px,color:#000000
```

**错误节点**
```
fill:#ffebee,stroke:#d32f2f,stroke-width:2px,color:#000000
```

**成功节点**
```
fill:#e8f5e8,stroke:#388e3c,stroke-width:2px,color:#000000
```

**人工确认节点**
```
fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,color:#000000
```

---

## 7. 绝对约束

### 代码一致性
- **规则**: 100%代码一致性
- **执行**: 所有技术信息必须与实际代码完全一致
- **违规**: 立即修正，零容忍

### 来源标注
- **规则**: 强制标注来源
- **格式**: `ComponentName.methodName()` (file/path:line_number)
- **范围**: 所有类、方法、配置引用

### 分支控制
- **规则**: 无分支限制
- **要求**: 可在任意分支生成知识库

### 强制验证
- **规则**: 每个文档生成后立即验证
- **独立性**: 不依赖生成时的上下文

### 输出位置
- **规则**: 输出位置固定
- **路径**: `gientech/wiki/`
- **执行**: 所有文档必须输出到此目录