#!/usr/bin/env python3
"""
需求分析器 - 从用户描述中提取 Skill 规划配置

Usage:
    echo '{"description": "用户需求描述", "examples": ["示例1", "示例2"]}' | python scripts/analyze_requirements.py

输出: 生成 generate_skill.py 所需的配置 JSON
"""

import sys
import json
import re
from typing import Dict, Any, List


def extract_scenarios(description: str, examples: List[str]) -> List[Dict]:
    """从描述和示例中提取场景"""
    scenarios = []
    
    # 常见场景关键词（中英文）
    scenario_patterns = [
        (r'创建|新建|生成|create|generate|new', 'create', '新建'),
        (r'编辑|修改|更新|edit|update|modify', 'edit', '编辑'),
        (r'删除|移除|delete|remove', 'delete', '删除'),
        (r'查询|搜索|查找|query|search|find', 'query', '查询'),
        (r'验证|检查|校验|validate|check|verify', 'validate', '验证'),
        (r'导出|输出|生成报告|export|output|report', 'export', '导出'),
        (r'导入|加载|读取|import|load|read', 'import', '导入'),
        (r'分析|统计|analyze|analysis|statistics', 'analyze', '分析'),
        (r'计算|calculate|compute', 'calculate', '计算'),
        (r'比较|对比|compare|contrast', 'compare', '比较'),
    ]
    
    combined_text = (description + " " + " ".join(examples)).lower()
    found_scenarios = set()
    
    for pattern, sid, name in scenario_patterns:
        if re.search(pattern, combined_text, re.IGNORECASE):
            found_scenarios.add((sid, name))
    
    # 生成场景列表
    for i, (sid, name) in enumerate(found_scenarios, 1):
        scenarios.append({
            "id": f"S{i}",
            "name": f"{name}流程",
            "trigger": name
        })
    
    # 如果没有识别到场景，创建默认场景
    if not scenarios:
        scenarios.append({
            "id": "S1",
            "name": "默认处理",
            "trigger": "默认"
        })
    
    return scenarios


def extract_infrastructure_hints(description: str, examples: List[str], scenarios: List[Dict]) -> Dict:
    """提取 Infrastructure 层资源提示，细粒度推荐参考文件"""
    hints = {
        "scripts": [],
        "references": {
            "required": [],      # 必需的参考文件
            "recommended": [],   # 推荐的参考文件
            "optional": []       # 可选的参考文件
        },
        "assets": []
    }
    
    combined_text = (description + " " + " ".join(examples)).lower()
    scenario_count = len(scenarios)
    
    # ========== 脚本推荐 ==========
    script_patterns = [
        (r'计算|公式|比率|统计|calculate|formula|ratio|statistics', 'calculate.py', '执行数学计算和公式'),
        (r'验证|校验|检查|审核|validate|verify|check', 'validate.py', '数据验证和格式检查'),
        (r'转换|格式化|编码|convert|format|encode', 'convert.py', '数据格式转换'),
        (r'提取|解析|读取|extract|parse|read', 'extract.py', '从文件/数据中提取信息'),
        (r'生成|创建|输出|generate|create|output', 'generate.py', '生成输出文件或报告'),
        (r'合并|拼接|组合|merge|combine|concat', 'merge.py', '合并多个数据源'),
        (r'拆分|分割|切片|split|divide|slice', 'split.py', '拆分数据或文件'),
        (r'下载|获取|抓取|download|fetch|crawl', 'download.py', '批量下载或获取资源'),
        (r'上传|发送|推送|upload|send|push', 'upload.py', '上传或发送数据'),
        (r'清理|清洗|过滤|clean|filter|sanitize', 'clean.py', '数据清洗和过滤'),
    ]
    
    for pattern, script, desc in script_patterns:
        if re.search(pattern, combined_text, re.IGNORECASE):
            hints["scripts"].append({"name": script, "description": desc})
    
    # ========== 细粒度参考文件推荐 ==========
    
    # 1. 基于场景数量推荐工作流参考
    if scenario_count >= 3:
        hints["references"]["required"].append({
            "name": "workflow-branching.md",
            "description": "多分支工作流设计指南",
            "template": "workflow"
        })
    if scenario_count >= 2:
        hints["references"]["recommended"].append({
            "name": "workflow-common-steps.md", 
            "description": "通用步骤抽取规范",
            "template": "workflow"
        })
    
    # 2. 基于功能类型推荐参考文件
    ref_patterns = [
        # 数据处理类
        (r'计算|公式|比率|财务|统计|calculate|formula|ratio|financial|statistics', [
            {"name": "calculation-formulas.md", "description": "计算公式定义", "priority": "required"},
            {"name": "data-validation-rules.md", "description": "数据验证规则", "priority": "required"},
            {"name": "output-format-spec.md", "description": "输出格式规范", "priority": "recommended"},
        ]),
        # API/接口类
        (r'API|接口|调用|请求|endpoint|request|response', [
            {"name": "api-endpoints.md", "description": "API 端点清单", "priority": "required"},
            {"name": "request-response-format.md", "description": "请求响应格式", "priority": "required"},
            {"name": "error-codes.md", "description": "错误码定义", "priority": "recommended"},
            {"name": "authentication.md", "description": "认证方式说明", "priority": "optional"},
        ]),
        # 文件处理类
        (r'PDF|文档|文件|Excel|Word|document|file|spreadsheet', [
            {"name": "file-format-spec.md", "description": "文件格式规范", "priority": "required"},
            {"name": "field-mapping.md", "description": "字段映射规则", "priority": "recommended"},
            {"name": "template-samples.md", "description": "模板示例", "priority": "optional"},
        ]),
        # 代码/开发类
        (r'代码|编程|开发|重构|审查|code|programming|develop|refactor|review', [
            {"name": "coding-standards.md", "description": "编码规范", "priority": "required"},
            {"name": "review-checklist.md", "description": "审查清单", "priority": "recommended"},
            {"name": "best-practices.md", "description": "最佳实践", "priority": "optional"},
        ]),
        # 分析/报告类
        (r'分析|报告|洞察|趋势|analyze|analysis|report|insight|trend', [
            {"name": "analysis-dimensions.md", "description": "分析维度定义", "priority": "required"},
            {"name": "report-template.md", "description": "报告模板", "priority": "required"},
            {"name": "visualization-guide.md", "description": "可视化指南", "priority": "optional"},
        ]),
        # 验证/质量类
        (r'验证|测试|质量|检查|validate|test|quality|check', [
            {"name": "validation-rules.md", "description": "验证规则定义", "priority": "required"},
            {"name": "test-cases.md", "description": "测试用例", "priority": "recommended"},
            {"name": "quality-metrics.md", "description": "质量指标", "priority": "optional"},
        ]),
    ]
    
    for pattern, refs in ref_patterns:
        if re.search(pattern, combined_text, re.IGNORECASE):
            for ref in refs:
                priority = ref.get("priority", "optional")
                ref_item = {"name": ref["name"], "description": ref["description"]}
                if priority == "required":
                    hints["references"]["required"].append(ref_item)
                elif priority == "recommended":
                    hints["references"]["recommended"].append(ref_item)
                else:
                    hints["references"]["optional"].append(ref_item)
    
    # 3. 通用参考文件（所有 Skill 都推荐）
    hints["references"]["recommended"].append({
        "name": "output-examples.md",
        "description": "输出示例集合"
    })
    
    # 4. 基于示例数量推荐
    if len(examples) >= 3:
        hints["references"]["recommended"].append({
            "name": "use-case-catalog.md",
            "description": "使用场景目录"
        })
    
    # 去重
    for priority in ["required", "recommended", "optional"]:
        seen = set()
        unique = []
        for ref in hints["references"][priority]:
            if ref["name"] not in seen:
                seen.add(ref["name"])
                unique.append(ref)
        hints["references"][priority] = unique
    
    return hints


