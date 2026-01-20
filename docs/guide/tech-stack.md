# 技术栈详解

本文档详细说明AI-NoteBook项目使用的所有技术选型及其原因。

## 前端技术栈

### 核心框架

#### Vue 3.4+

**选择理由**：
- **Composition API**: 更好的逻辑复用和代码组织
- **性能提升**: 相比Vue 2，性能提升40%+
- **TypeScript支持**: 原生TS支持，类型推断更准确
- **生态成熟**: 丰富的插件和工具链

**关键特性**：
```typescript
// Composition API示例
import { ref, computed, onMounted } from 'vue'

export default {
  setup() {
    const content = ref('')
    const isAnalyzing = computed(() => !content.value)

    onMounted(() => {
      // 初始化逻辑
    })

    return { content, isAnalyzing }
  }
}
```

#### TypeScript 5.0+

**选择理由**：
- **类型安全**: 编译时错误检测，减少运行时bug
- **IDE支持**: 更好的智能提示和重构
- **代码可维护性**: 大型项目的必备工具
- **渐进式**: 可选的静态类型，不影响JS代码

**配置示例**：
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "jsx": "preserve",
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

#### Vite 5.0+

**选择理由**：
- **极速冷启动**: 基于ESM，无需打包即可启动
- **即时热更新**: 比Webpack快10-100倍
- **原生支持**: 无需配置，开箱即用
- **生态丰富**: 丰富的插件生态

**配置示例**：
```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true
      }
    }
  },
  build: {
    target: 'es2015',
    outDir: 'dist',
    sourcemap: false,
    chunkSizeWarningLimit: 1500
  }
})
```

### UI组件库

#### Naive UI

**选择理由**：
- **设计现代**: 符合现代设计规范
- **类型完整**: 完整的TypeScript支持
- **主题定制**: 灵活的主题系统
- **无依赖**: 不依赖其他UI库
- **文档友好**: 清晰的文档和示例

**核心组件使用**：
```vue
<template>
  <n-space vertical>
    <n-input
      v-model:value="content"
      type="textarea"
      placeholder="请粘贴文章内容..."
      :rows="10"
    />
    <n-button
      type="primary"
      :loading="isAnalyzing"
      @click="analyze"
    >
      开始解析
    </n-button>
  </n-space>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { NInput, NButton, NSpace } from 'naive-ui'

const content = ref('')
const isAnalyzing = ref(false)
</script>
```

#### 其他UI方案对比

| 特性 | Naive UI | Element Plus | Ant Design Vue |
|-----|----------|--------------|----------------|
| TypeScript支持 | ✅ 完整 | ✅ 完整 | ✅ 完整 |
| 主题定制 | ✅ 灵活 | ✅ 支持 | ✅ 支持 |
| 组件丰富度 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Bundle大小 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 设计感 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

### 状态管理

#### Pinia

**选择理由**：
- **Vue 3官方推荐**: 将替代Vuex
- **类型安全**: 完整的TypeScript支持
- **极简API**: 比Vuex更简洁
- **DevTools**: 完美的开发工具集成
- **模块化**: 天然支持模块化

**使用示例**：
```typescript
// stores/user.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const apiKey = ref('')
  const membership = ref<Membership>(Membership.FREE)

  const isLoggedIn = computed(() => !!user.value)
  const maxConcurrent = computed(() => {
    switch (membership.value) {
      case Membership.FREE: return 1
      case Membership.PRO: return 5
      case Membership.ENTERPRISE: return 20
    }
  })

  function setUserData(data: User) {
    user.value = data
    apiKey.value = data.apiKey
    membership.value = data.membership
  }

  function clearUserData() {
    user.value = null
    apiKey.value = ''
    membership.value = Membership.FREE
  }

  return {
    user,
    apiKey,
    membership,
    isLoggedIn,
    maxConcurrent,
    setUserData,
    clearUserData
  }
})
```

### 路由管理

