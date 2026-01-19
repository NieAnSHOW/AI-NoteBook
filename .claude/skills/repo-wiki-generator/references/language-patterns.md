# 多语言识别模式

## 构建系统识别

### Java

**构建文件**:
- `pom.xml` (Maven)
- `build.gradle` / `build.gradle.kts` (Gradle)

**依赖管理**:
- Maven: `<dependencies>` 节点
- Gradle: `dependencies` 块

**项目结构**:
```
src/
├── main/
│   ├── java/
│   └── resources/
└── test/
    ├── java/
    └── resources/
```

---

### Python

**构建文件**:
- `requirements.txt` (pip)
- `setup.py` (setuptools)
- `pyproject.toml` (poetry/modern)

**依赖管理**:
- pip: `package==version`
- poetry: `[tool.poetry.dependencies]`

**项目结构**:
```
src/
├── {package_name}/
├── tests/
└── requirements.txt
```

---

### JavaScript / TypeScript

**构建文件**:
- `package.json` (npm/yarn)
- `yarn.lock` (yarn)
- `package-lock.json` (npm)
- `tsconfig.json` (TypeScript)

**依赖管理**:
- `dependencies`: 运行时依赖
- `devDependencies`: 开发依赖

**项目结构**:
```
src/
├── components/
├── services/
├── utils/
└── index.js/ts
```

---

### Go

**构建文件**:
- `go.mod` (模块定义)
- `go.sum` (依赖校验)

**依赖管理**:
- `require package version`

**项目结构**:
```
cmd/
├── {app_name}/
│   └── main.go
pkg/
├── {package}/
│   └── {file}.go
go.mod
```

---

### Rust

**构建文件**:
- `Cargo.toml` (包配置)
- `Cargo.lock` (依赖锁定)

**依赖管理**:
- `[dependencies]` 节点

**项目结构**:
```
src/
├── main.rs
├── lib.rs
└── modules/
Cargo.toml
```

---

### C#

**构建文件**:
- `*.csproj` (项目文件)
- `*.sln` (解决方案)

**依赖管理**:
- `<PackageReference>` 节点

**项目结构**:
```
src/
├── {Project}/
│   ├── Controllers/
│   ├── Services/
│   └── Models/
```

---

### Ruby

**构建文件**:
- `Gemfile` (Bundler)

**依赖管理**:
- `gem 'package', 'version'`

**项目结构**:
```
lib/
├── {module}/
├── app/
└── spec/
```

---

### PHP

**构建文件**:
- `composer.json` (Composer)

**依赖管理**:
- `"require": {"package": "version"}`

**项目结构**:
```
src/
├── {Namespace}/
├── config/
└── tests/
```

---

## 目录结构模式

### 源码目录

| 语言 | 常见目录 |
|------|---------|
| Java | `src/main/java/` |
| Python | `src/`, `app/`, `lib/` |
| JavaScript | `src/`, `app/` |
| Go | `cmd/`, `pkg/` |
| Rust | `src/` |
| C# | `src/` |
| Ruby | `lib/`, `app/` |
| PHP | `src/` |

### 测试目录

| 语言 | 常见目录 |
|------|---------|
| Java | `src/test/java/` |
| Python | `tests/`, `test/` |
| JavaScript | `tests/`, `__tests__/` |
| Go | `*_test.go` (同目录) |
| Rust | `tests/` |
| C# | `tests/` |
| Ruby | `spec/` |
| PHP | `tests/` |

### 配置目录

| 语言 | 常见目录 |
|------|---------|
| Java | `src/main/resources/` |
| Python | `config/`, `conf/` |
| JavaScript | `config/` |
| Go | `config/` |
| Rust | `config/` |
| C# | `config/`, `App_Data/` |
| Ruby | `config/` |
| PHP | `config/` |

---

## 接口层模式

### Java

**文件模式**:
- `*Controller.java`
- `*Api.java`
- `*Endpoint.java`
- `*Resource.java`

**注解**:
- `@RestController`
- `@RequestMapping`
- `@GetMapping`
- `@PostMapping`

**示例**:
```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) {
        // ...
    }
}
```

---

### Python

**文件模式**:
- `*view.py`
- `*api.py`
- `*router.py`
- `*handler.py`

**框架**:
- Django: `views.py`
- Flask: `routes.py`
- FastAPI: `router.py`

**示例**:
```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/users/{user_id}")
def get_user(user_id: int):
    # ...
```

---

### JavaScript / TypeScript

