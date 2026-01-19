#!/usr/bin/env python3
"""
Skill Initializer - 创建符合 DDD 四层架构的 Skill 模板

Usage:
    python scripts/init_skill.py <skill-name> --path <output-directory>

Examples:
    python scripts/init_skill.py financial-analyzer --path ./skills
    python scripts/init_skill.py pdf-editor --path ./output
"""

import sys
import json
from pathlib import Path
from typing import Optional


SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: 完整描述做什么 + 何时使用。示例: Calculate financial ratios (ROE, ROA). Use when (1) analyzing performance, (2) evaluating investments.]
---

# {skill_title}

[TODO: 一句话描述 Skill 核心功能]

## Application Layer

```mermaid
graph TD
    START([用户请求]) --> SR{{{{📋 场景识别}}}}
    
    SR -->|场景A| S1[处理流程A]
    SR -->|场景B| S2[处理流程B]
    
    S1 --> Common[通用处理]
    S2 --> Common
    Common --> Check{{验证通过?}}
    Check -->|是| END([完成])
    Check -->|否| Fix[修复问题]
    Fix --> Common
```

**MANDATORY**: 每次任务必须先执行场景识别，明确告知用户当前模式。

---

## Domain Layer

### S1[处理流程A]

**场景说明**: [TODO: 描述任务目标与触发条件]

#### 1. 执行工作流

1. **Step 1**: [TODO: 原子动作描述]
   - 具体操作
   - **CRITICAL**: [核心约束]

2. **Step 2**: [TODO: 逻辑加工步骤]
   - 执行计算：`echo '{{"data": 100}}' | python scripts/example.py`
   - 参考资料：`references/example.md`

#### 2. 输出确认

```
🔍 **[任务名称]完成**
- 处理项目：{{项目说明}}
- 执行结果：{{结果摘要}}
✅ [下一步说明]
```

---

### S2[处理流程B]

**场景说明**: [TODO: 描述任务目标与触发条件]

#### 1. 执行维度

1. **Dimension 1**: [TODO: 分析维度描述]
   - 具体操作

2. **Dimension 2**: [TODO: 分析维度描述]
   - 具体操作

---

### Common[通用处理]

**场景说明**: 所有场景共享的处理逻辑。

#### 1. 验证工作流

1. **Step 1**: 验证输出格式
   - **CRITICAL**: 确保输出符合预期

2. **Step 2**: 质量检查
   - 运行验证脚本（如适用）
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
{skill_title} - 示例脚本

从 stdin 读取 JSON，处理后输出到 stdout。
"""

import sys
import json
from typing import Dict, Any


def process(data: Dict[str, Any]) -> Dict[str, Any]:
    """处理输入数据"""
    # TODO: 实现实际处理逻辑
    return {{
        "status": "success",
        "input": data,
        "message": "处理完成"
    }}


def main():
    try:
        data = json.loads(sys.stdin.read())
        result = process(data)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        error = {{
            "status": "error",
            "error_type": type(e).__name__,
            "message": str(e)
        }}
        print(json.dumps(error, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# {skill_title} 参考文档

[TODO: 添加非核心的详细支撑信息]

## 目录

1. [概述](#概述)
2. [详细说明](#详细说明)
3. [示例](#示例)

---

## 概述

[TODO: 简要说明此参考文档的用途]

---

## 详细说明

[TODO: 添加详细的参考信息，如：
- API 文档
- 数据库 Schema
- 行业基准数据
- 长篇示例]

---

## 示例

[TODO: 添加具体示例]
"""


def title_case_skill_name(skill_name: str) -> str:
    """将连字符名称转换为标题格式"""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def validate_skill_name(skill_name: str) -> tuple[bool, str]:
    """验证 Skill 名称是否符合规范"""
    import re
    
    if not skill_name:
        return False, "名称不能为空"
    
    if len(skill_name) > 64:
        return False, f"名称过长 ({len(skill_name)} 字符)，最大 64 字符"
    
    if not re.match(r'^[a-z0-9-]+$', skill_name):
        return False, "名称只能包含小写字母、数字和连字符"
    
    if skill_name.startswith('-') or skill_name.endswith('-'):
        return False, "名称不能以连字符开头或结尾"
    
    if '--' in skill_name:
        return False, "名称不能包含连续连字符"
    
    return True, "名称有效"


def init_skill(skill_name: str, path: str) -> Optional[Path]:
    """
    初始化新的 Skill 目录。
    
    Args:
        skill_name: Skill 名称
        path: 输出目录路径
        
    Returns:
        创建的 Skill 目录路径，失败返回 None
    """
    # 验证名称
    valid, message = validate_skill_name(skill_name)
    if not valid:
        print(f"❌ 名称错误: {message}")
        return None
    
    skill_dir = Path(path).resolve() / skill_name
    
    if skill_dir.exists():
        print(f"❌ 目录已存在: {skill_dir}")
        return None
    
    try:
        # 创建目录结构
        skill_dir.mkdir(parents=True)
        print(f"✅ 创建目录: {skill_dir}")
        
        skill_title = title_case_skill_name(skill_name)
        
        # 创建 SKILL.md
        skill_content = SKILL_TEMPLATE.format(
            skill_name=skill_name,
            skill_title=skill_title
        )
        (skill_dir / 'SKILL.md').write_text(skill_content, encoding='utf-8')
        print("✅ 创建 SKILL.md")
        
        # 创建 scripts/
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir()
        script_content = EXAMPLE_SCRIPT.format(skill_title=skill_title)
        script_path = scripts_dir / 'example.py'
        script_path.write_text(script_content, encoding='utf-8')
        script_path.chmod(0o755)
        print("✅ 创建 scripts/example.py")
        
        # 创建 references/
        refs_dir = skill_dir / 'references'
        refs_dir.mkdir()
        ref_content = EXAMPLE_REFERENCE.format(skill_title=skill_title)
        (refs_dir / 'example.md').write_text(ref_content, encoding='utf-8')
        print("✅ 创建 references/example.md")
        
        # 创建 assets/
        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir()
        (assets_dir / '.gitkeep').write_text('')
        print("✅ 创建 assets/")
        
        print(f"\n✅ Skill '{skill_name}' 初始化完成")
        print("\n下一步:")
        print("1. 编辑 SKILL.md 完成 TODO 项")
        print("2. 实现或删除 scripts/example.py")
        print("3. 更新或删除 references/example.md")
        print("4. 运行 quick_validate.py 验证结构")
        
        return skill_dir
        
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        return None


def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("Usage: python scripts/init_skill.py <skill-name> --path <output-directory>")
        print("\n名称规范:")
        print("  - 小写字母、数字、连字符")
        print("  - 最大 64 字符")
        print("  - 示例: financial-analyzer, pdf-editor")
        print("\n示例:")
        print("  python scripts/init_skill.py my-skill --path ./skills")
        sys.exit(1)
    
    skill_name = sys.argv[1]
    path = sys.argv[3]
    
    print(f"🚀 初始化 Skill: {skill_name}")
    print(f"   位置: {path}\n")
    
    result = init_skill(skill_name, path)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
