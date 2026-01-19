#!/usr/bin/env python3
"""
文档验证脚本
验证生成的文档质量和一致性
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def validate_document(document_path: str) -> Dict:
    """
    验证文档质量和一致性
    
    Args:
        document_path: 文档文件路径
        
    Returns:
        验证结果
    """
    doc_path = Path(document_path)
    
    if not doc_path.exists():
        return {
            "valid": False,
            "errors": [f"文档文件不存在: {document_path}"]
        }
    
    # 读取文档内容
    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 执行各项验证
    validations = {
        "source_annotation": validate_source_annotations(content),
        "line_estimation": validate_line_estimation(content),
        "usage_examples": validate_usage_examples(content),
        "flowchart_clarity": validate_flowchart_clarity(content),
        "content_consistency": validate_content_consistency(content)
    }
    
    # 汇总结果
    all_errors = []
    all_warnings = []
    
    for validation_name, validation_result in validations.items():
        if validation_result.get("errors"):
            all_errors.extend(validation_result["errors"])
        if validation_result.get("warnings"):
            all_warnings.extend(validation_result["warnings"])
    
    is_valid = len(all_errors) == 0
    
    return {
        "valid": is_valid,
        "errors": all_errors,
        "warnings": all_warnings,
        "validations": validations
    }


def validate_source_annotations(content: str) -> Dict:
    """
    验证来源标注完整性
    
    Returns:
        验证结果
    """
    errors = []
    warnings = []
    
    # 检查是否包含来源标注
    source_pattern = r'来源：`[^`]+` \([^)]+\)'
    source_matches = re.findall(source_pattern, content)
    
    if len(source_matches) == 0:
        warnings.append("文档中没有找到来源标注")
    
    # 检查来源标注格式
    for match in source_matches:
        # 检查是否包含文件路径
        if not re.search(r'\([^)]+\)', match):
            errors.append(f"来源标注缺少文件路径: {match}")
        
        # 检查路径分隔符
        if '\\' in match:
            errors.append(f"来源标注使用了反斜杠，应使用正斜杠: {match}")
        
        # 检查行号
        if not re.search(r':\d+', match):
            warnings.append(f"来源标注可能缺少行号: {match}")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "count": len(source_matches)
    }


def validate_line_estimation(content: str) -> Dict:
    """
    验证预估行数标注
    
    Returns:
        验证结果
    """
    errors = []
    warnings = []
    
    # 查找所有章节标题
    heading_pattern = r'^#+\s+(.+)$'
    heading_matches = re.findall(heading_pattern, content, re.MULTILINE)
    
    # 查找包含预估行数的章节
    estimation_pattern = r'#+\s+.+\(预估约\s*\d+\s*行\)'
    estimation_matches = re.findall(estimation_pattern, content)
    
    if len(heading_matches) > 0 and len(estimation_matches) == 0:
        warnings.append("文档中没有找到预估行数标注")
    
    # 检查预估行数格式
    for match in estimation_matches:
        if not re.search(r'预估约\s*\d+\s*行', match):
            errors.append(f"预估行数格式不正确: {match}")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "count": len(estimation_matches)
    }


def validate_usage_examples(content: str) -> Dict:
    """
    验证使用示例完整性
    
    Returns:
        验证结果
    """
    errors = []
    warnings = []
    
    # 查找使用场景标注
    scenario_pattern = r'\*\*使用场景\*\*：.+'
    scenario_matches = re.findall(scenario_pattern, content)
    
    # 查找代码块
    code_block_pattern = r'```[\w]*\n.*?```'
    code_blocks = re.findall(code_block_pattern, content, re.DOTALL)
    
    # 查找预期结果标注
    result_pattern = r'\*\*预期结果\*\*：.+'
    result_matches = re.findall(result_pattern, content)
    
    if len(scenario_matches) == 0:
        warnings.append("文档中没有找到使用场景标注")
    
    if len(scenario_matches) > 0 and len(code_blocks) == 0:
        errors.append("存在使用场景但缺少代码示例")
    
    if len(scenario_matches) > 0 and len(result_matches) == 0:
        warnings.append("存在使用场景但缺少预期结果说明")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "scenario_count": len(scenario_matches),
        "code_block_count": len(code_blocks),
        "result_count": len(result_matches)
    }


def validate_flowchart_clarity(content: str) -> Dict:
    """
    验证流程图清晰度
    
    Returns:
        验证结果
    """
    errors = []
    warnings = []
    
    # 查找 Mermaid 流程图
    mermaid_pattern = r'```mermaid\n(.*?)```'
    mermaid_matches = re.findall(mermaid_pattern, content, re.DOTALL)
    
    if len(mermaid_matches) == 0:
        # 如果文档类型需要流程图但没有找到，给出警告
        if "业务模块" in content or "流程" in content:
            warnings.append("文档中可能需要流程图但没有找到 Mermaid 流程图")
    
    # 检查流程图是否有节点说明
    for i, mermaid in enumerate(mermaid_matches, 1):
        # 简单检查：流程图应该包含节点定义
        if not re.search(r'\[.*?\]', mermaid) and not re.search(r'\(.*?\)', mermaid):
            errors.append(f"第 {i} 个流程图可能缺少节点定义")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "count": len(mermaid_matches)
    }


def validate_content_consistency(content: str) -> Dict:
    """
    验证内容一致性
    
    Returns:
        验证结果
    """
    errors = []
    warnings = []
    
    # 检查模糊词汇
    vague_words = ["可能", "应该", "大概", "或许", "估计"]
    
    for word in vague_words:
        pattern = rf'{word}'
        matches = re.findall(pattern, content)
        if matches:
            warnings.append(f"文档中使用了模糊词汇 '{word}'，建议使用确定性语言")
    
    # 检查是否有"推测"、"臆造"等词汇
    speculation_words = ["推测", "臆造", "猜测"]
    for word in speculation_words:
        if word in content:
            errors.append(f"文档中使用了禁止词汇 '{word}'，违反零推测原则")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


def validate_all_documents(wiki_path: str) -> Dict:
    """
    验证所有文档
    
    Args:
        wiki_path: 知识库目录路径
        
    Returns:
        验证结果
    """
    wiki_dir = Path(wiki_path)
    
    if not wiki_dir.exists():
        return {
            "valid": False,
            "errors": [f"知识库目录不存在: {wiki_path}"]
        }
    
    # 查找所有 Markdown 文件
    md_files = list(wiki_dir.glob("*.md"))
    
    if len(md_files) == 0:
        return {
            "valid": False,
            "errors": [f"知识库目录中没有找到 Markdown 文件"]
        }
    
    # 验证每个文档
    all_results = {}
    all_errors = []
    all_warnings = []
    
    for md_file in md_files:
        result = validate_document(str(md_file))
        all_results[md_file.name] = result
        
        if result.get("errors"):
            all_errors.extend([f"{md_file.name}: {error}" for error in result["errors"]])
        if result.get("warnings"):
            all_warnings.extend([f"{md_file.name}: {warning}" for warning in result["warnings"]])
    
    # 检查文档间一致性
    consistency_result = validate_cross_document_consistency(wiki_dir)
    if consistency_result.get("errors"):
        all_errors.extend(consistency_result["errors"])
    if consistency_result.get("warnings"):
        all_warnings.extend(consistency_result["warnings"])
    
    is_valid = len(all_errors) == 0
    
    return {
        "valid": is_valid,
        "errors": all_errors,
        "warnings": all_warnings,
        "document_count": len(md_files),
        "results": all_results
    }


def validate_cross_document_consistency(wiki_dir: Path) -> Dict:
    """
    验证文档间一致性
    
    Returns:
        验证结果
    """
    errors = []
    warnings = []
    
    # 检查是否包含必要的文档
    required_docs = ["00-项目概述.md", "99-项目规范.md"]
    existing_docs = [f.name for f in wiki_dir.glob("*.md")]
    
    for required_doc in required_docs:
        if required_doc not in existing_docs:
            warnings.append(f"缺少必需文档: {required_doc}")
    
    # 检查是否有业务模块文档
    module_docs = [f for f in existing_docs if f.startswith("01-业务模块-")]
    if len(module_docs) == 0:
        warnings.append("没有找到业务模块文档")
    
    # 检查是否有文件关系文档
    relation_docs = [f for f in existing_docs if f.startswith("02-文件关系-")]
    if len(relation_docs) == 0:
        warnings.append("没有找到文件关系文档")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


if __name__ == "__main__":
    # 从 stdin 读取输入
    import sys
    
    # 尝试从 stdin 读取
    input_text = sys.stdin.read()
    
    # 如果 stdin 为空，尝试从命令行参数读取文件
    if not input_text and len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            input_text = f.read()
    
    # 处理可能的 UTF-8 BOM
    if input_text.startswith('\ufeff'):
        input_text = input_text[1:]
    
    input_data = json.loads(input_text)
    
    if "document_path" in input_data:
        # 验证单个文档
        result = validate_document(input_data["document_path"])
    elif "wiki_path" in input_data:
        # 验证所有文档
        result = validate_all_documents(input_data["wiki_path"])
    else:
        result = {
            "valid": False,
            "errors": ["缺少必需参数: document_path 或 wiki_path"]
        }
    
    # 输出结果到 stdout
    print(json.dumps(result, ensure_ascii=False, indent=2))