# 前端组件设计

本文档详细说明 AI-NoteBook 前端组件系统的设计规范和实现细节。

## 组件设计原则

### 核心原则

1. **单一职责**：每个组件只负责一个功能
2. **可复用性**：通过 props 实现灵活配置
3. **可组合性**：组件可以自由组合
4. **可测试性**：组件逻辑独立，易于测试
5. **可维护性**：清晰的代码结构和文档

### 组件分层

```
┌─────────────────────────────────────┐
│      Pages (页面层)                  │
│  Home.vue, Analyze.vue, ...         │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│   Business Components (业务组件)     │
│  ReadabilityCard, RefinedContent... │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│    Common Components (通用组件)      │
│  MarkdownEditor, ExportButton...    │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│   Base Components (基础组件)         │
│  Naive UI 原子组件                   │
└─────────────────────────────────────┘
```

## 通用组件库

### 1. MarkdownEditor

Markdown 编辑器组件，支持实时预览和语法高亮。

#### 组件代码

```vue
<!-- src/components/common/MarkdownEditor.vue -->
<template>
  <div class="markdown-editor">
    <Vditor
      v-model="internalValue"
      :height="height"
      :mode="mode"
      :theme="theme"
      :placeholder="placeholder"
      :toolbar="toolbarConfig"
      :cache="cache"
      @input="handleInput"
      @after="handleAfter"
      @focus="handleFocus"
      @blur="handleBlur"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import Vditor from 'vditor'
import 'vditor/dist/index.css'

interface Props {
  modelValue: string
  height?: number
  mode?: 'sv' | 'ir' | 'wysiwyg'
  theme?: 'classic' | 'dark'
  placeholder?: string
  readonly?: boolean
  cache?: boolean
}

interface Emits {
  (e: 'update:modelValue', value: string): void
  (e: 'change', value: string): void
  (e: 'save', value: string): void
  (e: 'focus'): void
  (e: 'blur'): void
}

const props = withDefaults(defineProps<Props>(), {
  height: 500,
  mode: 'sv',
  theme: 'classic',
  placeholder: '请输入 Markdown 内容...',
  readonly: false,
  cache: true
})

const emit = defineEmits<Emits>()

const internalValue = computed({
  get: () => props.modelValue,
  set: (value: string) => emit('update:modelValue', value)
})

// 工具栏配置
const toolbarConfig = [
  'headings',
  'bold',
  'italic',
  'strike',
  '|',
  'list',
  'ordered-list',
  'check',
  '|',
  'code',
  'inline-code',
  '|',
  'link',
  'table',
  '|',
  'undo',
  'redo',
  '|',
  'preview',
  'fullscreen'
]

const handleInput = (value: string) => {
  emit('change', value)
}

const handleAfter = () => {
  // 编辑器初始化完成
  console.log('Vditor initialized')
}

const handleFocus = () => {
  emit('focus')
}

const handleBlur = () => {
  emit('blur')
}

// 暴露实例方法
defineExpose({
  getValue: () => props.modelValue,
  setValue: (value: string) => {
    internalValue.value = value
  },
  insertValue: (value: string) => {
    internalValue.value += value
  }
})
</script>

<style scoped>
.markdown-editor {
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.markdown-editor :deep(.vditor) {
  border: none;
}
</style>
```

#### 使用示例

```vue
<template>
  <MarkdownEditor
    v-model="content"
    :height="600"
    mode="sv"
    @change="handleChange"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import MarkdownEditor from '@/components/common/MarkdownEditor.vue'

const content = ref('# 标题\n\n内容...')

const handleChange = (value: string) => {
  console.log('Content changed:', value)
}
</script>
```

### 2. MarkdownViewer

Markdown 渲染器组件，支持代码高亮和主题切换。

#### 组件代码

