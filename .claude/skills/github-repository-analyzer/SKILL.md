---
name: github-repository-analyzer
description: 深度分析 GitHub 仓库的技术栈、代码质量、架构设计、社区活跃度和发展趋势。适用于需要全面了解开源项目、技术调研、代码审查、项目选型或架构学习的场景。当用户要求分析 GitHub 仓库、评估开源项目、研究技术架构或需要生成项目分析报告时触发。
---

# GitHub 仓库分析器

## 概述

提供全面、深入的 GitHub 仓库分析能力，从多个维度系统性地评估开源项目。支持技术栈识别、代码质量评估、架构分析、社区活跃度跟踪和发展趋势预测，并生成结构化的详细分析报告。适用于技术决策、项目选型、架构学习、代码审查和开源项目调研。

## 分析工作流程

### 第一阶段：信息收集

#### 1.1 基础仓库信息
收集仓库基础元数据：
- 仓库名称、描述和主页
- 创建日期和最后更新时间戳
- Star、Fork 和 Watcher 数量
- 开放 Issue 和 Pull Request 数量
- 主要编程语言和语言构成
- 许可证类型
- 主题/标签
- 仓库大小和统计数据

**方法：**
- 通过 web_search 或直接仓库检查使用 GitHub API
- 读取 README.md 和文档文件
- 检查 .github/ 目录获取额外元数据

#### 1.2 文档分析
分析可用文档：
- README.md 完整性（安装、使用、贡献指南）
- API 文档存在性
- 架构图和设计文档
- 变更日志和发布说明
- 贡献指南和行为准则

### 第二阶段：技术栈分析

#### 2.1 语言和框架识别
识别技术栈：
- 主要编程语言和版本
- 使用的框架和库（从 package.json、requirements.txt、go.mod 等获取）
- 构建工具和依赖管理系统
- 测试框架
- DevOps 和 CI/CD 工具
- 数据库和存储技术

**方法：**
- 分析依赖文件（package.json、requirements.txt、Cargo.toml、go.mod、pom.xml、build.gradle）
- 搜索导入语句和依赖声明
- 检查 Dockerfile、docker-compose.yml 或容器化配置
- 检查 CI/CD 工作流（.github/workflows/、.gitlab-ci.yml 等）

#### 2.2 技术版本评估
评估技术版本和时效性：
- 比较框架/库版本与最新发布版本
- 识别已弃用或过时的依赖
- 检查安全漏洞
- 评估版本兼容性和升级路径

**方法：**
- 使用 web_search 检查依赖的最新版本
- 查找版本更新变更日志
- 检查依赖安全公告

### 第三阶段：代码质量评估

#### 3.1 代码库结构分析
评估代码组织和结构：
- 目录结构和模块化程度
- 关注点分离
- 使用的设计模式
- 代码重复和冗余
- 命名约定一致性

**方法：**
- 使用 search_content 和 search_file 探索目录结构
- 分析模块组织和包结构
- 通过代码分析查找设计模式
- 检查跨文件的代码重复

#### 3.2 代码指标和标准
评估代码质量指标：
- 代码复杂度（圈复杂度）
- 测试覆盖率（如果可用）
- 代码风格一致性
- 文档覆盖率（内联注释、文档字符串）
- 错误处理实践
- 类型安全性（对于静态类型语言）

**方法：**
- 分析代码文件的复杂度指标
- 检查测试文件和测试框架的存在
- 审查代码风格和格式
- 评估文档密度
- 评估错误处理模式

#### 3.3 最佳实践遵循情况
评估最佳实践遵循情况：
- SOLID 原则
- 干净代码实践
- 安全最佳实践
- 性能优化技术
- 无障碍标准（对于前端项目）
- API 设计标准

**方法：**
- 搜索常见反模式
- 根据设计原则分析代码组织
- 检查安全实现
- 审查性能关键部分
- 验证无障碍合规性（a11y）

