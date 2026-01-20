# GitHub 上 2300 人 Star 的 Claude Code 可视化工作流编辑器。

**发布日期**: 2024-09-26

---

这个叫 ClaudeCode Workflow Studio的开源项目是专为 ** Claude Code** 设计的

如果你是 Claude Code、Vs Code 的重度用户，可以研究研究。

目前已经在 GitHub 上获得 2000 的 Star 了。

01

**开源项目简介**

使用这个开源项目，你可以通过「拖拽节点」的方式，像画流程图一样来设计 Claude Code 的自动化任务、技能（Skills）和复杂的 Agent 逻辑，而不需要纯靠手写复杂的代码或配置文件。

除了部分你需要联网的 MCP 工具外，这个插件的所有编辑和生成逻辑都是在你的 VS Code 本地运行的，不会把你的隐私配置乱传到云端。

而且界面会根据你的 VS Code 语言设置自动切换，支持中文。

如果你懒得自己拖拽，可以直接点击 Edit with AI，然后用自然语言告诉它，它就会自动帮你把节点画好、线连好。

比如上面视频演示的就是一句话生成一个自动化的代码审查工作流。

你只需要输入：1）使用 GitHub MCP 工具获取 PR 详情；2）根据 PR 的规模，将其路由到小型/中型/大型代码审查流程3）如果发现问题则向用户报告，如果审查通过则请求批准权限

就能给你生成一个可以直接运行的工作流。

支持 MCP 和 Skills

而且 ClaudeCode Workflow Studio 支持 MCP 和 Skills。

可以通过 MCP 直接调用外部工具，也可以复用你之前写好的特定 Skill。

同时支持添加「询问用户」的节点，比如 AI 干完活了，弹个选项让你选通过还是打回。

支持导出

你在画布上画完之后，点击导出，它会自动生成 Claude Code 能直接识别的 .claude/agents/ 和 .claude/commands/ 文件。

不需要你再去手动转换格式，导出后在终端里直接敲命令就能跑。

02

**怎么玩？**

使用这个项目其实非常简单，你的电脑里需要先装好 Claude Code 命令行工具。如果你没装过，可以在终端运行：

` npm install -g @anthropic-ai/claude-code`

然后打开你的 VS Code，搜索 Claude Code Workflow Studio 然后安装就行了。

然后在 VS Code 里按下 Ctrl+Shift+P 打开命令面板，输入 Claude Code，选择 Claude Code Workflow Studio: Open Editor。

这时候你会看到一个新的标签页打开了，里面是一块空白的画布，这就是你的工作台。

`开源地址：https://github.com/breaking-brake/cc-wf-studio`

03

**点击下方卡片，关注逛逛 GitHub**

这个公众号历史发布过很多有趣的开源项目，如果你懒得翻文章一个个找，你直接关注微信公众号：逛逛 GitHub ，后台对话聊天就行了：

---

来源: https://mp.weixin.qq.com/s/jUM5CCSBGPpR-af39eX60Q
