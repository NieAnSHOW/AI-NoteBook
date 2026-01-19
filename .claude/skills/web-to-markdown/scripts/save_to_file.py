#!/usr/bin/env python3
"""
文件保存器

将 Markdown 内容保存到文件。

输入格式:
{
  "markdown": "Markdown 内容",
  "title": "标题（用于生成文件名）",
  "url": "原始URL（用于生成文件名）",
  "output_path": "输出路径（可选，默认当前目录）",
  "filename": "自定义文件名（可选）"
}

输出格式:
{
  "status": "success",
  "file_path": "保存的文件完整路径",
  "content_length": "内容长度"
}
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, Any
from urllib.parse import urlparse


def sanitize_filename(name: str) -> str:
    """
    清理文件名，移除非法字符

    Args:
        name: 原始名称

    Returns:
        清理后的文件名
    """
    # 移除或替换非法字符
    name = re.sub(r'[<>:"/\\|?*]', '-', name)
    # 移除首尾空格和点
    name = name.strip('. ')
    # 限制长度
    name = name[:200]
    return name if name else 'untitled'


def generate_filename(title: str = '', url: str = '') -> str:
    """
    根据标题或 URL 生成文件名

    Args:
        title: 标题
        url: URL

    Returns:
        文件名（不含扩展名）
    """
    if title:
        return sanitize_filename(title)
    elif url:
        # 从 URL 提取文件名或路径最后部分
        parsed = urlparse(url)
        path = parsed.path
        if path and path != '/':
            filename = path.rstrip('/').split('/')[-1]
            return sanitize_filename(filename)
        # 使用域名作为文件名
        return sanitize_filename(parsed.netloc)
    return 'untitled'


def save_to_file(
    markdown: str,
    title: str = '',
    url: str = '',
    output_path: str = '',
    filename: str = ''
) -> Dict[str, Any]:
    """
    将 Markdown 保存到文件

    Args:
        markdown: Markdown 内容
        title: 标题
        url: URL
        output_path: 输出目录
        filename: 自定义文件名

    Returns:
        包含保存结果的字典
    """
    try:
        # 生成文件名
        if filename:
            # 清理自定义文件名
            base_name = sanitize_filename(filename)
        else:
            base_name = generate_filename(title, url)

        # 添加 .md 扩展名
        if not base_name.endswith('.md'):
            base_name = f"{base_name}.md"

        # 确定输出目录
        if output_path:
            output_dir = Path(output_path)
        else:
            output_dir = Path.cwd()

        # 创建输出目录（如果不存在）
        output_dir.mkdir(parents=True, exist_ok=True)

        # 完整文件路径
        file_path = output_dir / base_name

        # 检查文件是否已存在，如果存在则添加序号
        counter = 1
        original_path = file_path
        while file_path.exists():
            stem = original_path.stem
            file_path = original_path.parent / f"{stem}_{counter}.md"
            counter += 1

        # 写入文件
        file_path.write_text(markdown, encoding='utf-8')

        return {
            'status': 'success',
            'file_path': str(file_path),
            'content_length': len(markdown)
        }

    except PermissionError as e:
        return {
            'status': 'error',
            'error_type': 'PermissionError',
            'message': f'权限错误，无法写入文件: {str(e)}'
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
        markdown = data.get('markdown', '')
        title = data.get('title', '')
        url = data.get('url', '')
        output_path = data.get('output_path', '')
        filename = data.get('filename', '')

        if not markdown:
            raise ValueError("Markdown 内容不能为空")

        # 保存文件
        result = save_to_file(markdown, title, url, output_path, filename)

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