```vue
<!-- src/components/common/MarkdownViewer.vue -->
<template>
  <div class="markdown-viewer" :class="themeClass">
    <div v-html="renderedHtml" class="markdown-body"></div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'

interface Props {
  content: string
  theme?: 'light' | 'dark'
  sanitize?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  theme: 'light',
  sanitize: true
})

// 创建 Markdown-it 实例
const md = new MarkdownIt({
  html: !props.sanitize,
  linkify: true,
  typographer: true,
  highlight: (str, lang) => {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(str, { language: lang }).value
      } catch (__) {}
    }
    return ''
  }
})

// 使用插件
import markdownItAnchor from 'markdown-it-anchor'
md.use(markdownItAnchor, {
  permalink: markdownItAnchor.permalink.linkInsideHeader({
    symbol: '#',
    placement: 'before'
  })
})

const themeClass = computed(() => `theme-${props.theme}`)

const renderedHtml = computed(() => {
  return md.render(props.content || '')
})
</script>

<style scoped>
.markdown-viewer {
  padding: 20px;
  background: #fff;
  border-radius: 4px;
}

.markdown-viewer.theme-dark {
  background: #1e1e1e;
  color: #d4d4d4;
}

.markdown-body {
  line-height: 1.6;
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3) {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
}

.markdown-body :deep(pre) {
  padding: 16px;
  overflow: auto;
  font-size: 85%;
  line-height: 1.45;
  background-color: #f6f8fa;
  border-radius: 6px;
}

.markdown-body.theme-dark :deep(pre) {
  background-color: #2d2d2d;
}

.markdown-body :deep(code) {
  padding: 0.2em 0.4em;
  margin: 0;
  font-size: 85%;
  background-color: rgba(175, 184, 193, 0.2);
  border-radius: 6px;
}

.markdown-body :deep(blockquote) {
  padding: 0 1em;
  color: #57606a;
  border-left: 0.25em solid #d0d7de;
}
</style>
```

### 3. ExportButton

导出按钮组件，支持多种格式导出。

#### 组件代码

```vue
<!-- src/components/common/ExportButton.vue -->
<template>
  <n-dropdown
    trigger="click"
    placement="bottom-start"
    :options="exportOptions"
    @select="handleExport"
  >
    <n-button :loading="exporting" :disabled="disabled">
      <template #icon>
        <n-icon :component="DownloadIcon" />
      </template>
      导出
    </n-button>
  </n-dropdown>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { NButton, NDropdown, NIcon, type DropdownOption } from 'naive-ui'
import { DownloadAsImage, DownloadPdf, DownloadWord } from '@vicons/carbon'

interface Props {
  content: string
  filename?: string
  disabled?: boolean
}

interface Emits {
  (e: 'export', format: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const exporting = ref(false)

const exportOptions: DropdownOption[] = [
  {
    label: '导出为 Markdown',
    key: 'md',
    icon: () => h(NIcon, null, { default: () => h(DownloadAsImage) })
  },
  {
    label: '导出为 PDF',
    key: 'pdf',
    icon: () => h(NIcon, null, { default: () => h(DownloadPdf) })
  },
  {
    label: '导出为 Word',
    key: 'docx',
    icon: () => h(NIcon, null, { default: () => h(DownloadWord) })
  }
]

const handleExport = async (format: string) => {
  exporting.value = true

  try {
    const filename = props.filename || `document_${Date.now()}`

    switch (format) {
      case 'md':
        await exportMarkdown(filename)
        break
      case 'pdf':
        await exportPdf(filename)
        break
      case 'docx':
        await exportWord(filename)
        break
    }

    emit('export', format)
    window.$message?.success(`导出成功：${filename}.${format}`)
  } catch (error) {
    console.error('Export error:', error)
    window.$message?.error('导出失败')
  } finally {
    exporting.value = false
  }
}

const exportMarkdown = async (filename: string) => {
  const blob = new Blob([props.content], { type: 'text/markdown' })
  downloadBlob(blob, `${filename}.md`)
}

const exportPdf = async (filename: string) => {
  const html2pdf = await import('html2pdf.js')
  const element = document.createElement('div')
  element.innerHTML = props.content
  document.body.appendChild(element)

  await html2pdf.default().set({
    margin: [10, 10],
    filename: `${filename}.pdf`,
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
  }).from(element).save()

  document.body.removeChild(element)
}

const exportWord = async (filename: string) => {
  const { Document, Packer, Paragraph, TextRun } = await import('docx')
  const { saveAs } = await import('file-saver')

  const doc = new Document({
    sections: [{
      properties: {},
      children: [
        new Paragraph({
          children: [
            new TextRun({
              text: props.content,
              bold: false
            })
          ]
        })
      ]
    }]
  })

  const blob = await Packer.toBlob(doc)
  saveAs(blob, `${filename}.docx`)
}

const downloadBlob = (blob: Blob, filename: string) => {
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.click()
  URL.revokeObjectURL(url)
}
</script>
```

