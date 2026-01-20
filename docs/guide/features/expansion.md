# 智能扩展

智能扩展是AI-NoteBook的核心功能之一,基于文章重点内容自动补充相关知识、技术背景和应用案例,帮助用户深入理解文章主题。

## 功能概述

智能扩展功能能够:
- **识别扩展点**: 自动判断哪些内容值得扩展(技术概念、前沿趋势、关联技术等)
- **知识补充**: 提供技术背景、发展历史、应用场景等信息
- **关联推荐**: 推荐相关的技术、工具、学习资源
- **案例丰富**: 补充实际应用案例和最佳实践

## 扩展策略

### 1. 扩展点识别

**识别规则**:

```typescript
interface ExpansionPoint {
  type: 'concept' | 'technology' | 'tool' | 'trend' | 'practice'
  text: string
  importance: number
  context: string
  expansionNeeded: boolean
}

interface ExpansionRule {
  pattern: RegExp
  type: ExpansionPoint['type']
  minImportance: number
  examples: string[]
}

const expansionRules: ExpansionRule[] = [
  // 技术概念
  {
    pattern: /(?:(?:微服务|容器化|服务网格|Serverless|云原生|DevOps)/gi,
    type: 'concept',
    minImportance: 0.7,
    examples: ['微服务架构', '容器化部署', '服务网格']
  },
  // 前沿技术
  {
    pattern: /(?:(?:AI|人工智能|机器学习|深度学习|大语言模型|Web3|区块链)/gi,
    type: 'trend',
    minImportance: 0.8,
    examples: ['大语言模型', 'AI应用', 'Web3技术']
  },
  // 开发工具
  {
    pattern: /(?:Docker|Kubernetes|Redis|MongoDB|GraphQL|gRPC)/gi,
    type: 'tool',
    minImportance: 0.6,
    examples: ['Docker容器', 'Kubernetes编排', 'Redis缓存']
  }
]

function identifyExpansionPoints(section: Section): ExpansionPoint[] {
  const points: ExpansionPoint[] = []

  for (const rule of expansionRules) {
    const matches = section.content.match(rule.pattern)
    if (matches) {
      matches.forEach(match => {
        const point: ExpansionPoint = {
          type: rule.type,
          text: match,
          importance: calculateImportance(match, section),
          context: extractContext(match, section.content),
          expansionNeeded: true
        }

        if (point.importance >= rule.minImportance) {
          points.push(point)
        }
      })
    }
  }

  return points
}

function calculateImportance(keyword: string, section: Section): number {
  let score = 0.5

  // 在标题中出现 -> 重要性高
  if (section.heading.includes(keyword)) {
    score += 0.3
  }

  // 在关键点中出现 -> 重要性高
  if (section.keyPoints?.some(kp => kp.text.includes(keyword))) {
    score += 0.2
  }

  // 出现频率高 -> 重要性高
  const frequency = (section.content.match(new RegExp(keyword, 'gi')) || []).length
  score += Math.min(frequency * 0.05, 0.2)

  return Math.min(score, 1.0)
}
```

### 2. 扩展内容生成

**扩展维度**:

```typescript
interface ExpansionContent {
  point: string
  type: string
  expansions: Expansion[]
}

interface Expansion {
  category: string
  title: string
  content: string
  source: string
  confidence: number
}

enum ExpansionCategory {
  Background = '技术背景',      // 发展历史、基本原理
  Applications = '应用场景',    // 实际应用案例
  RelatedTech = '关联技术',     // 相关技术栈
  Trends = '发展趋势',         // 前景和趋势
  Resources = '学习资源',       // 文档、教程、工具
  BestPractices = '最佳实践'    // 经验和技巧
}

async function generateExpansion(point: ExpansionPoint): Promise<ExpansionContent> {
  const expansions: Expansion[] = []

  // 1. 生成技术背景
  if (point.type === 'concept' || point.type === 'technology') {
    const background = await generateBackground(point)
    expansions.push(background)
  }

  // 2. 生成应用场景
  const applications = await generateApplications(point)
  expansions.push(applications)

  // 3. 生成关联技术
  const related = await generateRelatedTech(point)
  expansions.push(related)

  // 4. 生成发展趋势(仅前沿技术)
  if (point.type === 'trend') {
    const trends = await generateTrends(point)
    expansions.push(trends)
  }

  // 5. 生成学习资源
  const resources = await generateResources(point)
  expansions.push(resources)

  return {
    point: point.text,
    type: point.type,
    expansions
  }
}
```

