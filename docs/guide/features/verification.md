# 溯源校验

溯源校验是AI-NoteBook的核心功能之一,通过联网搜索、多源交叉验证和智能分析,确保文章内容的准确性和可靠性,为用户提供可信赖的信息。

## 功能概述

溯源校验功能能够:
- **事实核查**: 验证文章中的数据、事实陈述的真实性
- **来源追溯**: 查找信息的原始出处和权威来源
- **多源验证**: 对比多个数据源,交叉验证信息准确性
- **可信度评分**: 基于来源权威性给出内容可信度评级
- **更新提醒**: 检测内容是否过时,提示最新信息

## 校验策略

### 1. 校验点识别

```typescript
interface VerificationPoint {
  type: 'fact' | 'data' | 'quote' | 'date' | 'technical_claim'
  text: string
  confidence: number
  verifiable: boolean
  context: string
}

interface VerificationRule {
  pattern: RegExp
  type: VerificationPoint['type']
  priority: 'high' | 'medium' | 'low'
}

const verificationRules: VerificationRule[] = [
  // 数据统计
  {
    pattern: /(?:超过|超过于|约|大约|接近|达到)\s*(\d+(?:\.\d+)?)\s*(?:万|亿|千|百|%|个百分点)/g,
    type: 'data',
    priority: 'high'
  },
  // 技术版本
  {
    pattern: /\b[vV]?\d+\.\d+(?:\.\d+)?\b/g,
    type: 'technical_claim',
    priority: 'medium'
  },
  // 引用言论
  {
    pattern: /(?:据报道|据.*透露|.*表示|.*称|.*指出)/g,
    type: 'quote',
    priority: 'high'
  },
  // 时间日期
  {
    pattern: /\d{4}年\d{1,2}月|\d{4}-\d{1,2}-\d{1,2}/g,
    type: 'date',
    priority: 'medium'
  },
  // 事实陈述
  {
    pattern: /(?:首个|第一|首次|唯一|全球|世界|领先|突破)/g,
    type: 'fact',
    priority: 'high'
  }
]

function identifyVerificationPoints(content: string): VerificationPoint[] {
  const points: VerificationPoint[] = []

  for (const rule of verificationRules) {
    const matches = content.matchAll(rule.pattern)

    for (const match of matches) {
      const point: VerificationPoint = {
        type: rule.type,
        text: match[0],
        confidence: calculateConfidence(match[0], content),
        verifiable: true,
        context: extractContext(match.index, content)
      }

      points.push(point)
    }
  }

  return points
}

function calculateConfidence(text: string, content: string): number {
  let score = 0.5

  // 包含具体数字 -> 可信度高
  if (/\d+/.test(text)) {
    score += 0.2
  }

  // 在重点内容中出现 -> 重要性强
  if (content.includes(`**${text}**`) || content.includes(`__${text}__`)) {
    score += 0.2
  }

  // 有引用来源标注 -> 可验证性强
  if (content.includes('[]') || content.includes('[]:')) {
    score += 0.1
  }

  return Math.min(score, 1.0)
}
```

### 2. 联网搜索验证

```typescript
interface SearchResult {
  url: string
  title: string
  snippet: string
  publishedDate?: string
  author?: string
  domain: string
  authority: number
}

interface VerificationResult {
  point: VerificationPoint
  verified: boolean
  sources: SearchResult[]
  confidence: number
  discrepancy?: string
  suggestions?: string[]
}

async function verifyPoint(
  point: VerificationPoint,
  webSearchAPI: WebSearchAPI
): Promise<VerificationResult> {
  // 1. 构建搜索query
  const query = buildVerificationQuery(point)

  // 2. 执行搜索
  const searchResults = await webSearchAPI.search({
    query,
    searchEngine: 'search_pro_quark',
    searchIntent: true,
    numResults: 5
  })

  // 3. 分析结果
  const analysis = analyzeSearchResults(searchResults, point)

  return {
    point,
    verified: analysis.verified,
    sources: analysis.sources,
    confidence: analysis.confidence,
    discrepancy: analysis.discrepancy,
    suggestions: analysis.suggestions
  }
}

function buildVerificationQuery(point: VerificationPoint): string {
  const templates = {
    data: `"${
      point.text
    }" 数据统计 官方报告`,
    technical_claim: `${point.text} 版本 更新 发布`,
    quote: `${point.text} 原文 出处`,
    date: `${point.text} 发布 时间`,
    fact: `"${point.text}" 是真的吗 真伪`
  }

  return templates[point.type] || point.text
}

