# 部署指南

本文档说明如何部署AI-NoteBook系统到生产环境。

## 环境要求

### 服务器配置

**最低配置**：
- CPU: 2核
- 内存: 4GB
- 硬盘: 40GB SSD

**推荐配置**：
- CPU: 4核+
- 内存: 8GB+
- 硬盘: 100GB SSD

### 软件依赖

```bash
# Node.js
Node.js >= 20.x
npm >= 10.x

# 数据库
PostgreSQL >= 15.x
Redis >= 7.x

# Web服务器
Nginx >= 1.24
```

## 前端部署

### 1. 构建前端

```bash
cd frontend
npm install
npm run build
```

构建产物在 `dist/` 目录。

### 2. 配置Nginx

```nginx
server {
  listen 80;
  server_name app.ainotebook.com;

  # 强制HTTPS
  return 301 https://$server_name$request_uri;
}

server {
  listen 443 ssl http2;
  server_name app.ainotebook.com;

  # SSL证书
  ssl_certificate /etc/letsencrypt/live/app.ainotebook.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/app.ainotebook.com/privkey.pem;

  # 前端静态文件
  root /var/www/ainotebook/frontend/dist;
  index index.html;

  # Gzip压缩
  gzip on;
  gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
  gzip_min_length 1000;

  # 前端路由
  location / {
    try_files $uri $uri/ /index.html;
  }

  # API代理
  location /api {
    proxy_pass http://localhost:3000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_cache_bypass $http_upgrade;
  }

  # WebSocket支持
  location /ws {
    proxy_pass http://localhost:3000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_read_timeout 86400;
  }
}
```

### 3. 配置CDN（可选）

将静态资源上传到CDN：

```bash
# 上传到阿里云OSS
aws s3 sync dist/ s3://your-cdn-bucket/ --acl public-read
```

## 后端部署

### 1. 安装依赖

```bash
cd backend
npm install --production
```

### 2. 配置环境变量

创建 `.env` 文件：

```env
# 应用配置
NODE_ENV=production
PORT=3000
APP_NAME=AI-NoteBook
APP_URL=https://app.ainotebook.com

# 数据库
DATABASE_URL=postgresql://user:password@localhost:5432/ainotebook

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET=your-secret-key
JWT_REFRESH_SECRET=your-refresh-secret
JWT_EXPIRES_IN=15m
JWT_REFRESH_EXPIRES_IN=7d

# AI服务
VOLCENGINE_API_KEY=your-volcengine-key
OPENAI_API_KEY=your-openai-key
OPENAI_BASE_URL=https://api.openai.com/v1

# 搜索服务
SEARCH_ENGINE_API_KEY=your-search-api-key

# 支付配置
ALIPAY_APP_ID=your-alipay-app-id
ALIPAY_PRIVATE_KEY=your-alipay-private-key
ALIPAY_PUBLIC_KEY=your-alipay-public-key

WECHAT_APP_ID=your-wechat-app-id
WECHAT_MCH_ID=your-wechat-mch-id
WECHAT_API_KEY=your-wechat-api-key

# 文件存储
UPLOAD_DIR=/var/www/ainotebook/uploads
MAX_FILE_SIZE=5242880
```

### 3. 初始化数据库

```bash
# 生成Prisma客户端
npx prisma generate

# 执行数据库迁移
npx prisma migrate deploy

# 种子数据（可选）
npx prisma db seed
```

### 4. 使用PM2管理进程

安装PM2：

```bash
npm install -g pm2
```

创建 `ecosystem.config.js`：

```javascript
module.exports = {
  apps: [{
    name: 'ainotebook-api',
    script: './dist/main.js',
    instances: 'max',  // 使用所有CPU核心
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production',
      PORT: 3000
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    merge_logs: true,
    max_memory_restart: '1G'
  }]
}
```

启动服务：

```bash
# 构建TypeScript
npm run build

# 启动PM2
pm2 start ecosystem.config.js

# 查看状态
pm2 status

# 查看日志
pm2 logs ainotebook-api

# 重启服务
pm2 restart ainotebook-api

# 停止服务
pm2 stop ainotebook-api
```