### 4. LoadingSpinner

加载动画组件。

#### 组件代码

```vue
<!-- src/components/common/LoadingSpinner.vue -->
<template>
  <div class="loading-spinner" :class="[`size-${size}`, theme]">
    <div class="spinner"></div>
    <p v-if="text" class="loading-text">{{ text }}</p>
  </div>
</template>

<script setup lang="ts">
interface Props {
  size?: 'small' | 'medium' | 'large'
  text?: string
  theme?: 'light' | 'dark'
}

withDefaults(defineProps<Props>(), {
  size: 'medium',
  theme: 'light'
})
</script>

<style scoped>
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.spinner {
  border: 3px solid rgba(0, 0, 0, 0.1);
  border-top-color: #18a058;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.size-small .spinner {
  width: 20px;
  height: 20px;
  border-width: 2px;
}

.size-medium .spinner {
  width: 40px;
  height: 40px;
}

.size-large .spinner {
  width: 60px;
  height: 60px;
  border-width: 4px;
}

.loading-text {
  margin-top: 12px;
  font-size: 14px;
  color: #666;
}

.theme.dark .loading-text {
  color: #999;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
```

### 5. EmptyState

空状态组件。

#### 组件代码

```vue
<!-- src/components/common/EmptyState.vue -->
<template>
  <div class="empty-state">
    <div class="empty-icon">
      <n-icon :size="iconSize" :component="icon" />
    </div>
    <h3 v-if="title" class="empty-title">{{ title }}</h3>
    <p v-if="description" class="empty-description">{{ description }}</p>
    <n-button v-if="actionText" @click="handleAction" type="primary">
      {{ actionText }}
    </n-button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { NIcon, NButton } from 'naive-ui'
import { FolderOpen, DocumentOutline } from '@vicons/carbon'

interface Props {
  type?: 'no-data' | 'no-result' | 'error'
  title?: string
  description?: string
  actionText?: string
  size?: 'small' | 'medium' | 'large'
}

interface Emits {
  (e: 'action'): void
}

const props = withDefaults(defineProps<Props>(), {
  type: 'no-data',
  size: 'medium'
})

const emit = defineEmits<Emits>()

const icons = {
  'no-data': FolderOpen,
  'no-result': DocumentOutline,
  'error': DocumentOutline
}

const icon = computed(() => icons[props.type])

const iconSize = computed(() => {
  const sizes = { small: 48, medium: 64, large: 96 }
  return sizes[props.size]
})

const handleAction = () => {
  emit('action')
}
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.empty-icon {
  margin-bottom: 16px;
  color: #c1c1c1;
}

.empty-title {
  margin: 0 0 8px;
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.empty-description {
  margin: 0 0 24px;
  font-size: 14px;
  color: #666;
  max-width: 400px;
}
</style>
```

## 业务组件

### 1. ReadabilityCard

易读性评分卡片组件。

#### 组件代码