function analyzeSearchResults(
  results: SearchResult[],
  point: VerificationPoint
): VerificationAnalysis {
  let verifiedCount = 0
  let totalCount = results.length
  const discrepancies: string[] = []
  const credibleSources: SearchResult[] = []

  for (const result of results) {
    // 检查域名权威性
    if (isCredibleDomain(result.domain)) {
      credibleSources.push(result)
    }

    // 检查结果是否支持原文
    if (supportsClaim(result, point)) {
      verifiedCount++
    } else {
      discrepancies.push(extractDiscrepancy(result, point))
    }
  }

  const verificationRatio = verifiedCount / totalCount
  const authorityScore = calculateAuthorityScore(credibleSources)

  return {
    verified: verificationRatio > 0.6,
    sources: credibleSources.slice(0, 3),
    confidence: (verificationRatio * 0.6 + authorityScore * 0.4),
    discrepancy: discrepancies.length > 0 ? discrepancies[0] : undefined,
    suggestions: generateSuggestions(discrepancies, point)
  }
}

function isCredibleDomain(domain: string): boolean {
  const credibleDomains = [
    // 政府机构
    /\.gov\.cn$/,
    /\.gov$/,
    // 国际组织
    /\.org$/,
    // 权威媒体
    /(xinhuanet|people|cctv)\.com$/,
    // 官方网站
    /(mozilla|google|microsoft|apple)\.com$/,
    // 学术机构
    /\.edu\.cn$/,
    /\.edu$/
  ]

  return credibleDomains.some(pattern => pattern.test(domain))
}

function calculateAuthorityScore(sources: SearchResult[]): number {
  if (sources.length === 0) return 0.3

  const authorities = sources.map(s => s.authority)
  const avg = authorities.reduce((a, b) => a + b, 0) / authorities.length

  return avg
}
```

### 3. 多源交叉验证

```typescript
interface CrossValidationResult {
  point: VerificationPoint
  verified: boolean
  consensus: number        // 共识度 (0-1)
  conflicting: SearchResult[]
  supporting: SearchResult[]
  neutral: SearchResult[]
}

async function crossValidate(
  point: VerificationPoint,
  sources: SearchResult[]
): Promise<CrossValidationResult> {
  const analysis = await Promise.all(
    sources.map(source => analyzeSource(source, point))
  )

  const supporting = analysis.filter(a => a.stance === 'support')
  const conflicting = analysis.filter(a => a.stance === 'conflict')
  const neutral = analysis.filter(a => a.stance === 'neutral')

  const consensus = supporting.length / (supporting.length + conflicting.length)

  return {
    point,
    verified: consensus > 0.7,
    consensus,
    conflicting: conflicting.map(c => c.source),
    supporting: supporting.map(s => s.source),
    neutral
  }
}

async function analyzeSource(
  source: SearchResult,
  point: VerificationPoint
): Promise<{ stance: 'support' | 'conflict' | 'neutral', source: SearchResult }> {
  // 使用AI判断来源立场
  const prompt = `
判断以下来源是否支持原文陈述:

原文: ${point.text}
来源: ${source.snippet}
链接: ${source.url}

请判断:
- support: 支持原文,内容一致
- conflict: 反驳原文,内容矛盾
- neutral: 中立,未明确表态

返回JSON: {"stance": "support", "reason": "原因说明"}
  `

  const result = await aiService.chat({
    messages: [{ role: 'user', content: prompt }],
    temperature: 0.2,
    responseFormat: { type: 'json_object' }
  })

  const data = JSON.parse(result.content)

  return {
    stance: data.stance,
    source
  }
}
```

### 4. 时效性检查

```typescript
interface TimelinessCheck {
  isOutdated: boolean
  lastUpdate: Date
  timeSinceUpdate: number    // 距上次更新天数
  suggestions: string[]
}

