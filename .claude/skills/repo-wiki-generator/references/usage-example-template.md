# 使用场景示例模板

## 核心原则

所有类、方法、接口描述必须补充使用场景示例，确保文档的实用性和可理解性。

---

## 示例结构

### 标准模板

```markdown
**使用场景**：{场景描述}

```{language}
// 示例代码
{code_snippet}
```

**预期结果**：{结果说明}

来源：`{ComponentName}.{functionName}()` ({file_path}:{line_number})
```

### 组件说明

1. **使用场景**: 清晰描述何时、何地、为何使用此功能
2. **代码示例**: 提供完整、可运行的代码示例
3. **预期结果**: 说明执行后的预期输出或行为
4. **来源标注**: 标注代码来源文件路径和行号

---

## 不同场景的示例

### 1. API 接口示例

#### 场景：创建用户

```markdown
**使用场景**：用户注册时调用此接口创建新用户账户

```bash
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "张三",
    "email": "zhangsan@example.com",
    "password": "password123"
  }'
```

**预期结果**：返回创建成功的用户对象，包含自动生成的用户 ID

```json
{
  "code": 200,
  "message": "创建成功",
  "data": {
    "id": 1001,
    "name": "张三",
    "email": "zhangsan@example.com",
    "createdAt": "2024-01-14T10:30:00Z"
  }
}
```

来源：`UserController.createUser()` (src/controllers/UserController.java:45-60)
```

---

### 2. 服务方法示例

#### 场景：验证用户密码

```markdown
**使用场景**：用户登录时验证输入的密码是否正确

```java
UserService userService = new UserService(userRepository);
boolean isValid = userService.validatePassword(1001L, "password123");

if (isValid) {
    System.out.println("密码验证成功");
} else {
    System.out.println("密码错误");
}
```

**预期结果**：如果密码正确返回 `true`，否则返回 `false`

来源：`UserService.validatePassword()` (src/services/UserService.java:85-95)
```

---

### 3. 数据访问方法示例

#### 场景：根据 ID 查询用户

```markdown
**使用场景**：需要获取某个用户的详细信息时

```python
user_repository = UserRepository(db_session)
user = user_repository.find_by_id(1001)

if user:
    print(f"用户名: {user.name}")
    print(f"邮箱: {user.email}")
else:
    print("用户不存在")
```

**预期结果**：返回用户对象，如果用户不存在则返回 `None`

来源：`UserRepository.find_by_id()` (app/repositories/user_repository.py:25-35)
```

---

### 4. 工具函数示例

#### 场景：生成随机密码

```markdown
**使用场景**：用户重置密码时生成新的随机密码

```javascript
const password = generateRandomPassword(12);
console.log(`新密码: ${password}`);
```

**预期结果**：输出一个 12 位的随机密码，包含大小写字母和数字

```
新密码: aB3xY7kP9mQ2
```

来源：`PasswordUtils.generateRandomPassword()` (src/utils/passwordUtils.js:45-55)
```

---

### 5. 外部集成接口示例

#### 场景：调用支付接口

```markdown
**使用场景**：用户下单后调用第三方支付接口完成支付

```go
paymentClient := NewPaymentClient(config)
request := PaymentRequest{
    OrderID:   "ORD20240114001",
    Amount:    99.99,
    Currency:  "CNY",
    UserID:    1001,
}

result, err := paymentClient.Charge(request)
if err != nil {
    log.Printf("支付失败: %v", err)
    return
}

log.Printf("支付成功，交易ID: %s", result.TransactionID)
```

**预期结果**：调用支付接口成功后返回交易 ID

```
支付成功，交易ID: TXN2024011412345678
```

来源：`PaymentClient.Charge()` (internal/client/payment_client.go:60-80)
```

---

## 不同语言的示例格式

### Java

```markdown
**使用场景**：{场景描述}

```java
// 导入必要的类
import com.example.service.UserService;
import com.example.dto.UserDto;

// 创建服务实例
UserService userService = new UserService(userRepository);

// 准备数据
UserDto userDto = new UserDto();
userDto.setName("张三");
userDto.setEmail("zhangsan@example.com");

// 调用方法
User user = userService.createUser(userDto);

// 输出结果
System.out.println("创建的用户ID: " + user.getId());
```

**预期结果**：{结果说明}

来源：`UserService.createUser()` (src/services/UserService.java:45-60)
```

---

### Python

```markdown
**使用场景**：{场景描述}

```python
from app.services import UserService
from app.dto import UserDto

# 创建服务实例
user_service = UserService(user_repository)

# 准备数据
user_dto = UserDto(
    name="张三",
    email="zhangsan@example.com"
)

# 调用方法
user = user_service.create_user(user_dto)

# 输出结果
print(f"创建的用户ID: {user.id}")
```

**预期结果**：{结果说明}

来源：`UserService.create_user()` (app/services/user_service.py:45-60)
```

---

### JavaScript

```markdown
**使用场景**：{场景描述}

```javascript
const UserService = require('./services/userService');

// 创建服务实例
const userService = new UserService(userRepository);

// 准备数据
const userDto = {
  name: '张三',
  email: 'zhangsan@example.com'
};

// 调用方法
const user = await userService.createUser(userDto);

// 输出结果
console.log(`创建的用户ID: ${user.id}`);
```

**预期结果**：{结果说明}

来源：`UserService.createUser()` (src/services/userService.js:45-60)
```