**文件模式**:
- `*controller.js/ts`
- `*route.js/ts`
- `*api.js/ts`
- `*handler.js/ts`

**框架**:
- Express: `routes/`
- NestJS: `controllers/`

**示例**:
```typescript
@Controller('users')
export class UserController {
    @Get(':id')
    getUser(@Param('id') id: string) {
        // ...
    }
}
```

---

### Go

**文件模式**:
- `*handler.go`
- `*controller.go`
- `*api.go`

**框架**:
- Gin, Echo, Fiber

**示例**:
```go
func GetUser(c *gin.Context) {
    // ...
}

func SetupRoutes(r *gin.Engine) {
    r.GET("/users/:id", GetUser)
}
```

---

## 数据层模式

### Java

**文件模式**:
- `*Entity.java`
- `*Repository.java`
- `*Mapper.java`
- `*DAO.java`

**框架**:
- JPA: `@Entity`, `@Repository`
- MyBatis: `*Mapper.java`

**示例**:
```java
@Entity
public class User {
    @Id
    private Long id;
    // ...
}

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
}
```

---

### Python

**文件模式**:
- `*model.py`
- `*repository.py`
- `*dao.py`

**框架**:
- Django: `models.py`
- SQLAlchemy: `models/`

**示例**:
```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
```

---

### JavaScript / TypeScript

**文件模式**:
- `*model.js/ts`
- `*repository.js/ts`
- `*schema.js/ts`

**框架**:
- Mongoose: `models/`
- TypeORM: `entities/`

**示例**:
```typescript
@Entity()
export class User {
    @PrimaryGeneratedColumn()
    id: number;

    @Column()
    name: string;
}
```

---

## 业务层模式

### Java

**文件模式**:
- `*Service.java`
- `*Manager.java`
- `*Handler.java`

**注解**:
- `@Service`
- `@Transactional`

**示例**:
```java
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
    
    public User createUser(UserDto dto) {
        // ...
    }
}
```

---

### Python

**文件模式**:
- `*service.py`
- `*manager.py`
- `*handler.py`

**示例**:
```python
class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def create_user(self, user_dto: UserDto) -> User:
        # ...
```

---

## 适配器层模式

### Java

**文件模式**:
- `*Client.java`
- `*Adapter.java`
- `*Facade.java`

**示例**:
```java
@Service
public class PaymentClient {
    public PaymentResult charge(PaymentRequest request) {
        // 调用外部支付服务
    }
}
```

---

### Python

**文件模式**:
- `*client.py`
- `*adapter.py`
- `*facade.py`

**示例**:
```python
class PaymentClient:
    def charge(self, request: PaymentRequest) -> PaymentResult:
        # 调用外部支付服务
```

---

## 配置文件模式

### 通用配置

| 文件类型 | 用途 |
|---------|------|
| `*.yml` / `*.yaml` | YAML 配置 |
| `*.json` | JSON 配置 |
| `*.toml` | TOML 配置 |
| `.env` | 环境变量 |

### Java

| 文件 | 用途 |
|------|------|
| `application.yml` | 应用配置 |
| `application.properties` | 应用配置 |
| `logback.xml` | 日志配置 |

### Python

| 文件 | 用途 |
|------|------|
| `settings.py` | Django 配置 |
| `config.py` | Flask 配置 |
| `.env` | 环境变量 |

### JavaScript

| 文件 | 用途 |
|------|------|
| `.env` | 环境变量 |
| `config.js` | 配置文件 |
| `tsconfig.json` | TypeScript 配置 |

### Go

| 文件 | 用途 |
|------|------|
| `config.yaml` | 配置文件 |
| `config.toml` | 配置文件 |

---

## 语言特征识别

### 文件扩展名

| 语言 | 扩展名 |
|------|-------|
| Java | `.java` |
| Python | `.py` |
| JavaScript | `.js`, `.jsx` |
| TypeScript | `.ts`, `.tsx` |
| Go | `.go` |
| Rust | `.rs` |
| C# | `.cs` |
| Ruby | `.rb` |
| PHP | `.php` |

### 包/导入模式

| 语言 | 导入模式 |
|------|---------|
| Java | `import package.Class;` |
| Python | `from module import Class` |
| JavaScript | `import { Class } from 'module'` |
| Go | `import "package"` |
| Rust | `use module::Class;` |
| C# | `using Namespace;` |
| Ruby | `require 'module'` |
| PHP | `use Namespace\Class;` |