### 3. 联网搜索增强

**搜索策略**:

```typescript
interface SearchResult {
  title: string
  url: string
  snippet: string
  relevance: number
}

async function searchWithWebAPI(
  keyword: string,
  context: string
): Promise<SearchResult[]> {
  const apiKey = process.env.WEB_SEARCH_API_KEY
  const searchEngine = 'search_pro_quark'

  const query = buildSearchQuery(keyword, context)

  const response = await fetch('https://api.example.com/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`
    },
    body: JSON.stringify({
      search_engine: searchEngine,
      search_intent: true,
      query: query,
      num_results: 5
    })
  })

  const data = await response.json()

  return data.results.map((r: any) => ({
    title: r.title,
    url: r.url,
    snippet: r.snippet,
    relevance: calculateRelevance(r, keyword)
  }))
}

function buildSearchQuery(keyword: string, context: string): string {
  // 根据上下文构建更精准的搜索query
  const contextHints = {
    concept: '什么是 原理 特点',
    technology: '技术架构 应用场景 优势',
    tool: '使用教程 最佳实践 案例',
    trend: '发展趋势 未来 应用前景'
  }

  const hint = contextHints[keyword.type] || ''
  return `${keyword} ${hint}`
}
```

## AI提示词模板

```markdown
你是一个技术知识扩展专家。请为以下关键概念提供深度扩展:

## 扩展点
{{keyword}}

## 上下文信息
- 类型: {{type}}
- 出现位置: {{context}}
- 重要性: {{importance}}

## 扩展要求

### 1. 技术背景 (必需)
- 发展历史和里程碑
- 核心原理和机制
- 解决的核心问题
- 与传统方案的对比

### 2. 应用场景 (必需)
- 典型应用案例(至少3个)
- 适用场景分析
- 成功案例和失败教训
- 行业应用情况

### 3. 关联技术 (必需)
- 相关技术栈和工具
- 技术生态
- 可替代方案
- 技术选型建议

### 4. 发展趋势 (可选,仅前沿技术)
- 最新进展和版本
- 未来发展方向
- 潜在挑战和机遇
- 社区活跃度

### 5. 学习资源 (必需)
- 官方文档和网站
- 推荐书籍和课程
- 开源项目和示例
- 社区和论坛

## 输出格式

请以JSON格式返回扩展内容:

```json
{
  "keyword": "微服务架构",
  "background": {
    "title": "技术背景",
    "content": "微服务架构是一种...",
    "timeline": ["2014年: Martin Fowler提出定义", "2015年: Spring Cloud发布"],
    "sources": ["https://martinfowler.com/articles/microservices.html"]
  },
  "applications": {
    "title": "应用场景",
    "cases": [
      {
        "name": "Netflix",
        "description": "Netflix从单体架构迁移到微服务,处理每天数十亿次流媒体请求",
        "lessons": "强调了服务发现、容错机制的重要性"
      },
      {
        "name": "Uber",
        "description": "Uber使用微服务支撑全球业务扩张",
        "lessons": "需要完善的服务治理和监控体系"
      }
    ]
  },
  "relatedTech": {
    "title": "关联技术",
    "technologies": [
      {
        "name": "容器化 (Docker)",
        "relationship": "微服务部署的标准方式",
        "description": "提供环境一致性和快速部署能力"
      },
      {
        "name": "服务网格 (Istio)",
        "relationship": "微服务通信的基础设施层",
        "description": "提供服务发现、负载均衡、流量管理等"
      }
    ]
  },
  "trends": {
    "title": "发展趋势",
    "points": [
      "服务网格成为微服务通信标准",
      "Serverless进一步简化微服务部署",
      "微服务治理平台智能化"
    ],
    "sources": ["https://example.com/trends"]
  },
  "resources": {
    "title": "学习资源",
    "links": [
      {
        "name": "Spring Cloud官方文档",
        "url": "https://spring.io/projects/spring-cloud",
        "type": "官方文档",
        "level": "入门-进阶"
      },
      {
        "name": "《微服务架构设计模式》",
        "author": "Chris Richardson",
        "type": "书籍",
        "level": "进阶"
      }
    ]
  }
}
```

