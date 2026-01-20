# API文档

本文档详细说明AI-NoteBook系统的RESTful API设计。

## 基础信息

### Base URL

```
开发环境: http://localhost:3000/api
生产环境: https://api.ainotebook.com/api
```

### 认证方式

#### 1. JWT Token认证

用于前端用户认证：

```http
Authorization: Bearer <jwt_token>
```

#### 2. API Key认证

用于浏览器扩展和第三方应用：

```http
X-API-Key: <api_key>
```

### 响应格式

#### 成功响应

```json
{
  "success": true,
  "data": {},
  "message": "操作成功"
}
```

#### 错误响应

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "错误信息",
    "details": {}
  }
}
```

### HTTP状态码

| 状态码 | 说明 |
|-------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 429 | 请求过于频繁 |
| 500 | 服务器内部错误 |

## 认证模块

### 注册

```http
POST /api/auth/register
```

**请求参数**：

```json
{
  "email": "user@example.com",
  "password": "password123",
  "username": "昵称（可选）"
}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "username": "昵称",
      "membership": "FREE",
      "apiKey": "uuid"
    },
    "tokens": {
      "accessToken": "jwt_token",
      "refreshToken": "refresh_token"
    }
  }
}
```

### 登录

```http
POST /api/auth/login
```

**请求参数**：

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "membership": "PRO"
    },
    "tokens": {
      "accessToken": "jwt_token",
      "refreshToken": "refresh_token"
    }
  }
}
```

### 刷新Token

```http
POST /api/auth/refresh
```

**请求参数**：

```json
{
  "refreshToken": "refresh_token"
}
```

### 生成API Key

```http
POST /api/auth/api-key
Authorization: Bearer <jwt_token>
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "apiKey": "uuid-string"
  }
}
```

## 文章解析模块

### 创建解析任务

```http
POST /api/analysis
Authorization: Bearer <jwt_token>
```

**请求参数**：

```json
{
  "content": "# 文章标题\n\n文章内容...",
  "title": "文章标题（可选）",
  "enableExpansion": true
}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "taskId": "uuid",
    "status": "PROCESSING",
    "estimatedTime": 30
  }
}
```

### 批量解析

```http
POST /api/analysis/batch
Authorization: Bearer <jwt_token>
```

**请求参数**：

```json
{
  "articles": [
    {
      "content": "文章1内容...",
      "title": "标题1"
    },
    {
      "content": "文章2内容...",
      "title": "标题2"
    }
  ]
}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "batchId": "uuid",
    "taskIds": ["uuid1", "uuid2"],
    "total": 2,
    "status": "PROCESSING"
  }
}
```

### 获取解析结果

```http
GET /api/analysis/:id
Authorization: Bearer <jwt_token>
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "title": "文章标题",
    "originalContent": "...",
    "processedContent": "...",
    "readabilityScore": {
      "overall": 3,
      "vocabulary": 3,
      "sentence": 2,
      "logic": 4,
      "comment": "适合有一定技术背景的读者"
    },
    "expansions": [
      {
        "keyPoint": "重点内容",
        "expansion": "扩展说明",
        "sources": ["url1", "url2"]
      }
    ],
    "sources": [
      {
        "title": "来源标题",
        "url": "https://example.com",
        "snippet": "相关片段"
      }
    ],
    "status": "COMPLETED",
    "createdAt": "2026-01-20T10:00:00Z"
  }
}
```

### 获取解析历史

```http
GET /api/analysis/history?page=1&limit=20&status=COMPLETED
Authorization: Bearer <jwt_token>
```

**查询参数**：

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| page | number | 否 | 页码，默认1 |
| limit | number | 否 | 每页数量，默认20 |
| status | string | 否 | 状态筛选 |
| sortBy | string | 否 | 排序字段，默认createdAt |
| order | string | 否 | 排序方向，asc/desc，默认desc |

