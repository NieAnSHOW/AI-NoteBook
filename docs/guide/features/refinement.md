# 内容提炼

内容提炼是AI-NoteBook的核心功能之一,通过AI智能分析文章结构,过滤冗余内容,突出重点信息,让用户快速掌握文章精髓。

## 功能概述

内容提炼功能能够:
- **过滤废话**: 自动识别并去除重复啰嗦、无关紧要的内容
- **提炼结构**: 梳理文章的层次结构,展示清晰的逻辑脉络
- **标记重点**: 对关键信息进行加粗/下划线标记,方便快速浏览
- **保留完整**: 在精简的同时保持文章核心信息的完整性

## 提炼策略

### 1. 废话识别

**识别规则**:

```typescript
interface NoisePattern {
  type: 'repetition' | 'filler' | 'irrelevant' | 'verbose'
  pattern: RegExp
  confidence: number
}

const noisePatterns: NoisePattern[] = [
  // 重复内容
  {
    type: 'repetition',
    pattern: /(?:总的来说|综上所述|简而言之|也就是说)[^。]{0,100}/g,
    confidence: 0.8
  },
  // 填充词
  {
    type: 'filler',
    pattern: /(嗯|啊|那个|然后|就是){2,}/g,
    confidence: 0.9
  },
  // 啰嗦表达
  {
    type: 'verbose',
    pattern: /(?:非常|十分|特别|极其)+(?:重要|关键|必要)/g,
    confidence: 0.6
  }
]
```

### 2. 结构提取

**层次识别算法**:

```typescript
interface ArticleStructure {
  title: string
  sections: Section[]
}

interface Section {
  level: number          // 层级深度 (1-6)
  heading: string        // 章节标题
  content: string        // 章节内容
  keyPoints: string[]    // 关键点
  subsections?: Section[] // 子章节
}

function extractStructure(markdown: string): ArticleStructure {
  const lines = markdown.split('\n')
  const structure: ArticleStructure = {
    title: '',
    sections: []
  }

  const stack: Section[] = []
  let currentLevel = 0

  for (const line of lines) {
    // 识别标题
    const headingMatch = line.match(/^(#{1,6})\s+(.+)/)
    if (headingMatch) {
      const level = headingMatch[1].length
      const heading = headingMatch[2]

      const section: Section = {
        level,
        heading,
        content: '',
        keyPoints: []
      }

      // 维护层级关系
      while (stack.length > 0 && stack[stack.length - 1].level >= level) {
        stack.pop()
      }

      if (stack.length === 0) {
        structure.sections.push(section)
      } else {
        const parent = stack[stack.length - 1]
        if (!parent.subsections) {
          parent.subsections = []
        }
        parent.subsections.push(section)
      }

      stack.push(section)
      currentLevel = level
    } else {
      // 累积内容到当前章节
      if (stack.length > 0) {
        const current = stack[stack.length - 1]
        current.content += line + '\n'
      }
    }
  }

  return structure
}
```

### 3. 重点标记

**关键点识别**:

```typescript
interface KeyPoint {
  text: string
  importance: number    // 重要性分数 (0-1)
  position: number      // 在段落中的位置
  type: 'definition' | 'conclusion' | 'example' | 'warning'
}

async function extractKeyPoints(section: Section): Promise<KeyPoint[]> {
  const sentences = splitSentences(section.content)

  const keyPoints: KeyPoint[] = []

  for (const sentence of sentences) {
    // 规则1: 定义性语句
    if (sentence.match(/(?:是指|定义为|所谓)/)) {
      keyPoints.push({
        text: sentence,
        importance: 0.9,
        position: sentence.index,
        type: 'definition'
      })
    }

    // 规则2: 结论性语句
    if (sentence.match(/(?:因此|所以|综上|可见|总之)/)) {
      keyPoints.push({
        text: sentence,
        importance: 0.85,
        position: sentence.index,
        type: 'conclusion'
      })
    }

    // 规则3: 警告性语句
    if (sentence.match(/(?:注意|警告|重要|关键)/)) {
      keyPoints.push({
        text: sentence,
        importance: 0.95,
        position: sentence.index,
        type: 'warning'
      })
    }

    // 规则4: AI辅助判断
    const aiResult = await aiService.analyze({
      prompt: `判断以下句子的重要性(0-1): ${sentence}`,
      temperature: 0.2
    })

    if (aiResult.importance > 0.7) {
      keyPoints.push({
        text: sentence,
        importance: aiResult.importance,
        position: sentence.index,
        type: 'example'
      })
    }
  }

  // 按重要性排序
  return keyPoints.sort((a, b) => b.importance - a.importance)
}
```

