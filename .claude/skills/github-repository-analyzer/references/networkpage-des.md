# 设计规范 - NetworkPage

## 1. 核心设计风格

### 1.1 设计理念
- **玻璃拟态（Glassmorphism）**：现代化的半透明玻璃质感设计
- **极简主义**：简洁清晰的视觉层次
- **高对比度**：确保可读性和可访问性
- **流畅交互**：平滑的过渡动画和微交互

## 2. 颜色系统

### 2.1 主色调
```css
- 白色：#FFFFFF (text-white)
- 白色 80% 透明度：rgba(255, 255, 255, 0.8) (text-white/80)
- 白色 70% 透明度：rgba(255, 255, 255, 0.7) (text-white/70)
- 白色 60% 透明度：rgba(255, 255, 255, 0.6) (text-white/60)
- 白色 50% 透明度：rgba(255, 255, 255, 0.5) (text-white/50)
- 白色 30% 透明度：rgba(255, 255, 255, 0.3) (text-white/30)
- 白色 15% 透明度：rgba(255, 255, 255, 0.15)
- 白色 10% 透明度：rgba(255, 255, 255, 0.1)
- 白色 5% 透明度：rgba(255, 255, 255, 0.05)
- 黑色 10% 透明度：rgba(0, 0, 0, 0.1) (bg-black/10)
```

### 2.2 渐变配色
```css
- 白色到浅白渐变：from-white/30 to-white/10
- 白色到浅白渐变（按钮）：from-white/30 to-white/20
- 活跃状态渐变：linear-gradient(135deg, rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.2))
```

## 3. 字体系统

### 3.1 字体家族
```css
主字体：'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif
```

### 3.2 字重
```css
- Light: 300 (font-light)
- Normal: 400 (font-normal)
- Medium: 500 (font-medium)
- Semibold: 600 (font-semibold)
- Bold: 700 (font-bold)
```

### 3.3 字号体系
```css
- 大标题：text-5xl (48px)
- 小标题：text-2xl (24px)
- 正文：text-sm (14px)
- 标签：text-xs (12px)
```

### 3.4 字间距
```css
- 紧凑：tracking-tighter
```

### 3.5 行高
```css
- 紧凑：leading-none
- 正常：leading-snug
- 宽松：leading-tight
- 宽：leading-relaxed
```

## 4. 圆角系统

```css
- 超大圆角：rounded-3xl (24px)
- 大圆角：rounded-2xl (16px)
- 中圆角：rounded-xl (12px)
- 小圆角：rounded-lg (8px)
- 小圆角：rounded (4px)
```

## 5. 阴影系统

### 5.1 外部阴影

#### 5.1.1 美化阴影（Beautiful Shadow）
```css
.beautiful-shadow {
    box-shadow: 
        0 2.8px 2.2px rgba(0, 0, 0, 0.034),
        0 6.7px 5.3px rgba(0, 0, 0, 0.048),
        0 12.5px 10px rgba(0, 0, 0, 0.06),
        0 22.3px 17.9px rgba(0, 0, 0, 0.072),
        0 41.8px 33.4px rgba(0, 0, 0, 0.086),
        0 100px 80px rgba(0, 0, 0, 0.12);
}
```

### 5.2 内部阴影

#### 5.2.1 主容器内阴影
```css
box-shadow: 
    inset 2px 2px 1px 0 rgba(255, 255, 255, 0.5),
    inset -1px -1px 1px 1px rgba(255, 255, 255, 0.5);
border-radius: 24px;
```

#### 5.2.2 输入框内阴影
```css
box-shadow: 
    inset 1px 1px 1px 0 rgba(255, 255, 255, 0.3),
    inset -1px -1px 1px 1px rgba(255, 255, 255, 0.1);
border-radius: 12px;
```

#### 5.2.3 Logo 内阴影
```css
box-shadow: 
    inset 3px 3px 2px 0 rgba(255, 255, 255, 0.6),
    inset -2px -2px 2px 2px rgba(255, 255, 255, 0.4);
border-radius: 16px;
```