```vue
<!-- src/components/analysis/ReadabilityCard.vue -->
<template>
  <n-card title="易读性评分" class="readability-card">
    <n-space vertical :size="24">
      <!-- 综合评分 -->
      <div class="overall-score">
        <n-progress
          type="circle"
          :percentage="scorePercentage"
          :color="scoreColor"
          :stroke-width="12"
          :rail-style="{ opacity: 0.2 }"
        >
          <template #default="{ percentage }">
            <div class="score-display">
              <span class="score-number">{{ scoreData.overall }}</span>
              <span class="score-unit">分</span>
            </div>
          </template>
        </n-progress>
        <p v-if="scoreData.comment" class="score-comment">
          {{ scoreData.comment }}
        </p>
      </div>

      <!-- 分项评分 -->
      <n-divider />

      <div class="detail-scores">
        <div
          v-for="item in scoreItems"
          :key="item.key"
          class="score-item"
        >
          <div class="score-header">
            <n-icon :component="item.icon" :size="20" />
            <span class="score-label">{{ item.label }}</span>
          </div>
          <n-rate
            :model-value="item.score"
            readonly
            :color="scoreColor"
            size="small"
          />
          <p v-if="item.reason" class="score-reason">
            {{ item.reason }}
          </p>
        </div>
      </div>

      <!-- 目标读者 -->
      <n-alert v-if="scoreData.targetAudience" type="info" :icon="UserIcon">
        适合读者：{{ scoreData.targetAudience }}
      </n-alert>
    </n-space>
  </n-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import {
  NCard,
  NSpace,
  NProgress,
  NRate,
  NDivider,
  NAlert,
  NIcon
} from 'naive-ui'
import { Book, FormatList, Psychology, User } from '@vicons/carbon'

import type { ReadabilityScore } from '@/types/analysis'

interface Props {
  scoreData: ReadabilityScore
}

const props = defineProps<Props>()

const scorePercentage = computed(() => props.scoreData.overall * 20)

const scoreColor = computed(() => {
  const colors = [
    '#52c41a', // 1分 - 绿色
    '#73d13d', // 2分 - 浅绿
    '#ffc53d', // 3分 - 橙色
    '#ff7a45', // 4分 - 深橙
    '#f5222d'  // 5分 - 红色
  ]
  return colors[props.scoreData.overall - 1]
})

const scoreItems = computed(() => [
  {
    key: 'vocabulary',
    label: '词汇难度',
    score: props.scoreData.vocabulary,
    reason: props.scoreData.vocabularyReason,
    icon: Book
  },
  {
    key: 'sentence',
    label: '句式结构',
    score: props.scoreData.sentence,
    reason: props.scoreData.sentenceReason,
    icon: FormatList
  },
  {
    key: 'logic',
    label: '逻辑深度',
    score: props.scoreData.logic,
    reason: props.scoreData.logicReason,
    icon: Psychology
  }
])

const UserIcon = User
</script>

<style scoped>
.readability-card {
  height: 100%;
}

.overall-score {
  text-align: center;
  padding: 20px 0;
}

.score-display {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.score-number {
  font-size: 48px;
  font-weight: bold;
  line-height: 1;
}

.score-unit {
  font-size: 16px;
  color: #666;
  margin-top: 4px;
}

.score-comment {
  margin: 16px 0 0;
  font-size: 16px;
  color: #333;
  font-weight: 500;
}

.detail-scores {
  padding: 0 12px;
}

.score-item {
  margin-bottom: 24px;
}

.score-item:last-child {
  margin-bottom: 0;
}

.score-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.score-label {
  font-size: 14px;
}

.score-reason {
  margin: 8px 0 0;
  font-size: 13px;
  color: #666;
  line-height: 1.6;
}
</style>
```

### 2. RefinedContent

提炼内容展示组件。

#### 组件代码