### 第四阶段：架构分析

#### 4.1 系统架构
分析整体系统架构：
- 架构模式（MVC、微服务、单体、无服务器等）
- 组件交互和数据流
- 分层架构（表示层、业务逻辑层、数据访问层）
- 集成模式（API、事件驱动等）
- 可扩展性和性能考虑

**方法：**
- 分析项目结构和模块依赖
- 查找架构文档
- 审查 API 设计和端点
- 审查数据模型和架构
- 识别集成点和外部服务

#### 4.2 设计模式和原则
识别设计模式和架构原则：
- GoF 设计模式使用
- 领域驱动设计（DDD）实现
- 仓储模式、工厂模式等
- 依赖注入和 IoC 容器
- 事件驱动架构模式

**方法：**
- 搜索模式实现
- 分析类和组件关系
- 审查抽象层
- 检查 DI 容器或服务定位器

#### 4.3 数据架构
分析数据处理和持久化：
- 数据库技术和架构
- 数据建模方法
- ORM 或数据访问层设计
- 缓存策略
- 数据迁移和版本控制

**方法：**
- 检查数据库架构文件
- 审查 ORM 配置和模型
- 检查缓存实现
- 查找迁移脚本

### 第五阶段：社区和生态系统分析

#### 5.1 社区活动指标
评估社区参与度：
- Star 和 Fork 增长率（趋势分析）
- 提交频率和活动模式
- 贡献者多样性和分布
- Issue 解决时间
- Pull Request 接受率
- 最近发布活动

**方法：**
- 使用 GitHub API 分析提交历史
- 审查 Issue 和 Pull Request 模式
- 检查贡献者统计
- 审查发布频率和版本控制

#### 5.2 代码审查和协作质量
评估协作实践：
- 代码审查实践（PR 审查评论、批准工作流）
- 贡献者指南和入职流程
- 社区行为准则
- 贡献者文档
- Issue 分类和维护实践

**方法：**
- 审查 Pull Request 讨论和审查
- 检查 CONTRIBUTING.md 和相关文档
- 分析 Issue 管理实践
- 审查社区指南

#### 5.3 外部集成和生态系统
分析外部生态系统参与：
- 第三方集成和插件
- 社区插件和扩展
- API 使用和流行度
- 文档和教程可用性
- 商业支持和公司支持

**方法：**
- 搜索集成和插件
- 检查外部 API 使用
- 查找社区资源
- 验证公司或组织参与

### 第六阶段：趋势和未来发展

#### 6.1 开发速度和趋势
分析开发模式：
- 发布频率和版本控制策略
- 功能开发速度
- Bug 修复与新功能比例
- 技术债务指标
- 迁移趋势（例如单体到微服务）

**方法：**
- 分析发布历史和变更日志
- 审查提交消息分类
- 检查主要重构活动
- 识别架构演化模式

#### 6.2 技术演化
跟踪技术栈演化：
- 依赖更新和迁移
- 框架升级和重大变更
- 新技术采用
- 旧技术弃用
- 行业对齐和最佳实践

**方法：**
- 比较当前依赖与历史版本
- 审查升级指南和迁移说明
- 分析技术采用模式
- 检查弃用警告

#### 6.3 未来展望和建议
提供未来发展见解：
- 项目可持续性和维护状态
- 潜在风险和挑战
- 技术现代化需求
- 增长潜力和采用轨迹
- 推荐改进领域

**方法：**
- 综合所有阶段的发现
- 识别模式和指标
- 评估社区和维护者活动
- 与行业趋势比较

### 第七阶段：报告生成

#### 7.1 综合分析报告
生成包含以下部分的结构化 Markdown 报告：

**执行摘要**
- 仓库高层概览
- 主要发现和建议
- 整体评估（1-5 级评分或分数）

**仓库概览**
- 基础信息和元数据
- 目的和范围
- 目标受众和用例