### 5. 配置Systemd（可选）

创建 `/etc/systemd/system/ainotebook.service`：

```ini
[Unit]
Description=AI-NoteBook API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/ainotebook/backend
ExecStart=/usr/bin/node /var/www/ainotebook/backend/dist/main.js
Restart=on-failure
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=ainotebook

[Install]
WantedBy=multi-user.target
```

启用服务：

```bash
sudo systemctl enable ainotebook
sudo systemctl start ainotebook
sudo systemctl status ainotebook
```

## 数据库部署

### 1. PostgreSQL配置

#### 安装PostgreSQL

```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# CentOS/RHEL
sudo yum install postgresql-server
sudo postgresql-setup initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### 创建数据库和用户

```bash
sudo -u postgres psql
```

```sql
-- 创建用户
CREATE USER ainotebook WITH PASSWORD 'your-password';

-- 创建数据库
CREATE DATABASE ainotebook OWNER ainotebook;

-- 授权
GRANT ALL PRIVILEGES ON DATABASE ainotebook TO ainotebook;

-- 退出
\q
```

#### 优化配置

编辑 `/etc/postgresql/15/main/postgresql.conf`：

```ini
# 连接设置
max_connections = 100
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1

# 日志设置
logging_collector = on
log_directory = 'pg_log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_statement = 'mod'
```

### 2. Redis配置

#### 安装Redis

```bash
# Ubuntu/Debian
sudo apt install redis-server

# CentOS/RHEL
sudo yum install redis
sudo systemctl start redis
sudo systemctl enable redis
```

#### 配置Redis

编辑 `/etc/redis/redis.conf`：

```ini
# 绑定地址
bind 127.0.0.1

# 内存设置
maxmemory 256mb
maxmemory-policy allkeys-lru

# 持久化
save 900 1
save 300 10
save 60 10000

# 日志
loglevel notice
logfile /var/log/redis/redis-server.log
```

## Docker部署

### 使用Docker Compose

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: ainotebook-db
    environment:
      POSTGRES_DB: ainotebook
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: ainotebook-redis
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    restart: unless-stopped

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: ainotebook-api
    environment:
      NODE_ENV: production
      DATABASE_URL: postgresql://postgres:${DB_PASSWORD}@postgres:5432/ainotebook
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis
    ports:
      - "3000:3000"
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: ainotebook-frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### 后端Dockerfile

创建 `backend/Dockerfile`：

```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

# 复制依赖文件
COPY package*.json ./
COPY prisma ./prisma/

# 安装依赖
RUN npm ci

# 复制源代码
COPY . .

# 生成Prisma客户端
RUN npx prisma generate

# 构建项目
RUN npm run build

# 生产镜像
FROM node:20-alpine

WORKDIR /app

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/prisma ./prisma

EXPOSE 3000

CMD ["node", "dist/main.js"]
```

### 启动服务

```bash
docker-compose up -d
```

## 监控和日志

### 1. 日志管理

使用Winston记录日志：

```typescript
// logger.config.ts
import * as winston from 'winston'

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({
      filename: 'logs/error.log',
      level: 'error',
      maxsize: 10485760,  // 10MB
      maxFiles: 5
    }),
    new winston.transports.File({
      filename: 'logs/combined.log',
      maxsize: 10485760,
      maxFiles: 10
    })
  ]
})

if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple()
  }))
}
```

### 2. 性能监控

使用Prometheus + Grafana：

```typescript
// metrics.service.ts
import { Counter, Histogram, register } from 'prom-client'

export const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code']
})

export const aiRequestTotal = new Counter({
  name: 'ai_requests_total',
  help: 'Total number of AI requests',
  labelNames: ['provider', 'model']
})
```

### 3. 健康检查

```typescript
// health.controller.ts
import { Controller, Get } from '@nestjs/common'
import { HealthCheck, HealthCheckService, TypeOrmHealthIndicator } from '@nestjs/terminus'

@Controller('health')
export class HealthController {
  constructor(
    private health: HealthCheckService,
    private db: TypeOrmHealthIndicator
  ) {}

