# 前端状态管理

本文档详细说明 AI-NoteBook 前端状态管理系统的设计。

## 概述

AI-NoteBook 使用 **Pinia** 作为状态管理库，它是 Vue 3 官方推荐的状态管理方案。

### 为什么选择 Pinia？

- ✅ **完整的 TypeScript 支持**：类型推断更准确
- ✅ **Composition API 风格**：与 Vue 3 保持一致
- ✅ **极简 API**：相比 Vuex 更简洁
- ✅ **DevTools 集成**：调试体验优秀
- ✅ **模块化设计**：天然支持代码分割
- ✅ **无 Mutations**：简化状态更新逻辑

### Store 架构

```
src/stores/
├── index.ts              # Store 入口，统一导出
├── user.ts               # 用户状态
├── analysis.ts           # 分析状态
└── app.ts                # 应用状态
```

## Store 设计规范

### 1. 用户状态 (User Store)

管理用户登录、会员信息、API Key 等。

```typescript
// src/stores/user.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import type { User, Membership, LoginDto, RegisterDto } from '@/types/user'

export const useUserStore = defineStore('user', () => {
  // ===== State =====
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const apiKey = ref<string | null>(null)

  // ===== Getters =====
  const isLoggedIn = computed(() => !!user.value && !!accessToken.value)

  const membership = computed<Membership>(() => user.value?.membership || Membership.FREE)

  const maxConcurrent = computed(() => {
    const levels = {
      [Membership.FREE]: 1,
      [Membership.PRO]: 5,
      [Membership.ENTERPRISE]: 20
    }
    return levels[membership.value]
  })

  const canUseExpansion = computed(() => {
    return membership.value !== Membership.FREE
  })

  const displayName = computed(() => {
    return user.value?.username || user.value?.email || '用户'
  })

  // ===== Actions =====

  // 登录
  async function login(dto: LoginDto) {
    const data = await authApi.login(dto.email, dto.password)

    // 保存用户信息和 Token
    setUserData(data.user)
    setTokens(data.tokens)

    // 保存 API Key 到 localStorage
    if (data.user.apiKey) {
      localStorage.setItem('apiKey', data.user.apiKey)
      apiKey.value = data.user.apiKey
    }

    return data
  }

  // 注册
  async function register(dto: RegisterDto) {
    const data = await authApi.register(dto.email, dto.password, dto.username)

    setUserData(data.user)
    setTokens(data.tokens)

    if (data.user.apiKey) {
      localStorage.setItem('apiKey', data.user.apiKey)
      apiKey.value = data.user.apiKey
    }

    return data
  }

  // 登出
  async function logout() {
    // 清除本地状态
    clearUserData()

    // 清除 localStorage
    localStorage.removeItem('apiKey')
    localStorage.removeItem('refreshToken')

    // 跳转到登录页
    window.location.href = '/login'
  }

  // 刷新 Token
  async function refreshAccessToken() {
    if (!refreshToken.value) {
      throw new Error('No refresh token available')
    }

    const data = await authApi.refreshToken(refreshToken.value)

    accessToken.value = data.accessToken

    return data.accessToken
  }

  // 设置用户数据
  function setUserData(data: User) {
    user.value = data
  }

  // 设置 Tokens
  function setTokens(tokens: { accessToken: string; refreshToken: string }) {
    accessToken.value = tokens.accessToken
    refreshToken.value = tokens.refreshToken

    // Refresh Token 存储到 localStorage
    localStorage.setItem('refreshToken', tokens.refreshToken)
  }

  // 设置 Access Token
  function setAccessToken(token: string) {
    accessToken.value = token
  }

  // 设置 API Key
  function setApiKey(key: string) {
    apiKey.value = key
    localStorage.setItem('apiKey', key)

    // 同步更新 user
    if (user.value) {
      user.value.apiKey = key
    }
  }

  // 清除用户数据
  function clearUserData() {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    apiKey.value = null
  }

  // 从 localStorage 恢复会话
  function restoreSession() {
    const savedApiKey = localStorage.getItem('apiKey')
    const savedRefreshToken = localStorage.getItem('refreshToken')

    if (savedApiKey) {
      apiKey.value = savedApiKey
    }

    if (savedRefreshToken) {
      refreshToken.value = savedRefreshToken
      // 尝试用 refresh token 获取新的 access token
      refreshAccessToken().catch(() => {
        // Refresh token 无效，清除会话
        clearUserData()
      })
    }
  }

  return {
    // State
    user,
    accessToken,
    refreshToken,
    apiKey,

    // Getters
    isLoggedIn,
    membership,
    maxConcurrent,
    canUseExpansion,
    displayName,

    // Actions
    login,
    register,
    logout,
    refreshAccessToken,
    setUserData,
    setTokens,
    setAccessToken,
    setApiKey,
    clearUserData,
    restoreSession
  }
})

// 持久化配置
export const userStorePersist = {
  key: 'user-store',
  storage: localStorage,
  paths: ['user', 'apiKey'] // 只持久化这些字段
}
```

