#!/usr/bin/env python3
"""
Skill 内容生成器 - 根据规划自动生成 SKILL.md 内容

Usage:
    python scripts/generate_skill.py <config-file>
    echo '<json>' | python scripts/generate_skill.py

输入 JSON 格式:
{
    "name": "my-skill",
    "description": "做什么 + 何时使用",
    "scenarios": [
        {"id": "S1", "name": "场景A", "trigger": "条件A"},
        {"id": "S2", "name": "场景B", "trigger": "条件B"}
    ],
    "tasks": [
        {
            "node_id": "S1",
            "name": "处理流程A",
            "description": "场景说明",
            "steps": [
                {"type": "step", "content": "执行操作1"},
                {"type": "critical", "content": "核心约束"}
            ],
            "output": "输出确认模板"
        }
    ],
    "common_task": {
        "name": "通用处理",
        "steps": ["验证输出", "质量检查"]
    }
}
"""

import sys
import json
from typing import Dict, Any, List, Optional
from pathlib import Path


def generate_frontmatter(name: str, description: str) -> str:
    """生成 YAML frontmatter"""
    return f"""---
name: {name}
description: {description}
---"""


def generate_mermaid_graph(scenarios: List[Dict], common_task: Optional[Dict] = None) -> str:
    """生成 Mermaid 工作流图"""
    lines = [
        "```mermaid",
        "graph TD",
        "    START([用户请求]) --> SR{{📋 场景识别}}",
        ""
    ]
    
    # 场景分支
    for scenario in scenarios:
        sid = scenario.get("id", "S1")
        name = scenario.get("name", "处理流程")
        trigger = scenario.get("trigger", "场景")
        lines.append(f"    SR -->|{trigger}| {sid}[{name}]")
    
    # 通用处理节点
    if common_task:
        lines.append("")
        for scenario in scenarios:
            sid = scenario.get("id", "S1")
            lines.append(f"    {sid} --> Common[{common_task.get('name', '通用处理')}]")
        lines.extend([
            "    Common --> Check{验证通过?}",
            "    Check -->|是| END([完成])",
            "    Check -->|否| Fix[修复问题]",
            "    Fix --> Common"
        ])
    else:
        # 直接结束
        lines.append("")
        for scenario in scenarios:
            sid = scenario.get("id", "S1")
            lines.append(f"    {sid} --> END([完成])")
    
    lines.append("```")
    return "\n".join(lines)


def generate_task_section(task: Dict) -> str:
    """生成单个 Task 的 Domain 层内容"""
    node_id = task.get("node_id", "Task")
    name = task.get("name", "任务名称")
    description = task.get("description", "场景说明")
    steps = task.get("steps", [])
    output = task.get("output", "")
    
    lines = [
        f"### {node_id}[{name}]",
        "",
        f"**场景说明**: {description}",
        "",
        "#### 1. 执行工作流",
        ""
    ]
    
    # 生成步骤
    for i, step in enumerate(steps, 1):
        if isinstance(step, str):
            lines.append(f"{i}. **Step {i}**: {step}")
        elif isinstance(step, dict):
            step_type = step.get("type", "step")
            content = step.get("content", "")
            script = step.get("script", "")
            reference = step.get("reference", "")
            
            if step_type == "critical":
                lines.append(f"{i}. **CRITICAL**: {content}")
            elif step_type == "mandatory":
                lines.append(f"{i}. **MANDATORY**: {content}")
            else:
                lines.append(f"{i}. **Step {i}**: {content}")
            
            if script:
                lines.append(f"   - 执行脚本：`python scripts/{script}`")
            if reference:
                lines.append(f"   - 参考资料：`references/{reference}`")
        lines.append("")
    
    # 输出确认
    if output:
        lines.extend([
            "#### 2. 输出确认",
            "",
            "```",
            output,
            "```",
            ""
        ])
    
    return "\n".join(lines)


def generate_common_task(common_task: Dict) -> str:
    """生成通用处理 Task"""
    name = common_task.get("name", "通用处理")
    steps = common_task.get("steps", [])
    
    lines = [
        f"### Common[{name}]",
        "",
        "**场景说明**: 所有场景共享的处理逻辑。",
        "",
        "#### 1. 验证工作流",
        ""
    ]
    
    for i, step in enumerate(steps, 1):
        if isinstance(step, str):
            lines.append(f"{i}. **Step {i}**: {step}")
        elif isinstance(step, dict):
            lines.append(f"{i}. **Step {i}**: {step.get('content', '')}")
        lines.append("")
    
    return "\n".join(lines)


def generate_skill_md(config: Dict[str, Any]) -> str:
    """生成完整的 SKILL.md 内容"""
    name = config.get("name", "my-skill")
    description = config.get("description", "[TODO: 描述]")
    title = config.get("title", " ".join(w.capitalize() for w in name.split("-")))
    scenarios = config.get("scenarios", [{"id": "S1", "name": "默认流程", "trigger": "默认"}])
    tasks = config.get("tasks", [])
    common_task = config.get("common_task")
    
    sections = []
    
    # 1. Frontmatter
    sections.append(generate_frontmatter(name, description))
    
    # 2. Title
    sections.append(f"\n# {title}\n")
    
    # 3. Application Layer
    sections.append("## Application Layer\n")
    sections.append(generate_mermaid_graph(scenarios, common_task))
    sections.append("\n**MANDATORY**: 每次任务必须先执行场景识别，明确告知用户当前模式。\n")
    sections.append("---\n")
    
    # 4. Domain Layer
    sections.append("## Domain Layer\n")
    
    for task in tasks:
        sections.append(generate_task_section(task))
        sections.append("---\n")
    
    if common_task:
        sections.append(generate_common_task(common_task))
        sections.append("---\n")
    
    return "\n".join(sections)


def main():
    try:
        # 从 stdin 或文件读取配置
        if len(sys.argv) > 1:
            config_file = Path(sys.argv[1])
            if config_file.exists():
                config = json.loads(config_file.read_text(encoding='utf-8-sig'))
            else:
                print(f"❌ 配置文件不存在: {config_file}", file=sys.stderr)
                sys.exit(1)
        else:
            # 处理可能的 BOM
            raw_input = sys.stdin.read()
            if raw_input.startswith('\ufeff'):
                raw_input = raw_input[1:]
            config = json.loads(raw_input)
        
        # 生成 SKILL.md 内容
        content = generate_skill_md(config)
        print(content)
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 生成失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