  @Get()
  @HealthCheck()
  check() {
    return this.health.check([
      () => this.db.pingCheck('database')
    ])
  }
}
```

## 备份策略

### 1. 数据库备份

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/var/backups/ainotebook"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
pg_dump -U postgres -d ainotebook > $BACKUP_DIR/db_$DATE.sql

# 压缩备份
gzip $BACKUP_DIR/db_$DATE.sql

# 删除30天前的备份
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +30 -delete
```

### 2. 定时任务

```bash
# 添加到crontab
crontab -e

# 每天凌晨2点执行备份
0 2 * * * /var/www/ainotebook/scripts/backup.sh
```

## 安全加固

### 1. 防火墙配置

```bash
# UFW
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 2. Fail2Ban

```bash
sudo apt install fail2ban
```

配置 `/etc/fail2ban/jail.local`：

```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[nginx-http-auth]
enabled = true
```

## 故障排查

### 常见问题

1. **数据库连接失败**
   ```bash
   # 检查PostgreSQL状态
   sudo systemctl status postgresql

   # 查看日志
   sudo tail -f /var/log/postgresql/postgresql-15-main.log
   ```

2. **Redis连接失败**
   ```bash
   # 检查Redis状态
   sudo systemctl status redis

   # 测试连接
   redis-cli ping
   ```

3. **应用无法启动**
   ```bash
   # 查看PM2日志
   pm2 logs ainotebook-api

   # 查看系统日志
   sudo journalctl -u ainotebook -f
   ```

## 性能优化

### 应用层优化

#### 1. Node.js 集群模式

使用所有 CPU 核心：

```javascript
// cluster.ts
import cluster from 'cluster'
import os from 'os'

if (cluster.isPrimary) {
  const numCPUs = os.cpus().length

  console.log(`Master ${process.pid} is running`)
  console.log(`Forking ${numCPUs} workers...`)

  // Fork workers
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork()
  }

  // 重启崩溃的 worker
  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died`)
    cluster.fork()
  })
} else {
  // Worker 进程启动应用
  require('./dist/main.js')
}
```

#### 2. 内存管理

```typescript
// 内存限制配置
const MAX_MEMORY = 1024 * 1024 * 1024 // 1GB

// 定期检查内存使用
setInterval(() => {
  const used = process.memoryUsage()
  const usagePercent = (used.heapUsed / used.heapTotal) * 100

  if (usagePercent > 90) {
    logger.warn('High memory usage', {
      heapUsed: `${Math.round(used.heapUsed / 1024 / 1024)}MB`,
      heapTotal: `${Math.round(used.heapTotal / 1024 / 1024)}MB`,
      usagePercent: `${Math.round(usagePercent)}%`
    })

    // 触发 GC（仅在需要时）
    if (global.gc) {
      global.gc()
    }
  }
}, 60000) // 每分钟检查一次

// 流式处理大文件
import { createReadStream } from 'fs'
import { pipeline } from 'stream/promises'

async function processLargeFile(filePath: string) {
  const readStream = createReadStream(filePath)
  const transformStream = createTransformStream()
  const writeStream = createWriteStream('output.txt')

  await pipeline(readStream, transformStream, writeStream)
}
```

#### 3. 异步优化

```typescript
// 使用 Promise.all 并行处理
async function fetchArticleData(articleIds: string[]) {
  // ❌ 串行处理（慢）
  // for (const id of articleIds) {
  //   await processArticle(id)
  // }

  // ✅ 并行处理（快）
  const chunks = chunkArray(articleIds, 10) // 每次处理10个

  for (const chunk of chunks) {
    await Promise.all(chunk.map(id => processArticle(id)))
  }
}

// 使用 worker_threads 处理 CPU 密集型任务
import { Worker, isMainThread, parentPort, workerData } from 'worker_threads'

if (isMainThread) {
  // 主线程
  function processInWorker(data: any) {
    return new Promise((resolve, reject) => {
      const worker = new Worker(__filename, {
        workerData: data
      })

      worker.on('message', resolve)
      worker.on('error', reject)
      worker.on('exit', (code) => {
        if (code !== 0) reject(new Error(`Worker stopped with exit code ${code}`))
      })
    })
  }
} else {
  // Worker 线程执行 CPU 密集型任务
  const result = heavyComputation(workerData)
  parentPort.postMessage(result)
}
```