#### 5.2.4 按钮内阴影
```css
box-shadow: 
    inset 2px 2px 1px 0 rgba(255, 255, 255, 0.5),
    inset -1px -1px 1px 1px rgba(255, 255, 255, 0.3);
border-radius: 12px;
```

#### 5.2.5 下拉菜单内阴影
```css
box-shadow: 
    inset 1px 1px 1px 0 rgba(255, 255, 255, 0.4),
    inset -1px -1px 1px 1px rgba(255, 255, 255, 0.2);
border-radius: 12px;
```

## 6. 玻璃拟态效果

### 6.1 主容器玻璃效果
```css
.glass-filter { filter: url(#glass-distortion); }
.backdrop-blur-md { backdrop-filter: blur(12px); }
.bg-white/15 { background-color: rgba(255, 255, 255, 0.15); }
```

### 6.2 Logo 玻璃效果
```css
.backdrop-blur-sm { backdrop-filter: blur(4px); }
.bg-gradient-to-br from-white/30 to-white/10
```

### 6.3 输入框玻璃效果
```css
.backdrop-blur-sm { backdrop-filter: blur(4px); }
.bg-white/10 { background-color: rgba(255, 255, 255, 0.1); }
```

### 6.4 下拉菜单玻璃效果
```css
.backdrop-blur-lg { backdrop-filter: blur(16px); }
.bg-white/15 { background-color: rgba(255, 255, 255, 0.15); }
```

## 7. 过渡动画

### 7.1 自定义过渡
```css
.transition-custom { 
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 2.2); 
}
```

### 7.2 步骤指示器过渡
```css
.step-indicator {
    transition: all 0.3s ease;
}
```

### 7.3 下拉菜单过渡
```css
.dropdown-menu {
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    opacity: 0;
    visibility: hidden;
    transform: translateY(-10px);
}

.dropdown-menu.open {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}
```

### 7.4 下拉选项过渡
```css
.dropdown-option {
    transition: all 0.15s ease;
}

.dropdown-option:hover {
    background: rgba(255, 255, 255, 0.15) !important;
}
```

### 7.5 箭头旋转过渡
```css
#dropdownChevron {
    transition: transform 0.2s;
}
```

## 8. 布局系统

### 8.1 容器布局
```css
- 主容器：flex flex-col overflow-hidden max-w-2xl w-full
- 顶部区域：h-2/4 flex flex-col text-center bg-black/10
- 底部区域：h-full flex flex-col p-8 overflow-y-auto
```

### 8.2 间距
```css
- 小间距：gap-2 (8px)
- 中间距：gap-3 (12px)
- 大间距：gap-4 (16px)
```

### 8.3 内边距
```css
- 极小：py-2 (8px), px-4 (16px)
- 小：py-3 (12px), px-4 (16px)
- 中：p-8 (32px)
```

## 9. 下拉菜单规范

### 9.1 结构
```html
<div class="dropdown-container">
    <div class="dropdown-trigger relative overflow-hidden rounded-xl">
        <!-- 触发器内容 -->
        <div id="roleDisplay">
            <span>默认文本</span>
            <svg>箭头图标</svg>
        </div>
    </div>
    
    <div class="dropdown-menu" id="roleDropdown">
        <div class="relative overflow-hidden rounded-xl">
            <!-- 下拉选项 -->
            <div class="dropdown-option" data-value="value">选项文本</div>
        </div>
    </div>
</div>
```

### 9.2 样式规范
```css
/* 触发器 */
.dropdown-trigger {
    cursor: pointer;
}

/* 下拉菜单 */
.dropdown-menu {
    position: absolute;
    top: calc(100% + 8px);
    left: 0;
    right: 0;
    z-index: 50;
    opacity: 0;
    visibility: hidden;
    transform: translateY(-10px);
    max-height: 200px;
    overflow-y: auto;
}

.dropdown-menu.open {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}

/* 下拉选项 */
.dropdown-option {
    cursor: pointer;
    padding: 8px 16px;
    background: rgba(255, 255, 255, 0.05);
}

/* 自定义滚动条 */
.dropdown-menu::-webkit-scrollbar {
    width: 4px;
}

.dropdown-menu::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 2px;
}

.dropdown-menu::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 2px;
}
```