**技术栈分析**
- 主要技术和框架
- 依赖概览和版本
- 技术优势和劣势

**代码质量评估**
- 代码结构和组织
- 质量指标和标准
- 最佳实践遵循情况
- 需要改进的领域

**架构分析**
- 系统架构概览
- 设计模式和原则
- 数据架构
- 可扩展性和性能考虑

**社区和生态系统**
- 社区活动指标
- 协作质量
- 外部集成
- 生态系统支持

**趋势和未来发展**
- 开发速度
- 技术演化
- 未来展望和建议

**优势**
- 仓库的关键优势
- 竞争优势
- 值得注意的功能

**劣势和风险**
- 已识别的劣势
- 潜在风险
- 需要改进的领域

**建议**
- 可操作的建议
- 按优先级排序的改进建议
- 战略指导

**附录**
- 详细指标
- 文件结构分析
- 依赖列表
- 额外资源

#### 7.2 输出格式
- 主要：综合 Markdown 报告（显示给用户）
- 文件输出：保存到磁盘的 Markdown 文件
- 网页：遵循 NetworkPage 设计系统的交互式 HTML 报告

#### 7.3 Markdown 文件输出
生成 Markdown 报告内容后：
1. 根据仓库名称和时间戳生成唯一文件名
   - 格式：`{repository-name}-analysis-{YYYYMMDD-HHmmss}.md`
   - 示例：`react-analysis-20260115-143022.md`
2. 使用 `write_to_file` 工具将报告保存到工作区
3. 向用户输出完整文件路径
4. 确保文件保存在项目内的可访问位置

**重要：**
- 始终将 Markdown 文件保存到磁盘磁盘，而不仅仅是显示
- 保存后报告确切文件路径
- 使用清晰、描述性的文件名
- 时间戳确保多次分析的唯一性

#### 7.4 HTML 网页生成
生成并保存 Markdown 报告后，使用 `references/networkpage-des.md` 中定义的 NetworkPage 设计系统将其转换为交互式 HTML 页面：

**设计系统要求：**
- 使用玻璃拟态效果
- 应用定义的颜色系统（不同不透明度级别的白色）
- 使用 Inter 字体系列
- 实现漂亮的阴影和内阴影
- 应用背景模糊效果
- 遵循布局系统和间距指南
- 使用指定的动画和过渡样式
- 实现响应式设计
- 确保无障碍合规

**HTML 结构：**
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub 仓库分析报告</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* 基于 networkpage-des.md 的自定义样式 */
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: url('https://images.unsplash.com/photo-1635151227785-429f420c6b9d?w=2160&q=80') center/cover no-repeat fixed;
        }
        .beautiful-shadow {
            box-shadow:
                0 2.8px 2.2px rgba(0, 0, 0, 0.034),
                0 6.7px 5.3px rgba(0, 0, 0, 0.048),
                0 12.5px 10px rgba(0, 0, 0, 0.06),
                0 22.3px 17.9px rgba(0, 0, 0, 0.072),
                0 41.8px 33.4px rgba(0, 0, 0, 0.086),
                0 100px 80px rgba(0, 0, 0, 0.12);
        }
        .glass-inner-shadow {
            box-shadow:
                inset 2px 2px 1px 0 rgba(255, 255, 255, 0.5),
                inset -1px -1px 1px 1px rgba(255, 255, 255, 0.5);
        }
        .transition-custom {
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 2.2);
        }
        /* 平滑滚动 */
        html {
            scroll-behavior: smooth;
        }
        /* 部分样式 */
        .section-card {
            margin-bottom: 2rem;
            padding: 1.5rem;
        }
        /* 表格样式 */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }
        th, td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        th {
            font-weight: 600;
            background: rgba(255, 255, 255, 0.1);
        }
        /* 代码块样式 */
        pre {
            background: rgba(0, 0, 0, 0.3);
            padding: 1rem;
            border-radius: 8px;
            overflow-x: auto;
            margin: 1rem 0;
        }
        code {
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.875rem;
        }
        /* 列表样式 */
        ul, ol {
            margin: 1rem 0;
            padding-left: 1.5rem;
        }
        li {
            margin: 0.5rem 0;
        }
        /* 链接样式 */
        a {
            color: white;
            text-decoration: underline;
            transition: opacity 0.2s;
        }
        a:hover {
            opacity: 0.8;
        }
    </style>