async function checkTimeliness(
  content: string,
  publishDate: Date
): Promise<TimelinessCheck> {
  // 1. 提取时效性敏感信息
  const sensitivePoints = extractTimeSensitiveInfo(content)

  // 2. 搜索最新信息
  const updates = await searchForUpdates(sensitivePoints)

  // 3. 判断是否过时
  const outdatedInfo = updates.filter(u => u.hasUpdate)

  return {
    isOutdated: outdatedInfo.length > 0,
    lastUpdate: publishDate,
    timeSinceUpdate: Date.now() - publishDate.getTime(),
    suggestions: outdatedInfo.map(u => u.updateSuggestion)
  }
}

function extractTimeSensitiveInfo(content: string): string[] {
  const sensitivePatterns = [
    /(?:目前|当前|现在|最新|近期)/g,
    /(?:版本|发布|更新|上线)/g,
    /\d{4}年/g
  ]

  const info: string[] = []

  for (const pattern of sensitivePatterns) {
    const matches = content.match(pattern)
    if (matches) {
      info.push(...matches)
    }
  }

  return [...new Set(info)]
}

async function searchForUpdates(
  keywords: string[]
): Promise<UpdateInfo[]> {
  const updates: UpdateInfo[] = []

  for (const keyword of keywords) {
    const results = await webSearchAPI.search({
      query: `${keyword} 最新 更新 ${new Date().getFullYear()}`,
      searchEngine: 'search_pro_quark',
      searchIntent: true,
      numResults: 3
    })

    // 分析是否有更新
    const hasUpdate = results.some(r =>
      r.snippet.includes('更新') || r.snippet.includes('新版')
    )

    if (hasUpdate) {
      updates.push({
        keyword,
        hasUpdate: true,
        updateSuggestion: `${keyword} 可能有更新版本,建议核实最新信息`,
        sources: results
      })
    }
  }

  return updates
}
```

## AI提示词模板

```markdown
你是一个专业的事实核查专家。请验证以下内容的真实性和可靠性:

## 待验证内容
{{content}}

## 验证要求

### 1. 识别需要验证的陈述
找出以下类型的内容:
- 数据统计(数字、比例、排名等)
- 技术声明(版本号、技术特性等)
- 引用言论(某人说/表示等)
- 事实陈述(首个、第一、首次等)
- 时间日期(发布时间、版本时间等)

### 2. 验证标准
- **可信来源**: 官方网站、权威媒体、学术论文、政府报告
- **数据准确**: 数字、比例、日期等与权威来源一致
- **时效性**: 信息是否最新,是否有更新版本
- **多方印证**: 至少2个可信来源支持该陈述

### 3. 可信度评级
- **高可信度** (90-100%): 多个权威来源支持,数据准确,时效性好
- **中等可信度** (70-89%): 有可信来源支持,但存在一些疑点
- **低可信度** (50-69%): 来源不够权威或存在矛盾
- **不可信** (0-49%): 多个来源反驳或无法验证

### 4. 生成验证报告
对每个验证点:
- 说明验证结果(可信/存疑/不可信)
- 列出支持来源(至少2个)
- 标注重要性(高/中/低)
- 如有矛盾,说明差异
- 给出建议(更新内容/补充来源/删除内容)

## 输出格式

请以JSON格式返回验证结果:

```json
{
  "overall": {
    "credibilityScore": 85,
    "summary": "文章内容基本可信,但部分数据需要更新",
    "verifiedCount": 8,
    "questionableCount": 2,
    "outdatedCount": 1
  },
  "verificationPoints": [
    {
      "text": "根据IDC报告,2023年全球云市场规模达到5000亿美元",
      "type": "data",
      "importance": "high",
      "verified": true,
      "credibility": 90,
      "sources": [
        {
          "url": "https://www.idc.com/",
          "title": "IDC官方报告",
          "domain": "idc.com",
          "authority": 0.95,
          "supporting": true,
          "excerpt": "2023年全球云市场规模达到5000亿美元"
        }
      ],
      "discrepancy": null,
      "suggestions": null
    },
    {
      "text": "Docker是最受欢迎的容器技术",
      "type": "fact",
      "importance": "medium",
      "verified": false,
      "credibility": 60,
      "sources": [
        {
          "url": "https://survey.stackoverflow.co/2023/",
          "title": "Stack Overflow 2023 Survey",
          "domain": "stackoverflow.co",
          "authority": 0.85,
          "supporting": false,
          "excerpt": "Kubernetes已超越Docker成为最受欢迎的容器技术"
        }
      ],
      "discrepancy": "Kubernetes已成为最受欢迎的容器技术",
      "suggestions": "建议更新为:Kubernetes和Docker是最受欢迎的容器技术之一"
    }
  ],
  "timeliness": {
    "checked": true,
    "isOutdated": true,
    "outdatedPoints": [
      {
        "text": "Node.js 14是LTS版本",
        "currentVersion": "Node.js 20 LTS",
        "suggestion": "建议更新为Node.js 20 LTS"
      }
    ]
  }
}
```
```

## 前端展示

### 组件设计

```vue
<template>
  <div class="verification-panel">
    <!-- 总体可信度 -->
    <n-card class="overall-card">
      <div class="overall-score">
        <n-progress
          type="circle"
          :percentage="verificationData.overall.credibilityScore"
          :color="getScoreColor(verificationData.overall.credibilityScore)"
          :stroke-width="12"
          :rail-color="getRailColor()"
        >
          <template #default="{ percentage }">
            <span class="score-number">{{ percentage }}</span>
            <span class="score-label">可信度</span>
          </template>
        </n-progress>

        <div class="overall-info">
          <h3>{{ verificationData.overall.summary }}</h3>
          <n-space>
            <n-statistic label="已验证" :value="verificationData.overall.verifiedCount">
              <template #prefix>
                <n-icon :component="CheckCircleIcon" color="#52c41a" />
              </template>
            </n-statistic>
            <n-statistic label="存疑" :value="verificationData.overall.questionableCount">
              <template #prefix>
                <n-icon :component="QuestionCircleIcon" color="#faad14" />
              </template>
            </n-statistic>
            <n-statistic label="已过时" :value="verificationData.overall.outdatedCount">
              <template #prefix>
                <n-icon :component="UpdateIcon" color="#ff4d4f" />
              </template>
            </n-statistic>
          </n-space>
        </div>
      </div>
    </n-card>

    <!-- 验证点列表 -->
    <n-card class="points-card">
      <template #header>
        <div class="header-content">
          <h3>验证详情</h3>
          <n-space>
            <n-select
              v-model:value="filterType"
              :options="filterOptions"
              size="small"
              style="width: 120px"
            />
            <n-select
              v-model:value="filterImportance"
              :options="importanceOptions"
              size="small"
              style="width: 120px"
            />
          </n-space>
        </div>
      </template>

      <div class="verification-points">
        <div
          v-for="(point, index) in filteredPoints"
          :key="index"
          class="verification-point"
          :class="{
            'verified': point.verified,
            'questionable': !point.verified && point.credibility > 50,
            'unverified': point.credibility <= 50
          }"
        >
          <!-- 验证状态 -->
          <div class="point-status">
            <n-icon
              :component="getStatusIcon(point)"
              :color="getStatusColor(point)"
              size="24"
            />
            <n-tag
              :type="getTypeColor(point.type)"
              size="small"
            >
              {{ getTypeLabel(point.type) }}
            </n-tag>
            <n-tag
              v-if="point.importance === 'high'"
              type="error"
              size="small"
            >
              重要
            </n-tag>
          </div>

          <!-- 待验证内容 -->
          <div class="point-content">
            <p class="point-text">"{{ point.text }}"</p>

            <!-- 可信度 -->
            <div class="credibility-bar">
              <n-progress
                type="line"
                :percentage="point.credibility"
                :color="getScoreColor(point.credibility)"
                :show-indicator="false"
              />
              <span class="credibility-label">{{ point.credibility }}%可信度</span>
            </div>

            <!-- 验证来源 -->
            <n-collapse v-if="point.sources?.length">
              <n-collapse-item title="查看来源">
                <div class="sources-list">
                  <div
                    v-for="(source, sIndex) in point.sources"
                    :key="sIndex"
                    class="source-item"
                  >
                    <div class="source-header">
                      <n-icon :component="LinkIcon" size="16" />
                      <n-a :href="source.url" target="_blank">
                        {{ source.title }}
                      </n-a>
                      <n-tag size="tiny" type="info">
                        {{ source.domain }}
                      </n-tag>
                      <n-progress
                        type="line"
                        :percentage="source.authority * 100"
                        :show-indicator="false"
                        :stroke-width="4"
                        :color="getAuthorityColor(source.authority)"
                      />
                    </div>
                    <p class="source-excerpt">{{ source.excerpt }}</p>
                  </div>
                </div>
              </n-collapse-item>
            </n-collapse>

            <!-- 矛盾说明 -->
            <n-alert
              v-if="point.discrepancy"
              type="warning"
              :bordered="false"
              class="discrepancy-alert"
            >
              <template #header>内容矛盾</template>
              {{ point.discrepancy }}
            </n-alert>

            <!-- 建议操作 -->
            <n-alert
              v-if="point.suggestions"
              type="info"
              :bordered="false"
              class="suggestions-alert"
            >
              <template #header>建议</template>
              {{ point.suggestions }}
            </n-alert>
          </div>
        </div>
      </div>
    </n-card>

    <!-- 时效性检查 -->
    <n-card
      v-if="verificationData.timeliness?.isOutdated"
      class="timeliness-card"
    >
      <template #header>
        <n-icon :component="UpdateIcon" color="#ff4d4f" />
        <span>内容过时提醒</span>
      </template>

      <div
        v-for="(point, index) in verificationData.timeliness.outdatedPoints"
        :key="index"
        class="outdated-item"
      >
        <p>{{ point.text }}</p>
        <n-alert type="error">
          {{ point.suggestion }}
        </n-alert>
      </div>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import {
  NCard, NProgress, NSpace, NStatistic, NIcon, NTag, NSelect,
  NCollapse, NCollapseItem, NA, NAlert
} from 'naive-ui'