## 扩展质量控制

### 1. 相关性过滤

```typescript
function filterRelevantExpansions(
  expansions: Expansion[],
  originalContext: string
): Expansion[] {
  return expansions.filter(expansion => {
    // 检查与原文的相关性
    const similarity = calculateSimilarity(
      expansion.content,
      originalContext
    )

    // 检查内容质量
    const quality = assessQuality(expansion)

    return similarity > 0.3 && quality > 0.6
  })
}

function calculateSimilarity(text1: string, text2: string): number {
  // 使用余弦相似度或Jaccard相似度
  const tokens1 = tokenize(text1)
  const tokens2 = tokenize(text2)

  const intersection = tokens1.filter(t => tokens2.includes(t))
  const union = [...new Set([...tokens1, ...tokens2])]

  return intersection.length / union.length
}
```

### 2. 冗余去除

```typescript
function removeRedundancy(expansions: Expansion[]): Expansion[] {
  const unique: Expansion[] = []

  for (const expansion of expansions) {
    const isDuplicate = unique.some(u =>
      calculateSimilarity(u.content, expansion.content) > 0.8
    )

    if (!isDuplicate) {
      unique.push(expansion)
    }
  }

  return unique
}
```

## 前端展示

### 组件设计

```vue
<template>
  <div class="expansion-panel">
    <!-- 扩展点列表 -->
    <div class="expansion-points">
      <n-tag
        v-for="point in expansionPoints"
        :key="point.text"
        :type="getTypeColor(point.type)"
        :bordered="false"
        size="medium"
        class="point-tag"
        @click="selectPoint(point)"
      >
        <template #icon>
          <n-icon :component="getIcon(point.type)" />
        </template>
        {{ point.text }}
        <n-badge :value="point.expansionCount" :max="99" />
      </n-tag>
    </div>

    <!-- 扩展内容展示 -->
    <n-card v-if="selectedPoint" class="expansion-content">
      <template #header>
        <div class="header-left">
          <n-icon :component="getIcon(selectedPoint.type)" size="20" />
          <h2>{{ selectedPoint.text }}</h2>
          <n-tag :type="getTypeColor(selectedPoint.type)" size="small">
            {{ getTypeLabel(selectedPoint.type) }}
          </n-tag>
        </div>
        <div class="header-right">
          <n-button text @click="copyAll">
            <template #icon>
              <n-icon :component="CopyIcon" />
            </template>
            复制全部
          </n-button>
        </div>
      </template>

      <!-- 扩展分类Tabs -->
      <n-tabs type="card" animated>
        <n-tab-pane
          v-for="expansion in selectedPoint.expansions"
          :key="expansion.category"
          :name="expansion.category"
          :tab="expansion.category"
        >
          <div class="expansion-detail">
            <!-- 技术背景 -->
            <template v-if="expansion.category === '技术背景'">
              <div class="background-section">
                <h3>{{ expansion.title }}</h3>
                <p>{{ expansion.content }}</p>

                <!-- 发展时间线 -->
                <n-timeline v-if="expansion.timeline">
                  <n-timeline-item
                    v-for="(event, index) in expansion.timeline"
                    :key="index"
                    :title="event"
                  />
                </n-timeline>

                <!-- 来源标注 -->
                <div class="sources" v-if="expansion.sources">
                  <n-text depth="3">来源:</n-text>
                  <n-a
                    v-for="(source, index) in expansion.sources"
                    :key="index"
                    :href="source"
                    target="_blank"
                    class="source-link"
                  >
                    {{ formatUrl(source) }}
                  </n-a>
                </div>
              </div>
            </template>

            <!-- 应用场景 -->
            <template v-else-if="expansion.category === '应用场景'">
              <div class="applications-section">
                <n-collapse>
                  <n-collapse-item
                    v-for="(case, index) in expansion.cases"
                    :key="index"
                    :title="case.name"
                  >
                    <template #header-extra>
                      <n-tag size="small" type="info">案例</n-tag>
                    </template>

                    <p>{{ case.description }}</p>

                    <n-alert v-if="case.lessons" type="success" :bordered="false">
                      <template #header>经验教训</template>
                      {{ case.lessons }}
                    </n-alert>
                  </n-collapse-item>
                </n-collapse>
              </div>
            </template>

            <!-- 关联技术 -->
            <template v-else-if="expansion.category === '关联技术'">
              <div class="related-section">
                <div
                  v-for="(tech, index) in expansion.technologies"
                  :key="index"
                  class="tech-card"
                >
                  <div class="tech-header">
                    <h4>{{ tech.name }}</h4>
                    <n-tag size="tiny">{{ tech.relationship }}</n-tag>
                  </div>
                  <p>{{ tech.description }}</p>
                </div>
              </div>
            </template>

            <!-- 发展趋势 -->
            <template v-else-if="expansion.category === '发展趋势'">
              <div class="trends-section">
                <n-list>
                  <n-list-item v-for="(point, index) in expansion.points" :key="index">
                    <n-thing>
                      <template #header>{{ point }}</template>
                    </n-thing>
                  </n-list-item>
                </n-list>

                <div class="sources" v-if="expansion.sources">
                  <n-text depth="3">来源:</n-text>
                  <n-a
                    v-for="(source, index) in expansion.sources"
                    :key="index"
                    :href="source"
                    target="_blank"
                  >
                    {{ formatUrl(source) }}
                  </n-a>
                </div>
              </div>
            </template>

            <!-- 学习资源 -->
            <template v-else-if="expansion.category === '学习资源'">
              <div class="resources-section">
                <div
                  v-for="(resource, index) in expansion.links"
                  :key="index"
                  class="resource-item"
                >
                  <div class="resource-header">
                    <n-icon :component="getResourceIcon(resource.type)" />
                    <h4>{{ resource.name }}</h4>
                    <n-tag size="small" type="info">{{ resource.type }}</n-tag>
                    <n-tag size="small" type="warning">{{ resource.level }}</n-tag>
                  </div>
                  <n-a :href="resource.url" target="_blank">
                    {{ resource.url }}
                  </n-a>
                </div>
              </div>
            </template>

            <!-- 最佳实践 -->
            <template v-else-if="expansion.category === '最佳实践'">
              <div class="practices-section">
                <n-collapse>
                  <n-collapse-item
                    v-for="(practice, index) in expansion.practices"
                    :key="index"
                    :title="practice.title"
                  >
                    <p>{{ practice.description }}</p>

                    <n-code v-if="practice.code" :code="practice.code" language="typescript" />

                    <n-alert v-if="practice.warning" type="warning">
                      {{ practice.warning }}
                    </n-alert>
                  </n-collapse-item>
                </n-collapse>
              </div>
            </template>
          </div>
        </n-tab-pane>
      </n-tabs>
    </n-card>

    <!-- 空状态 -->
    <n-empty
      v-else
      description="选择一个扩展点查看详细内容"
      :icon="null"
      class="empty-state"
    >
      <template #extra>
        <n-text depth="3">点击上方标签查看AI扩展内容</n-text>
      </template>
    </n-empty>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import {
  NTabs, NTabPane, NCard, NTag, NIcon, NButton,
  NTimeline, NTimelineItem, NCollapse, NCollapseItem,
  NAlert, NList, NListItem, NThing, NCode, NA,
  NText, NEmpty, NBadge
} from 'naive-ui'

interface Props {
  expansionData: ExpansionContent[]
}

const props = defineProps<Props>()

const selectedPoint = ref<ExpansionContent | null>(null)

const expansionPoints = computed(() => props.expansionData.map(data => ({
  text: data.point,
  type: data.type,
  expansionCount: data.expansions.length,
  ...data
})))

function selectPoint(point: ExpansionContent) {
  selectedPoint.value = point
}

function getTypeColor(type: string): 'success' | 'info' | 'warning' | 'error' | 'default' {
  const colors = {
    concept: 'info',
    technology: 'success',
    tool: 'warning',
    trend: 'error',
    practice: 'default'
  }
  return colors[type] || 'default'
}

function getTypeLabel(type: string): string {
  const labels = {
    concept: '概念',
    technology: '技术',
    tool: '工具',
    trend: '趋势',
    practice: '实践'
  }
  return labels[type] || type
}

function getIcon(type: string) {
  const icons = {
    concept: LightbulbIcon,
    technology: CpuIcon,
    tool: WrenchIcon,
    trend: TrendingUpIcon,
    practice: CheckCircleIcon
  }
  return icons[type] || CircleIcon
}

function getResourceIcon(type: string) {
  const icons = {
    '官方文档': BookIcon,
    '书籍': BookOpenIcon,
    '课程': VideoIcon,
    '教程': FileTextIcon,
    '工具': DownloadIcon
  }
  return icons[type] || LinkIcon
}

function formatUrl(url: string): string {
  try {
    const urlObj = new URL(url)
    return urlObj.hostname
  } catch {
    return url
  }
}

async function copyAll() {
  if (!selectedPoint.value) return

  const text = selectedPoint.value.expansions
    .map(e => `## ${e.category}\n\n${e.content}`)
    .join('\n\n')

  await navigator.clipboard.writeText(text)

  // 显示复制成功提示
  message.success('已复制到剪贴板')
}
</script>

