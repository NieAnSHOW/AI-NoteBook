# 来源标注格式规范

## 核心原则

所有结论、图表、示例必须标注来源，确保100%可追溯性。

---

## 标注格式

### 1. 模块/类引用

**格式**:
```
来源：`{module_path}.{ClassName}` ({file_path}:{line_number})
```

**示例**:
```
来源：`com.example.service.UserService` (src/main/java/com/example/service/UserService.java:25)
来源：`app.services.UserService` (app/services/user_service.py:25)
来源：`userservice.UserService` (internal/service/user_service.go:45)
```

**使用场景**:
- 描述类/模块时
- 引用组件时
- 说明模块职责时

---

### 2. 方法/函数引用

**格式**:
```
来源：`{ClassName}.{methodName}()` ({file_path}:{line_number})
```

**示例**:
```
来源：`UserService.createUser()` (src/main/java/com/example/service/UserService.java:45-60)
来源：`UserService.create_user()` (app/services/user_service.py:45-60)
来源：`UserService.CreateUser()` (Services/UserService.cs:45-60)
```

**使用场景**:
- 描述方法功能时
- 说明调用关系时
- 解释业务逻辑时

---

### 3. 接口引用

**格式**:
```
来源：`{InterfaceName}` ({file_path}:{line_number})
```

**示例**:
```
来源：`UserRepository` (src/main/java/com/example/repository/UserRepository.java:15)
来源：`IUserRepository` (Repositories/IUserRepository.cs:10)
```

**使用场景**:
- 描述接口时
- 说明依赖关系时
- 解释抽象层时

---

### 4. 配置引用

**格式**:
```
来源：配置文件 `{config_file}` ({line_number} 行)
```

**示例**:
```
来源：配置文件 `application.yml` (15-20 行)
来源：配置文件 `config.json` (10 行)
来源：配置文件 `.env` (5 行)
```

**使用场景**:
- 引用配置参数时
- 说明中间件配置时
- 解释环境变量时

---

### 5. 数据模型引用

**格式**:
```
来源：`{ModelName}` ({file_path}:{line_number})
```

**示例**:
```
来源：`User` (src/main/java/com/example/entity/User.java:20)
来源：`User` (app/models/user.py:15)
来源：`User` (internal/model/user.go:10)
```

**使用场景**:
- 描述数据模型时
- 说明字段定义时
- 解释数据关系时

---

### 6. 流程图节点引用

**格式**:
```
- 来源：`{ClassName}.{methodName}()` ({file_path}:{line_number})
```

**示例**:
```markdown
1. **步骤1**: 验证用户输入
   - 来源：`UserService.validateInput()` (src/main/java/com/example/service/UserService.java:30-45)
2. **步骤2**: 创建用户
   - 来源：`UserService.createUser()` (src/main/java/com/example/service/UserService.java:50-70)
3. **步骤3**: 发送通知
   - 来源：`NotificationService.sendWelcomeEmail()` (src/main/java/com/example/service/NotificationService.java:20-35)
```

**使用场景**:
- 流程图节点说明
- 步骤详解
- 调用链路说明

---

## 路径格式规范

### 绝对路径 vs 相对路径

**推荐使用相对路径**（从项目根目录开始）:
```
✅ 正确：src/main/java/com/example/service/UserService.java
❌ 错误：/home/user/project/src/main/java/com/example/service/UserService.java
```

### 路径分隔符

**统一使用正斜杠 `/`**:
```
✅ 正确：src/main/java/com/example/service/UserService.java
❌ 错误：src\main\java\com\example\service\UserService.java
```

### 行号格式

**单行**:
```
来源：`UserService.createUser()` (src/main/java/com/example/service/UserService.java:45)
```

**多行范围**:
```
来源：`UserService.createUser()` (src/main/java/com/example/service/UserService.java:45-60)
```

---

## 不同语言的标注示例

### Java

```markdown
**类引用**:
来源：`com.example.service.UserService` (src/main/java/com/example/service/UserService.java:25)

**方法引用**:
来源：`UserService.createUser()` (src/main/java/com/example/service/UserService.java:45-60)

**接口引用**:
来源：`UserRepository` (src/main/java/com/example/repository/UserRepository.java:15)

**配置引用**:
来源：配置文件 `application.yml` (15-20 行)
```

---

### Python

```markdown
**类引用**:
来源：`app.services.user_service.UserService` (app/services/user_service.py:25)

**方法引用**:
来源：`UserService.create_user()` (app/services/user_service.py:45-60)

**接口引用**:
来源：`UserRepository` (app/repositories/user_repository.py:15)

**配置引用**:
来源：配置文件 `settings.py` (30 行)
```

---

### JavaScript / TypeScript

```markdown
**类引用**:
来源：`UserService` (src/services/userService.js:25)

**方法引用**:
来源：`UserService.createUser()` (src/services/userService.js:45-60)

**接口引用**:
来源：`IUserRepository` (src/repositories/userRepository.ts:15)

**配置引用**:
来源：配置文件 `config.js` (20 行)
```

---

### Go

