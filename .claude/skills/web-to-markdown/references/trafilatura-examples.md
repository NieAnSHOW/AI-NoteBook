# Trafilatura 使用示例

## 概述

Trafilatura 是一个智能网页内容提取库，核心优势：

1. **智能提取**: 自动识别和提取网页正文内容
2. **元数据提取**: 自动获取标题、作者、发布日期等信息
3. **内容清理**: 过滤广告、导航、页脚等无关内容
4. **多种格式**: 支持 Markdown、JSON、XML、纯文本输出

## 依赖安装

```bash
pip install trafilatura requests
```

## 使用方式

### 1. 通过 URL 直接转换（推荐）

最简单的方式：直接提供 URL，脚本会自动获取并转换。

```bash
# 基本用法 - 从 URL 获取并转换
echo '{"url": "https://example.com/article"}' | \
  python scripts/convert_with_trafilatura.py
```

### 2. 指定输出格式

```bash
# 输出 JSON 格式
echo '{"url": "https://example.com", "output_format": "json"}' | \
  python scripts/convert_with_trafilatura.py

# 输出纯文本
echo '{"url": "https://example.com", "output_format": "txt"}' | \
  python scripts/convert_with_trafilatura.py

# 输出 XML
echo '{"url": "https://example.com", "output_format": "xml"}' | \
  python scripts/convert_with_trafilatura.py
```

### 3. 包含/排除元数据

```bash
# 包含元数据（默认）
echo '{"url": "https://example.com", "include_metadata": true}' | \
  python scripts/convert_with_trafilatura.py

# 不包含元数据
echo '{"url": "https://example.com", "include_metadata": false}' | \
  python scripts/convert_with_trafilatura.py
```

### 4. 自定义超时时间

```bash
# 设置 60 秒超时
echo '{"url": "https://example.com", "timeout": 60}' | \
  python scripts/convert_with_trafilatura.py
```

### 5. 从 HTML 内容转换

如果已经获取了 HTML，可以直接转换：

```bash
# 从本地 HTML 文件转换
echo '{"html": "'"$(cat article.html | jq -Rs .)"'", "url": "https://example.com"}' | \
  python scripts/convert_with_trafilatura.py
```

## 完整工作流示例

### 示例 1: 从 URL 获取并保存到文件

```bash
# 1. 使用 trafilatura 转换
RESULT=$(echo '{"url": "https://example.com"}' | \
  python scripts/convert_with_trafilatura.py)

# 2. 提取内容和元数据
MARKDOWN=$(echo "$RESULT" | jq -r '.content')
TITLE=$(echo "$RESULT" | jq -r '.metadata.title')
URL=$(echo "$RESULT" | jq -r '.metadata.url')

# 3. 保存到文件
echo "{\"markdown\": \"$MARKDOWN\", \"title\": \"$TITLE\", \"url\": \"$URL\"}" | \
  python scripts/save_to_file.py
```

### 示例 2: 单行命令完整流程

```bash
# 一行命令完成转换和保存
echo '{"url": "https://example.com"}' | \
  python scripts/convert_with_trafilatura.py | \
  jq '{markdown: .content, title: .metadata.title, url: .metadata.url}' | \
  python scripts/save_to_file.py
```

### 示例 3: 指定输出路径和文件名

```bash
echo '{"url": "https://example.com"}' | \
  python scripts/convert_with_trafilatura.py | \
  jq '{
      markdown: .content,
      title: .metadata.title,
      url: .metadata.url,
      output_path: "/path/to/articles",
      filename: "my-article.md"
    }' | \
  python scripts/save_to_file.py
```

## 输出格式说明

### Markdown 格式（默认）

```
# 标题

**作者**: 作者名
**发布日期**: 2024-01-19
**描述**: 文章描述

---

正文内容...

---

来源: https://example.com
```

### JSON 格式

```json
{
  "status": "success",
  "content": "# 标题\n\n正文内容...",
  "metadata": {
    "title": "标题",
    "author": "作者",
    "date": "2024-01-19",
    "description": "描述",
    "url": "https://example.com"
  },
  "url": "https://example.com"
}
```

### 错误响应

```json
{
  "status": "error",
  "error_type": "HTTPError",
  "message": "HTTP 错误: 404"
}
```

## 支持的网站类型

Trafilatura 可以处理多种类型的网站：

- ✅ 新闻网站文章
- ✅ 博客文章
- ✅ 技术文档
- ✅ 学术论文
- ✅ 普通网页
- ⚠️ 微信公众号（需要先通过其他方式获取 HTML）
- ⚠️ 需要登录的网站（需要先获取已登录的 HTML）

对于有反爬机制的网站（如微信公众号），建议：
1. 使用浏览器获取 HTML
2. 粘贴 HTML 内容到工具中
3. 使用 trafilatura 转换

## 最佳实践

### 1. 使用 URL 模式（最简单）

```bash
# 直接使用 URL
echo '{"url": "https://example.com"}' | \
  python scripts/convert_with_trafilatura.py | \
  python scripts/save_to_file.py
```

### 2. 处保存到指定目录

```bash
# 保存到特定目录
echo '{"url": "https://example.com"}' | \
  python scripts/convert_with_trafilatura.py | \
  jq '{markdown: .content, title: .metadata.title, url: .metadata.url, output_path: "./articles"}' | \
  python scripts/save_to_file.py
```

### 3. 批量处理多个 URL

```bash
#!/bin/bash
URLS=(
  "https://example.com/article1"
  "https://example.com/article2"
  "https://example.com/article3"
)

for url in "${URLS[@]}"; do
  echo "处理: $url"
  echo "{\"url\": \"$url\"}" | \
    python scripts/convert_with_trafilatura.py | \
    jq '{markdown: .content, title: .metadata.title, url: .metadata.url, output_path: "./articles"}' | \
    python scripts/save_to_file.py
done
```

## 常见问题

### Q: 提取的内容不完整？

A: 某些网站使用 JavaScript 动态加载内容。对于这种情况：
1. 使用浏览器打开页面
2. 右键"查看页面源代码"或使用开发者工具
3. 复制 HTML 内容
4. 使用 HTML 模式转换

### Q: 如何处理微信文章？

A: 微信公众号有反爬机制，建议：
1. 使用浏览器打开微信文章
2. 使用浏览器扩展或开发者工具获取完整 HTML
3. 使用 HTML 模式转换

### Q: 超时怎么办？

A: 可以增加超时时间：

```bash
echo '{"url": "https://example.com", "timeout": 60}' | \
  python scripts/convert_with_trafilatura.py
```

### Q: 如何获取纯文本不含元数据？

A:

```bash
echo '{"url": "https://example.com", "output_format": "txt", "include_metadata": false}' | \
  python scripts/convert_with_trafilatura.py
```