---

### Go

```markdown
**使用场景**：{场景描述}

```go
package main

import (
    "fmt"
    "your-project/internal/service"
    "your-project/internal/dto"
)

func main() {
    // 创建服务实例
    userService := service.NewUserService(userRepository)

    // 准备数据
    userDto := dto.UserDto{
        Name:  "张三",
        Email: "zhangsan@example.com",
    }

    // 调用方法
    user, err := userService.CreateUser(userDto)
    if err != nil {
        fmt.Printf("创建用户失败: %v\n", err)
        return
    }

    // 输出结果
    fmt.Printf("创建的用户ID: %d\n", user.ID)
}
```

**预期结果**：{结果说明}

来源：`UserService.CreateUser()` (internal/service/user_service.go:45-60)
```

---

## 复杂场景示例

### 场景：完整业务流程

```markdown
**使用场景**：用户下单的完整流程，包括创建订单、扣减库存、处理支付

```java
// 1. 创建订单
OrderService orderService = new OrderService(orderRepository);
OrderDto orderDto = new OrderDto();
orderDto.setUserId(1001L);
orderDto.setProductId(2001L);
orderDto.setQuantity(2);

Order order = orderService.createOrder(orderDto);

// 2. 扣减库存
InventoryService inventoryService = new InventoryService(inventoryRepository);
inventoryService.deductStock(2001L, 2);

// 3. 处理支付
PaymentService paymentService = new PaymentService(paymentClient);
PaymentResult result = paymentService.processPayment(
    order.getId(), 
    order.getTotalAmount()
);

if (result.isSuccess()) {
    // 4. 更新订单状态
    orderService.updateOrderStatus(order.getId(), OrderStatus.PAID);
    System.out.println("订单处理完成");
} else {
    // 支付失败，回滚库存
    inventoryService.restoreStock(2001L, 2);
    orderService.updateOrderStatus(order.getId(), OrderStatus.FAILED);
    System.out.println("订单处理失败");
}
```

**预期结果**：
- 如果支付成功：订单状态更新为"已支付"，库存已扣减
- 如果支付失败：订单状态更新为"失败"，库存已恢复

来源：
- `OrderService.createOrder()` (src/services/OrderService.java:30-50)
- `InventoryService.deductStock()` (src/services/InventoryService.java:25-35)
- `PaymentService.processPayment()` (src/services/PaymentService.java:40-60)
```

---

## 错误处理示例

### 场景：处理异常情况

```markdown
**使用场景**：当用户不存在时的错误处理

```python
try:
    user = user_service.get_user(9999)
    print(f"用户名: {user.name}")
except UserNotFoundError as e:
    print(f"错误: {e.message}")
    # 执行错误处理逻辑
    logging.error(f"用户不存在: {e.user_id}")
except Exception as e:
    print(f"未知错误: {str(e)}")
    logging.exception("获取用户失败")
```

**预期结果**：
- 如果用户存在：输出用户信息
- 如果用户不存在：捕获 `UserNotFoundError` 异常并输出错误信息
- 如果发生其他错误：捕获通用异常并记录日志

来源：`UserService.get_user()` (app/services/user_service.py:70-85)
```

---

## 示例质量标准

### 1. 完整性

- [ ] 包含完整的代码示例
- [ ] 代码可以独立运行
- [ ] 包含必要的导入语句
- [ ] 包含必要的变量初始化

### 2. 清晰性

- [ ] 使用有意义的变量名
- [ ] 添加适当的注释
- [ ] 代码格式规范
- [ ] 逻辑清晰易懂

### 3. 实用性

- [ ] 场景描述清晰
- [ ] 预期结果明确
- [ ] 涵盖常见使用情况
- [ ] 包含错误处理

### 4. 准确性

- [ ] 代码与实际实现一致
- [ ] 预期结果与实际行为一致
- [ ] 来源标注正确
- [ ] 无语法错误

---

## 验证清单

在生成示例时，检查以下项目：

- [ ] 示例包含使用场景描述
- [ ] 示例包含完整代码
- [ ] 示例包含预期结果说明
- [ ] 示例包含来源标注
- [ ] 代码格式正确
- [ ] 变量命名有意义
- [ ] 包含必要的注释
- [ ] 预期结果准确
- [ ] 来源标注格式正确
- [ ] 代码可以独立运行

---

## 常见错误

### 错误1: 缺少使用场景描述

```
❌ 错误：
```java
UserService userService = new UserService();
User user = userService.createUser(userDto);
```

✅ 正确：
**使用场景**：用户注册时创建新用户账户

```java
UserService userService = new UserService();
User user = userService.createUser(userDto);
```
```

### 错误2: 缺少预期结果

```
❌ 错误：
```java
User user = userService.createUser(userDto);
```

来源：`UserService.createUser()` (src/services/UserService.java:45-60)

✅ 正确：
```java
User user = userService.createUser(userDto);
```

**预期结果**：返回创建的用户对象，包含自动生成的 ID

来源：`UserService.createUser()` (src/services/UserService.java:45-60)
```

### 错误3: 代码不完整

```
❌ 错误：
```java
User user = userService.createUser(userDto);
```

✅ 正确：
```java
UserService userService = new UserService(userRepository);
UserDto userDto = new UserDto();
userDto.setName("张三");
userDto.setEmail("zhangsan@example.com");

User user = userService.createUser(userDto);
```