### 数据库优化

#### 1. 索引优化

```sql
-- 创建合适的索引
CREATE INDEX idx_articles_user_id ON articles(user_id);
CREATE INDEX idx_articles_created_at ON articles(created_at DESC);
CREATE INDEX idx_articles_status ON articles(status) WHERE status != 'deleted';

-- 复合索引（遵循最左前缀原则）
CREATE INDEX idx_articles_user_status_time ON articles(user_id, status, created_at DESC);

-- 部分索引（只索引活跃数据）
CREATE INDEX idx_active_articles ON articles(id, created_at)
WHERE status = 'active' AND deleted_at IS NULL;

-- 表达式索引
CREATE INDEX idx_articles_lower_title ON articles(LOWER(title));

-- 查看索引使用情况
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan as index_scans,
  idx_tup_read as tuples_read,
  idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- 查找未使用的索引
SELECT
  schemaname,
  tablename,
  indexname
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexname NOT LIKE '%_pkey';
```

#### 2. 查询优化

```typescript
// 使用查询优化器
import { Prisma } from '@prisma/client'

// ✅ 选择需要的字段（减少网络传输和内存）
const articles = await prisma.article.findMany({
  select: {
    id: true,
    title: true,
    createdAt: true
    // 不查询 content 等大字段
  },
  where: {
    status: 'published'
  },
  take: 20,
  orderBy: {
    createdAt: 'desc'
  }
})

// ✅ 使用游标分页（性能更好）
const articles = await prisma.article.findMany({
  take: 20,
  skip: 1, // 跳过游标本身
  cursor: {
    id: lastArticleId
  },
  orderBy: {
    id: 'asc'
  }
})

// ✅ 使用事务批量操作
await prisma.$transaction(async (tx) => {
  // 批量插入
  await tx.article.createMany({
    data: articles,
    skipDuplicates: true
  })

  // 批量更新
  await tx.article.updateMany({
    where: { status: 'draft' },
    data: { status: 'published' }
  })
})

// ❌ 避免 N+1 查询
const users = await prisma.user.findMany()
for (const user of users) {
  const articles = await prisma.article.findMany({
    where: { userId: user.id }
  })
}

// ✅ 使用 include 或 join
const users = await prisma.user.findMany({
  include: {
    articles: {
      take: 10,
      orderBy: { createdAt: 'desc' }
    }
  }
})
```

#### 3. 连接池优化

```typescript
// prisma.schema
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")

  // 连接池配置
  pool_timeout = 30         // 连接超时（秒）
  connection_limit = 20     // 最大连接数
}

// 环境变量
DATABASE_URL="postgresql://user:pass@localhost:5432/db?connection_limit=20&pool_timeout=30"

// 应用层连接池
import { Pool } from 'pg'

const pool = new Pool({
  host: 'localhost',
  port: 5432,
  database: 'ainotebook',
  user: 'postgres',
  password: 'password',
  max: 20,                          // 最大连接数
  min: 5,                           // 最小连接数
  idleTimeoutMillis: 30000,         // 空闲连接超时
  connectionTimeoutMillis: 2000,    // 连接超时
  statement_timeout: 10000          // 查询超时
})
```

#### 4. 慢查询优化

```sql
-- 启用慢查询日志
ALTER DATABASE ainotebook SET log_min_duration_statement = 1000; -- 1秒

-- 分析慢查询
SELECT
  query,
  calls,
  total_time,
  mean_time,
  max_time,
  stddev_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- 使用 EXPLAIN ANALYZE 分析查询计划
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT * FROM articles
WHERE user_id = 123
  AND status = 'published'
ORDER BY created_at DESC
LIMIT 20;

-- 优化示例：添加索引后的查询计划
-- 如果出现 Seq Scan（全表扫描），考虑添加索引
-- 如果出现 Nested Loop，考虑优化 join 顺序
```

### 缓存策略