## AI提示词模板

```markdown
你是一个专业的文章提炼专家。请对以下文章进行智能提炼:

## 原文内容
{{content}}

## 提炼要求

### 1. 结构梳理
- 识别文章的章节层次
- 提取每个章节的核心观点
- 保持逻辑关系的完整性

### 2. 内容精简
- 删除重复啰嗦的表达
- 去除无关的填充内容
- 合并相似的论述

### 3. 重点标记
- **加粗**: 核心概念和关键结论
- __下划线__: 重要定义和专业术语
- > 引用块: 需要特别注意的内容

### 4. 保留原则
- 必须保留: 核心论点、关键数据、重要结论
- 可选保留: 辅助说明、案例细节
- 应该删除: 重复内容、无关论述、过长的铺垫

## 输出格式

请以JSON格式返回提炼结果:

```json
{
  "title": "文章标题",
  "summary": "一句话总结文章核心观点(不超过50字)",
  "structure": [
    {
      "level": 1,
      "heading": "章节标题",
      "summary": "本章核心观点",
      "keyPoints": [
        {
          "text": "**加粗的关键点**",
          "importance": 0.9,
          "type": "definition"
        }
      ],
      "refinedContent": "精简后的章节内容,保留重点标记"
    }
  ],
  "statistics": {
    "originalLength": 5000,
    "refinedLength": 2000,
    "compressionRatio": 0.4,
    "keyPointsCount": 15
  }
}
```

## 提炼示例

**原文段落**:
```
微服务架构是一种将单个应用程序开发为一套小型服务的方法,每个服务运行在自己的进程中,并使用轻量级机制(通常是HTTP API)进行通信。这些服务围绕业务能力构建,可以通过全自动部署机制独立部署。这些服务可以用不同的编程语言编写,使用不同的数据存储技术。总的来说,微服务架构就是将复杂的单体应用拆分成多个独立的小服务,每个服务专注于单一的业务功能。简单来说,微服务架构就是一种更加灵活、可扩展的架构模式。
```

**提炼后**:
```
微服务架构是将复杂单体应用拆分为多个独立小服务的架构模式。

**核心特征**:
- 每个服务运行在独立进程中
- 使用轻量级机制(HTTP API)通信
- __围绕业务能力构建__
- 支持__全自动独立部署__
- 可使用不同编程语言和数据存储技术
```
```

## 前端展示

### 组件设计