interface Props {
  verificationData: VerificationReport
}

const props = defineProps<Props>()

const filterType = ref('all')
const filterImportance = ref('all')

const filterOptions = [
  { label: '全部', value: 'all' },
  { label: '数据', value: 'data' },
  { label: '事实', value: 'fact' },
  { label: '引用', value: 'quote' },
  { label: '技术', value: 'technical_claim' }
]

const importanceOptions = [
  { label: '全部', value: 'all' },
  { label: '重要', value: 'high' },
  { label: '中等', value: 'medium' },
  { label: '一般', value: 'low' }
]

const filteredPoints = computed(() => {
  return props.verificationData.verificationPoints.filter(point => {
    if (filterType.value !== 'all' && point.type !== filterType.value) {
      return false
    }
    if (filterImportance.value !== 'all' && point.importance !== filterImportance.value) {
      return false
    }
    return true
  })
})

function getScoreColor(score: number): string {
  if (score >= 90) return '#52c41a'
  if (score >= 70) return '#73d13d'
  if (score >= 50) return '#faad14'
  return '#ff4d4f'
}

function getRailColor(): string {
  return '#f0f0f0'
}

function getStatusIcon(point: VerificationPoint): Component {
  if (point.verified) return CheckCircleIcon
  if (point.credibility > 50) return QuestionCircleIcon
  return CloseCircleIcon
}

function getStatusColor(point: VerificationPoint): string {
  if (point.verified) return '#52c41a'
  if (point.credibility > 50) return '#faad14'
  return '#ff4d4f'
}

function getTypeColor(type: string): 'success' | 'info' | 'warning' | 'error' {
  const colors = {
    data: 'info',
    fact: 'success',
    quote: 'warning',
    technical_claim: 'error',
    date: 'info'
  }
  return colors[type] || 'default'
}

function getTypeLabel(type: string): string {
  const labels = {
    data: '数据',
    fact: '事实',
    quote: '引用',
    technical_claim: '技术',
    date: '日期'
  }
  return labels[type] || type
}

function getAuthorityColor(authority: number): string {
  if (authority >= 0.8) return '#52c41a'
  if (authority >= 0.6) return '#73d13d'
  return '#faad14'
}
</script>

<style scoped>
.verification-panel {
  padding: 20px;
}

.overall-card {
  margin-bottom: 20px;
}

.overall-score {
  display: flex;
  align-items: center;
  gap: 40px;
  padding: 20px 0;
}

.score-number {
  font-size: 36px;
  font-weight: bold;
  display: block;
}

