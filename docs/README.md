# AI-NoteBook 技术文档

这是AI-NoteBook项目的完整技术文档，使用VitePress构建。

## 快速开始

### 安装依赖

```bash
cd docs
npm install
```

### 本地开发

```bash
npm run docs:dev
```

访问 http://localhost:5173 查看文档

### 构建生产版本

```bash
npm run docs:build
```

构建后的文件在 `.vitepress/dist` 目录

### 预览生产版本

```bash
npm run docs:preview
```

## 文档结构

```
docs/
├── .vitepress/
│   └── config.ts          # VitePress配置
├── guide/
│   ├── introduction.md    # 项目介绍
│   ├── architecture.md    # 系统架构
│   ├── tech-stack.md     # 技术栈详解
│   ├── database.md       # 数据库设计
│   ├── api.md            # API文档
│   └── features/         # 核心功能
│       ├── readability.md
│       ├── refinement.md
│       ├── expansion.md
│       └── verification.md
├── index.md              # 首页
└── package.json
```

## 编写文档

### 添加新页面

1. 在 `guide/` 目录下创建 `.md` 文件
2. 在 `.vitepress/config.ts` 中添加到侧边栏配置

```typescript
sidebar: {
  '/guide/': [
    {
      text: '项目概览',
      items: [
        { text: '新页面标题', link: '/guide/new-page' }
      ]
    }
  ]
}
```

### 使用Vue组件

在Markdown中可以直接使用Vue组件：

```vue
<template>
  <div class="custom-component">
    <!-- 组件内容 -->
  </div>
</template>
```

### 代码高亮

使用代码块语法：

``````markdown
```typescript
function hello() {
  console.log('Hello, AI-NoteBook!')
}
```
``````

## 部署

### 部署到GitHub Pages

```bash
npm run docs:deploy
```

### 部署到自定义域名

1. 构建文档：`npm run docs:build`
2. 将 `.vitepress/dist` 目录上传到服务器
3. 配置Nginx：

```nginx
server {
  listen 80;
  server_name docs.yourdomain.com;
  root /path/to/dist;
  index index.html;

  location / {
    try_files $uri $uri/ /index.html;
  }
}
```

## 更新日志

### v1.0.0 (2026-01-20)

- ✨ 初始版本
- 📚 完整的技术栈文档
- 🏗️ 系统架构设计
- 💾 数据库设计文档
- 🔌 API接口文档
- ⚡ 核心功能说明

## 贡献指南

欢迎提交Issue和Pull Request来改进文档！

## 许可证

MIT License

---

**AI-NoteBook** - AI驱动的智能内容分析系统