```vue
<template>
  <div class="content-refinement">
    <!-- 原文与提炼对比 -->
    <n-tabs type="line" animated>
      <n-tab-pane name="refined" tab="提炼内容">
        <div class="refined-content">
          <!-- 文章概要 -->
          <n-card class="summary-card" v-if="refinedData.summary">
            <template #header>
              <n-icon :component="SparklesIcon" />
              核心观点
            </template>
            <p class="summary-text">{{ refinedData.summary }}</p>
          </n-card>

          <!-- 结构化内容 -->
          <div class="structure-tree">
            <TreeNode
              v-for="section in refinedData.structure"
              :key="section.heading"
              :node="section"
              :level="0"
            />
          </div>

          <!-- 统计信息 -->
          <n-card class="stats-card">
            <n-statistic label="精简比例" :value="compressionRatio">
              <template #suffix>%</template>
            </n-statistic>
            <n-statistic label="关键点数" :value="refinedData.statistics.keyPointsCount" />
          </n-card>
        </div>
      </n-tab-pane>

      <n-tab-pane name="original" tab="原始内容">
        <div class="original-content">
          <MarkdownRenderer :content="originalContent" />
        </div>
      </n-tab-pane>

      <n-tab-pane name="comparison" tab="对比视图">
        <div class="comparison-view">
          <div class="comparison-item" v-for="(section, index) in comparisonData" :key="index">
            <div class="original">
              <h4>原文</h4>
              <p>{{ section.original }}</p>
            </div>
            <n-icon :component="ArrowIcon" size="24" />
            <div class="refined">
              <h4>提炼</h4>
              <p v-html="section.refined"></p>
            </div>
          </div>
        </div>
      </n-tab-pane>
    </n-tabs>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { NTabs, NTabPane, NCard, NIcon, NStatistic } from 'naive-ui'
import TreeNode from './TreeNode.vue'
import MarkdownRenderer from './MarkdownRenderer.vue'

interface Props {
  originalContent: string
  refinedData: RefinedContent
}

const props = defineProps<Props>()

const compressionRatio = computed(() =>
  Math.round(props.refinedData.statistics.compressionRatio * 100)
)

const comparisonData = computed(() => {
  // 生成原文与提炼内容的对比数据
  return props.refinedData.structure.map(section => ({
    original: section.originalContent || '',
    refined: section.refinedContent
  }))
})
</script>

<style scoped>
.summary-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  margin-bottom: 20px;
}

.summary-text {
  font-size: 18px;
  font-weight: 500;
  line-height: 1.6;
}

.structure-tree {
  margin: 20px 0;
}

.stats-card {
  display: flex;
  gap: 40px;
  margin-top: 20px;
}

.comparison-view {
  display: grid;
  gap: 20px;
}

.comparison-item {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 16px;
  align-items: start;
}

.comparison-item .original,
.comparison-item .refined {
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.comparison-item .original {
  background: #f9fafb;
}

.comparison-item .refined {
  background: #ecfdf5;
  border-color: #10b981;
}

.comparison-item h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #6b7280;
}

/* 重点标记样式 */
.refined :deep(strong) {
  font-weight: 700;
  color: #059669;
  background: linear-gradient(180deg, transparent 65%, #d1fae5 65%);
}

.refined :deep(u) {
  text-decoration: underline;
  text-decoration-color: #8b5cf6;
  text-decoration-thickness: 2px;
}
</style>
```

### 树形节点组件

```vue
<template>
  <div class="tree-node" :class="`level-${level}`">
    <div class="node-header">
      <n-icon
        :component="expanded ? ChevronDownIcon : ChevronRightIcon"
        @click="toggleExpand"
        class="expand-icon"
      />
      <h3 :class="`heading-${node.level}`">{{ node.heading }}</h3>
      <n-tag v-if="node.keyPoints?.length" type="success" size="small">
        {{ node.keyPoints.length }} 个重点
      </n-tag>
    </div>

    <n-collapse-transition :show="expanded">
      <div class="node-content">
        <!-- 本章概要 -->
        <p v-if="node.summary" class="section-summary">{{ node.summary }}</p>

        <!-- 关键点列表 -->
        <div v-if="node.keyPoints?.length" class="key-points">
          <div
            v-for="(point, index) in node.keyPoints"
            :key="index"
            class="key-point-item"
            :class="`type-${point.type}`"
          >
            <n-icon :component="getIcon(point.type)" />
            <span v-html="point.text"></span>
            <n-rate
              :model-value="point.importance * 5"
              readonly
              size="small"
              count="5"
            />
          </div>
        </div>

        <!-- 精炼内容 -->
        <div v-if="node.refinedContent" class="refined-content">
          <MarkdownRenderer :content="node.refinedContent" />
        </div>

        <!-- 子节点 -->
        <div v-if="node.subsections?.length" class="subsections">
          <TreeNode
            v-for="child in node.subsections"
            :key="child.heading"
            :node="child"
            :level="level + 1"
          />
        </div>
      </div>
    </n-collapse-transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { NIcon, NTag, NRate, NCollapseTransition } from 'naive-ui'

interface Props {
  node: Section
  level: number
}

const props = defineProps<Props>()
const expanded = ref(props.level < 2) // 默认展开前两层

function toggleExpand() {
  expanded.value = !expanded.value
}

function getIcon(type: string) {
  const icons = {
    definition: BookOpenIcon,
    conclusion: LightbulbIcon,
    example: CodeIcon,
    warning: AlertTriangleIcon
  }
  return icons[type] || CircleIcon
}
</script>

<style scoped>
.tree-node {
  margin: 12px 0;
  padding-left: calc(props.level * 20px);
  border-left: 2px solid #e5e7eb;
}

.node-header {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 8px 0;
}

.expand-icon:hover {
  color: #3b82f6;
}

.key-points {
  margin: 16px 0;
  display: grid;
  gap: 12px;
}

.key-point-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 12px;
  border-radius: 8px;
  background: #f9fafb;
  border-left: 3px solid #d1d5db;
}

.key-point-item.type-definition {
  border-left-color: #3b82f6;
  background: #eff6ff;
}

.key-point-item.type-conclusion {
  border-left-color: #10b981;
  background: #ecfdf5;
}

.key-point-item.type-warning {
  border-left-color: #f59e0b;
  background: #fef3c7;
}
</style>
```

