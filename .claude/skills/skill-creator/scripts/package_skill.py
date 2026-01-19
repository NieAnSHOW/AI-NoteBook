#!/usr/bin/env python3
"""
Skill 打包脚本 - 创建可分发的 .skill 文件

Usage:
    python scripts/package_skill.py <skill-directory> [output-directory]

Examples:
    python scripts/package_skill.py ./my-skill
    python scripts/package_skill.py ./my-skill ./dist
"""

import sys
import zipfile
from pathlib import Path

# 导入验证函数
from quick_validate import validate_skill


def package_skill(skill_path: str, output_dir: str = None) -> Path | None:
    """
    将 Skill 目录打包为 .skill 文件。
    
    Args:
        skill_path: Skill 目录路径
        output_dir: 输出目录（可选，默认当前目录）
        
    Returns:
        创建的 .skill 文件路径，失败返回 None
    """
    skill_path = Path(skill_path).resolve()
    
    # 验证目录存在
    if not skill_path.exists():
        print(f"❌ 目录不存在: {skill_path}")
        return None
    
    if not skill_path.is_dir():
        print(f"❌ 路径不是目录: {skill_path}")
        return None
    
    # 验证 SKILL.md 存在
    if not (skill_path / "SKILL.md").exists():
        print(f"❌ SKILL.md 不存在于 {skill_path}")
        return None
    
    # 运行验证
    print("🔍 验证 Skill...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"❌ 验证失败: {message}")
        print("   请修复错误后重新打包")
        return None
    print(f"{message}\n")
    
    # 确定输出位置
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()
    
    skill_filename = output_path / f"{skill_name}.skill"
    
    # 创建 .skill 文件（zip 格式）
    try:
        with zipfile.ZipFile(skill_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in skill_path.rglob('*'):
                if file_path.is_file():
                    # 跳过隐藏文件和 __pycache__
                    if any(part.startswith('.') or part == '__pycache__' 
                           for part in file_path.parts):
                        continue
                    
                    arcname = file_path.relative_to(skill_path.parent)
                    zipf.write(file_path, arcname)
                    print(f"  添加: {arcname}")
        
        print(f"\n📦 打包完成: {skill_filename}")
        return skill_filename
        
    except Exception as e:
        print(f"❌ 打包失败: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/package_skill.py <skill-directory> [output-directory]")
        print("\nExamples:")
        print("  python scripts/package_skill.py ./my-skill")
        print("  python scripts/package_skill.py ./my-skill ./dist")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"📦 打包 Skill: {skill_path}")
    if output_dir:
        print(f"   输出目录: {output_dir}")
    print()
    
    result = package_skill(skill_path, output_dir)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