#### Vue Router 4.x

**选择理由**：
- **Vue 3官方路由**: 完美集成
- **类型安全**: 完整的TypeScript支持
- **动态路由**: 支持路由懒加载
- **导航守卫**: 灵活的权限控制

**配置示例**：
```typescript
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/analyze',
    name: 'Analyze',
    component: () => import('@/views/Analyze.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/history',
    name: 'History',
    component: () => import('@/views/History.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 导航守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router
```

### HTTP客户端

#### Axios

**选择理由**：
- **功能强大**: 拦截器、超时、取消请求
- **浏览器兼容**: 支持老版本浏览器
- **Promise API**: 现代化的异步处理
- **生态成熟**: 丰富的插件和解决方案

**配置示例**：
```typescript
import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig } from 'axios'

const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器：自动注入API Key
api.interceptors.request.use(
  (config) => {
    const apiKey = localStorage.getItem('apiKey')
    if (apiKey) {
      config.headers['X-API-Key'] = apiKey
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截器：统一错误处理
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      // API Key失效，跳转登录
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
```

### Markdown处理

#### Vditor (编辑器)

**选择理由**：
- **功能丰富**: 所见即所得、即时渲染、分屏预览
- **性能优秀**: 虚拟滚动，大文件处理流畅
- **可扩展**: 丰富的插件系统
- **中文友好**: 国产开源，中文支持完美

**使用示例**：
```vue
<template>
  <Vditor
    v-model="content"
    :height="500"
    :toolbar="toolbar"
    :mode="mode"
    @after="onAfter"
  />
</template>

<script setup lang="ts">
import Vditor from 'vditor'
import 'vditor/dist/index.css'

const content = ref('')
const mode = 'wysiwyg'
const toolbar = [
  'headings', 'bold', 'italic', 'strike',
  '|', 'list', 'ordered-list', 'check',
  '|', 'code', 'inline-code', 'link'
]

const onAfter = () => {
  console.log('编辑器初始化完成')
}
</script>
```

#### markdown-it (渲染器)

**选择理由**：
- **性能卓越**: 最快的Markdown解析器之一
- **可扩展**: 丰富的插件生态
- **CommonMark兼容**: 严格遵循标准
- **安全可靠**: XSS防护

**配置示例**：
```typescript
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'

const md = new MarkdownIt({
  html: true,        // 允许HTML标签
  linkify: true,     // 自动转换URL为链接
  typographer: true, // 启用排版优化
  highlight: (str, lang) => {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(str, { language: lang }).value
      } catch (__) {}
    }
    return ''
  }
})

// 使用插件
import markdownItAnchor from 'markdown-it-anchor'
md.use(markdownItAnchor, {
  permalink: markdownItAnchor.permalink.linkInsideHeader({
    symbol: '#',
    placement: 'before'
  })
})

export default md
```

#### highlight.js (代码高亮)

**选择理由**：
- **语言丰富**: 支持190+种编程语言
- **性能优秀**: 快速高亮
- **主题丰富**: 多种主题可选
- **自动检测**: 可自动识别语言

### 文档导出

#### html2pdf.js (PDF导出)

**选择理由**：
- **简单易用**: API简洁
- **格式保留**: 保留原始样式
- **纯前端**: 无需后端支持

**使用示例**：
```typescript
import html2pdf from 'html2pdf.js'

function exportToPDF(element: HTMLElement, filename: string) {
  const opt = {
    margin: [10, 10],
    filename: `${filename}.pdf`,
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
  }

  html2pdf().set(opt).from(element).save()
}
```

#### docx (Word导出)

**选择理由**：
- **功能完整**: 支持复杂格式
- **纯前端**: 无需后端支持
- **TypeScript支持**: 类型完整