### 9.3 交互规范
```javascript
// 状态变量
let selectedValue = '';
let isOpen = false;

// 开关下拉菜单
function toggleDropdown() {
    isOpen = !isOpen;
    dropdownMenu.classList.toggle('open', isOpen);
    dropdownChevron.style.transform = isOpen ? 'rotate(180deg)' : 'rotate(0deg)';
}

// 关闭下拉菜单
function closeDropdown() {
    isOpen = false;
    dropdownMenu.classList.remove('open');
    dropdownChevron.style.transform = 'rotate(0deg)';
}

// 点击外部关闭
document.addEventListener('click', (e) => {
    if (!dropdownTrigger.contains(e.target) && !dropdownMenu.contains(e.target)) {
        closeDropdown();
    }
});
```

## 10. Z-Index 层级

```css
- z-0: 背景玻璃滤镜层
- z-10: 半透明白色背景层
- z-20: 内阴影边框层
- z-30: 内容层（文本、输入框、按钮）
- z-50: 下拉菜单层
```

## 11. 表单元素规范

### 11.1 输入框
```html
<div class="relative overflow-hidden rounded-xl">
    <div class="absolute z-0 inset-0 backdrop-blur-sm glass-filter"></div>
    <div class="z-10 absolute inset-0 bg-white bg-opacity-10"></div>
    <div class="absolute inset-0 z-20" style="box-shadow: inset 1px 1px 1px 0 rgba(255, 255, 255, 0.3), inset -1px -1px 1px 1px rgba(255, 255, 255, 0.1); border-radius: 12px;"></div>
    <input type="text" class="z-30 relative bg-transparent w-full px-4 py-3 text-sm placeholder-gray-300 text-white border-none focus:outline-none" placeholder="Placeholder" required>
</div>
```

### 11.2 按钮
```html
<div class="relative overflow-hidden rounded-xl cursor-pointer transition-custom hover:shadow-lg pt-4">
    <div class="absolute z-0 inset-0 backdrop-blur-sm glass-filter"></div>
    <div class="z-10 absolute inset-0 bg-gradient-to-r from-white/30 to-white/20"></div>
    <div class="absolute inset-0 z-20 items-center" style="box-shadow: inset 2px 2px 1px 0 rgba(255, 255, 255, 0.5), inset -1px -1px 1px 1px rgba(255, 255, 255, 0.3); border-radius: 12px;"></div>
    <button type="submit" class="z-30 relative w-full border-none flex gap-2 text-sm font-semibold text-white bg-transparent pt-0 pr-4 pb-3 pl-4 items-center justify-center">
        <span>按钮文本</span>
        <svg>图标</svg>
    </button>
</div>
```

### 11.3 复选框
```html
<input type="checkbox" class="w-4 h-4 bg-opacity-20 border-opacity-30 focus:ring-0 focus:ring-offset-0 bg-white border-white rounded" required>
```

## 12. 响应式设计

### 12.1 隐藏元素
```css
- 小屏幕隐藏：.hidden sm:block
```

### 12.2 容器宽度
```css
- 最大宽度：max-w-2xl (672px)
- 全宽：w-full
```

## 13. SVG 图标规范

### 13.1 尺寸
```css
- Logo: 28px × 28px
- 小图标: 16px × 16px
- 按钮图标: 16px × 16px
```

### 13.2 样式
```html
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="0.75" stroke-linecap="round" stroke-linejoin="round">
```

### 13.3 颜色
```css
- 主色: text-white
- 次要色: text-white/50
- 占位符: text-gray-300
```

## 14. 可访问性规范

### 14.1 焦点状态
```css
- 输入框：focus:outline-none（配合自定义边框高亮）
- 按钮：focus:outline-none
```

### 14.2 必填字段
```html
- 使用 required 属性
- 清晰的标签和占位符文本
```

### 14.3 链接样式
```css
- 链接: text-white hover:opacity-80 transition-opacity
- 下划线: underline
```

## 15. 交互状态

### 15.1 Hover 状态
```css
- 按钮: hover:shadow-lg
- 链接: hover:opacity-80
- 下拉选项: background: rgba(255, 255, 255, 0.15)
```

### 15.2 Active 状态
```css
- 步骤指示器: .active class with gradient background
```