#### 1. 多级缓存

```typescript
// cache.service.ts
import Redis from 'ioredis'

class CacheService {
  private redis: Redis
  private localCache: Map<string, { value: any, expires: number }>

  constructor() {
    this.redis = new Redis(process.env.REDIS_URL)
    this.localCache = new Map()
  }

  // 多级缓存：本地 -> Redis -> 数据库
  async get<T>(key: string): Promise<T | null> {
    // L1: 本地缓存
    const local = this.localCache.get(key)
    if (local && local.expires > Date.now()) {
      return local.value as T
    }

    // L2: Redis 缓存
    const cached = await this.redis.get(key)
    if (cached) {
      const value = JSON.parse(cached)
      // 回写到本地缓存
      this.localCache.set(key, {
        value,
        expires: Date.now() + 60000 // 本地缓存1分钟
      })
      return value as T
    }

    return null
  }

  async set(key: string, value: any, ttl: number = 3600): Promise<void> {
    // 写入 Redis
    await this.redis.setex(key, ttl, JSON.stringify(value))

    // 写入本地缓存
    this.localCache.set(key, {
      value,
      expires: Date.now() + Math.min(ttl * 1000, 60000)
    })
  }

  async invalidate(pattern: string): Promise<void> {
    // 清除本地缓存
    for (const key of this.localCache.keys()) {
      if (key.match(pattern)) {
        this.localCache.delete(key)
      }
    }

    // 清除 Redis 缓存
    const keys = await this.redis.keys(pattern)
    if (keys.length > 0) {
      await this.redis.del(...keys)
    }
  }
}
```

#### 2. 缓存预热

```typescript
// cache-warmup.service.ts
class CacheWarmupService {
  async warmupPopularArticles() {
    // 预热热门文章
    const popularArticles = await prisma.article.findMany({
      where: { status: 'published' },
      orderBy: { views: 'desc' },
      take: 100
    })

    for (const article of popularArticles) {
      const key = `article:${article.id}`
      await cacheService.set(key, article, 3600) // 缓存1小时
    }
  }

  async warmupUserData() {
    // 预热活跃用户数据
    const activeUsers = await prisma.user.findMany({
      where: {
        lastLoginAt: {
          gte: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000) // 7天内登录
        }
      },
      take: 1000
    })

    for (const user of activeUsers) {
      const key = `user:${user.id}`
      await cacheService.set(key, user, 1800) // 缓存30分钟
    }
  }
}

// 在应用启动时预热
async function bootstrap() {
  logger.info('Starting cache warmup...')
  await warmupService.warmupPopularArticles()
  await warmupService.warmupUserData()
  logger.info('Cache warmup completed')
}
```

#### 3. 缓存更新策略

```typescript
// Cache-Aside Pattern（懒加载）
async function getArticle(id: string) {
  const key = `article:${id}`

  // 1. 先查缓存
  let article = await cacheService.get(key)
  if (article) {
    return article
  }

  // 2. 缓存未命中，查数据库
  article = await prisma.article.findUnique({ where: { id } })
  if (!article) {
    return null
  }

  // 3. 写入缓存
  await cacheService.set(key, article, 3600)

  return article
}

// Write-Through Pattern（写穿透）
async function updateArticle(id: string, data: any) {
  // 1. 更新数据库
  const article = await prisma.article.update({
    where: { id },
    data
  })

  // 2. 同步更新缓存
  const key = `article:${id}`
  await cacheService.set(key, article, 3600)

  return article
}

// Write-Behind Pattern（写回/异步写）
async function incrementViews(id: string) {
  const key = `article:views:${id}`

  // 1. 只更新缓存（快速）
  await cacheService.incr(key)

  // 2. 异步批量写入数据库
  await queueService.add('update-views', { articleId: id })
}

// 定时批量更新（每分钟）
cron.schedule('* * * * *', async () => {
  const jobs = await queueService.getJobs('update-views', 100)

  const updates = new Map<string, number>()
  for (const job of jobs) {
    const { articleId } = job.data
    updates.set(articleId, (updates.get(articleId) || 0) + 1)
  }

  // 批量更新数据库
  for (const [articleId, count] of updates) {
    await prisma.article.update({
      where: { id: articleId },
      data: { views: { increment: count } }
    })
  }
})
```