### 2. 分析状态 (Analysis Store)

管理文章分析任务、历史记录、当前分析等。

```typescript
// src/stores/analysis.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { analysisApi } from '@/api/analysis'
import { wsService } from '@/api/websocket'
import type {
  AnalysisDetail,
  AnalyzeDto,
  AnalysisStatus,
  ReadabilityScore
} from '@/types/analysis'

export const useAnalysisStore = defineStore('analysis', () => {
  // ===== State =====
  const currentAnalysis = ref<AnalysisDetail | null>(null)
  const analysisHistory = ref<AnalysisDetail[]>([])
  const processingCount = ref(0)
  const loading = ref(false)

  // ===== Getters =====
  const hasCurrentAnalysis = computed(() => !!currentAnalysis.value)

  const isProcessing = computed(() => {
    return currentAnalysis.value?.status === 'PROCESSING'
  })

  const isCompleted = computed(() => {
    return currentAnalysis.value?.status === 'COMPLETED'
  })

  const isFailed = computed(() => {
    return currentAnalysis.value?.status === 'FAILED'
  })

  const completedAnalyses = computed(() => {
    return analysisHistory.value.filter(a => a.status === 'COMPLETED')
  })

  const failedAnalyses = computed(() => {
    return analysisHistory.value.filter(a => a.status === 'FAILED')
  })

  // ===== Actions =====

  // 创建分析任务
  async function createAnalysis(dto: AnalyzeDto) {
    loading.value = true

    try {
      const result = await analysisApi.create(dto)

      // 设置当前分析
      currentAnalysis.value = {
        id: result.taskId,
        status: 'PROCESSING',
        userId: '', // 从后端获取
        title: dto.title || '未命名文章',
        originalContent: dto.content,
        processedContent: '',
        readabilityScore: {} as ReadabilityScore,
        expansions: null,
        sources: null,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      }

      // 订阅进度更新
      subscribeToProgress(result.taskId)

      // 增加处理中计数
      processingCount.value++

      return result
    } finally {
      loading.value = false
    }
  }

  // 获取分析详情
  async function getAnalysis(id: string) {
    loading.value = true

    try {
      const data = await analysisApi.getOne(id)
      currentAnalysis.value = data
      return data
    } finally {
      loading.value = false
    }
  }

  // 获取历史记录
  async function fetchHistory(params?: {
    page?: number
    limit?: number
    status?: AnalysisStatus
  }) {
    loading.value = true

    try {
      const data = await analysisApi.getHistory(params || {})
      analysisHistory.value = data.items

      // 更新处理中计数
      processingCount.value = data.items.filter(
        a => a.status === 'PROCESSING'
      ).length

      return data
    } finally {
      loading.value = false
    }
  }

  // 删除分析
  async function deleteAnalysis(id: string) {
    await analysisApi.delete(id)

    // 从历史记录中移除
    const index = analysisHistory.value.findIndex(a => a.id === id)
    if (index > -1) {
      analysisHistory.value.splice(index, 1)
    }

    // 如果删除的是当前分析，清除当前分析
    if (currentAnalysis.value?.id === id) {
      currentAnalysis.value = null
    }
  }

  // 批量删除
  async function batchDelete(ids: string[]) {
    await Promise.all(ids.map(id => deleteAnalysis(id)))
  }

  // 清空历史
  function clearHistory() {
    analysisHistory.value = []
    currentAnalysis.value = null
    processingCount.value = 0
  }

  // 订阅进度更新
  function subscribeToProgress(taskId: string) {
    const unsubscribe = wsService.subscribeToAnalysis(
      taskId,
      (data: { progress: number; message: string; result?: any }) => {
        if (currentAnalysis.value?.id === taskId) {
          // 更新进度
          if (data.result) {
            // 分析完成，更新完整数据
            currentAnalysis.value = {
              ...currentAnalysis.value,
              ...data.result,
              status: 'COMPLETED'
            }
          }

          // 减少处理中计数
          if (data.progress === 100 || data.result) {
            processingCount.value--
          }
        }
      }
    )

    // 返回取消订阅函数
    return unsubscribe
  }

  // 更新当前分析
  function updateCurrentAnalysis(data: Partial<AnalysisDetail>) {
    if (currentAnalysis.value) {
      currentAnalysis.value = {
        ...currentAnalysis.value,
        ...data
      }
    }
  }

  // 清除当前分析
  function clearCurrentAnalysis() {
    currentAnalysis.value = null
  }

  return {
    // State
    currentAnalysis,
    analysisHistory,
    processingCount,
    loading,

    // Getters
    hasCurrentAnalysis,
    isProcessing,
    isCompleted,
    isFailed,
    completedAnalyses,
    failedAnalyses,

    // Actions
    createAnalysis,
    getAnalysis,
    fetchHistory,
    deleteAnalysis,
    batchDelete,
    clearHistory,
    subscribeToProgress,
    updateCurrentAnalysis,
    clearCurrentAnalysis
  }
})

// 持久化配置
export const analysisStorePersist = {
  key: 'analysis-store',
  storage: sessionStorage, // 使用 sessionStorage，关闭浏览器清除
  paths: ['analysisHistory'] // 只持久化历史记录
}
```

