# AI-NoteBook 快速参考指南

> **当前版本**: MVP v0.1.0
> **最后更新**: 2026-01-20
> **开发进度**: 20% (Phase 2 进行中)

---

## 🚀 快速启动

### 1. 启动数据库服务
```bash
docker-compose up -d
```

### 2. 启动后端服务
```bash
cd backend
npm run start:dev
```
服务地址: `http://localhost:3000/api`

### 3. 查看服务状态
```bash
# 检查 Docker 容器
docker-compose ps

# 检查后端日志
tail -f /tmp/backend.log

# 查看数据库（Prisma Studio）
npx prisma studio
```

---

## 📡 可用 API 端点

### 认证 API

#### 用户注册
```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "username": "测试用户"
  }'
```

#### 用户登录
```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

#### 获取用户信息（需认证）
```bash
curl -X GET http://localhost:3000/api/auth/profile \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 🗄️ 数据库模型

### User 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| email | String | 邮箱（唯一） |
| password | String | bcrypt 加密密码 |
| username | String? | 用户名 |
| apiKey | String? | API Key（唯一） |
| membership | Enum | FREE/BASIC/PRO |
| balance | Decimal | 余额 |

### Analysis 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| userId | UUID | 用户 ID（外键） |
| title | String | 文章标题 |
| originalContent | Text | 原始内容 |
| processedContent | JSON | 处理后内容 |
| readabilityScore | Int | 易读性评分（1-5） |
| readabilityDetail | JSON | 评分详情 |
| status | Enum | PENDING/PROCESSING/COMPLETED/FAILED |

---

## 📁 关键文件路径

### 后端核心文件
```
backend/
├── src/
│   ├── auth/
│   │   ├── auth.controller.ts    # 认证控制器
│   │   ├── auth.service.ts       # 认证服务
│   │   ├── strategies/
│   │   │   └── jwt.strategy.ts   # JWT 策略
│   │   └── guards/
│   │       └── jwt-auth.guard.ts # JWT 守卫
│   ├── common/
│   │   └── prisma.service.ts     # Prisma 服务
│   └── main.ts                   # 应用入口
├── prisma/
│   ├── schema.prisma             # 数据库模型
│   └── migrations/               # 数据库迁移
└── .env                          # 环境变量
```

### 开发日志
```
devlogs/
├── README.md                              # 日志索引
├── TEMPLATE.md                            # 日志模板
└── 2026-01-20-progress-report.md          # Day 1 日志
```

---

## 🛠️ 常用命令

### 数据库操作
```bash
# 生成 Prisma Client
npx prisma generate

# 创建迁移
npx prisma migrate dev --name <描述>

# 重置数据库（开发环境）
npx prisma migrate reset

# 打开 Prisma Studio
npx prisma studio
```

### 开发服务器
```bash
# 启动开发服务器
npm run start:dev

# 构建生产版本
npm run build

# 启动生产服务器
npm run start:prod
```

### 测试
```bash
# 单元测试
npm run test

# E2E 测试
npm run test:e2e

# 测试覆盖率
npm run test:cov
```

---

## 📊 当前任务状态

### ✅ 已完成
- [x] 项目结构搭建
- [x] Docker Compose 配置
- [x] Prisma 数据库模型
- [x] 用户认证模块
- [x] JWT 认证机制

### ⏳ 进行中
- [ ] AI 服务集成（下一任务）

### 📋 待开发
- [ ] 文章解析模块
- [ ] BullMQ 任务队列
- [ ] 前端 Vue 3 项目
- [ ] 前端页面开发

---

## 🎯 下一步任务 (Phase 2 续)

### 1. AI 服务集成 (预计 2-3 小时)
**优先级**: 🔥 P0

**任务清单**:
- [ ] 创建 AI Module
- [ ] 封装 Volcengine API
- [ ] 实现易读性评分
- [ ] 实现内容提炼
- [ ] 测试 AI 调用

**关键文件**:
- `src/ai/ai.module.ts`
- `src/ai/ai.service.ts`
- `src/ai/prompts/*.ts`

### 2. 文章解析模块 (预计 3-4 小时)
**优先级**: 🔥 P0

**任务清单**:
- [ ] 创建 Analysis Module
- [ ] 实现 CRUD API
- [ ] 配置 BullMQ 队列
- [ ] 实现 Worker 处理器
- [ ] 端到端测试

**关键文件**:
- `src/analysis/analysis.module.ts`
- `src/analysis/analysis.controller.ts`
- `src/analysis/workers/analyze.worker.ts`

---

## ⚠️ 注意事项

### Prisma 版本
- 当前使用 Prisma 5.x（不是 7.x）
- Prisma 7 有破坏性变更，需使用 adapter

### 环境变量
- 确保 `.env` 文件正确配置
- 不要将 `.env` 提交到 Git
- 生产环境需更改 `JWT_SECRET`

### API Key
- 需要申请火山引擎 ARK API Key
- 配置在 `VOLCENGINE_API_KEY` 环境变量中

---

## 🐛 常见问题

### 1. 端口被占用
```bash
# 杀掉占用 3000 端口的进程
lsof -ti:3000 | xargs kill -9
```

### 2. 数据库连接失败
```bash
# 检查 Docker 容器状态
docker-compose ps

# 重启数据库
docker-compose restart db
```

### 3. Prisma Client 过期
```bash
# 重新生成 Prisma Client
npx prisma generate
```

---

## 📚 参考文档

### 内部文档
- [需求文档.md](../需求文档.md) - 完整需求规划
- [devlogs/README.md](./devlogs/README.md) - 开发日志索引
- [devlogs/2026-01-20-progress-report.md](./devlogs/2026-01-20-progress-report.md) - Day 1 详细日志

### 外部文档
- [NestJS 文档](https://docs.nestjs.com/)
- [Prisma 文档](https://www.prisma.io/docs)
- [BullMQ 文档](https://docs.bullmq.io/)
- [Volcengine ARK](https://www.volcengine.com/docs/82379)

---

**文档维护**: 每日更新
**反馈**: 如有问题请查看开发日志或联系开发团队