#### 4. 缓存问题处理

```typescript
// 缓存穿透（查询不存在的数据）
async function getArticleWithLock(id: string) {
  const key = `article:${id}`

  // 使用布隆过滤器
  const exists = await bloomFilter.exists(id)
  if (!exists) {
    return null // 提前返回，避免查询数据库
  }

  // 查询缓存
  let article = await cacheService.get(key)

  if (article === null) {
    // 使用分布式锁防止缓存击穿
    const lockKey = `lock:${key}`
    const lock = await redis.set(lockKey, '1', 'NX', 'EX', 10) // 10秒锁

    if (lock === 'OK') {
      try {
        // 再次查询缓存（双重检查）
        article = await cacheService.get(key)
        if (article) {
          return article
        }

        // 查询数据库
        article = await prisma.article.findUnique({ where: { id } })

        if (article) {
          await cacheService.set(key, article, 3600)
        } else {
          // 缓存空值，防止穿透
          await cacheService.set(key, null, 60) // 短时间缓存
        }
      } finally {
        // 释放锁
        await redis.del(lockKey)
      }
    } else {
      // 等待其他进程重建缓存
      await sleep(100)
      return getArticleWithLock(id)
    }
  }

  return article
}

// 缓存雪崩（大量缓存同时失效）
async function getArticleWithRandomExpiry(id: string) {
  const key = `article:${id}`

  let article = await cacheService.get(key)

  if (!article) {
    article = await prisma.article.findUnique({ where: { id } })

    if (article) {
      // 添加随机过期时间，防止雪崩
      const randomExpiry = 3600 + Math.random() * 600 // 3600-4200秒
      await cacheService.set(key, article, randomExpiry)
    }
  }

  return article
}
```

### 前端优化

#### 1. 资源压缩

```nginx
# Nginx Gzip 压缩
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_comp_level 6;
gzip_types
  text/plain
  text/css
  text/xml
  text/javascript
  application/json
  application/javascript
  application/xml+rss
  application/rss+xml
  application/atom+xml
  image/svg+xml
  text/x-component
  text/x-cross-domain-policy;

# Brotli 压缩（更好的压缩率）
brotli on;
brotli_comp_level 6;
brotli_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript image/svg+xml;
```

```javascript
// vite.config.ts / next.config.js
export default {
  // 压缩配置
  compress: {
    gzip: true,
    brotli: true
  }
}
```

#### 2. 代码分割和懒加载

```typescript
// 路由级别代码分割
import { lazy, Suspense } from 'react'

const Dashboard = lazy(() => import('./pages/Dashboard'))
const ArticleEditor = lazy(() => import('./pages/ArticleEditor'))

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/editor" element={<ArticleEditor />} />
      </Routes>
    </Suspense>
  )
}

// 组件级别懒加载
const HeavyComponent = lazy(() => import('./components/HeavyComponent'))

function ArticlePage() {
  const [showDetails, setShowDetails] = useState(false)

  return (
    <div>
      <h1>Article Title</h1>

      {showDetails && (
        <Suspense fallback={<Skeleton />}>
          <HeavyComponent />
        </Suspense>
      )}

      <button onClick={() => setShowDetails(true)}>
        Show Details
      </button>
    </div>
  )
}

// 动态导入（按需加载）
async function loadMarkdownParser() {
  const { parse } = await import('markdown-parser')
  return parse
}
```

#### 3. 图片优化

```typescript
// 使用 Next.js Image 组件
import Image from 'next/image'

function ArticleImage({ src, alt }) {
  return (
    <Image
      src={src}
      alt={alt}
      width={800}
      height={600}
      placeholder="blur"
      loading="lazy"
      sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
    />
  )
}

// 响应式图片
function ResponsiveImage() {
  return (
    <picture>
      <source media="(min-width: 1024px)" srcSet="image-large.webp" />
      <source media="(min-width: 768px)" srcSet="image-medium.webp" />
      <source media="(min-width: 480px)" srcSet="image-small.webp" />
      <img src="image-fallback.jpg" alt="Description" loading="lazy" />
    </picture>
  )
}
```

