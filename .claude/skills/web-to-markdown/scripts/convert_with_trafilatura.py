#!/usr/bin/env python3
"""
使用 Trafilatura 将网页转换为 Markdown 格式

Trafilatura 优势:
- 自动提取网页正文（智能过滤广告、导航等无关内容）
- 提取元数据（标题、作者、日期、描述等）
- 支持多种输出格式（XML, JSON, Markdown, 纯文本）

依赖安装:
    pip install trafilatura requests

输入格式 (提供 URL):
{
  "url": "https://example.com",
  "output_format": "markdown/json/xml/txt (可选，默认 markdown)",
  "include_metadata": true/false (可选，默认 true),
  "timeout": 30 (可选，请求超时秒数，默认 30)
}

输入格式 (提供 HTML):
{
  "html": "<html>...</html>",
  "url": "https://example.com (可选，用于元数据提取)",
  "output_format": "markdown/json/xml/txt (可选，默认 markdown)",
  "include_metadata": true/false (可选，默认 true)
}

输出格式:
{
  "status": "success",
  "content": "Markdown 内容",
  "metadata": {
    "title": "标题",
    "author": "作者",
    "date": "日期",
    "description": "描述"
  },
  "url": "原始URL"
}
"""

import sys
import json
import re
from typing import Dict, Any
from urllib.parse import urlparse


def fetch_html(url: str, timeout: int = 30) -> Dict[str, Any]:
    """
    使用 requests 获取网页 HTML 内容

    Args:
        url: 网页 URL
        timeout: 超时时间（秒）

    Returns:
        包含 HTML 内容的字典
    """
    try:
        import requests
    except ImportError:
        return {
            'status': 'error',
            'error_type': 'ImportError',
            'message': 'requests 未安装，请运行: pip install requests'
        }

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

        response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        response.raise_for_status()
        response.encoding = response.apparent_encoding or 'utf-8'

        return {
            'status': 'success',
            'html': response.text
        }

    except requests.exceptions.Timeout:
        return {
            'status': 'error',
            'error_type': 'TimeoutError',
            'message': f'请求超时，超过 {timeout} 秒'
        }
    except requests.exceptions.HTTPError as e:
        return {
            'status': 'error',
            'error_type': 'HTTPError',
            'message': f'HTTP 错误: {e.response.status_code}'
        }
    except requests.exceptions.RequestException as e:
        return {
            'status': 'error',
            'error_type': 'RequestError',
            'message': f'请求错误: {str(e)}'
        }
    except Exception as e:
        return {
            'status': 'error',
            'error_type': type(e).__name__,
            'message': str(e)
        }


def extract_with_trafilatura(
    html: str,
    url: str = '',
    output_format: str = 'markdown',
    include_metadata: bool = True
) -> Dict[str, Any]:
    """
    使用 Trafilatura 提取网页内容

    Args:
        html: HTML 内容
        url: 原始 URL
        output_format: 输出格式 (markdown/json/xml/txt)
        include_metadata: 是否包含元数据

    Returns:
        包含提取结果的字典
    """
    try:
        import trafilatura
    except ImportError:
        return {
            'status': 'error',
            'error_type': 'ImportError',
            'message': 'trafilatura 未安装，请运行: pip install trafilatura'
        }

    try:
        # 提取元数据
        metadata = {}
        if include_metadata:
            try:
                from trafilatura.metadata import extract_metadata
                metadata_dict = extract_metadata(
                    html,
                    default_url=url if url else None
                )

                metadata = {
                    'title': metadata_dict.title if hasattr(metadata_dict, 'title') and metadata_dict.title else '',
                    'author': metadata_dict.author if hasattr(metadata_dict, 'author') and metadata_dict.author else '',
                    'date': str(metadata_dict.date) if hasattr(metadata_dict, 'date') and metadata_dict.date else '',
                    'description': metadata_dict.description if hasattr(metadata_dict, 'description') and metadata_dict.description else '',
                    'url': metadata_dict.url if hasattr(metadata_dict, 'url') and metadata_dict.url else url
                }
            except Exception as e:
                # 如果元数据提取失败，使用 trafilatura.extract 的返回值
                pass

        # 提取正文内容
        extracted_text = trafilatura.extract(
            html,
            output_format=output_format,
            include_comments=False,
            include_tables=True,
            no_fallback=False
        )

        if not extracted_text:
            # 如果 trafilatura 提取失败，尝试 html2txt
            extracted_text = trafilatura.html2txt(html)

        if not extracted_text:
            return {
                'status': 'error',
                'error_type': 'ExtractionError',
                'message': '未能从 HTML 中提取有效内容'
            }

        # 清理多余的空行
        extracted_text = re.sub(r'\n{3,}', '\n\n', extracted_text)
        extracted_text = extracted_text.strip()

        # 格式化输出
        if output_format == 'markdown' and metadata.get('title'):
            # 在 Markdown 顶部添加标题和元数据
            result = f"# {metadata['title']}\n\n"

            # 添加其他元数据
            meta_lines = []
            if metadata.get('author'):
                meta_lines.append(f"**作者**: {metadata['author']}")
            if metadata.get('date'):
                meta_lines.append(f"**发布日期**: {metadata['date']}")
            if metadata.get('description'):
                meta_lines.append(f"**描述**: {metadata['description']}")

            if meta_lines:
                result += '\n'.join(meta_lines) + '\n\n---\n\n'

            result += extracted_text

            if url:
                result += f"\n\n---\n\n来源: {url}"
        else:
            result = extracted_text

        return {
            'status': 'success',
            'content': result,
            'metadata': metadata,
            'url': url
        }

    except Exception as e:
        return {
            'status': 'error',
            'error_type': type(e).__name__,
            'message': str(e)
        }


def main():
    try:
        # 读取输入
        input_text = sys.stdin.read()
        # 处理 BOM
        if input_text.startswith('\ufeff'):
            input_text = input_text[1:]

        data = json.loads(input_text)

        # 检查是否有 URL 或 HTML
        url = data.get('url', '')
        html = data.get('html', '')

        if not url and not html:
            raise ValueError("必须提供 URL 或 HTML 内容之一")

        output_format = data.get('output_format', 'markdown')
        include_metadata = data.get('include_metadata', True)
        timeout = data.get('timeout', 30)

        # 验证输出格式
        valid_formats = ['markdown', 'json', 'xml', 'txt']
        if output_format not in valid_formats:
            raise ValueError(f"不支持的输出格式: {output_format}，支持的格式: {', '.join(valid_formats)}")

        # 如果没有 HTML，先获取
        if not html and url:
            fetch_result = fetch_html(url, timeout)
            if fetch_result['status'] != 'success':
                print(json.dumps(fetch_result, indent=2), file=sys.stderr)
                sys.exit(1)
            html = fetch_result['html']

        # 提取内容
        result = extract_with_trafilatura(html, url, output_format, include_metadata)

        if result['status'] == 'success':
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(json.dumps(result, indent=2), file=sys.stderr)
            sys.exit(1)

    except json.JSONDecodeError as e:
        error = {
            'status': 'error',
            'error_type': 'JSONDecodeError',
            'message': f'JSON 解析错误: {str(e)}'
        }
        print(json.dumps(error, indent=2), file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        error = {
            'status': 'error',
            'error_type': 'ValueError',
            'message': str(e)
        }
        print(json.dumps(error, indent=2), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error = {
            'status': 'error',
            'error_type': type(e).__name__,
            'message': str(e)
        }
        print(json.dumps(error, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
