# 前端样式主题

本文档详细说明 AI-NoteBook 前端样式系统的设计规范。

## 概述

AI-NoteBook 采用 **CSS Variables + Naive UI 主题系统** 构建灵活的主题方案。

### 核心特性

- 🎨 **多主题支持**：亮色/暗色主题自动切换
- 🌈 **CSS 变量**：统一的样式变量管理
- 📱 **响应式设计**：移动端优先
- ♿ **无障碍访问**：遵循 WCAG 2.1 标准
- 🎯 **组件主题**：基于 Naive UI 的主题定制

## 主题系统

### 主题切换

```typescript
// src/stores/app.ts
export type Theme = 'light' | 'dark' | 'auto'

export const useAppStore = defineStore('app', () => {
  const theme = ref<Theme>('light')

  const isDarkTheme = computed(() => {
    if (theme.value === 'auto') {
      return window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    return theme.value === 'dark'
  })

  function applyTheme() {
    const dark = isDarkTheme.value
    document.documentElement.classList.toggle('dark', dark)
  }

  return {
    theme,
    isDarkTheme,
    applyTheme
  }
})
```

### CSS 变量定义

```scss
// src/assets/styles/variables.scss
:root {
  // ===== 主色 =====
  --primary-color: #18a058;
  --primary-color-hover: #36ad6a;
  --primary-color-active: #0c7a43;
  --primary-color-disabled: #abeac9;

  // ===== 中性色 =====
  --text-color: #333333;
  --text-color-1: #333333;
  --text-color-2: #666666;
  --text-color-3: #999999;
  --text-color-disabled: #c9c9c9;

  // ===== 背景色 =====
  --bg-color: #ffffff;
  --bg-color-1: #ffffff;
  --bg-color-2: #f5f5f5;
  --bg-color-3: #e8e8e8;

  // ===== 边框色 =====
  --border-color: #e0e0e0;
  --border-color-1: #e0e0e0;
  --border-color-2: #cccccc;

  // ===== 功能色 =====
  --success-color: #18a058;
  --info-color: #2080f0;
  --warning-color: #f0a020;
  --error-color: #d03050;

  // ===== 阴影 =====
  --shadow-1: 0 2px 8px rgba(0, 0, 0, 0.08);
  --shadow-2: 0 4px 16px rgba(0, 0, 0, 0.12);
  --shadow-3: 0 8px 24px rgba(0, 0, 0, 0.16);

  // ===== 圆角 =====
  --border-radius-small: 4px;
  --border-radius-medium: 8px;
  --border-radius-large: 12px;

  // ===== 间距 =====
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;

  // ===== 字体 =====
  --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
    'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
    'Noto Color Emoji';
  --font-family-mono: 'SF Mono', Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;

  // ===== 字号 =====
  --font-size-xs: 12px;
  --font-size-sm: 13px;
  --font-size-base: 14px;
  --font-size-md: 16px;
  --font-size-lg: 18px;
  --font-size-xl: 20px;
  --font-size-2xl: 24px;
  --font-size-3xl: 30px;

  // ===== 字重 =====
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  // ===== 行高 =====
  --line-height-base: 1.5;
  --line-height-heading: 1.25;

  // ===== 过渡 =====
  --transition-duration: 0.3s;
  --transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

// 暗色主题
.dark {
  --text-color: #e8e8e8;
  --text-color-1: #e8e8e8;
  --text-color-2: #b8b8b8;
  --text-color-3: #888888;
  --text-color-disabled: #5a5a5a;

  --bg-color: #1e1e1e;
  --bg-color-1: #1e1e1e;
  --bg-color-2: #2a2a2a;
  --bg-color-3: #363636;

  --border-color: #3a3a3a;
  --border-color-1: #3a3a3a;
  --border-color-2: #4a4a4a;

  --shadow-1: 0 2px 8px rgba(0, 0, 0, 0.3);
  --shadow-2: 0 4px 16px rgba(0, 0, 0, 0.4);
  --shadow-3: 0 8px 24px rgba(0, 0, 0, 0.5);
}
```

### Naive UI 主题配置

```typescript
// src/composables/useTheme.ts
import { computed } from 'vue'
import { darkTheme, type GlobalTheme } from 'naive-ui'
import { useAppStore } from '@/stores/app'

export function useTheme() {
  const appStore = useAppStore()

  // Naive UI 主题覆盖
  const themeOverrides = computed<GlobalTheme | null>(() => {
    if (appStore.isDarkTheme) {
      return darkTheme
    }
    return null
  })

  // 主题变量覆盖
  const themeCommonVars = computed(() => ({
    primaryColor: '#18a058',
    primaryColorHover: '#36ad6a',
    primaryColorPressed: '#0c7a43',
    primaryColorSuppl: '#36ad6a'
  }))

  return {
    themeOverrides,
    themeCommonVars
  }
}
```