#### 4. CDN 配置

```nginx
# 静态资源 CDN 缓存
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
  expires 1y;
  add_header Cache-Control "public, immutable";

  # 如果使用 CDN
  # proxy_pass https://your-cdn.example.com;
}

# 上传到 CDN
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3'

const s3 = new S3Client({
  region: 'us-east-1',
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
  }
})

async function uploadToCDN(file: Buffer, key: string) {
  const command = new PutObjectCommand({
    Bucket: 'your-cdn-bucket',
    Key: key,
    Body: file,
    CacheControl: 'public, max-age=31536000', // 1年
    ContentType: 'application/javascript'
  })

  await s3.send(command)

  return `https://cdn.example.com/${key}`
}
```

### 负载均衡

#### 1. Nginx 负载均衡

```nginx
# 定义后端服务器组
upstream backend_servers {
  # 负载均衡算法
  least_conn;  # 最少连接

  server backend1:3000 weight=3 max_fails=3 fail_timeout=30s;
  server backend2:3000 weight=2 max_fails=3 fail_timeout=30s;
  server backend3:3000 weight=1 max_fails=3 fail_timeout=30s backup;  # 备用服务器

  # 健康检查
  check interval=3000 rise=2 fall=3 timeout=1000;
}

server {
  listen 80;

  location /api {
    proxy_pass http://backend_servers;

    # 健康检查端点
    proxy_next_upstream error timeout http_502 http_503 http_504;
    proxy_next_upstream_tries 2;
  }

  # 健康检查接口
  location /health {
    access_log off;
    proxy_pass http://backend_servers/health;
  }
}
```

#### 2. 会话保持

```nginx
upstream backend_servers {
  # IP 哈希（同一 IP 分配到同一服务器）
  ip_hash;

  server backend1:3000;
  server backend2:3000;

  # 或使用 sticky cookie
  sticky cookie srv_id expires=1h domain=.example.com path=/;
}
```

### 消息队列优化

#### 1. 任务批处理

```typescript
// 批量处理任务
import { Queue, Worker, Job } from 'bullmq'

const articleQueue = new Queue('article-processing', {
  connection: { host: 'localhost', port: 6379 }
})

// 批量添加任务
async function batchAddJobs(jobs: any[]) {
  const batch = jobs.map(job => ({
    name: 'process-article',
    data: job,
    opts: {
      attempts: 3,
      backoff: {
        type: 'exponential',
        delay: 2000
      }
    }
  }))

  await articleQueue.addBulk(batch)
}

// 批量处理 Worker
const worker = new Worker('article-processing',
  async (job: Job) => {
    // 处理逻辑
    await processArticle(job.data)
  },
  {
    connection: { host: 'localhost', port: 6379 },
    concurrency: 10,  // 并发处理10个任务
    limiter: {
      max: 100,      // 每分钟最多100个
      duration: 60000
    }
  }
)
```

#### 2. 优先级队列

```typescript
// 高优先级任务（付费用户）
await highPriorityQueue.add('process-article', data, {
  priority: 1  // 数字越小优先级越高
})

// 普通任务
await normalQueue.add('process-article', data, {
  priority: 5
})

// 低优先级任务（批量处理）
await lowPriorityQueue.add('process-article', data, {
  priority: 10
})
```

### 性能监控

```typescript
// 性能监控中间件
import { performance } from 'perf_hooks'

export function performanceMonitor(req: Request, res: Response, next: NextFunction) {
  const start = performance.now()

  res.on('finish', () => {
    const duration = performance.now() - start

    // 记录慢请求
    if (duration > 1000) {
      logger.warn('Slow request detected', {
        url: req.url,
        method: req.method,
        duration: `${duration.toFixed(2)}ms`,
        userAgent: req.headers['user-agent']
      })
    }

    // 发送到监控系统
    metricsService.recordHttpRequest({
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration
    })
  })

  next()
}
```

详细监控指南请查看 [监控日志](/guide/monitoring)