### 3. 应用状态 (App Store)

管理应用级别的状态，如主题、侧边栏、通知等。

```typescript
// src/stores/app.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export type Theme = 'light' | 'dark' | 'auto'
export type SidebarPosition = 'left' | 'right'

export const useAppStore = defineStore('app', () => {
  // ===== State =====
  const theme = ref<Theme>('light')
  const sidebarCollapsed = ref(false)
  const sidebarPosition = ref<SidebarPosition>('left')
  const loading = ref(false)
  const globalMessage = ref<string | null>(null)

  // ===== Getters =====
  const isDarkTheme = computed(() => {
    if (theme.value === 'auto') {
      return window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    return theme.value === 'dark'
  })

  const loadingText = computed(() => {
    return globalMessage.value || '加载中...'
  })

  // ===== Actions =====

  // 设置主题
  function setTheme(newTheme: Theme) {
    theme.value = newTheme
    applyTheme()
  }

  // 切换主题
  function toggleTheme() {
    const themes: Theme[] = ['light', 'dark', 'auto']
    const currentIndex = themes.indexOf(theme.value)
    const nextIndex = (currentIndex + 1) % themes.length
    setTheme(themes[nextIndex])
  }

  // 应用主题
  function applyTheme() {
    const dark = isDarkTheme.value

    if (dark) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  // 切换侧边栏
  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  // 设置侧边栏状态
  function setSidebarCollapsed(collapsed: boolean) {
    sidebarCollapsed.value = collapsed
  }

  // 设置侧边栏位置
  function setSidebarPosition(position: SidebarPosition) {
    sidebarPosition.value = position
  }

  // 显示全局加载
  function showLoading(message?: string) {
    loading.value = true
    if (message) {
      globalMessage.value = message
    }
  }

  // 隐藏全局加载
  function hideLoading() {
    loading.value = false
    globalMessage.value = null
  }

  // 初始化
  function init() {
    // 从 localStorage 恢复主题设置
    const savedTheme = localStorage.getItem('theme') as Theme
    if (savedTheme) {
      theme.value = savedTheme
    }

    // 应用主题
    applyTheme()

    // 监听系统主题变化（auto 模式）
    if (theme.value === 'auto') {
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applyTheme)
    }
  }

  return {
    // State
    theme,
    sidebarCollapsed,
    sidebarPosition,
    loading,
    globalMessage,

    // Getters
    isDarkTheme,
    loadingText,

    // Actions
    setTheme,
    toggleTheme,
    applyTheme,
    toggleSidebar,
    setSidebarCollapsed,
    setSidebarPosition,
    showLoading,
    hideLoading,
    init
  }
})

// 持久化配置
export const appStorePersist = {
  key: 'app-store',
  storage: localStorage,
  paths: ['theme', 'sidebarCollapsed', 'sidebarPosition']
}
```