#### 在 App.vue 中应用

```vue
<!-- src/App.vue -->
<template>
  <n-config-provider
    :theme="themeOverrides"
    :theme-overrides="themeCommonVars"
    class="app-container"
  >
    <n-message-provider>
      <n-dialog-provider>
        <n-notification-provider>
          <RouterView />
        </n-notification-provider>
      </n-dialog-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { NConfigProvider, NMessageProvider, NDialogProvider, NNotificationProvider } from 'naive-ui'
import { useTheme } from '@/composables/useTheme'

const { themeOverrides, themeCommonVars } = useTheme()
</script>

<style>
.app-container {
  min-height: 100vh;
  background: var(--bg-color-2);
  color: var(--text-color);
  transition: background var(--transition-duration), color var(--transition-duration);
}
</style>
```

## 组件样式

### 通用样式类

```scss
// src/assets/styles/common.scss
// 文本
.text {
  &-xs { font-size: var(--font-size-xs); }
  &-sm { font-size: var(--font-size-sm); }
  &-base { font-size: var(--font-size-base); }
  &-md { font-size: var(--font-size-md); }
  &-lg { font-size: var(--font-size-lg); }
  &-xl { font-size: var(--font-size-xl); }

  &-primary { color: var(--primary-color); }
  &-success { color: var(--success-color); }
  &-info { color: var(--info-color); }
  &-warning { color: var(--warning-color); }
  &-error { color: var(--error-color); }

  &-left { text-align: left; }
  &-center { text-align: center; }
  &-right { text-align: right; }

  &-ellipsis {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

// 间距
.m {
  &-xs { margin: var(--spacing-xs); }
  &-sm { margin: var(--spacing-sm); }
  &-md { margin: var(--spacing-md); }
  &-lg { margin: var(--spacing-lg); }
  &-xl { margin: var(--spacing-xl); }

  &t-xs { margin-top: var(--spacing-xs); }
  &t-sm { margin-top: var(--spacing-sm); }
  &t-md { margin-top: var(--spacing-md); }
  &t-lg { margin-top: var(--spacing-lg); }
  &t-xl { margin-top: var(--spacing-xl); }

  &b-xs { margin-bottom: var(--spacing-xs); }
  &b-sm { margin-bottom: var(--spacing-sm); }
  &b-md { margin-bottom: var(--spacing-md); }
  &b-lg { margin-bottom: var(--spacing-lg); }
  &b-xl { margin-bottom: var(--spacing-xl); }
}

.p {
  &-xs { padding: var(--spacing-xs); }
  &-sm { padding: var(--spacing-sm); }
  &-md { padding: var(--spacing-md); }
  &-lg { padding: var(--spacing-lg); }
  &-xl { padding: var(--spacing-xl); }
}

// Flex
.flex {
  display: flex;

  &-center {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &-between {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  &-column {
    display: flex;
    flex-direction: column;
  }
}

// 圆角
.rounded {
  &-small { border-radius: var(--border-radius-small); }
  &-medium { border-radius: var(--border-radius-medium); }
  &-large { border-radius: var(--border-radius-large); }
  &-full { border-radius: 9999px; }
}

// 阴影
.shadow {
  &-1 { box-shadow: var(--shadow-1); }
  &-2 { box-shadow: var(--shadow-2); }
  &-3 { box-shadow: var(--shadow-3); }
  &-none { box-shadow: none; }
}
```

### Markdown 样式

```scss
// src/assets/styles/markdown.scss
.markdown-body {
  font-family: var(--font-family);
  font-size: var(--font-size-base);
  line-height: var(--line-height-base);
  color: var(--text-color);
  word-wrap: break-word;

  // 标题
  h1, h2, h3, h4, h5, h6 {
    margin-top: 24px;
    margin-bottom: 16px;
    font-weight: var(--font-weight-semibold);
    line-height: var(--line-height-heading);
  }

  h1 { font-size: var(--font-size-3xl); }
  h2 { font-size: var(--font-size-2xl); }
  h3 { font-size: var(--font-size-xl); }
  h4 { font-size: var(--font-size-lg); }
  h5 { font-size: var(--font-size-md); }
  h6 { font-size: var(--font-size-base); }

  // 段落
  p {
    margin-top: 0;
    margin-bottom: 16px;
  }

  // 链接
  a {
    color: var(--primary-color);
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }

  // 列表
  ul, ol {
    margin-top: 0;
    margin-bottom: 16px;
    padding-left: 2em;
  }

  li {
    margin-bottom: 4px;
  }

  // 代码
  code {
    padding: 2px 6px;
    margin: 0 2px;
    font-family: var(--font-family-mono);
    font-size: 0.9em;
    background: var(--bg-color-2);
    border-radius: var(--border-radius-small);
  }

  pre {
    padding: 16px;
    margin: 0 0 16px;
    overflow: auto;
    font-family: var(--font-family-mono);
    font-size: var(--font-size-sm);
    line-height: 1.45;
    background: var(--bg-color-2);
    border-radius: var(--border-radius-medium);

    code {
      padding: 0;
      margin: 0;
      font-size: 100%;
      background: transparent;
      border-radius: 0;
    }
  }

  // 引用
  blockquote {
    padding: 0 1em;
    margin: 0 0 16px;
    color: var(--text-color-2);
    border-left: 4px solid var(--border-color-1);
  }

  // 表格
  table {
    width: 100%;
    margin-bottom: 16px;
    border-collapse: collapse;
  }

  th, td {
    padding: 8px 16px;
    border: 1px solid var(--border-color-1);
  }

  th {
    font-weight: var(--font-weight-semibold);
    background: var(--bg-color-2);
  }

  // 分隔线
  hr {
    height: 1px;
    margin: 24px 0;
    padding: 0;
    background: var(--border-color-1);
    border: none;
  }

  // 图片
  img {
    max-width: 100%;
    height: auto;
    border-radius: var(--border-radius-small);
  }
}
```

