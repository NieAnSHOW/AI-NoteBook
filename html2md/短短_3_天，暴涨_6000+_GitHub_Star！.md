# 短短 3 天，暴涨 6000+ GitHub Star！

自从去年 Claude Code 和 Gemini 3 推出之后，大众对 AI 编程的热情被重新点燃，不论是否有一定编程基础，都开始尝试尝试用 AI 来开发个人应用。

但与此同时，当你深入开始用 AI 构建前端界面后，便会发现不少问题。

首先是 AI 生成的前端样式不一致，有时候也会因为组件搭配不对，而导致整个界面错乱。甚至更严重的，AI 在编写代码时，因为没有遵从各种规范和约束，导致项目出现不少安全隐患。

种种问题，使得项目开发效率降低，成本增高，在实际应用到生产环境后，也会让运维工作激增。

为了解决这个问题，知名网站托管平台，同时也是前端主流框架 Next.js 的创造者：Vercel Labs，终于出手了，在 GitHub 上正式开源了 **json-render**。

项目上线短短三天，就暴涨 6000+ GitHub Star，可见一直以来，大家都被这个问题折磨得不轻。

![star-history-2026118 (1)](https://mmbiz.qpic.cn/mmbiz_png/uDRkMWLia28gURArdTRujds07Ft04uE1lQiaStiakIVlSCnJCxYicBE2YX8gMH0VCjM41ZLVSGNoGlePlT5BwEd9Vw/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

对于 AI 乱写代码问题，Vercel 的解决方案简单粗暴：**既然 AI 写代码容易失控，那就基于规范定义，对它加以限制。**

这次的代码生成逻辑，与以往不同，JSON Render 直接制定了一条全新的规则：AI 不再负责 “造房子”（写逻辑代码），只负责“画图纸”（输出结构化的 JSON 数据）。

先让 AI 为前端产出对应的 JSON 格式文件，在基于此文件中定义的样式组件，来生成固定、规范化的前端 UI 代码。

在原有的基础上，重新定义了一套全新流程，即： **“AI → JSON → UI”。**

![image-20260118150745161](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

在这个流程里，JSON 就像是一张标准化的“填空题”。AI 只能在格子里填内容，而不能在纸上乱涂乱画。

采取这种 “降维打击” 般的策略，把不可控的生成式 AI，变成了精准的填空题，并带来了三大杀手锏。

![image-20260118150602729](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

### 1\. 彻底的安全 “紧箍咒”

既然是填空题，那就必须遵循规则。因此技术团队引入了 **Catalog（目录）** 的概念，也就是先给 UI 定义一套清晰明确的组件库清单。

然后告诉 AI：“你只能用这里面的卡片、按钮、图表等等组件。”

如果 AI 脑子一抽，想捏造一个不存在的组件，或者想偷偷运行一段破坏性的脚本，内置渲染引擎会直接拦截。

这就彻底杜绝了 AI 瞎写代码导致的安全风险，让它只能在我们划定的圈子里干活。

![image-20260118150431000](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

### 2\. 让界面 “活” 过来

这是 JSON Render 最令人惊艳的地方。

传统的 AI 生成界面往往是死的，但 Vercel 在这套 JSON 规则里设计了 **数据绑定** 的功能。

AI 只需要在数据里标记一下， 就能快速指向数据库里的某个字段，自动完成数据更新。

当界面渲染出来时，它会自动去后台拉取最新的真实数据，甚至点击按钮能真正触发后端的业务逻辑。

![Introducingjson-renderAI-generatedUI.Determinis-ezgif.com-video-to-gif-converter](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

### 3\. 一键 “翻译”，回源代码

很多时候，我们不仅希望能在 AI 聊天窗口中，直接看到成品效果，更希望代码能做到拿来即用。

得益于这种结构化的设计，json-render 新增了 **Code Export（代码导出）**功能。

它能把这套 JSON 指令，自动翻译成标准的、无依赖的 Next.js 代码文件。

下载下来，粘贴到你的项目里，直接就能跑，彻底打通了从“想法”到“产品落地”的最后一公里。

![image-20260118150332929](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

安装 & 使用

至于上手使用，那就更加简单了，一行代码安装依赖包：

```
npm install @json-render/core @json-render/react
```

第一步，定义规则（Catalog），告诉 AI 有哪些组件可用：

```
import { createCatalog } from '@json-render/core';
```

第二步，将用户的 Prompt 发给 AI，让其按照规范生成 JSON 数据。

第三步，在前端使用 `Renderer` 组件进行解析渲染，或者直接调用导出函数。

```
import { Renderer, useUIStream } from '@json-render/react';
```

### 写在最后

在项目短短几天，便能收获如此多的 Star 来看，除了技术团队本身在开源社区的影响力，更为重要的是这个项目解决了目前前端 UI 开发中，代码生成不可控的问题。

它借鉴了传统的 DSL，通过声明式语法，来更加稳定的输出代码，同时基于 AI 的对话能力，优化了整个交互流程，提升了编程体验。

整体而言，这确实算得上是一款极具前瞻性的开源工具。

在当下大家都在追求让 AI 产出各种前端酷炫界面的环境下，Vercel Labs 没有选择随大流，而是立足于开发者，知道得先让前端 UI 代码更可控，才能真正应用到商业应用。

目前，该项目仍在持续迭代与更新，对于想提升项目代码质量与稳定性的同学，建议上手把玩一下，同时也可以学习下该项目的设计理念。

GitHub 项目：https://github.com/vercel-labs/json-render

今天的分享到此结束，感谢大家抽空阅读，我们下期再见，Respect！

---
Source: [短短 3 天，暴涨 6000+ GitHub Star！](https://mp.weixin.qq.com/s/6SUXkg6jxomET90JlGCr7w)