**响应示例**：

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "uuid",
        "title": "文章标题",
        "readabilityScore": 3,
        "status": "COMPLETED",
        "createdAt": "2026-01-20T10:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100,
      "totalPages": 5
    }
  }
}
```

### 删除解析记录

```http
DELETE /api/analysis/:id
Authorization: Bearer <jwt_token>
```

## 支付模块

### 创建订单

```http
POST /api/payment/order
Authorization: Bearer <jwt_token>
```

**请求参数**：

```json
{
  "membership": "PRO",
  "duration": 30,
  "paymentMethod": "ALIPAY"
}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "orderId": "uuid",
    "orderNo": "AIN20260120123456",
    "amount": 29.00,
    "paymentUrl": "https://openapi.alipay.com/..."
  }
}
```

### 查询订单状态

```http
GET /api/payment/order/:id
Authorization: Bearer <jwt_token>
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "orderNo": "AIN20260120123456",
    "amount": 29.00,
    "status": "PAID",
    "membership": "PRO",
    "duration": 30,
    "paidAt": "2026-01-20T10:00:00Z"
  }
}
```

### 支付回调

```http
POST /api/payment/callback/alipay
```

**请求参数**（由支付宝平台发起）：

```json
{
  "trade_no": "支付宝交易号",
  "out_trade_no": "商户订单号",
  "trade_status": "TRADE_SUCCESS"
}
```

## 用户模块

### 获取用户信息

```http
GET /api/user/me
Authorization: Bearer <jwt_token>
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "username": "昵称",
    "membership": "PRO",
    "balance": 100.50,
    "apiKey": "uuid",
    "stats": {
      "totalAnalyses": 50,
      "completedAnalyses": 48,
      "failedAnalyses": 2
    }
  }
}
```

### 更新用户信息

```http
PATCH /api/user/me
Authorization: Bearer <jwt_token>
```

**请求参数**：

```json
{
  "username": "新昵称"
}
```

### 修改密码

```http
POST /api/user/change-password
Authorization: Bearer <jwt_token>
```

**请求参数**：

```json
{
  "oldPassword": "old_password",
  "newPassword": "new_password"
}
```

### 获取会员套餐

```http
GET /api/user/membership-plans
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "plans": [
      {
        "name": "PRO",
        "displayName": "专业版",
        "price": 29,
        "duration": 30,
        "features": [
          "5篇并发解析",
          "1000篇存储空间",
          "优先处理"
        ]
      },
      {
        "name": "ENTERPRISE",
        "displayName": "企业版",
        "price": 199,
        "duration": 30,
        "features": [
          "20篇并发解析",
          "无限存储空间",
          "专属客服",
          "API调用额度提升"
        ]
      }
    ]
  }
}
```

## 统计模块

### 获取使用统计

```http
GET /api/stats/overview
Authorization: Bearer <jwt_token>
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "todayAnalyses": 5,
    "monthAnalyses": 120,
    "totalAnalyses": 1500,
    "avgReadabilityScore": 3.2,
    "membershipExpiry": "2026-02-20T00:00:00Z"
  }
}
```

### 获取API调用统计

```http
GET /api/stats/api-usage?startDate=2026-01-01&endDate=2026-01-20
Authorization: Bearer <jwt_token>
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "totalCalls": 500,
    "successCalls": 480,
    "failedCalls": 20,
    "avgResponseTime": 150,
    "dailyUsage": [
      {
        "date": "2026-01-01",
        "calls": 25
      },
      {
        "date": "2026-01-02",
        "calls": 30
      }
    ]
  }
}
```

## WebSocket接口

### 实时进度推送

连接地址：

```
ws://localhost:3000/ws?token=<jwt_token>
```

**消息格式**：

```json
{
  "event": "analysis.progress",
  "data": {
    "taskId": "uuid",
    "status": "PROCESSING",
    "progress": 50,
    "currentStep": "正在提炼内容..."
  }
}
```

**完成消息**：

```json
{
  "event": "analysis.completed",
  "data": {
    "taskId": "uuid",
    "result": { /* 解析结果 */ }
  }
}
```

## 限流规则

### 免费用户

- 解析请求: 10次/小时
- API调用: 100次/小时
- 并发解析: 1篇

### 专业版用户

- 解析请求: 50次/小时
- API调用: 500次/小时
- 并发解析: 5篇

### 企业版用户

- 解析请求: 200次/小时
- API调用: 2000次/小时
- 并发解析: 20篇

## 错误码说明

| 错误码 | 说明 | 处理建议 |
|-------|------|---------|
| INVALID_PARAMS | 请求参数错误 | 检查请求格式 |
| UNAUTHORIZED | 未授权 | 重新登录 |
| INSUFFICIENT_BALANCE | 余额不足 | 充值 |
| QUOTA_EXCEEDED | 额度超限 | 升级会员 |
| AI_SERVICE_ERROR | AI服务错误 | 稍后重试 |
| CONTENT_TOO_LONG | 内容过长 | 分段处理 |
| INVALID_API_KEY | API Key无效 | 重新生成 |

## SDK示例

### JavaScript/TypeScript

```typescript
import { AINoteBookClient } from '@ainotebook/sdk'

const client = new AINoteBookClient({
  apiKey: 'your-api-key',
  baseURL: 'https://api.ainotebook.com/api'
})

// 解析文章
const result = await client.analysis.create({
  content: '# 标题\n内容...',
  enableExpansion: true
})

// 获取结果
const analysis = await client.analysis.get(result.taskId)
console.log(analysis.processedContent)
```

### Python

```python
from ainotebook import AINoteBookClient

client = AINoteBookClient(
    api_key='your-api-key',
    base_url='https://api.ainotebook.com/api'
)

# 解析文章
result = client.analysis.create(
    content='# 标题\n内容...',
    enable_expansion=True
)

# 获取结果
analysis = client.analysis.get(result['task_id'])
print(analysis['processed_content'])
```

详细设计请查看：
- [认证鉴权](/guide/authentication)
- [任务队列](/guide/queue)