</head>
<body class="flex items-center justify-center min-h-screen py-12 px-4">
    <!-- 主卡片容器 -->
    <div class="relative flex flex-col overflow-hidden beautiful-shadow transition-custom max-w-5xl w-full font-semibold text-white rounded-3xl">
        <!-- 玻璃背景层 -->
        <div class="absolute z-0 inset-0 backdrop-blur-md overflow-hidden isolate"></div>
        <div class="z-10 absolute inset-0 bg-white bg-opacity-15"></div>
        <div class="absolute inset-0 z-20 overflow-hidden glass-inner-shadow rounded-3xl"></div>

        <!-- 内容容器 -->
        <div class="relative z-30 flex flex-col h-full overflow-hidden">
            <!-- 头部部分 -->
            <div class="p-8 border-b border-white/10">
                <h1 class="leading-tight text-5xl font-normal text-white tracking-tighter mb-4">GitHub 仓库分析报告</h1>
                <p class="leading-relaxed text-sm font-light text-white/80" id="report-date"></p>
            </div>

            <!-- 可滚动内容区域 -->
            <div class="flex-1 overflow-y-auto p-8" id="report-content">
                <!-- 报告内容将在此动态插入 -->
            </div>

            <!-- 页脚 -->
            <div class="p-6 border-t border-white/10 text-center">
                <p class="text-sm font-normal text-white/60">由 GitHub 仓库分析器生成</p>
            </div>
        </div>
    </div>

    <script>
        // 解析 Markdown 内容并渲染为 HTML
        function renderMarkdown(markdown) {
            // 基本元素的简单 Markdown 解析器
            let html = markdown
                // 标题
                .replace(/^### (.*$)/gim, '<h3 class="text-2xl font-semibold text-white mt-6 mb-3">$1</h3>')
                .replace(/^## (.*$)/gim, '<h2 class="text-3xl font-semibold text-white mt-8 mb-4">$1</h2>')
                .replace(/^# (.*$)/gim, '<h1 class="text-4xl font-bold text-white mt-4 mb-4">$1</h1>')
                // 粗体和斜体
                .replace(/\*\*(.*?)\*\*/g, '<strong class="font-semibold">$1</strong>')
                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                // 列表
                .replace(/^\- (.*$)/gim, '<li class="text-white/80 text-sm">$1</li>')
                .replace(/^\d+\. (.*$)/gim, '<li class="text-white/80 text-sm">$1</li>')
                // 代码块
                .replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code class="text-green-300">$2</code></pre>')
                // 内联代码
                .replace(/`([^`]+)`/g, '<code class="bg-white/10 px-2 py-1 rounded text-green-300 text-xs">$1</code>')
                // 链接
                .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="underline">$1</a>')
                // 段落
                .replace(/^(?!<[a-z]).+$/gm, '<p class="leading-relaxed text-sm font-light text-white/80 mb-3">$&</p>');

            // 包裹列表
            html = html.replace(/(<li[^>]*>.*<\/li>)/gs, '<ul class="list-disc pl-6 mb-4">$1</ul>');

            return html;
        }

        // 加载并渲染 Markdown 报告
        async function loadReport() {
            // 设置报告日期
            document.getElementById('report-date').textContent = new Date().toLocaleDateString('zh-CN', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });

            // Markdown 内容占位符 - 生产中从 Markdown 文件加载
            const markdownContent = `
                <!-- Markdown 内容将在此插入 -->
            `;

            document.getElementById('report-content').innerHTML = renderMarkdown(markdownContent);
        }

        // 初始化
        loadReport();
    </script>
</body>
</html>
```

**HTML 页面输出流程：**
1. 生成并保存 Markdown 文件后
2. 生成与 Markdown 文件匹配的 HTML 文件名
   - 格式：`{repository-name}-analysis-{YYYYMMDD-HHmmss}.html`
   - 示例：`react-analysis-20260115-143022.html`
3. 按照 NetworkPage 设计系统将 Markdown 内容转换为 HTML
4. 使用 `write_to_file` 工具保存 HTML 文件
5. 向用户报告完整文件路径
6. （可选）使用 `preview_url` 工具在浏览器中预览 HTML 页面

**转换指南：**
- 保留 Markdown 报告中的所有内容部分
- 对容器和卡片应用玻璃拟态效果
- 使用设计系统中的适当字体大小和粗细
- 确保高对比度和可读性
- 添加平滑动画和过渡
- 为移动设备实现响应式布局
- 为长报告包含导航或目录
- 添加交互元素（可展开部分、选项卡等）以改善用户体验
- 使用定义的颜色调色板（不同不透明度级别的白色）
- 应用漂亮的阴影和内阴影
- 确保无障碍性，具有适当的对比度和焦点状态

## 分析技术

### 代码探索策略
有效使用以下工具和技术：

1. **目录结构分析**
   - 使用 `list_files` 了解项目结构
   - 识别关键目录（src/、lib/、tests/、docs/ 等）
   - 注意配置文件及其用途

2. **内容搜索**
   - 使用 `search_content` 查找特定模式、导入或关键字
   - 搜索设计模式、架构关键字
   - 查找特定库或框架的使用

3. **文件读取**
   - 读取关键文件：README、包配置、主入口点
   - 检查示例代码以了解代码风格和模式
   - 审查文档文件以获取架构见解

4. **模式识别**
   - 查找常见架构模式（MVC、MVVM 等）
   - 识别依赖注入模式
   - 搜索工厂、单例或其他设计模式

### 质量评估检查点
创建系统化评估：

- **结构**：代码库是否组织良好和模块化？
- **可读性**：代码是否易于理解和遵循？
- **可维护性**：代码是否易于修改和扩展？
- **可测试性**：代码是否可测试且存在测试？
- **性能**：是否考虑了性能问题？
- **安全性**：是否遵循安全最佳实践？
- **文档**：代码是否充分文档化？
- **一致性**：是否一致应用编码标准？

### 趋势分析方法
通过以下方式分析趋势：

- **时间分析**：检查随时间的提交频率
- **发布分析**：审查发布节奏和版本演进
- **贡献者分析**：跟踪贡献者增长和留存
- **Issue 分析**：分析 Issue 解决模式和类型
- **依赖分析**：跟踪依赖更新和更改

## 本技能的最佳实践

### 分析期间
- 彻底且系统化 - 按顺序遵循工作流阶段
- 提供具体示例和代码片段以支持发现
- 尽可能使用客观指标和证据
- 平衡积极和建设性反馈
- 评估时考虑项目背景和目标
- 突出优势和需要改进的领域

### 编写报告时
- 使用清晰、专业的语言
- 使用适当的标题和副标题构建内容
- 包含特定文件引用（使用行号格式：`startLine:endLine:filepath`）
- 提供可操作的建议
- 用证据支持声明
- 使用表格或列表以便轻松扫描关键信息
- 包含执行摘要以便快速概览

### 质量保证
- 用代码证据或文档验证所有声明
- 跨多个来源交叉引用发现
- 确保建议切实可行和现实
- 检查报告部分是否完整和连贯
- 审查清晰性和完整性

## 何时使用此技能

当用户请求以下内容时激活此技能：
- "分析这个 GitHub 仓库"
- "评估这个开源项目"
- "这个项目使用什么技术？"
- "这个项目维护得好吗？"
- "评估此仓库的代码质量"
- "审查此项目的架构"
- "为此仓库生成技术分析报告"
- "将此项目与替代方案进行比较"
- "我们应该使用这个库/框架吗？"

## 限制和注意事项

- 访问私有仓库需要适当权限
- 非常大的仓库可能需要选择性地分析关键区域
- 某些指标（如测试覆盖率）可能需要运行工具才能获得
- 历史趋势分析可能受到 GitHub API 速率限制的限制
- 分析深度应与时间约束平衡
- 某些评估需要了解项目目标和约束

## 报告生成工作流程（已更新）

### 分步流程

1. **生成分析内容**
   - 遵循阶段 1-6收集和分析仓库信息
   - 生成包含所有必需部分的综合 Markdown 内容

2. **保存 Markdown 报告**
   - 使用 Markdown 内容生成带时间戳的文件名
   - 格式：`{repository-name}-analysis-{YYYYMMDD-HHmmss}.md`
   - 使用 `write_to_file` 工具将 Markdown 文件保存到工作区
   - 向用户报告确切文件路径

3. **生成 HTML 报告**
   - 读取 `scripts/report-template.html` 模板文件
   - 将 `{{MARKDOWN_CONTENT}}` 占位符替换为实际的 Markdown 内容
   - 使用 `write_to_file` 工具保存带有匹配时间戳的 HTML 文件
   - 格式：`{repository-name}-analysis-{YYYYMMDD-HHmmss}.html`
   - 向用户报告确切文件路径

4. **可选：预览 HTML 报告**
   - 生成 HTML 文件后，提供在浏览器中预览
   - 使用 `preview_url` 工具和本地文件路径（如果可能）
   - 或提供在浏览器中打开文件的说明

**实现示例：**

```javascript
// 1. 生成 Markdown 内容后
const markdownContent = `# 仓库分析报告\n...`;

// 2. 生成文件名
const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
const repoName = 'example-repo';
const mdFilename = `${repoName}-analysis-${timestamp}.md`;
const htmlFilename = `${repoName}-analysis-${timestamp}.html`;

// 3. 保存 Markdown 文件
await write_to_file(mdFilename, markdownContent);
console.log(`Markdown 报告已保存到：${mdFilename}`);

// 4. 读取模板并生成 HTML
const template = await read_file('scripts/report-template.html');
const htmlContent = template.replace('{{MARKDOWN_CONTENT}}', markdownContent);
await write_to_file(htmlFilename, htmlContent);
console.log(`HTML 报告已保存到：${htmlFilename}`);
```

## 资源

### scripts/
- `generate-report.js`：报告生成的辅助脚本（Node.js）
  - 提供文件名生成函数
  - 演示 Markdown 和 HTML 文件创建
  - 可用作参考或直接在 Node.js 环境中使用

### references/
- `networkpage-des.md`：详细的设计系统规范
  - 完整的颜色调色板和排版
  - 玻璃拟态效果和阴影系统
  - 组件指南和最佳实践
  - CSS 变量和实用类参考

### scripts/
- `report-template.html`：用于 Web 报告生成的 HTML 模板
  - 使用 NetworkPage 设计系统预配置
  - 包含 Tailwind CSS 和 Google Fonts
  - 带侧边栏导航的响应式布局
  - JavaScript 中的 Markdown 到 HTML 转换
  - 玻璃拟态效果和动画
  - 交互式目录

### 报告输出文件
此技能为每次分析生成两个文件：
- **Markdown 文件**：包含原始 Markdown 内容的 `.md` 文件
- **HTML 文件**：带有样式、交互式 Web 报告的 `.html` 文件

两个文件都使用相同的时间戳保存，以便于匹配。

---

**注意：** 此技能提供了一个全面的 GitHub 仓库分析框架，具有自动 Markdown 和 HTML 报告生成功能。报告遵循 NetworkPage 设计系统，具有专业、现代的展示效果。
