# 易读性评分

易读性评分是AI-NoteBook的核心功能之一，帮助用户快速判断文章的难度等级。

## 评分标准

### 评分维度 (1-5分)

```typescript
interface ReadabilityScore {
  vocabulary: number    // 词汇难度
  sentence: number      // 句式结构
  logic: number         // 逻辑深度
  overall: number       // 综合评分
  comment: string       // 评语
}
```

### 评分等级

| 分数 | 难度 | 适用人群 | 特征 |
|-----|------|---------|------|
| 1分 | 通俗易懂 | 初学者 | 无专业术语，句子简短，逻辑线性 |
| 2分 | 简单易懂 | 有一定基础 | 少量专业术语，偶有复杂句式 |
| 3分 | 中等难度 | 技术从业者 | 较多术语，逻辑较复杂 |
| 4分 | 较难理解 | 技术专家 | 大量专业术语，长难句多 |
| 5分 | 极其晦涩 | 资深专家 | 需要深厚背景知识，逻辑复杂 |

## 评分算法

### 1. 词汇难度 (Vocabulary)

**评估指标**：
- 专业术语密度
- 生僻字/词比例
- 技术词汇占比

**计算公式**：
```typescript
function calculateVocabularyDifficulty(content: string): number {
  const tokens = tokenize(content)
  const technicalTerms = detectTechnicalTerms(tokens)
  const rareWords = detectRareWords(tokens)

  const technicalRatio = technicalTerms.length / tokens.length
  const rareWordRatio = rareWords.length / tokens.length

  // 综合计算
  let score = 1
  if (technicalRatio > 0.1) score += 1
  if (technicalRatio > 0.2) score += 1
  if (rareWordRatio > 0.05) score += 1
  if (rareWordRatio > 0.1) score += 1

  return Math.min(score, 5)
}
```

### 2. 句式结构 (Sentence)

**评估指标**：
- 平均句长
- 复合句比例
- 嵌套层级

**计算公式**：
```typescript
function calculateSentenceComplexity(content: string): number {
  const sentences = splitSentences(content)
  const avgLength = sentences.reduce((sum, s) => sum + s.length, 0) / sentences.length

  const compoundSentences = sentences.filter(s =>
    containsConjunctions(s) || containsClauses(s)
  )

  const compoundRatio = compoundSentences.length / sentences.length

  let score = 1
  if (avgLength > 50) score += 1
  if (avgLength > 100) score += 1
  if (compoundRatio > 0.3) score += 1
  if (compoundRatio > 0.6) score += 1

  return Math.min(score, 5)
}
```

### 3. 逻辑深度 (Logic)

**评估指标**：
- 论证层次
- 因果关系复杂度
- 抽象程度

**AI分析**：
```typescript
async function analyzeLogicalDepth(content: string): Promise<number> {
  const prompt = `
    分析以下文章的逻辑复杂度，评分1-5分：

    文章内容：
    ${content}

    评分标准：
    - 1分：单一论点，线性逻辑
    - 2分：多个论点，简单关联
    - 3分：多个论点，中等复杂度关联
    - 4分：复杂论证，多层级推理
    - 5分：高度抽象，需要深度思考

    请返回JSON格式：{"score": 3, "reason": "评分原因"}
  `

  const result = await aiService.analyze(prompt)
  return result.score
}
```

## AI提示词模板

```markdown
你是一个专业的易读性分析专家。请从以下三个维度对文章进行评分：

## 文章内容
{{content}}

## 评分维度

### 1. 词汇难度 (1-5分)
- 1分：无专业术语，常用词汇
- 2分：少量专业术语，偶尔需要查词
- 3分：较多专业术语，需要一定背景
- 4分：大量专业术语，专业性强
- 5分：高度专业化，术语密集

### 2. 句式结构 (1-5分)
- 1分：句子简短，结构简单
- 2分：偶尔出现长句
- 3分：中等长度句子，有一定复杂度
- 4分：长难句较多，结构复杂
- 5分：句子极长，嵌套层级深

### 3. 逻辑深度 (1-5分)
- 1分：单一观点，线性叙述
- 2分：多个观点，简单关联
- 3分：多个观点，中等复杂度关联
- 4分：复杂论证，多层推理
- 5分：高度抽象，深度思考

## 输出格式

请以JSON格式返回：

```json
{
  "vocabulary": {
    "score": 3,
    "reason": "文章包含一定数量的专业术语，但上下文有解释"
  },
  "sentence": {
    "score": 2,
    "reason": "大部分句子结构简单，偶有长难句"
  },
  "logic": {
    "score": 4,
    "reason": "论证层次丰富，需要一定推理能力"
  },
  "overall": 3,
  "comment": "适合有一定技术背景的读者阅读",
  "target_audience": "有1-3年经验的技术从业者"
}
```
```

## 前端展示

### 组件设计