**使用示例**：
```typescript
import { Document, Packer, Paragraph, TextRun } from 'docx'
import { saveAs } from 'file-saver'

async function exportToWord(content: string, filename: string) {
  const doc = new Document({
    sections: [{
      properties: {},
      children: [
        new Paragraph({
          children: [
            new TextRun({
              text: content,
              bold: false
            })
          ]
        })
      ]
    }]
  })

  const blob = await Packer.toBlob(doc)
  saveAs(blob, `${filename}.docx`)
}
```

## 后端技术栈

### 核心框架

#### NestJS 10.x

**选择理由**：
- **企业级框架**: 适合大型项目
- **TypeScript原生**: 完整的类型支持
- **模块化架构**: 代码组织清晰
- **依赖注入**: 松耦合设计
- **装饰器语法**: 优雅的API设计
- **生态丰富**: 官方和社区支持完善

**核心特性**：
```typescript
// Controller示例
import { Controller, Get, Post, Body, UseGuards } from '@nestjs/common'
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger'
import { JwtAuthGuard } from '@/auth/guards/jwt-auth.guard'
import { AnalysisService } from './analysis.service'

@ApiTags('文章解析')
@Controller('analysis')
export class AnalysisController {
  constructor(private readonly analysisService: AnalysisService) {}

  @Post()
  @ApiOperation({ summary: '创建解析任务' })
  @ApiBearerAuth()
  @UseGuards(JwtAuthGuard)
  async create(@Body() dto: AnalyzeDto) {
    return this.analysisService.create(dto)
  }

  @Get(':id')
  @ApiOperation({ summary: '获取解析结果' })
  @ApiBearerAuth()
  @UseGuards(JwtAuthGuard)
  async findOne(@Param('id') id: string) {
    return this.analysisService.findOne(id)
  }
}
```

#### Node.js 20.x

**选择理由**：
- **LTS版本**: 长期支持，稳定可靠
- **性能提升**: V8引擎持续优化
- **ESM支持**: 原生ES模块
- **内置工具**: 丰富的内置API

### ORM框架

#### Prisma

**选择理由**：
- **类型安全**: 自动生成TypeScript类型
- **迁移友好**: 声明式迁移系统
- **开发体验**: 优秀的IDE支持
- **性能优秀**: 查询优化和连接池
- **多数据库**: PostgreSQL、MySQL、SQLite等

**配置示例**：
```prisma
// prisma/schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id         String   @id @default(uuid())
  email      String   @unique
  password   String
  username   String?
  apiKey     String?  @unique
  membership Membership @default(FREE)
  balance    Decimal  @default(0)
  analyses   Analysis[]
  orders     Order[]
  createdAt  DateTime @default(now())
  updatedAt  DateTime @updatedAt
}

enum Membership {
  FREE
  PRO
  ENTERPRISE
}
```

**使用示例**：
```typescript
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

// 查询
const user = await prisma.user.findUnique({
  where: { email: 'user@example.com' },
  include: { analyses: true }
})

// 创建
const newUser = await prisma.user.create({
  data: {
    email: 'user@example.com',
    password: hashedPassword,
    membership: Membership.FREE
  }
})

// 更新
const updated = await prisma.user.update({
  where: { id: userId },
  data: { membership: Membership.PRO }
})
```

### 数据库

#### PostgreSQL 15+

**选择理由**：
- **功能强大**: 支持复杂查询、JSON、全文搜索
- **可靠性**: ACID事务保证
- **扩展性**: 丰富的扩展和索引类型
- **开源免费**: 无厂商锁定
- **社区活跃**: 活跃的社区支持

**关键特性**：
```sql
-- 全文搜索
SELECT * FROM articles
WHERE to_tsvector('chinese', content) @@ to_tsquery('关键词');

-- JSON查询
SELECT * FROM analyses
WHERE expansions->>'key' = 'value';

-- 窗口函数
SELECT
  id,
  created_at,
  LAG(created_at) OVER (PARTITION BY user_id ORDER BY created_at) as prev_time
FROM analyses;
```

### 缓存

#### Redis 7.x