## 响应式设计

### 断点系统

```scss
// src/assets/styles/breakpoints.scss
$breakpoints: (
  'xs': 480px,
  'sm': 576px,
  'md': 768px,
  'lg': 992px,
  'xl': 1200px,
  'xxl': 1600px
);

// Mixins
@mixin respond-to($breakpoint) {
  @if map-has-key($breakpoints, $breakpoint) {
    @media (min-width: map-get($breakpoints, $breakpoint)) {
      @content;
    }
  } @else {
    @warn "Unknown breakpoint: #{$breakpoint}.";
  }
}

@mixin respond-between($lower, $upper) {
  @if map-has-key($breakpoints, $lower) and map-has-key($breakpoints, $upper) {
    @media (min-width: map-get($breakpoints, $lower)) and (max-width: map-get($breakpoints, $upper)) {
      @content;
    }
  }
}

// 使用示例
.container {
  padding: 16px;

  @include respond-to('md') {
    padding: 24px;
  }

  @include respond-to('lg') {
    padding: 32px;
  }
}
```

### 网格系统

```vue
<!-- 响应式布局 -->
<template>
  <div class="container">
    <n-grid
      :cols="1"
      :x-gap="16"
      :y-gap="16"
      responsive="screen"
    >
      <n-grid-item :span="1">
        <!-- 移动端: 1列 -->
      </n-grid-item>
      <n-grid-item :span="2">
        <!-- 平板: 2列 -->
      </n-grid-item>
      <n-grid-item :span="3">
        <!-- 桌面: 3列 -->
      </n-grid-item>
    </n-grid>
  </div>
</template>
```

### 移动端适配

```scss
// 移动端优先
.container {
  padding: 16px; // 默认移动端样式

  @media (min-width: 768px) {
    padding: 24px; // 平板
  }

  @media (min-width: 1024px) {
    padding: 32px; // 桌面
  }
}

// 字体大小
.heading {
  font-size: 24px; // 移动端

  @media (min-width: 768px) {
    font-size: 32px; // 桌面
  }
}
```

## 组件样式覆盖

### Naive UI 组件覆盖

```scss
// src/assets/styles/naive-ui-overrides.scss
// 按钮
.n-button {
  &--primary {
    &.n-button--disabled {
      opacity: 0.5;
    }
  }
}

// 卡片
.n-card {
  border-radius: var(--border-radius-medium);
  box-shadow: var(--shadow-1);

  &:hover {
    box-shadow: var(--shadow-2);
  }
}

// 输入框
.n-input {
  .n-input__input {
    font-size: var(--font-size-base);
  }

  &.n-input--focus {
    box-shadow: 0 0 0 2px rgba(24, 160, 88, 0.2);
  }
}

// 下拉菜单
.n-dropdown-menu {
  border-radius: var(--border-radius-medium);
  box-shadow: var(--shadow-2);
}

// 模态框
.n-modal {
  .n-modal-container {
    border-radius: var(--border-radius-large);
  }
}
```

### 自定义组件样式

```vue
<!-- 组件中使用 -->
<template>
  <div class="custom-card">
    <div class="custom-card__header">
      <h3 class="custom-card__title">{{ title }}</h3>
    </div>
    <div class="custom-card__body">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.custom-card {
  background: var(--bg-color-1);
  border: 1px solid var(--border-color-1);
  border-radius: var(--border-radius-medium);
  box-shadow: var(--shadow-1);
  transition: box-shadow var(--transition-duration);

  &:hover {
    box-shadow: var(--shadow-2);
  }

  &__header {
    padding: var(--spacing-md);
    border-bottom: 1px solid var(--border-color-1);
  }

  &__title {
    margin: 0;
    font-size: var(--font-size-lg);
    font-weight: var(--font-weight-semibold);
    color: var(--text-color-1);
  }

  &__body {
    padding: var(--spacing-md);
  }
}
</style>
```

