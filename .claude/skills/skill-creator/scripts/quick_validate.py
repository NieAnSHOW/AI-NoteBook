#!/usr/bin/env python3
"""
Skill 快速验证脚本

Usage:
    python scripts/quick_validate.py <skill-directory>

Example:
    python scripts/quick_validate.py ./my-skill
"""

import sys
import re
import yaml
from pathlib import Path


def validate_skill(skill_path: str) -> tuple[bool, str]:
    """
    验证 Skill 结构和内容。
    
    Args:
        skill_path: Skill 目录路径
        
    Returns:
        (是否有效, 消息)
    """
    skill_path = Path(skill_path)
    
    # 检查 SKILL.md 存在
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md 不存在"
    
    content = skill_md.read_text(encoding='utf-8')
    
    # 检查 frontmatter 存在
    if not content.startswith('---'):
        return False, "缺少 YAML frontmatter"
    
    # 提取 frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "frontmatter 格式无效"
    
    frontmatter_text = match.group(1)
    
    # 解析 YAML
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "frontmatter 必须是 YAML 字典"
    except yaml.YAMLError as e:
        return False, f"YAML 解析错误: {e}"
    
    # 检查允许的属性
    ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata'}
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, f"frontmatter 包含未知属性: {', '.join(sorted(unexpected_keys))}"
    
    # 检查必需字段
    if 'name' not in frontmatter:
        return False, "缺少 'name' 字段"
    if 'description' not in frontmatter:
        return False, "缺少 'description' 字段"
    
    # 验证 name
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"name 必须是字符串，当前类型: {type(name).__name__}"
    
    name = name.strip()
    if name:
        # 检查命名规范
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"name '{name}' 必须是小写字母、数字和连字符"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"name '{name}' 不能以连字符开头/结尾或包含连续连字符"
        if len(name) > 64:
            return False, f"name 过长 ({len(name)} 字符)，最大 64 字符"
    
    # 验证 description
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"description 必须是字符串，当前类型: {type(description).__name__}"
    
    description = description.strip()
    if description:
        if '<' in description or '>' in description:
            return False, "description 不能包含尖括号 (< 或 >)"
        if len(description) > 1024:
            return False, f"description 过长 ({len(description)} 字符)，最大 1024 字符"
    
    # 检查是否包含 TODO（警告）
    warnings = []
    if '[TODO' in content:
        warnings.append("SKILL.md 包含未完成的 TODO 项")
    
    # 检查禁止的文件
    forbidden_files = ['README.md', 'CHANGELOG.md', 'INSTALLATION_GUIDE.md']
    for f in forbidden_files:
        if (skill_path / f).exists():
            return False, f"不应包含辅助文档: {f}"
    
    # 检查路径格式（Windows 反斜杠）
    if '\\' in content:
        warnings.append("检测到 Windows 路径格式 (\\)，建议使用正斜杠 (/)")
    
    # 构建结果消息
    result_msg = "✅ Skill 验证通过"
    if warnings:
        result_msg += "\n⚠️ 警告:\n  - " + "\n  - ".join(warnings)
    
    return True, result_msg


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/quick_validate.py <skill-directory>")
        print("\nExample:")
        print("  python scripts/quick_validate.py ./my-skill")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    print(f"🔍 验证 Skill: {skill_path}\n")
    
    valid, message = validate_skill(skill_path)
    print(message)
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