## 后端实现

### Service层

```typescript
// backend/analysis/refinement.service.ts
import { Injectable } from '@nestjs/common'
import { AiService } from '@/ai/ai.service'
import { RedisService } from '@/redis/redis.service'

interface RefinementConfig {
  maxCompressionRatio: number  // 最大压缩比例 (0.3 = 30%)
  minKeyPoints: number         // 最少关键点数量
  preserveSections: string[]   // 必须保留的章节
}

@Injectable()
export class RefinementService {
  private readonly config: RefinementConfig = {
    maxCompressionRatio: 0.5,
    minKeyPoints: 5,
    preserveSections: ['结论', '总结', '摘要']
  }

  constructor(
    private readonly aiService: AiService,
    private readonly redis: RedisService
  ) {}

  async refine(content: string, options?: Partial<RefinementConfig>): Promise<RefinedContent> {
    const config = { ...this.config, ...options }

    // 1. 提取结构
    const structure = this.extractStructure(content)

    // 2. AI提炼每个章节
    const refinedSections = await Promise.all(
      structure.sections.map(section => this.refineSection(section))
    )

    // 3. 生成摘要
    const summary = await this.generateSummary(content)

    // 4. 计算统计信息
    const statistics = this.calculateStatistics(content, refinedSections)

    return {
      title: structure.title,
      summary,
      structure: refinedSections,
      statistics
    }
  }

  private async refineSection(section: Section): Promise<RefinedSection> {
    const prompt = this.buildRefinementPrompt(section)

    const result = await this.aiService.chat({
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.3,
      responseFormat: { type: 'json_object' }
    })

    return this.parseRefinement(result.content)
  }

  private buildRefinementPrompt(section: Section): string {
    return `
你是一个专业的内容提炼专家。请对以下章节进行智能提炼:

## 章节标题
${section.heading}

## 章节内容
${section.content}

## 提炼要求

1. **内容精简**: 删除重复啰嗦,保留核心观点,压缩比例控制在50%以内
2. **重点标记**: 使用Markdown语法标记重点
   - **加粗**: 核心概念和关键结论
   - __下划线__: 重要定义和专业术语
   - > 引用: 需要特别注意的内容
3. **提取关键点**: 识别3-5个最重要的论点
4. **生成概要**: 用一句话总结本章核心观点(不超过30字)

## 输出格式

请返回JSON格式:
{
  "summary": "本章核心观点",
  "keyPoints": [
    {
      "text": "**关键论点**",
      "importance": 0.9,
      "type": "conclusion"
    }
  ],
  "refinedContent": "**提炼后的内容**,保留重点标记"
}
    `
  }

  private async generateSummary(content: string): Promise<string> {
    const prompt = `