## 动画效果

### 过渡动画

```scss
// src/assets/styles/transitions.scss
// 淡入淡出
.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--transition-duration);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

// 滑动
.slide-enter-active,
.slide-leave-active {
  transition: transform var(--transition-duration);
}

.slide-enter-from {
  transform: translateX(-100%);
}

.slide-leave-to {
  transform: translateX(100%);
}

// 缩放
.scale-enter-active,
.scale-leave-active {
  transition: transform var(--transition-duration);
}

.scale-enter-from,
.scale-leave-to {
  transform: scale(0.9);
  opacity: 0;
}
```

### Vue Transition 使用

```vue
<template>
  <transition name="fade" mode="out-in">
    <component :is="currentComponent" />
  </transition>
</template>
```

### 加载动画

```scss
// 脉冲动画
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.loading-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

// 旋转动画
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.loading-spinner {
  animation: spin 1s linear infinite;
}
```

## 无障碍访问

### ARIA 属性

```vue
<template>
  <!-- 按钮带提示 -->
  <n-button
    aria-label="关闭对话框"
    @click="close"
  >
    <template #icon>
      <n-icon :component="CloseIcon" />
    </template>
  </n-button>

  <!-- 表单标签 -->
  <n-form-item label="邮箱">
    <n-input
      id="email"
      v-model:value="email"
      aria-required="true"
      aria-describedby="email-hint"
    />
    <template #feedback>
      <span id="email-hint">请输入您的邮箱地址</span>
    </template>
  </n-form-item>
</template>
```

### 焦点管理

```scss
// 可见焦点样式
:focus-visible {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}

// 跳过链接
.skip-to-content {
  position: absolute;
  top: -40px;
  left: 0;
  padding: 8px;
  background: var(--primary-color);
  color: white;
  text-decoration: none;
  z-index: 100;

  &:focus {
    top: 0;
  }
}
```

### 颜色对比度

```scss
// 确保足够的对比度（至少 4.5:1）
.text-on-primary {
  background: var(--primary-color);
  color: #ffffff; // 在绿色背景上使用白色
}

.text-on-disabled {
  background: var(--bg-color-3);
  color: var(--text-color-disabled); // 使用足够的对比度
}
```

## 性能优化

### CSS 优化

```scss
// 避免深层嵌套（不超过 3 层）
// ❌ 不好
.card {
  .header {
    .title {
      .text {
        color: red;
      }
    }
  }
}

// ✅ 好
.card {
  .header {
    // ...
  }

  &__title {
    // ...
  }

  &__text {
    color: red;
  }
}
```

### 减少重排重绘

```scss
// 使用 transform 代替 top/left
.animated {
  // ❌ 不好：触发重排
  // left: 100px;

  // ✅ 好：只触发合成
  transform: translateX(100px);
}

// 使用 opacity 代替 visibility
.fade {
  // ✅ 好：可以使用 GPU 加速
  opacity: 0;
  transition: opacity 0.3s;
}
```

### 关键 CSS

```html
<!-- 内联关键 CSS -->
<style>
  /* 首屏立即需要的样式 */
  .header {
    /* ... */
  }
</style>

<!-- 延迟加载非关键 CSS -->
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
```

## 最佳实践

### 1. BEM 命名规范

```scss
// Block
.card {}

// Element
.card__header {}
.card__body {}
.card__footer {}

// Modifier
.card--primary {}
.card--disabled {}
```

### 2. 使用 CSS 变量

```scss
// ✅ 好的做法
.button {
  background: var(--primary-color);
  padding: var(--spacing-md);
  border-radius: var(--border-radius-medium);
}

// ❌ 不好的做法（硬编码）
.button {
  background: #18a058;
  padding: 16px;
  border-radius: 8px;
}
```

### 3. 避免使用 !important

```scss
// ❌ 不好
.button {
  color: red !important;
}

// ✅ 好：使用更高优先级的选择器
.card .button {
  color: red;
}

// 或使用 CSS 变量
.button {
  color: var(--button-color);
}

.button--primary {
  --button-color: red;
}
```

### 4. 模块化样式

```vue
<!-- 组件作用域样式 -->
<style scoped>
/* 只作用于当前组件 */
.card {
  background: var(--bg-color);
}
</style>

<!-- 全局样式（谨慎使用） -->
<style>
/* 影响所有组件 */
body {
  margin: 0;
  font-family: var(--font-family);
}
</style>
```

## 相关文档

- [前端架构](/guide/frontend-architecture)
- [组件设计](/guide/frontend-components)
- [状态管理](/guide/frontend-state-management)