**选择理由**：
- **性能优秀**: 内存存储，极快的读写速度
- **数据结构丰富**: String、List、Set、Hash、ZSet
- **持久化**: RDB和AOF两种方式
- **分布式**: 原生支持集群、哨兵
- **用途广泛**: 缓存、队列、计数器、Session

**使用场景**：
```typescript
// 缓存热点数据
await redis.setex(`user:${userId}`, 3600, JSON.stringify(user))

// 任务队列
await queue.add('analyze', { userId, content })

// 计数器
await redis.incr(`api_calls:${userId}:${date}`)
await redis.expire(`api_calls:${userId}:${date}`, 86400)

// Session存储
await redis.setex(`session:${sessionId}`, 604800, JSON.stringify(sessionData))
```

### 任务队列

#### BullMQ

**选择理由**：
- **基于Redis**: 无需额外依赖
- **类型安全**: 完整的TypeScript支持
- **功能丰富**: 优先级、延迟、重试、并发控制
- **可视化**: Bull Board监控面板
- **可靠性**: 消息持久化，不丢失

**使用示例**：
```typescript
import { Queue, Worker } from 'bullmq'

// 创建队列
export const analysisQueue = new Queue('analysis', {
  connection: { host: 'localhost', port: 6379 }
})

// 添加任务
await analysisQueue.add('analyze-article', {
  userId: 'xxx',
  content: '...'
}, {
  priority: 1,
  attempts: 3,
  backoff: { type: 'exponential', delay: 2000 }
})

// 创建Worker
const worker = new Worker('analysis', async (job) => {
  const { userId, content } = job.data

  // 处理逻辑
  const result = await analyzeContent(content)

  // 保存结果
  await saveResult(userId, result)

  return result
}, {
  connection: { host: 'localhost', port: 6379 },
  concurrency: 5
})
```

### 认证鉴权

#### JWT (@nestjs/jwt)

**选择理由**：
- **无状态**: 不需要服务器存储Session
- **跨域友好**: 适合分布式系统
- **性能好**: 避免数据库查询
- **标准化**: 通用标准

**使用示例**：
```typescript
import { JwtService } from '@nestjs/jwt'

@Injectable()
export class AuthService {
  constructor(private jwtService: JwtService) {}

  async login(user: User) {
    const payload = {
      sub: user.id,
      email: user.email,
      membership: user.membership
    }

    return {
      access_token: this.jwtService.sign(payload, {
        expiresIn: '15m'
      }),
      refresh_token: this.jwtService.sign(payload, {
        secret: process.env.JWT_REFRESH_SECRET,
        expiresIn: '7d'
      })
    }
  }
}
```

#### Passport (@nestjs/passport)

**选择理由**：
- **灵活**: 支持多种认证策略
- **中间件**: Express风格的中间件
- **社区成熟**: 500+种策略
- **官方支持**: NestJS官方集成

**自定义Guard示例**：
```typescript
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common'
import { Reflector } from '@nestjs/core'

@Injectable()
export class MembershipGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredMembership = this.reflector.get<Membership>(
      'membership',
      context.getHandler()
    )

    if (!requiredMembership) {
      return true
    }

    const request = context.switchToHttp().getRequest()
    const user = request.user

    return this.checkMembership(user.membership, requiredMembership)
  }

  private checkMembership(
    userMembership: Membership,
    required: Membership
  ): boolean {
    const levels = { FREE: 1, PRO: 2, ENTERPRISE: 3 }
    return levels[userMembership] >= levels[required]
  }
}
```

### API文档

#### Swagger (@nestjs/swagger)

**选择理由**：
- **自动生成**: 基于装饰器自动生成文档
- **交互式**: 在线测试API
- **标准化**: OpenAPI 3.0规范
- **类型安全**: TypeScript集成