请用一句话总结以下文章的核心观点(不超过50字):

${content.substring(0, 2000)}
    `

    const result = await this.aiService.chat({
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.3,
      maxTokens: 100
    })

    return result.content.trim()
  }

  private calculateStatistics(
    original: string,
    refined: RefinedSection[]
  ): RefinementStatistics {
    const originalLength = original.length
    const refinedLength = refined.reduce(
      (sum, s) => sum + s.refinedContent.length,
      0
    )

    const keyPointsCount = refined.reduce(
      (sum, s) => sum + (s.keyPoints?.length || 0),
      0
    )

    return {
      originalLength,
      refinedLength,
      compressionRatio: refinedLength / originalLength,
      keyPointsCount
    }
  }

  private extractStructure(markdown: string): ArticleStructure {
    // 实现结构提取逻辑
    // (参考前面的结构提取算法)
  }

  private parseRefinement(content: string): RefinedSection {
    try {
      const data = JSON.parse(content)
      return {
        heading: data.heading,
        summary: data.summary,
        keyPoints: data.keyPoints,
        refinedContent: data.refinedContent
      }
    } catch (error) {
      throw new Error('AI返回结果解析失败')
    }
  }
}
```

### 控制器

```typescript
// backend/analysis/refinement.controller.ts
import { Controller, Post, Body, UseGuards } from '@nestjs/common'
import { RefinementService } from './refinement.service'
import { ApiKeyGuard } from '@/auth/guards/api-key.guard'

@Controller('analysis/refinement')
@UseGuards(ApiKeyGuard)
export class RefinementController {
  constructor(private readonly refinementService: RefinementService) {}

  @Post()
  async refine(@Body() dto: RefinementDto) {
    const result = await this.refinementService.refine(
      dto.content,
      dto.options
    )
    return {
      success: true,
      data: result
    }
  }
}
```

## API接口

### 请求示例

```http
POST /api/analysis/refinement
Content-Type: application/json
X-API-Key: your-api-key

{
  "content": "# 微服务架构设计\n\n微服务架构是一种...",
  "options": {
    "maxCompressionRatio": 0.4,
    "minKeyPoints": 5
  }
}
```

### 响应示例

```json
{
  "success": true,
  "data": {
    "title": "微服务架构设计",
    "summary": "微服务架构通过拆分复杂应用为独立小服务,实现灵活部署和扩展",
    "structure": [
      {
        "level": 1,
        "heading": "核心特征",
        "summary": "微服务的五大核心特点",
        "keyPoints": [
          {
            "text": "**每个服务运行在独立进程中**",
            "importance": 0.95,
            "type": "definition"
          },
          {
            "text": "__使用轻量级机制(HTTP API)通信__",
            "importance": 0.9,
            "type": "definition"
          }
        ],
        "refinedContent": "**核心特征**:\n\n1. **独立进程**: 每个服务运行在自己的进程中\n2. __轻量通信__: 使用HTTP API进行服务间通信\n3. 业务驱动: 围绕业务能力构建服务\n"
      }
    ],
    "statistics": {
      "originalLength": 5000,
      "refinedLength": 2000,
      "compressionRatio": 0.4,
      "keyPointsCount": 15
    }
  }
}
```

## 优化建议

### 1. 提高提炼质量

- 建立不同领域的提炼规则库
- 使用用户反馈持续优化提炼算法
- 支持自定义提炼偏好(更详细/更简洁)

### 2. 性能优化

- 对长文章分章节并行处理
- 缓存常见句式和表达模式
- 使用流式AI响应,边生成边展示

### 3. 用户体验增强

- 支持手动调整提炼结果
- 提供提炼历史版本对比
- 导出为PDF/Word文档

### 4. 智能交互

- 支持用户点击重点查看原文对应位置
- 提供提炼程度滑块(30%-70%)
- 根据阅读时长自动调整提炼密度

---

其他核心功能文档:
- [易读性评分](/guide/features/readability)
- [智能扩展](/guide/features/expansion)
- [溯源校验](/guide/features/verification)