## Store 持久化

### Pinia Plugin: persist

使用 `pinia-plugin-persistedstate` 实现状态持久化。

#### 安装

```bash
npm install pinia-plugin-persistedstate
```

#### 配置

```typescript
// src/main.ts
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

app.use(pinia)
```

#### 使用

在每个 Store 中定义 `persist` 配置：

```typescript
export const useUserStore = defineStore('user', () => {
  // ... store logic
}, {
  persist: {
    key: 'user-store',
    storage: localStorage,
    paths: ['user', 'apiKey'] // 只持久化特定字段
  }
})
```

### 自定义持久化策略

```typescript
// src/stores/plugins/persist.ts
import { PiniaPluginContext } from 'pinia'

interface PersistOptions {
  key?: string
  storage?: Storage
  paths?: string[]
  serializer?: {
    serialize: (state: any) => string
    deserialize: (value: string) => any
  }
}

export function createPersist(options: PersistOptions = {}) {
  return (context: PiniaPluginContext) => {
    const { store } = context

    const {
      key = store.$id,
      storage = localStorage,
      paths,
      serializer = JSON
    } = options

    // 从 storage 恢复状态
    const savedState = storage.getItem(key)
    if (savedState) {
      try {
        const state = serializer.deserialize(savedState)
        store.$patch(state)
      } catch (error) {
        console.error('Failed to restore state:', error)
      }
    }

    // 监听状态变化，保存到 storage
    store.$subscribe((mutation, state) => {
      let toSave: any = state

      // 如果指定了 paths，只保存特定字段
      if (paths) {
        toSave = paths.reduce((acc, path) => {
          acc[path] = state[path]
          return acc
        }, {} as any)
      }

      try {
        storage.setItem(key, serializer.stringify(toSave))
      } catch (error) {
        console.error('Failed to persist state:', error)
      }
    })
  }
}

// 使用
// src/main.ts
import { createPersist } from './stores/plugins/persist'

pinia.use(createPersist({
  storage: localStorage
}))
```

## Store 测试

### 单元测试

```typescript
// stores/__tests__/user.spec.ts
import { setActivePinia, createPinia } from 'pinia'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useUserStore } from '../user'
import { authApi } from '@/api/auth'

vi.mock('@/api/auth')

describe('User Store', () => {
  beforeEach(() => {
    // 创建新的 pinia 实例
    setActivePinia(createPinia())
  })

  it('initial state is correct', () => {
    const store = useUserStore()

    expect(store.user).toBeNull()
    expect(store.accessToken).toBeNull()
    expect(store.isLoggedIn).toBe(false)
  })

  it('login updates user state', async () => {
    const mockUser = {
      id: '123',
      email: 'test@example.com',
      membership: 'PRO',
      apiKey: 'test-key'
    }

    authApi.login = vi.fn().mockResolvedValue({
      user: mockUser,
      tokens: {
        accessToken: 'access-token',
        refreshToken: 'refresh-token'
      }
    })

    const store = useUserStore()
    await store.login({
      email: 'test@example.com',
      password: 'password'
    })

    expect(store.user).toEqual(mockUser)
    expect(store.accessToken).toBe('access-token')
    expect(store.isLoggedIn).toBe(true)
  })

  it('logout clears user state', () => {
    const store = useUserStore()

    store.setUserData({
      id: '123',
      email: 'test@example.com',
      membership: 'FREE',
      apiKey: 'key'
    } as any)
    store.setAccessToken('token')

    expect(store.isLoggedIn).toBe(true)

    store.clearUserData()

    expect(store.user).toBeNull()
    expect(store.accessToken).toBeNull()
    expect(store.isLoggedIn).toBe(false)
  })

  it('maxConcurrent returns correct value', () => {
    const store = useUserStore()

    store.setUserData({ membership: 'FREE' } as any)
    expect(store.maxConcurrent).toBe(1)

    store.setUserData({ membership: 'PRO' } as any)
    expect(store.maxConcurrent).toBe(5)

    store.setUserData({ membership: 'ENTERPRISE' } as any)
    expect(store.maxConcurrent).toBe(20)
  })
})
```