```vue
<template>
  <n-card title="易读性评分">
    <n-space vertical>
      <!-- 综合评分 -->
      <div class="overall-score">
        <n-progress
          type="circle"
          :percentage="scoreData.overall * 20"
          :color="getScoreColor(scoreData.overall)"
          :stroke-width="12"
        >
          <template #default="{ percentage }">
            <span class="score-number">{{ scoreData.overall }}</span>
            <span class="score-text">分</span>
          </template>
        </n-progress>
        <p class="score-comment">{{ scoreData.comment }}</p>
      </div>

      <!-- 分项评分 -->
      <n-divider />

      <div class="detail-scores">
        <div v-for="item in details" :key="item.label" class="score-item">
          <div class="score-label">
            <n-icon :component="getIcon(item.key)" />
            <span>{{ item.label }}</span>
          </div>
          <n-rate
            :model-value="item.score"
            readonly
            :color="getScoreColor(item.score)"
          />
          <p class="score-reason">{{ item.reason }}</p>
        </div>
      </div>

      <!-- 目标读者 -->
      <n-alert type="info" v-if="scoreData.target_audience">
        <template #icon>
          <n-icon :component="UserIcon" />
        </template>
        适合读者：{{ scoreData.target_audience }}
      </n-alert>
    </n-space>
  </n-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { NCard, NProgress, NRate, NSpace, NDivider, NAlert, NIcon } from 'naive-ui'

interface Props {
  scoreData: ReadabilityScore
}

const props = defineProps<Props>()

const details = computed(() => [
  {
    key: 'vocabulary',
    label: '词汇难度',
    score: props.scoreData.vocabulary,
    reason: props.scoreData.vocabularyReason
  },
  {
    key: 'sentence',
    label: '句式结构',
    score: props.scoreData.sentence,
    reason: props.scoreData.sentenceReason
  },
  {
    key: 'logic',
    label: '逻辑深度',
    score: props.scoreData.logic,
    reason: props.scoreData.logicReason
  }
])

function getScoreColor(score: number): string {
  const colors = ['#52c41a', '#73d13d', '#ffc53d', '#ff7a45', '#f5222d']
  return colors[score - 1]
}

function getIcon(key: string) {
  const icons = {
    vocabulary: BookIcon,
    sentence: FormatIcon,
    logic: ThinkingIcon
  }
  return icons[key]
}
</script>

<style scoped>
.overall-score {
  text-align: center;
  padding: 20px 0;
}

.score-number {
  font-size: 48px;
  font-weight: bold;
}

.score-text {
  font-size: 16px;
  color: #666;
}

.score-comment {
  font-size: 16px;
  color: #333;
  margin-top: 16px;
}

.detail-scores {
  padding: 0 20px;
}

.score-item {
  margin-bottom: 24px;
}

.score-label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-weight: 500;
}

.score-reason {
  font-size: 14px;
  color: #666;
  margin-top: 8px;
}
</style>
```

## 后端实现

### Service层

```typescript
// backend/analysis/readability.service.ts
import { Injectable } from '@nestjs/common'
import { AiService } from '@/ai/ai.service'

@Injectable()
export class ReadabilityService {
  constructor(private readonly aiService: AiService) {}

  async score(content: string): Promise<ReadabilityScore> {
    const prompt = this.buildPrompt(content)

    const result = await this.aiService.chat({
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.3,  // 降低温度以获得更稳定的结果
      responseFormat: { type: 'json_object' }
    })

    return this.parseScore(result.content)
  }

  private buildPrompt(content: string): string {
    return `
你是一个专业的易读性分析专家。请从词汇、句式、逻辑三个维度对文章评分（1-5分）。

文章内容：
${content.substring(0, 5000)}

请以JSON格式返回评分结果：
{
  "vocabulary": {"score": 3, "reason": "..."},
  "sentence": {"score": 2, "reason": "..."},
  "logic": {"score": 4, "reason": "..."},
  "overall": 3,
  "comment": "综合评语"
}
    `
  }

  private parseScore(content: string): ReadabilityScore {
    try {
      const data = JSON.parse(content)
      return {
        vocabulary: data.vocabulary.score,
        vocabularyReason: data.vocabulary.reason,
        sentence: data.sentence.score,
        sentenceReason: data.sentence.reason,
        logic: data.logic.score,
        logicReason: data.logic.reason,
        overall: data.overall,
        comment: data.comment
      }
    } catch (error) {
      throw new Error('AI返回结果解析失败')
    }
  }
}
```

### 缓存策略

```typescript
// 缓存评分结果，避免重复计算
async function scoreWithCache(content: string): Promise<ReadabilityScore> {
  const cacheKey = `readability:${hash(content)}`

  // 尝试从缓存获取
  const cached = await redis.get(cacheKey)
  if (cached) {
    return JSON.parse(cached)
  }

  // 计算评分
  const score = await readabilityService.score(content)

  // 缓存7天
  await redis.setex(cacheKey, 604800, JSON.stringify(score))

  return score
}
```

## API接口

### 请求示例

```http
POST /api/analysis/readability
Content-Type: application/json
X-API-Key: your-api-key

{
  "content": "# 文章标题\n\n这是一篇关于..."
}
```

### 响应示例

```json
{
  "success": true,
  "data": {
    "vocabulary": 3,
    "vocabularyReason": "文章包含一定数量的专业术语，但上下文有解释",
    "sentence": 2,
    "sentenceReason": "大部分句子结构简单，偶有长难句",
    "logic": 4,
    "logicReason": "论证层次丰富，需要一定推理能力",
    "overall": 3,
    "comment": "适合有一定技术背景的读者阅读",
    "targetAudience": "有1-3年经验的技术从业者"
  }
}
```

## 优化建议

### 1. 提高评分准确性

- 使用多个AI模型交叉验证
- 建立人工标注数据集进行微调
- 收集用户反馈持续优化

### 2. 性能优化

- 对相似文章使用缓存
- 分批处理长文章
- 异步处理，返回任务ID

### 3. 用户体验

- 提供评分历史趋势
- 支持不同领域的技术文章
- 提供评分对比功能

其他核心功能文档：
- [内容提炼](/guide/features/refinement)
- [智能扩展](/guide/features/expansion)
- [溯源校验](/guide/features/verification)