### 15.3 Placeholder 状态
```css
- 颜色: text-gray-300
```

## 16. 背景系统

### 16.1 主背景
```html
<body class="flex items-center justify-center min-h-screen font-light bg-[url(背景图片URL)] bg-cover">
```

### 16.2 背景图片
```css
- 推荐使用高质量自然风景或抽象图片
- URL: https://images.unsplash.com/photo-1635151227785-429f420c6b9d?w=2160&q=80
```

## 17. 文本规范

### 17.1 标题
```html
<h1 class="leading-tight text-5xl font-normal text-white tracking-tighter mb-2">标题文本</h1>
```

### 17.2 副标题
```html
<h2 class="text-2xl font-medium text-white mb-2">副标题文本</h2>
```

### 17.3 描述文本
```html
<p class="leading-relaxed text-sm font-light text-white/80">描述文本</p>
```

### 17.4 说明文本
```html
<p class="text-sm font-normal text-white/70">说明文本</p>
```

### 17.5 步骤说明
```html
<p class="text-sm font-normal text-white/70">Step X of Y • 说明文本</p>
```

## 18. 组件示例

### 18.1 卡片组件
```html
<div class="relative flex flex-col overflow-hidden cursor-default beautiful-shadow transition-custom max-w-2xl w-full font-semibold text-white rounded-3xl mx-4">
    <div class="absolute z-0 inset-0 backdrop-blur-md glass-filter overflow-hidden isolate"></div>
    <div class="z-10 absolute inset-0 bg-white bg-opacity-15"></div>
    <div class="absolute inset-0 z-20 overflow-hidden shadow-inner" style="box-shadow: inset 2px 2px 1px 0 rgba(255, 255, 255, 0.5), inset -1px -1px 1px 1px rgba(255, 255, 255, 0.5); border-radius: 24px;"></div>
    <!-- 内容 -->
</div>
```

### 18.2 进度条组件
```html
<div class="flex items-center gap-3">
    <div class="flex items-center gap-2">
        <div class="step-indicator active w-8 h-8 rounded-lg flex items-center justify-center text-xs font-semibold backdrop-blur-sm">1</div>
        <span class="text-xs font-medium text-white/90 hidden sm:block">步骤名称</span>
    </div>
    <div class="w-6 h-px bg-white/30"></div>
    <!-- 更多步骤 -->
</div>
```

## 19. CSS 变量建议（可选扩展）

```css
:root {
    --glass-blur-md: 12px;
    --glass-blur-lg: 16px;
    --glass-blur-sm: 4px;
    
    --white-100: rgba(255, 255, 255, 1);
    --white-80: rgba(255, 255, 255, 0.8);
    --white-70: rgba(255, 255, 255, 0.7);
    --white-60: rgba(255, 255, 255, 0.6);
    --white-50: rgba(255, 255, 255, 0.5);
    --white-30: rgba(255, 255, 255, 0.3);
    --white-15: rgba(255, 255, 255, 0.15);
    --white-10: rgba(255, 255, 255, 0.1);
    --white-5: rgba(255, 255, 255, 0.05);
    
    --transition-custom: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 2.2);
    --transition-fast: all 0.15s ease;
    --transition-medium: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    --transition-slow: all 0.3s ease;
}
```

## 20. 最佳实践

### 20.1 性能优化
- 使用 backdrop-filter 时注意性能影响
- 限制模糊效果的层级
- 使用 CSS transform 和 opacity 进行动画

### 20.2 可维护性
- 使用语义化的类名
- 保持样式的一致性
- 合理使用组件化思维

### 20.3 响应式
- 在小屏幕上隐藏非关键元素
- 使用相对单位
- 确保触摸友好的交互区域

### 20.4 可访问性
- 提供足够的对比度
- 使用语义化 HTML
- 支持键盘导航
- 提供清晰的焦点状态

## 21. 依赖库

```html
<!-- Tailwind CSS -->
<script src="https://cdn.tailwindcss.com"></script>

<!-- Google Fonts - Inter -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

---

**文档版本**: 1.0  
**最后更新**: 2026-01-15  
**设计来源**: demo.html