**配置示例**：
```typescript
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger'

async function bootstrap() {
  const app = await NestFactory.create(AppModule)

  const config = new DocumentBuilder()
    .setTitle('AI-NoteBook API')
    .setDescription('AI驱动的内容分析系统API文档')
    .setVersion('1.0')
    .addBearerAuth()
    .addTag('auth', '认证相关')
    .addTag('analysis', '文章解析')
    .build()

  const document = SwaggerModule.createDocument(app, config)
  SwaggerModule.setup('api-docs', app, document)

  await app.listen(3000)
}
```

### 日志系统

#### Winston

**选择理由**：
- **功能强大**: 多传输、多格式
- **灵活**: 可自定义日志格式
- **生产级**: 大型项目验证
- **生态丰富**: 丰富的Transport

**配置示例**：
```typescript
import * as winston from 'winston'

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.splat(),
    winston.format.json()
  ),
  defaultMeta: { service: 'ai-notebook' },
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
})

if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple()
  }))
}
```

### 文件处理

#### Multer

**选择理由**：
- **Express官方**: 官方推荐
- ** multipart/form-data**: 处理文件上传
- **内存存储**: 支持内存和磁盘存储
- **灵活性**: 可自定义存储策略

**配置示例**：
```typescript
import { MulterModule } from '@nestjs/platform-express'
import { memoryStorage } from 'multer'

MulterModule.register({
  storage: memoryStorage(),
  limits: {
    fileSize: 5 * 1024 * 1024, // 5MB
    files: 10
  },
  fileFilter: (req, file, cb) => {
    if (file.mimetype.match(/\/(md|txt)$/)) {
      cb(null, true)
    } else {
      cb(new Error('只支持.md和.txt文件'), false)
    }
  }
})
```

## AI集成

### Volcengine ARK

**选择理由**：
- **国产模型**: GLM-4.7、Doubao等
- **响应速度快**: 国内部署延迟低
- **中文优化**: 中文理解能力强
- **性价比高**: 价格相对便宜

**使用示例**：
```typescript
import { Ark } from '@volcengine/ark'

const client = new Ark({
  apiKey: process.env.ARK_API_KEY
})

async function analyzeContent(content: string) {
  const response = await client.chat.completions.create({
    model: 'glm-4.7',
    messages: [{
      role: 'user',
      content: `请分析以下文章的易读性：\n\n${content}`
    }],
    temperature: 0.7,
    max_tokens: 2000
  })

  return response.choices[0].message.content
}
```

### OpenAI兼容接口

**选择理由**：
- **标准化**: 通用API协议
- **多模型支持**: 可切换不同模型
- **生态成熟**: 丰富的SDK和工具

**使用示例**：
```typescript
import OpenAI from 'openai'

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: process.env.OPENAI_BASE_URL
})

async function refineContent(content: string) {
  const response = await client.chat.completions.create({
    model: 'gpt-4',
    messages: [{
      role: 'system',
      content: '你是一个专业的内容提炼专家...'
    }, {
      role: 'user',
      content: `请提炼以下文章的核心内容：\n\n${content}`
    }]
  })

  return response.choices[0].message.content
}
```

## 支付集成

### 支付宝

**选择理由**：
- **用户基数大**: 国内主流支付方式
- **文档完善**: 官方SDK和文档
- **安全可靠**: 官方支持

### 微信支付

**选择理由**：
- **用户基数大**: 微信生态
- **便捷支付**: 扫码支付、H5支付
- **官方SDK**: 完善的Node.js SDK

## 开发工具

### 代码质量

```json
{
  "scripts": {
    "lint": "eslint . --ext .ts,.vue",
    "format": "prettier --write .",
    "type-check": "tsc --noEmit"
  }
}
```

### Git Hooks

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# 前端
cd frontend
npm run lint
npm run type-check

# 后端
cd ../backend
npm run lint
npm run type-check
npm run test
```

详细设计请查看其他文档：
- [数据库设计](/guide/database)
- [API文档](/guide/api)
- [认证鉴权](/guide/authentication)