```vue
<!-- src/components/analysis/RefinedContent.vue -->
<template>
  <n-card title="提炼内容" class="refined-content">
    <template #header-extra>
      <n-space>
        <n-button
          text
          @click="handleCopy"
          :disabled="!content"
        >
          <template #icon>
            <n-icon :component="CopyIcon" />
          </template>
          复制
        </n-button>
        <ExportButton
          :content="content"
          :filename="filename"
        />
      </n-space>
    </template>

    <div v-if="content" class="content-container">
      <MarkdownViewer
        :content="content"
        :theme="theme"
      />

      <!-- 统计信息 -->
      <n-divider />

      <n-space :size="16" class="content-stats">
        <n-statistic label="字数" :value="wordCount" />
        <n-statistic label="阅读时间" :value="readingTime" suffix="分钟" />
      </n-space>
    </div>

    <EmptyState
      v-else
      type="no-data"
      title="暂无提炼内容"
      description="文章解析完成后将显示在此处"
    />
  </n-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import {
  NCard,
  NSpace,
  NButton,
  NIcon,
  NDivider,
  NStatistic
} from 'naive-ui'
import { Copy } from '@vicons/carbon'
import MarkdownViewer from '@/components/common/MarkdownViewer.vue'
import ExportButton from '@/components/common/ExportButton.vue'
import EmptyState from '@/components/common/EmptyState.vue'

interface Props {
  content?: string
  title?: string
  theme?: 'light' | 'dark'
}

interface Emits {
  (e: 'copy'): void
}

const props = withDefaults(defineProps<Props>(), {
  theme: 'light'
})

const emit = defineEmits<Emits>()

const CopyIcon = Copy

const filename = computed(() => props.title || 'refined_content')

const wordCount = computed(() => {
  return props.content ? props.content.length : 0
})

const readingTime = computed(() => {
  // 假设阅读速度 500字/分钟
  return Math.ceil(wordCount.value / 500) || 0
})

const handleCopy = async () => {
  try {
    await navigator.clipboard.writeText(props.content || '')
    window.$message?.success('已复制到剪贴板')
    emit('copy')
  } catch (error) {
    window.$message?.error('复制失败')
  }
}
</script>

<style scoped>
.refined-content {
  height: 100%;
}

.content-container {
  min-height: 300px;
}

.content-stats {
  margin-top: 16px;
  padding: 0 12px;
}
</style>
```

### 3. ExpansionPanel

扩展内容面板组件。

#### 组件代码

```vue
<!-- src/components/analysis/ExpansionPanel.vue -->
<template>
  <n-card title="智能扩展" class="expansion-panel">
    <n-collapse v-if="expansions && expansions.length > 0">
      <n-collapse-item
        v-for="(expansion, index) in expansions"
        :key="index"
        :title="expansion.keyPoint"
        :name="index"
      >
        <template #header-extra>
          <n-tag size="small" type="info">
            扩展 {{ index + 1 }}
          </n-tag>
        </template>

        <n-space vertical :size="12">
          <!-- 扩展内容 -->
          <div class="expansion-content">
            <MarkdownViewer
              :content="expansion.expansion"
              :theme="theme"
            />
          </div>

          <!-- 来源链接 -->
          <div v-if="expansion.sources && expansion.sources.length > 0" class="sources-section">
            <n-divider style="margin: 12px 0" />
            <p class="sources-title">
              <n-icon :component="LinkIcon" />
              参考来源
            </p>
            <n-space vertical :size="8">
              <n-text
                v-for="(source, sIndex) in expansion.sources"
                :key="sIndex"
                tag="a"
                :href="source.url"
                target="_blank"
                class="source-link"
              >
                {{ source.title || source.url }}
              </n-text>
            </n-space>
          </div>
        </n-space>
      </n-collapse-item>
    </n-collapse>

    <EmptyState
      v-else
      type="no-data"
      title="暂无扩展内容"
      description="启用智能扩展后将显示相关知识的详细说明"
    />
  </n-card>
</template>

<script setup lang="ts">
import { NCollapse, NCollapseItem, NTag, NSpace, NDivider, NIcon, NText, NCard } from 'naive-ui'
import { Link } from '@vicons/carbon'
import MarkdownViewer from '@/components/common/MarkdownViewer.vue'
import EmptyState from '@/components/common/EmptyState.vue'

interface Expansion {
  keyPoint: string
  expansion: string
  sources: Array<{
    url: string
    title?: string
  }>
}

interface Props {
  expansions?: Expansion[]
  theme?: 'light' | 'dark'
}

withDefaults(defineProps<Props>(), {
  expansions: () => [],
  theme: 'light'
})

const LinkIcon = Link
</script>

<style scoped>
.expansion-panel {
  height: 100%;
}

.expansion-content {
  padding: 12px 0;
  line-height: 1.8;
}

.sources-section {
  margin-top: 12px;
}

.sources-title {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 0 0 8px;
  font-size: 13px;
  font-weight: 500;
  color: #666;
}

.source-link {
  color: #18a058;
  text-decoration: none;
  font-size: 13px;
  word-break: break-all;
}

.source-link:hover {
  text-decoration: underline;
}
</style>
```

