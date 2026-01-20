import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'AI-NoteBook 技术文档',
  description: 'AI驱动的智能内容分析与笔记系统',
  lang: 'zh-CN',
  base: '/',
  head: [
    ['link', { rel: 'icon', href: '/logo.ico' }]
  ],

  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '技术方案', link: '/guide/architecture' },
      { text: '技术栈', link: '/guide/tech-stack' },
      { text: '数据库设计', link: '/guide/database' },
      { text: 'API文档', link: '/guide/api' },
    ],

    sidebar: {
      '/guide/': [
        {
          text: '项目概览',
          items: [
            { text: '项目介绍', link: '/guide/introduction' },
            { text: '架构设计', link: '/guide/architecture' },
            { text: '技术栈', link: '/guide/tech-stack' },
          ]
        },
        {
          text: '核心功能',
          items: [
            { text: '易读性评分', link: '/guide/features/readability' },
            { text: '内容提炼', link: '/guide/features/refinement' },
            { text: '智能扩展', link: '/guide/features/expansion' },
            { text: '溯源校验', link: '/guide/features/verification' },
          ]
        },
        {
          text: '后端设计',
          items: [
            { text: '数据库设计', link: '/guide/database' },
            { text: 'API设计', link: '/guide/api' },
            { text: '认证鉴权', link: '/guide/authentication' },
            { text: '任务队列', link: '/guide/queue' },
          ]
        },
        {
          text: '前端设计',
          items: [
            { text: '前端架构', link: '/guide/frontend-architecture' },
            { text: '组件设计', link: '/guide/frontend-components' },
            { text: '状态管理', link: '/guide/frontend-state-management' },
            { text: '主题系统', link: '/guide/frontend-theming' },
          ]
        },
        {
          text: '部署运维',
          items: [
            { text: '环境配置', link: '/guide/deployment' },
            { text: '性能优化', link: '/guide/performance' },
            { text: '监控日志', link: '/guide/monitoring' },
          ]
        },
      ]
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/yourusername/AI-NoteBook' }
    ],

    footer: {
      message: '基于 MIT 许可发布',
      copyright: 'Copyright © 2026-Present AI-NoteBook'
    },

    search: {
      provider: 'local'
    }
  },

  markdown: {
    lineNumbers: true,
    config: (md) => {
      // 可以添加markdown-it插件
    }
  }
})