```markdown
**类引用**:
来源：`userservice.UserService` (internal/service/user_service.go:25)

**方法引用**:
来源：`UserService.CreateUser()` (internal/service/user_service.go:45-60)

**接口引用**:
来源：`UserRepository` (internal/repository/user_repository.go:15)

**配置引用**:
来源：配置文件 `config.yaml` (10 行)
```

---

### Rust

```markdown
**类引用**:
来源：`user_service::UserService` (src/service/user_service.rs:25)

**方法引用**:
来源：`UserService::create_user()` (src/service/user_service.rs:45-60)

**接口引用**:
来源：`UserRepository` (src/repository/user_repository.rs:15)

**配置引用**:
来源：配置文件 `config.toml` (10 行)
```

---

### C#

```markdown
**类引用**:
来源：`Services.UserService` (Services/UserService.cs:25)

**方法引用**:
来源：`UserService.CreateUser()` (Services/UserService.cs:45-60)

**接口引用**:
来源：`IUserRepository` (Repositories/IUserRepository.cs:15)

**配置引用**:
来源：配置文件 `appsettings.json` (20 行)
```

---

## 标注位置规范

### 文档中的标注位置

#### 1. 章节标题后
```markdown
## 对外接口 (预估约 X 行)

**接口清单**:
| 接口路径 | 功能描述 | 文件位置 |
|---------|---------|---------|
| `/api/users` | 获取用户列表 | `UserController.getUsers()` (src/controllers/UserController.java:25) |
```

#### 2. 功能描述后
```markdown
**功能描述**: 创建新用户，验证输入数据并持久化到数据库。

来源：`UserService.createUser()` (src/services/UserService.java:45-60)
```

#### 3. 代码示例后
```markdown
```java
UserService userService = new UserService();
User user = userService.createUser(userDto);
```

**预期结果**: 返回创建的用户对象，包含自动生成的 ID。

来源：`UserService.createUser()` (src/services/UserService.java:45-60)
```

#### 4. 流程图节点中
```markdown
1. **步骤1**: 验证用户输入
   - 验证邮箱格式
   - 验证密码强度
   - 来源：`UserService.validateInput()` (src/services/UserService.java:30-45)
```

---

## 常见错误

### 错误1: 缺少文件路径
```
❌ 错误：来源：UserService.createUser()
✅ 正确：来源：`UserService.createUser()` (src/services/UserService.java:45-60)
```

### 错误2: 缺少行号
```
❌ 错误：来源：`UserService.createUser()` (src/services/UserService.java)
✅ 正确：来源：`UserService.createUser()` (src/services/UserService.java:45-60)
```

### 错误3: 使用绝对路径
```
❌ 错误：来源：`UserService.createUser()` (/home/user/project/src/services/UserService.java:45-60)
✅ 正确：来源：`UserService.createUser()` (src/services/UserService.java:45-60)
```

### 错误4: 使用反斜杠
```
❌ 错误：来源：`UserService.createUser()` (src\services\UserService.java:45-60)
✅ 正确：来源：`UserService.createUser()` (src/services/UserService.java:45-60)
```

### 错误5: 缺少反引号
```
❌ 错误：来源：UserService.createUser() (src/services/UserService.java:45-60)
✅ 正确：来源：`UserService.createUser()` (src/services/UserService.java:45-60)
```

---

## 批量标注示例

### 接口清单表格
```markdown
| 接口路径 | 功能描述 | 文件位置 |
|---------|---------|---------|
| `/api/users` | 获取用户列表 | `UserController.getUsers()` (src/controllers/UserController.java:25) |
| `/api/users/{id}` | 获取用户详情 | `UserController.getUser()` (src/controllers/UserController.java:35) |
| `/api/users` | 创建用户 | `UserController.createUser()` (src/controllers/UserController.java:45) |
```

### 方法清单表格
```markdown
| 方法名 | 功能 | 使用场景 | 文件位置 |
|-------|------|---------|---------|
| `createUser()` | 创建用户 | 用户注册 | `UserService.createUser()` (src/services/UserService.java:45-60) |
| `updateUser()` | 更新用户 | 用户信息修改 | `UserService.updateUser()` (src/services/UserService.java:65-80) |
| `deleteUser()` | 删除用户 | 用户注销 | `UserService.deleteUser()` (src/services/UserService.java:85-95) |
```

---

## 验证清单

在生成文档时，检查以下项目：

- [ ] 所有类/模块引用都有文件路径和行号
- [ ] 所有方法/函数引用都有文件路径和行号
- [ ] 所有接口引用都有文件路径和行号
- [ ] 所有配置引用都有文件路径和行号
- [ ] 所有数据模型引用都有文件路径和行号
- [ ] 所有流程图节点都有来源标注
- [ ] 所有代码示例都有来源标注
- [ ] 使用相对路径（从项目根目录开始）
- [ ] 使用正斜杠 `/` 作为路径分隔符
- [ ] 使用反引号包裹类名和方法名
- [ ] 行号格式正确（单行或范围）

---

## 自动化验证

使用验证脚本检查标注完整性：

```bash
python scripts/validate_document.py <document_path>
```

**验证内容**:
1. 来源标注格式是否正确
2. 文件路径是否存在
3. 行号是否在合理范围内
4. 路径分隔符是否正确
5. 是否缺少必要的标注