### 4. ProgressIndicator

任务进度指示器组件。

#### 组件代码

```vue
<!-- src/components/analysis/ProgressIndicator.vue -->
<template>
  <div class="progress-indicator">
    <!-- 进度条 -->
    <n-progress
      type="line"
      :percentage="progress"
      :status="progressStatus"
      :show-indicator="false"
    />

    <!-- 进度信息 -->
    <div class="progress-info">
      <div class="progress-message">
        <n-spin v-if="processing" :size="14" />
        <span>{{ message }}</span>
      </div>
      <div class="progress-percentage">
        {{ progress }}%
      </div>
    </div>

    <!-- 步骤指示器 -->
    <n-steps :current="currentStep" :status="stepStatus" size="small">
      <n-step
        v-for="step in steps"
        :key="step.key"
        :title="step.title"
        :description="step.description"
      />
    </n-steps>
  </div>
</template>

<script setup lang="ts">
import { computed, watch } from 'vue'
import { NProgress, NSpin, NSteps, NStep } from 'naive-ui'

interface Step {
  key: string
  title: string
  description: string
  threshold: number
}

interface Props {
  progress: number
  message: string
  status?: 'processing' | 'success' | 'error' | 'warning'
}

const props = withDefaults(defineProps<Props>(), {
  status: 'processing'
})

const steps: Step[] = [
  { key: 'readability', title: '易读性评分', description: '分析词汇和句式', threshold: 20 },
  { key: 'refinement', title: '内容提炼', description: '提取核心信息', threshold: 40 },
  { key: 'expansion', title: '智能扩展', description: '补充相关知识', threshold: 60 },
  { key: 'completion', title: '完成', description: '生成分析报告', threshold: 100 }
]

const processing = computed(() => props.status === 'processing')

const progressStatus = computed(() => {
  if (props.status === 'success') return 'success'
  if (props.status === 'error') return 'error'
  if (props.status === 'warning') return 'warning'
  return undefined
})

const stepStatus = computed(() => {
  if (props.status === 'success') return 'success'
  if (props.status === 'error') return 'error'
  if (props.status === 'warning') return 'warning'
  return 'process'
})

const currentStep = computed(() => {
  // 根据进度计算当前步骤
  for (let i = steps.length - 1; i >= 0; i--) {
    if (props.progress >= steps[i].threshold) {
      return i + 1
    }
  }
  return 1
})
</script>

<style scoped>
.progress-indicator {
  padding: 20px;
  background: #f5f5f5;
  border-radius: 4px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
  padding: 0 4px;
}

.progress-message {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #333;
}

.progress-percentage {
  font-size: 18px;
  font-weight: bold;
  color: #18a058;
}

.progress-indicator :deep(.n-steps) {
  margin-top: 24px;
}
</style>
```

## 组件通信模式

### 1. Props Down / Events Up

```vue
<!-- 父组件 -->
<template>
  <ChildComponent
    v-model:value="value"
    :options="options"
    @change="handleChange"
    @submit="handleSubmit"
  />
</template>

<!-- 子组件 -->
<script setup lang="ts">
interface Props {
  value: string
  options: string[]
}

interface Emits {
  (e: 'update:value', value: string): void
  (e: 'change', value: string): void
  (e: 'submit', value: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const updateValue = (newValue: string) => {
  emit('update:value', newValue)
  emit('change', newValue)
}

const submit = () => {
  emit('submit', props.value)
}
</script>
```

### 2. Provide / Inject