### 集成测试

```typescript
// stores/__tests__/integration.spec.ts
import { setActivePinia, createPinia } from 'pinia'
import { describe, it, expect, beforeEach } from 'vitest'
import { useUserStore } from '../user'
import { useAnalysisStore } from '../analysis'

describe('Store Integration', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('user login affects analysis permissions', () => {
    const userStore = useUserStore()
    const analysisStore = useAnalysisStore()

    // FREE 用户
    userStore.setUserData({ membership: 'FREE' } as any)

    expect(userStore.maxConcurrent).toBe(1)
    expect(userStore.canUseExpansion).toBe(false)

    // 升级到 PRO
    userStore.setUserData({ membership: 'PRO' } as any)

    expect(userStore.maxConcurrent).toBe(5)
    expect(userStore.canUseExpansion).toBe(true)
  })
})
```

## 最佳实践

### 1. Store 命名规范

```typescript
// ✅ 好的命名
useUserStore
useAnalysisStore
useAppStore

// ❌ 不好的命名
user
userData
storeUser
```

### 2. 状态结构设计

```typescript
// ✅ 使用扁平化结构
export const useUserStore = defineStore('user', () => {
  const id = ref<string>()
  const email = ref<string>()
  const membership = ref<Membership>()

  return { id, email, membership }
})

// ❌ 避免深层嵌套
export const useUserStore = defineStore('user', () => {
  const data = ref({
    profile: {
      id: '',
      email: '',
      membership: ''
    }
  })

  return { data }
})
```

### 3. 异步 Action 处理

```typescript
// ✅ 好的做法：明确的错误处理
async function login(dto: LoginDto) {
  loading.value = true
  error.value = null

  try {
    const data = await authApi.login(dto.email, dto.password)
    setUserData(data.user)
    return data
  } catch (err) {
    error.value = err.message
    throw err
  } finally {
    loading.value = false
  }
}

// ❌ 不好的做法：不处理错误
async function login(dto: LoginDto) {
  const data = await authApi.login(dto.email, dto.password)
  setUserData(data.user)
}
```

### 4. 避免在 Store 中直接调用 UI

```typescript
// ❌ 不好的做法
async function login(dto: LoginDto) {
  const data = await authApi.login(dto.email, dto.password)
  window.$message?.success('登录成功') // 不要在 Store 中直接调用 UI
  setUserData(data.user)
}

// ✅ 好的做法：返回结果，让组件处理 UI
async function login(dto: LoginDto) {
  const data = await authApi.login(dto.email, dto.password)
  setUserData(data.user)
  return data
}

// 在组件中
const { login } = useUserStore()
try {
  await login(dto)
  window.$message?.success('登录成功')
} catch (error) {
  window.$message?.error('登录失败')
}
```

### 5. 合理使用 Getters

```typescript
// ✅ 使用 getter 计算派生状态
const displayName = computed(() => {
  return user.value?.username || user.value?.email || '用户'
})

// ❌ 在组件中重复计算
// component.vue
const userStore = useUserStore()
const displayName = computed(() =>
  userStore.user?.username || userStore.user?.email || '用户'
)
```

### 6. Store 模块化

```typescript
// ✅ 相关状态组织在一个 Store 中
export const useAnalysisStore = defineStore('analysis', () => {
  const currentAnalysis = ref<AnalysisDetail | null>(null)
  const analysisHistory = ref<AnalysisDetail[]>([])
  const processingCount = ref(0)

  // 所有分析相关的状态和方法
  return {
    currentAnalysis,
    analysisHistory,
    processingCount,
    // ...
  }
})

// ❌ 分散在多个 Store 中
export const useCurrentAnalysisStore = defineStore('currentAnalysis', () => {
  const currentAnalysis = ref<AnalysisDetail | null>(null)
  return { currentAnalysis }
})

export const useAnalysisHistoryStore = defineStore('analysisHistory', () => {
  const analysisHistory = ref<AnalysisDetail[]>([])
  return { analysisHistory }
})
```

## 相关文档

- [前端架构](/guide/frontend-architecture)
- [组件设计](/guide/frontend-components)
- [样式主题](/guide/frontend-theming)
