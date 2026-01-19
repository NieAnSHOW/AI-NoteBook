# GitHub Repository Analyzer - Report Generation Guide

本指南说明如何使用优化后的 GitHub Repository Analyzer 技能生成 markdown 和 HTML 报告。

## 功能概述

优化后的技能现在支持：
1. ✅ **Markdown 报告生成** - 自动保存分析结果为 .md 文件
2. ✅ **HTML 网页报告** - 使用 NetworkPage 设计系统生成精美的交互式网页
3. ✅ **双文件输出** - 同时生成 markdown 和 HTML 文件

## 使用方法

### 基本流程

1. **激活技能**
   当用户要求分析 GitHub 仓库时，技能会自动激活

2. **执行分析**
   遵循 SKILL.md 中定义的分析流程，包括：
   - 信息收集
   - 技术栈分析
   - 代码质量评估
   - 架构分析
   - 社区生态系统分析
   - 趋势分析

3. **生成报告**
   分析完成后，技能会自动：
   - 生成包含所有章节的完整 markdown 内容
   - 保存为 `{repo-name}-analysis-{timestamp}.md` 文件
   - 使用 HTML 模板生成网页版本
   - 保存为 `{repo-name}-analysis-{timestamp}.html` 文件

### 输出文件说明

#### Markdown 文件
- **格式**: `.md`
- **用途**: 原始文本格式，适合版本控制、文档系统和 Markdown 编辑器
- **命名示例**: `react-analysis-20260115-143022.md`
- **内容**: 完整的分析报告，包含所有章节和格式

#### HTML 文件
- **格式**: `.html`
- **用途**: 交互式网页，可以在浏览器中直接查看和分享
- **命名示例**: `react-analysis-20260115-143022.html`
- **设计**: 采用 NetworkPage 设计系统
  - 玻璃拟态效果
  - 响应式布局
  - 侧边栏导航
  - 平滑滚动
  - 高对比度可读性
  - 流畅动画

## 文件结构

```
.github-repository-analyzer/
├── SKILL.md                           # 技能主文档
├── scripts/                           # 脚本和模板目录
│   ├── generate-report.js            # 报告生成辅助脚本
│   └── report-template.html          # HTML 报告模板
└── references/                        # 参考文档目录
    ├── README.md                     # 本文件（使用指南）
    ├── networkpage-des.md            # 网页设计规范
    ├── example-report.md             # 示例报告
    └── OPTIMIZATION_SUMMARY.md       # 优化总结
```

## 设计系统 (NetworkPage)

报告网页使用 NetworkPage 设计系统，主要特性：

### 核心设计风格
- **玻璃拟态** (Glassmorphism) - 半透明玻璃质感
- **极简主义** - 简洁清晰的视觉层次
- **高对比度** - 确保可读性和可访问性
- **流畅交互** - 平滑的过渡动画和微交互

### 颜色系统
- 白色主色调，不同透明度层次（100%, 80%, 60%, 30%, 15%, 10%, 5%）
- 渐变背景
- 柔和阴影

### 字体系统
- 主字体: Inter
- 字重: 300 (Light) 到 700 (Bold)
- 字号: 12px 到 48px

### 效果
- 毛玻璃模糊
- 美化阴影
- 内阴影边框
- 自定义过渡动画

## HTML 模板特性

`scripts/report-template.html` 提供以下功能：

### 响应式布局
- 桌面端: 带侧边栏的双栏布局
- 移动端: 单栏垂直布局

### 交互功能
- 自动生成目录 (TOC)
- 点击目录项滚动到对应章节
- Markdown 到 HTML 自动转换
- 平滑滚动效果

### 样式支持
- 标题 (H1, H2, H3)
- 列表 (有序、无序)
- 代码块
- 表格
- 链接
- 粗体和斜体

## 使用 generate-report.js

如果需要手动生成报告，可以使用提供的 Node.js 脚本：

```javascript
const { generateCompleteReport } = require('../scripts/generate-report.js');

// 示例 Markdown 内容
const markdownContent = `# Executive Summary
...

# Repository Overview
...

[完整的报告内容]
`;

// 生成报告
generateCompleteReport(markdownContent, 'example-repo', './output')
    .then(result => {
        console.log('Markdown:', result.markdown);
        console.log('HTML:', result.html);
    })
    .catch(error => {
        console.error('Error:', error);
    });
```

## 最佳实践

### 报告生成
1. **命名规范**: 使用仓库名作为文件名前缀，确保可识别性
2. **时间戳**: 自动添加时间戳，防止文件名冲突
3. **完整性**: 确保所有必需的章节都包含在报告中

### HTML 报告
1. **预览**: 生成后建议在浏览器中预览
2. **分享**: 可以将 HTML 文件托管或直接分享给团队成员
3. **兼容性**: 使用现代浏览器获得最佳体验

### 维护
1. **模板更新**: 如需修改网页样式，编辑 `scripts/report-template.html`
2. **设计更新**: 如需更新设计规范，参考 `networkpage-des.md`
3. **功能扩展**: 可以在模板中添加新的交互功能

## 故障排除

### Markdown 文件未生成
- 检查 `write_to_file` 工具是否正确调用
- 确保文件名包含有效的时间戳
- 验证输出目录是否可写

### HTML 文件未生成
- 确认 `scripts/report-template.html` 文件存在
- 检查 markdown 内容是否正确注入
- 验证模板中的 `{{MARKDOWN_CONTENT}}` 占位符

### 网页样式异常
- 确认 Tailwind CSS CDN 可访问
- 检查 Google Fonts 是否加载
- 验证背景图片 URL 是否有效

## 示例输出

### Markdown 文件
```markdown
# Executive Summary
This repository demonstrates excellent...

## Repository Overview
- Name: example/repo
- Stars: 1000

[更多内容...]
```

### HTML 文件
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <!-- NetworkPage 设计系统 -->
    <title>GitHub Repository Analysis Report</title>
    <!-- 样式和脚本 -->
</head>
<body>
    <!-- 玻璃拟态主容器 -->
    <!-- 侧边栏导航 -->
    <!-- 报告内容 -->
    <!-- 页脚 -->
</body>
</html>
```

## 支持和反馈

如有问题或建议，请检查：
1. SKILL.md 中的详细文档
2. references/networkpage-des.md 中的设计规范
3. scripts/generate-report.js 中的示例代码

---

**最后更新**: 2026-01-15
**版本**: 2.0