.score-label {
  font-size: 14px;
  color: #666;
  margin-top: 8px;
  display: block;
}

.overall-info h3 {
  margin: 0 0 16px 0;
  font-size: 18px;
}

.verification-points {
  display: grid;
  gap: 16px;
}

.verification-point {
  padding: 16px;
  border-radius: 8px;
  border: 2px solid transparent;
  transition: all 0.3s;
}

.verification-point.verified {
  background: #f6ffed;
  border-color: #b7eb8f;
}

.verification-point.questionable {
  background: #fffbe6;
  border-color: #ffe58f;
}

.verification-point.unverified {
  background: #fff1f0;
  border-color: #ffccc7;
}

.point-status {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.point-content {
  padding-left: 32px;
}

.point-text {
  font-size: 15px;
  margin: 0 0 12px 0;
  color: #333;
}

.credibility-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.credibility-label {
  font-size: 13px;
  color: #666;
  min-width: 80px;
}

.sources-list {
  display: grid;
  gap: 12px;
}

.source-item {
  padding: 12px;
  background: white;
  border-radius: 6px;
}

.source-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.source-header .n-progress {
  width: 80px;
}

.source-excerpt {
  font-size: 13px;
  color: #666;
  margin: 0;
}

.discrepancy-alert,
.suggestions-alert {
  margin-top: 12px;
}

.timeliness-card {
  margin-top: 20px;
  border: 2px solid #ffccc7;
}

.outdated-item {
  margin-bottom: 16px;
}

.outdated-item:last-child {
  margin-bottom: 0;
}

.outdated-item p {
  margin: 0 0 12px 0;
  font-weight: 500;
}
</style>
```

## 后端实现

### Service层

```typescript
// backend/analysis/verification.service.ts
import { Injectable } from '@nestjs/common'
import { AiService } from '@/ai/ai.service'
import { WebSearchService } from '@/web-search/web-search.service'

interface VerificationConfig {
  enableTimelinessCheck: boolean
  maxVerificationPoints: number
  minSourcesPerPoint: number
  minAuthorityScore: number
}

@Injectable()
export class VerificationService {
  private readonly config: VerificationConfig = {
    enableTimelinessCheck: true,
    maxVerificationPoints: 20,
    minSourcesPerPoint: 2,
    minAuthorityScore: 0.6
  }

  constructor(
    private readonly aiService: AiService,
    private readonly webSearchService: WebSearchService
  ) {}

  async verify(
    content: string,
    options?: Partial<VerificationConfig>
  ): Promise<VerificationReport> {
    const config = { ...this.config, ...options }

    // 1. 识别验证点
    const points = this.identifyVerificationPoints(content)
      .slice(0, config.maxVerificationPoints)

    // 2. 验证每个点
    const results = await Promise.all(
      points.map(point => this.verifyPoint(point, config))
    )

    // 3. 计算总体可信度
    const overall = this.calculateOverall(results)

    // 4. 时效性检查
    let timeliness: TimelinessResult | undefined
    if (config.enableTimelinessCheck) {
      timeliness = await this.checkTimeliness(content)
    }

    return {
      overall,
      verificationPoints: results,
      timeliness
    }
  }

  private async verifyPoint(
    point: VerificationPoint,
    config: VerificationConfig
  ): Promise<VerifiedPoint> {
    // 1. 搜索验证
    const sources = await this.webSearchService.search({
      query: point.text,
      searchEngine: 'search_pro_quark',
      searchIntent: true,
      numResults: 10
    })

    // 2. 分析来源
    const analyzed = await this.analyzeSources(sources, point)

    // 3. 交叉验证
    const crossValidated = await this.crossValidate(analyzed, point)

    // 4. 生成验证结果
    return this.buildVerificationResult(point, crossValidated, config)
  }

  private async analyzeSources(
    sources: SearchResult[],
    point: VerificationPoint
  ): Promise<AnalyzedSource[]> {
    const analyzed: AnalyzedSource[] = []

    for (const source of sources) {
      // 判断权威性
      const authority = this.assessAuthority(source)

      // 判断是否支持原文
      const supporting = await this.judgeSupport(source, point)

      analyzed.push({
        ...source,
        authority,
        supporting: supporting.stance === 'support',
        excerpt: supporting.excerpt
      })
    }

    return analyzed
  }

  private async judgeSupport(
    source: SearchResult,
    point: VerificationPoint
  ): Promise<{ stance: 'support' | 'conflict' | 'neutral', excerpt: string }> {
    const prompt = `
判断以下搜索结果是否支持原文陈述:

原文: ${point.text}

搜索结果:
标题: ${source.title}
摘要: ${source.snippet}
链接: ${source.url}

请判断:
1. 是否支持原文(内容一致)
2. 提取相关片段(50字以内)

返回JSON格式:
{
  "stance": "support",
  "excerpt": "相关片段..."
}
    `

    const result = await this.aiService.chat({
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.2,
      responseFormat: { type: 'json_object' }
    })

    const data = JSON.parse(result.content)

    return {
      stance: data.stance,
      excerpt: data.excerpt
    }
  }

  private async crossValidate(
    sources: AnalyzedSource[],
    point: VerificationPoint
  ): Promise<CrossValidationResult> {
    const supporting = sources.filter(s => s.supporting)
    const conflicting = sources.filter(s => !s.supporting && s.authority > 0.6)

    const verified = supporting.length >= this.config.minSourcesPerPoint
    const credibility = verified
      ? Math.min(100, (supporting.length / sources.length) * 100)
      : Math.max(0, 50 - conflicting.length * 10)

    let discrepancy: string | undefined
    if (conflicting.length > 0) {
      discrepancy = `有${conflicting.length}个来源反驳此陈述`
    }

    return {
      verified,
      credibility,
      supporting: supporting.slice(0, 3),
      conflicting,
      discrepancy
    }
  }

  private assessAuthority(source: SearchResult): number {
    let score = 0.5

    // 域名权威性
    if (isCredibleDomain(source.domain)) {
      score += 0.3
    }

    // 官方网站
    if (source.url.includes('official') || source.title.includes('官方')) {
      score += 0.2
    }

    return Math.min(score, 1.0)
  }

  private buildVerificationResult(
    point: VerificationPoint,
    validation: CrossValidationResult,
    config: VerificationConfig
  ): VerifiedPoint {
    return {
      text: point.text,
      type: point.type,
      importance: point.importance,
      verified: validation.verified,
      credibility: Math.round(validation.credibility),
      sources: validation.supporting.map(s => ({
        url: s.url,
        title: s.title,
        domain: s.domain,
        authority: s.authority,
        supporting: true,
        excerpt: s.excerpt
      })),
      discrepancy: validation.discrepancy,
      suggestions: this.generateSuggestions(validation)
    }
  }

  private generateSuggestions(
    validation: CrossValidationResult
  ): string | undefined {
    if (!validation.verified && validation.conflicting.length > 0) {
      return `建议更新内容或补充来源。有${validation.conflicting.length}个权威来源不支持此陈述。`
    }

    if (validation.supporting.length < this.config.minSourcesPerPoint) {
      return '建议补充更多可信来源'
    }

    return undefined
  }

  private calculateOverall(results: VerifiedPoint[]): OverallResult {
    const avgCredibility = results.length > 0
      ? results.reduce((sum, r) => sum + r.credibility, 0) / results.length
      : 100

    const verifiedCount = results.filter(r => r.verified).length
    const questionableCount = results.filter(r => !r.verified && r.credibility > 50).length
    const outdatedCount = results.filter(r => r.credibility <= 50).length

    let summary = '文章内容可信'
    if (questionableCount > 0) {
      summary = '文章内容基本可信,但部分内容需要核实'
    } else if (outdatedCount > 0) {
      summary = '文章内容存在多处不准确,建议谨慎参考'
    }

    return {
      credibilityScore: Math.round(avgCredibility),
      summary,
      verifiedCount,
      questionableCount,
      outdatedCount
    }
  }

  private async checkTimeliness(content: string): Promise<TimelinessResult> {
    // 提取时效性敏感信息
    const sensitivePoints = this.extractTimeSensitiveInfo(content)

    const outdated: OutdatedPoint[] = []

    for (const point of sensitivePoints) {
      const updates = await this.searchForUpdates(point)

      if (updates.hasUpdate) {
        outdated.push({
          text: point,
          currentVersion: updates.currentVersion,
          suggestion: updates.suggestion
        })
      }
    }

    return {
      checked: true,
      isOutdated: outdated.length > 0,
      outdatedPoints: outdated
    }
  }

  private extractTimeSensitiveInfo(content: string): string[] {
    const patterns = [
      /(?:v|version)?\s*\d+\.\d+(?:\.\d+)?/gi,
      /(?:目前|当前|现在|最新)/g,
      /\d{4}年/g
    ]

    const info: string[] = []

    for (const pattern of patterns) {
      const matches = content.match(pattern)
      if (matches) {
        info.push(...matches)
      }
    }

    return [...new Set(info)]
  }

  private async searchForUpdates(
    keyword: string
  ): Promise<{ hasUpdate: boolean, currentVersion?: string, suggestion?: string }> {
    const currentYear = new Date().getFullYear()

    const results = await this.webSearchService.search({
      query: `${keyword} 最新 ${currentYear}`,
      searchEngine: 'search_pro_quark',
      searchIntent: true,
      numResults: 5
    })

    // AI判断是否有更新
    const prompt = `
判断以下搜索结果是否显示"${keyword}"有更新版本:

搜索结果:
${results.map(r => `- ${r.title}: ${r.snippet}`).join('\n')}

返回JSON:
{
  "hasUpdate": true/false,
  "currentVersion": "最新版本",
  "suggestion": "建议说明"
}
    `

    const aiResult = await this.aiService.chat({
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.2,
      responseFormat: { type: 'json_object' }
    })

    return JSON.parse(aiResult.content)
  }

  private identifyVerificationPoints(content: string): VerificationPoint[] {
    // 实现验证点识别逻辑
    return []
  }

  private isCredibleDomain(domain: string): boolean {
    const crediblePatterns = [
      /\.gov\.cn$/,
      /\.gov$/,
      /\.org$/,
      /\.edu\.cn$/,
      /\.edu$/,
      /(xinhuanet|people|cctv)\.com$/
    ]

    return crediblePatterns.some(pattern => pattern.test(domain))
  }
}
```

## API接口

### 请求示例

```http
POST /api/analysis/verification
Content-Type: application/json
X-API-Key: your-api-key

{
  "content": "根据IDC报告,2023年全球云市场规模达到5000亿美元...",
  "options": {
    "enableTimelinessCheck": true,
    "maxVerificationPoints": 20
  }
}
```

### 响应示例

```json
{
  "success": true,
  "data": {
    "overall": {
      "credibilityScore": 85,
      "summary": "文章内容基本可信,但部分数据需要更新",
      "verifiedCount": 8,
      "questionableCount": 2,
      "outdatedCount": 1
    },
    "verificationPoints": [
      {
        "text": "根据IDC报告,2023年全球云市场规模达到5000亿美元",
        "type": "data",
        "importance": "high",
        "verified": true,
        "credibility": 90,
        "sources": [
          {
            "url": "https://www.idc.com/",
            "title": "IDC Worldwide Semiannual Public Cloud Services Tracker",
            "domain": "idc.com",
            "authority": 0.95,
            "supporting": true,
            "excerpt": "The worldwide public cloud services market reached $500 billion in 2023"
          }
        ]
      }
    ],
    "timeliness": {
      "checked": true,
      "isOutdated": true,
      "outdatedPoints": [
        {
          "text": "Node.js 14是LTS版本",
          "currentVersion": "Node.js 20 LTS",
          "suggestion": "建议更新为Node.js 20 LTS"
        }
      ]
    }
  }
}
```

## 优化建议

### 1. 提高验证准确性

- 建立权威来源白名单
- 使用多个搜索引擎交叉验证
- 收集用户反馈,持续优化判断逻辑

### 2. 性能优化

- 对常见陈述缓存验证结果
- 并行处理多个验证点
- 使用批量搜索API减少请求次数

### 3. 用户体验增强

- 提供验证进度指示
- 支持用户提交可信来源
- 允许用户调整验证标准

### 4. 智能化升级

- 学习用户信任的来源
- 根据领域自动调整验证策略
- 提供内容更新建议和自动更新功能

---

其他核心功能文档:
- [易读性评分](/guide/features/readability)
- [内容提炼](/guide/features/refinement)
- [智能扩展](/guide/features/expansion)