```vue
<!-- 祖先组件 -->
<script setup lang="ts">
import { provide, computed } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

provide('apiKey', computed(() => userStore.apiKey))
provide('userMembership', computed(() => userStore.membership))
</script>

<!-- 后代组件 -->
<script setup lang="ts">
import { inject } from 'vue'

const apiKey = inject<ComputedRef<string>>('apiKey')
const membership = inject<ComputedRef<Membership>>('userMembership')
</script>
```

### 3. Vuex / Pinia Store

```typescript
// store/user.ts
export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)

  function setUserData(data: User) {
    user.value = data
  }

  return { user, setUserData }
})

// 组件中使用
<script setup lang="ts">
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const user = computed(() => userStore.user)
</script>
```

### 4. Event Bus（不推荐）

```typescript
// utils/eventBus.ts
import { mitt } from 'mitt'

type Events = {
  'analysis:progress': { taskId: string; progress: number }
  'analysis:completed': { taskId: string; result: any }
}

export const eventBus = mitt<Events>()

// 组件中使用
import { eventBus } from '@/utils/eventBus'

eventBus.on('analysis:progress', (data) => {
  console.log('Progress:', data.progress)
})

eventBus.emit('analysis:progress', { taskId: '123', progress: 50 })
```

## 组件性能优化

### 1. 计算属性缓存

```typescript
// ✅ 使用计算属性（有缓存）
const filteredList = computed(() => {
  return list.value.filter(item => item.active)
})

// ❌ 使用方法（每次都重新计算）
function filterList() {
  return list.value.filter(item => item.active)
}
```

### 2. 虚拟滚动

```vue
<template>
  <n-virtual-list
    :items="largeList"
    :item-size="50"
    :item-resizable="true"
  >
    <template #default="{ item }">
      <div>{{ item }}</div>
    </template>
  </n-virtual-list>
</template>
```

### 3. 懒加载组件

```typescript
// 路由懒加载
const routes = [
  {
    path: '/heavy',
    component: () => import('@/views/HeavyPage.vue')
  }
]

// 组件懒加载
const HeavyComponent = defineAsyncComponent(() =>
  import('./HeavyComponent.vue')
)
```

### 4. v-once 指令

```vue
<template>
  <!-- 只渲染一次 -->
  <div v-once>
    <h1>{{ title }}</h1>
    <p>{{ description }}</p>
  </div>

  <!-- 列表只渲染一次 -->
  <div v-for="item in staticList" v-once :key="item.id">
    {{ item }}
  </div>
</template>
```

## 组件测试

### 单元测试

```typescript
// components/__tests__/MarkdownEditor.spec.ts
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import MarkdownEditor from '../MarkdownEditor.vue'

describe('MarkdownEditor', () => {
  it('renders properly', () => {
    const wrapper = mount(MarkdownEditor, {
      props: {
        modelValue: '# Test',
        height: 500
      }
    })

    expect(wrapper.find('.markdown-editor').exists()).toBe(true)
  })

  it('emits update:modelValue on input', async () => {
    const wrapper = mount(MarkdownEditor, {
      props: {
        modelValue: ''
      }
    })

    await wrapper.vm.internalValue = '# New Content'

    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')[0]).toEqual(['# New Content'])
  })

  it('exposes getValue method', () => {
    const wrapper = mount(MarkdownEditor, {
      props: {
        modelValue: '# Test'
      }
    })

    expect(wrapper.vm.getValue()).toBe('# Test')
  })
})
```

### E2E 测试

```typescript
// e2e/analysis.spec.ts
import { test, expect } from '@playwright/test'

test('create analysis and view result', async ({ page }) => {
  await page.goto('/analyze')

  // 输入内容
  await page.fill('textarea', '# Test Article\n\nThis is a test...')

  // 点击分析按钮
  await page.click('button:has-text("开始分析")')

  // 等待完成
  await page.waitForSelector('.readability-card')

  // 检查结果
  const score = await page.textContent('.score-number')
  expect(parseInt(score || '0')).toBeGreaterThan(0)
})
```

## 相关文档

- [前端架构](/guide/frontend-architecture)
- [状态管理](/guide/frontend-state-management)
- [样式主题](/guide/frontend-theming)