def generate_config(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """生成 Skill 配置"""
    description = input_data.get("description", "")
    examples = input_data.get("examples", [])
    name = input_data.get("name", "")
    
    # 如果没有提供名称，尝试从描述生成
    if not name:
        # 简单的名称生成逻辑
        words = re.findall(r'[\u4e00-\u9fa5]+|[a-zA-Z]+', description)[:3]
        name = "-".join(words).lower()[:64]
        if not name:
            name = "my-skill"
    
    scenarios = extract_scenarios(description, examples)
    infra_hints = extract_infrastructure_hints(description, examples, scenarios)
    
    # 生成任务列表
    tasks = []
    for scenario in scenarios:
        task = {
            "node_id": scenario["id"],
            "name": scenario["name"],
            "description": f"当用户需要{scenario['trigger']}时使用",
            "steps": [
                {"type": "step", "content": "[TODO: 具体操作步骤]"},
                {"type": "critical", "content": "[TODO: 核心约束]"}
            ],
            "output": f"🔍 **{scenario['name']}完成**\n- 处理项目：{{项目说明}}\n✅ 下一步说明",
            "references": []  # 该任务需要引用的参考文件
        }
        
        # 添加脚本引用提示
        if infra_hints["scripts"]:
            task["steps"].insert(1, {
                "type": "step",
                "content": "执行处理",
                "script": infra_hints["scripts"][0]["name"]
            })
        
        # 为任务添加相关参考文件引用
        if infra_hints["references"]["required"]:
            task["references"] = [ref["name"] for ref in infra_hints["references"]["required"][:2]]
        
        tasks.append(task)
    
    # 构建参考文件规划摘要
    references_plan = {
        "required": infra_hints["references"]["required"],
        "recommended": infra_hints["references"]["recommended"],
        "optional": infra_hints["references"]["optional"],
        "total_count": (
            len(infra_hints["references"]["required"]) +
            len(infra_hints["references"]["recommended"]) +
            len(infra_hints["references"]["optional"])
        )
    }
    
    config = {
        "name": name,
        "description": description if description else "[TODO: 完整描述做什么 + 何时使用]",
        "scenarios": scenarios,
        "tasks": tasks,
        "common_task": {
            "name": "通用处理",
            "steps": ["验证输出格式", "质量检查"]
        },
        "infrastructure_plan": {
            "scripts": infra_hints["scripts"],
            "references": references_plan,
            "assets": infra_hints["assets"]
        }
    }
    
    return config


def main():
    try:
        # 处理可能的 BOM
        raw_input = sys.stdin.read()
        if raw_input.startswith('\ufeff'):
            raw_input = raw_input[1:]
        input_data = json.loads(raw_input)
        config = generate_config(input_data)
        print(json.dumps(config, indent=2, ensure_ascii=False))
        
    except json.JSONDecodeError as e:
        error = {"status": "error", "message": f"JSON 解析错误: {e}"}
        print(json.dumps(error, indent=2), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error = {"status": "error", "message": str(e)}
        print(json.dumps(error, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
