# 依赖安装指南

## 概述

web-to-markdown Skill 使用 Trafilatura 进行网页内容提取和 Markdown 转换。

## 核心依赖

### 必需依赖

| 依赖 | 版本要求 | 用途 |
|-----|---------|------|
| `trafilatura` | 最新版 | 网页内容智能提取和 Markdown 转换 |
| `requests` | 最新版 | HTTP 请求（获取网页内容） |

### 安装命令

```bash
# 安装所有依赖
pip install trafilatura requests
```

## 详细说明

### Trafilatura

**用途**: 智能网页内容提取和 Markdown 转换

**特性**:
- 自动提取网页正文（智能过滤广告、导航等无关内容）
- 提取元数据（标题、作者、发布日期、描述等）
- 支持多种输出格式（XML、JSON、Markdown、纯文本）
- 更好的内容质量和准确性

**安装**:
```bash
pip install trafilatura
```

**验证**:
```bash
python -c "import trafilatura; print('trafilatura 安装成功')"
```

---

### requests

**用途**: HTTP 请求库，用于获取网页内容

**安装**:
```bash
pip install requests
```

**验证**:
```bash
python -c "import requests; print('requests 安装成功')"
```

---

## 虚拟环境（推荐）

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install trafilatura requests
```

## 快速测试

安装完成后，可以快速测试：

```bash
# 测试转换功能
echo '{"url": "https://example.com"}' | python scripts/convert_with_trafilatura.py
```

## 故障排除

### 依赖冲突

**问题**: 已安装的包版本冲突

**解决方案**:
```bash
# 升级所有依赖
pip install --upgrade trafilatura requests

# 或使用 pipenv/poetry 管理依赖
pipenv install trafilatura requests
```

### 网络问题

**问题**: pip 下载速度慢或失败

**解决方案**:
```bash
# 使用国内镜像源
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple trafilatura requests

# 或永久配置
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### SSL 证书问题

**问题**: SSL 验证失败导致 requests 报错

**解决方案**:
```bash
# 升级 certifi
pip install --upgrade certifi
```