<style scoped>
.expansion-panel {
  padding: 20px;
}

.expansion-points {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 24px;
}

.point-tag {
  cursor: pointer;
  transition: all 0.3s;
}

.point-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.expansion-content {
  margin-top: 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-left h2 {
  margin: 0;
  font-size: 20px;
}

.header-right {
  display: flex;
  gap: 8px;
}

.expansion-detail {
  padding: 16px 0;
}

/* 技术背景样式 */
.background-section {
  max-width: 800px;
}

.timeline {
  margin: 24px 0;
}

.sources {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.source-link {
  color: #3b82f6;
  text-decoration: none;
}

.source-link:hover {
  text-decoration: underline;
}

/* 应用场景样式 */
.applications-section {
  max-width: 900px;
}

/* 关联技术样式 */
.related-section {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.tech-card {
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #f9fafb;
}

.tech-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.tech-header h4 {
  margin: 0;
  flex: 1;
}

/* 学习资源样式 */
.resources-section {
  display: grid;
  gap: 16px;
}

.resource-item {
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  transition: all 0.3s;
}

.resource-item:hover {
  border-color: #3b82f6;
  background: #eff6ff;
}

.resource-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.resource-header h4 {
  margin: 0;
  flex: 1;
}

.empty-state {
  padding: 60px 20px;
}
</style>
```

## 后端实现

### Service层

```typescript
// backend/analysis/expansion.service.ts
import { Injectable } from '@nestjs/common'
import { AiService } from '@/ai/ai.service'
import { WebSearchService } from '@/web-search/web-search.service'

interface ExpansionConfig {
  maxPointsPerSection: number    // 每节最多扩展点数
  maxExpansionsPerPoint: number  // 每点最多扩展数
  enableWebSearch: boolean        // 是否启用联网搜索
  minRelevanceScore: number       // 最小相关性分数
}

@Injectable()
export class ExpansionService {
  private readonly config: ExpansionConfig = {
    maxPointsPerSection: 5,
    maxExpansionsPerPoint: 10,
    enableWebSearch: true,
    minRelevanceScore: 0.3
  }

  constructor(
    private readonly aiService: AiService,
    private readonly webSearchService: WebSearchService
  ) {}

  async expand(
    sections: Section[],
    options?: Partial<ExpansionConfig>
  ): Promise<ExpansionContent[]> {
    const config = { ...this.config, ...options }
    const results: ExpansionContent[] = []

    for (const section of sections) {
      // 1. 识别扩展点
      const points = this.identifyExpansionPoints(section)
        .slice(0, config.maxPointsPerSection)

      // 2. 为每个扩展点生成内容
      for (const point of points) {
        const expansion = await this.generateExpansion(point, config)
        results.push(expansion)
      }
    }

    return results
  }

  private async generateExpansion(
    point: ExpansionPoint,
    config: ExpansionConfig
  ): Promise<ExpansionContent> {
    // 1. 使用AI生成基础扩展
    const aiExpansion = await this.expandWithAI(point)

    // 2. 如果启用联网搜索,补充实时信息
    let webExpansion: Expansion[] = []
    if (config.enableWebSearch) {
      webExpansion = await this.expandWithWeb(point)
    }

    // 3. 合并并去重
    const merged = this.mergeExpansions(aiExpansion, webExpansion)

    // 4. 过滤低质量内容
    const filtered = this.filterByQuality(merged, point.context, config)

    return {
      point: point.text,
      type: point.type,
      expansions: filtered.slice(0, config.maxExpansionsPerPoint)
    }
  }

  private async expandWithAI(point: ExpansionPoint): Promise<Expansion[]> {
    const prompt = this.buildExpansionPrompt(point)

    const result = await this.aiService.chat({
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.4,
      responseFormat: { type: 'json_object' }
    })

    return this.parseExpansion(result.content)
  }

  private async expandWithWeb(point: ExpansionPoint): Promise<Expansion[]> {
    const searchResults = await this.webSearchService.search(
      point.text,
      {
        numResults: 5,
        searchIntent: true
      }
    )

    // 基于搜索结果生成扩展
    const expansions: Expansion[] = []

    for (const result of searchResults) {
      const expansion = await this.summarizeSearchResult(result, point)
      if (expansion) {
        expansions.push(expansion)
      }
    }

    return expansions
  }

  private buildExpansionPrompt(point: ExpansionPoint): string {
    return `
你是一个技术知识扩展专家。请为以下关键概念提供深度扩展:

## 扩展点
${point.text}

## 上下文
${point.context}

## 扩展要求

请提供以下维度的扩展内容(JSON格式):

1. **技术背景**: 发展历史、核心原理、解决的问题
2. **应用场景**: 典型案例(至少3个)、适用场景、经验教训
3. **关联技术**: 相关技术栈、工具、替代方案
4. **学习资源**: 官方文档、推荐书籍、开源项目
5. **最佳实践** (可选): 使用技巧、注意事项

## 输出格式

```json
{
  "background": {
    "title": "技术背景",
    "content": "详细说明...",
    "timeline": ["2014年: 事件", "2015年: 事件"],
    "sources": ["https://example.com"]
  },
  "applications": {
    "title": "应用场景",
    "cases": [
      {
        "name": "案例名称",
        "description": "详细描述",
        "lessons": "经验教训"
      }
    ]
  },
  "relatedTech": {
    "title": "关联技术",
    "technologies": [
      {
        "name": "技术名称",
        "relationship": "关系描述",
        "description": "技术说明"
      }
    ]
  },
  "resources": {
    "title": "学习资源",
    "links": [
      {
        "name": "资源名称",
        "url": "https://example.com",
        "type": "官方文档",
        "level": "入门"
      }
    ]
  }
}
```
    `
  }

  private async summarizeSearchResult(
    result: SearchResult,
    point: ExpansionPoint
  ): Promise<Expansion | null> {
    const prompt = `
请基于以下搜索结果,为"${point.text}"生成扩展内容:

## 搜索结果
标题: ${result.title}
链接: ${result.url}
摘要: ${result.snippet}

## 要求
- 提取关键信息,生成简明的扩展内容
- 判断内容类型(技术背景/应用场景/关联技术/学习资源)
- 确保内容与原文相关
- 标注来源

请返回JSON格式:
{
  "category": "内容类型",
  "title": "标题",
  "content": "扩展内容(100-200字)",
  "source": "来源URL",
  "confidence": 0.8
}
    `

    const aiResult = await this.aiService.chat({
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.3,
      responseFormat: { type: 'json_object' }
    })

    const data = JSON.parse(aiResult.content)

    // 检查相关性
    if (data.confidence < 0.5) {
      return null
    }

    return {
      category: data.category,
      title: data.title,
      content: data.content,
      source: data.source,
      confidence: data.confidence
    }
  }

  private mergeExpansions(
    aiExpansions: Expansion[],
    webExpansions: Expansion[]
  ): Expansion[] {
    // 按category分组
    const grouped = new Map<string, Expansion[]>()

    for (const expansion of [...aiExpansions, ...webExpansions]) {
      if (!grouped.has(expansion.category)) {
        grouped.set(expansion.category, [])
      }
      grouped.get(expansion.category)!.push(expansion)
    }

    // 去重(相似度>0.8视为重复)
    const unique: Expansion[] = []

    for (const [category, items] of grouped) {
      const deduped = items.filter((item, index) => {
        return !items.slice(0, index).some(other =>
          this.calculateSimilarity(other.content, item.content) > 0.8
        )
      })

      unique.push(...deduped)
    }

    return unique
  }

  private filterByQuality(
    expansions: Expansion[],
    context: string,
    config: ExpansionConfig
  ): Expansion[] {
    return expansions.filter(expansion => {
      // 相关性检查
      const relevance = this.calculateSimilarity(expansion.content, context)
      if (relevance < config.minRelevanceScore) {
        return false
      }

      // 质量检查
      const quality = this.assessQuality(expansion)
      if (quality < 0.6) {
        return false
      }

      return true
    })
  }

  private calculateSimilarity(text1: string, text2: string): number {
    // 简化的余弦相似度计算
    const tokens1 = new Set(this.tokenize(text1))
    const tokens2 = new Set(this.tokenize(text2))

    const intersection = [...tokens1].filter(t => tokens2.has(t))
    const union = new Set([...tokens1, ...tokens2])

    return intersection.length / union.size
  }

  private assessQuality(expansion: Expansion): number {
    let score = 0.5

    // 有来源 -> 质量高
    if (expansion.source) {
      score += 0.2
    }

    // 内容长度适中
    const length = expansion.content.length
    if (length >= 50 && length <= 500) {
      score += 0.2
    }

    // 置信度高
    if (expansion.confidence > 0.7) {
      score += 0.1
    }

    return Math.min(score, 1.0)
  }

  private tokenize(text: string): string[] {
    return text
      .toLowerCase()
      .replace(/[^\u4e00-\u9fa5a-z0-9]/g, ' ')
      .split(/\s+/)
      .filter(t => t.length > 1)
  }

  private parseExpansion(content: string): Expansion[] {
    try {
      const data = JSON.parse(content)
      const expansions: Expansion[] = []

      for (const [key, value] of Object.entries(data)) {
        if (value && typeof value === 'object') {
          expansions.push({
            category: (value as any).title || key,
            title: (value as any).title,
            content: (value as any).content || JSON.stringify(value),
            source: (value as any).source,
            confidence: 0.8
          })
        }
      }

      return expansions
    } catch (error) {
      throw new Error('AI返回结果解析失败')
    }
  }

  private identifyExpansionPoints(section: Section): ExpansionPoint[] {
    // (前面已实现的识别逻辑)
    return []
  }
}
```

### 控制器

```typescript
// backend/analysis/expansion.controller.ts
import { Controller, Post, Body, UseGuards } from '@nestjs/common'
import { ExpansionService } from './expansion.service'
import { ApiKeyGuard } from '@/auth/guards/api-key.guard'

@Controller('analysis/expansion')
@UseGuards(ApiKeyGuard)
export class ExpansionController {
  constructor(private readonly expansionService: ExpansionService) {}

  @Post()
  async expand(@Body() dto: ExpansionDto) {
    const result = await this.expansionService.expand(
      dto.sections,
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
POST /api/analysis/expansion
Content-Type: application/json
X-API-Key: your-api-key

{
  "sections": [
    {
      "heading": "微服务架构",
      "content": "微服务架构是一种...",
      "level": 1
    }
  ],
  "options": {
    "maxPointsPerSection": 5,
    "enableWebSearch": true
  }
}
```

### 响应示例

```json
{
  "success": true,
  "data": [
    {
      "point": "微服务架构",
      "type": "concept",
      "expansions": [
        {
          "category": "技术背景",
          "title": "技术背景",
          "content": "微服务架构起源于2014年...",
          "source": "https://martinfowler.com/articles/microservices.html",
          "confidence": 0.9
        },
        {
          "category": "应用场景",
          "title": "应用场景",
          "content": "Netflix、Uber等大型互联网公司...",
          "source": "https://example.com/cases",
          "confidence": 0.85
        }
      ]
    }
  ]
}
```

## 优化建议

### 1. 提高扩展质量

- 建立技术知识图谱,确保扩展内容准确
- 使用多个数据源交叉验证
- 收集用户反馈,持续优化扩展策略

### 2. 性能优化

- 对常见技术术语缓存扩展结果
- 并行处理多个扩展点
- 使用流式响应,边生成边展示

### 3. 用户体验增强

- 支持用户自定义扩展偏好
- 允许用户编辑和补充扩展内容
- 提供扩展内容的置信度指示

### 4. 智能推荐

- 基于用户阅读历史推荐扩展内容
- 根据文章难度自动调整扩展深度
- 提供个性化学习路径

---

其他核心功能文档:
- [易读性评分](/guide/features/readability)
- [内容提炼](/guide/features/refinement)
- [溯源校验](/guide/features/verification)
