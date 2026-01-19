#!/usr/bin/env python3
"""
项目结构扫描脚本
扫描项目结构，识别模块、分层和组件
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def scan_project_structure(project_path: str) -> Dict:
    """
    扫描项目结构
    
    Args:
        project_path: 项目根目录路径
        
    Returns:
        包含项目结构信息的字典
    """
    project_root = Path(project_path)
    
    if not project_root.exists():
        return {"error": f"项目路径不存在: {project_path}"}
    
    result = {
        "project_path": str(project_root),
        "build_system": detect_build_system(project_root),
        "directory_structure": scan_directory_structure(project_root),
        "interface_layer": scan_interface_layer(project_root),
        "data_layer": scan_data_layer(project_root),
        "business_layer": scan_business_layer(project_root),
        "adapter_layer": scan_adapter_layer(project_root),
        "middleware": scan_middleware(project_root),
        "language": detect_language(project_root)
    }
    
    return result


def detect_build_system(project_root: Path) -> Dict:
    """
    识别构建系统
    
    Returns:
        构建系统信息
    """
    build_files = {
        "pom.xml": "maven",
        "build.gradle": "gradle",
        "build.gradle.kts": "gradle-kotlin",
        "requirements.txt": "pip",
        "setup.py": "setuptools",
        "pyproject.toml": "poetry",
        "package.json": "npm",
        "yarn.lock": "yarn",
        "go.mod": "go",
        "Cargo.toml": "cargo",
        "*.csproj": "msbuild",
        "*.sln": "msbuild",
        "Gemfile": "bundler",
        "composer.json": "composer"
    }
    
    detected = []
    
    for pattern, system in build_files.items():
        if "*" in pattern:
            # 处理通配符
            files = list(project_root.rglob(pattern.replace("*", "")))
            if files:
                detected.append({
                    "system": system,
                    "files": [str(f.relative_to(project_root)) for f in files]
                })
        else:
            file_path = project_root / pattern
            if file_path.exists():
                detected.append({
                    "system": system,
                    "file": str(file_path.relative_to(project_root))
                })
    
    return {"detected": detected}


def detect_language(project_root: Path) -> Dict:
    """
    识别主要编程语言
    
    Returns:
        语言信息
    """
    language_patterns = {
        "java": [".java"],
        "python": [".py"],
        "javascript": [".js", ".jsx"],
        "typescript": [".ts", ".tsx"],
        "go": [".go"],
        "rust": [".rs"],
        "csharp": [".cs"],
        "ruby": [".rb"],
        "php": [".php"]
    }
    
    file_counts = {}
    
    for language, extensions in language_patterns.items():
        count = 0
        for ext in extensions:
            count += len(list(project_root.rglob(f"*{ext}")))
        if count > 0:
            file_counts[language] = count
    
    # 按文件数量排序
    sorted_languages = sorted(file_counts.items(), key=lambda x: x[1], reverse=True)
    
    return {
        "primary": sorted_languages[0][0] if sorted_languages else "unknown",
        "file_counts": dict(sorted_languages)
    }


def scan_directory_structure(project_root: Path) -> Dict:
    """
    扫描目录结构
    
    Returns:
        目录结构信息
    """
    common_patterns = {
        "source": ["src", "lib", "app", "pkg"],
        "test": ["test", "tests", "__tests__"],
        "config": ["config", "conf", "settings"],
        "docs": ["docs", "doc"]
    }
    
    result = {}
    
    for category, patterns in common_patterns.items():
        found_dirs = []
        for pattern in patterns:
            dirs = [d for d in project_root.rglob(pattern) if d.is_dir()]
            found_dirs.extend([str(d.relative_to(project_root)) for d in dirs])
        result[category] = found_dirs
    
    return result


def scan_interface_layer(project_root: Path) -> List[Dict]:
    """
    扫描接口层
    
    Returns:
        接口层文件列表
    """
    patterns = {
        "java": ["*Controller.java", "*Api.java", "*Endpoint.java", "*Resource.java"],
        "python": ["*view.py", "*api.py", "*router.py", "*handler.py"],
        "javascript": ["*controller.js", "*route.js", "*api.js", "*handler.js"],
        "typescript": ["*controller.ts", "*route.ts", "*api.ts", "*handler.ts"],
        "go": ["*handler.go", "*controller.go", "*api.go"],
        "rust": ["*handler.rs", "*controller.rs"],
        "csharp": ["*Controller.cs", "*Api.cs"]
    }
    
    language = detect_language(project_root)["primary"]
    interface_files = patterns.get(language, [])
    
    result = []
    for pattern in interface_files:
        files = list(project_root.rglob(pattern))
        for file in files:
            result.append({
                "file": str(file.relative_to(project_root)),
                "type": "interface"
            })
    
    return result


def scan_data_layer(project_root: Path) -> List[Dict]:
    """
    扫描数据层
    
    Returns:
        数据层文件列表
    """
    patterns = {
        "java": ["*Entity.java", "*Repository.java", "*Mapper.java", "*DAO.java"],
        "python": ["*model.py", "*repository.py", "*dao.py"],
        "javascript": ["*model.js", "*repository.js", "*schema.js"],
        "typescript": ["*model.ts", "*repository.ts", "*schema.ts"],
        "go": ["*model.go", "*repository.go"],
        "rust": ["*model.rs", "*repository.rs"],
        "csharp": ["*Entity.cs", "*Repository.cs"]
    }
    
    language = detect_language(project_root)["primary"]
    data_files = patterns.get(language, [])
    
    result = []
    for pattern in data_files:
        files = list(project_root.rglob(pattern))
        for file in files:
            result.append({
                "file": str(file.relative_to(project_root)),
                "type": "data"
            })
    
    return result


def scan_business_layer(project_root: Path) -> List[Dict]:
    """
    扫描业务层
    
    Returns:
        业务层文件列表
    """
    patterns = {
        "java": ["*Service.java", "*Manager.java", "*Handler.java"],
        "python": ["*service.py", "*manager.py", "*handler.py"],
        "javascript": ["*service.js", "*manager.js"],
        "typescript": ["*service.ts", "*manager.ts"],
        "go": ["*service.go", "*manager.go"],
        "rust": ["*service.rs", "*manager.rs"],
        "csharp": ["*Service.cs", "*Manager.cs"]
    }
    
    language = detect_language(project_root)["primary"]
    business_files = patterns.get(language, [])
    
    result = []
    for pattern in business_files:
        files = list(project_root.rglob(pattern))
        for file in files:
            result.append({
                "file": str(file.relative_to(project_root)),
                "type": "business"
            })
    
    return result


def scan_adapter_layer(project_root: Path) -> List[Dict]:
    """
    扫描适配器层
    
    Returns:
        适配器层文件列表
    """
    patterns = {
        "java": ["*Client.java", "*Adapter.java", "*Facade.java"],
        "python": ["*client.py", "*adapter.py", "*facade.py"],
        "javascript": ["*client.js", "*adapter.js"],
        "typescript": ["*client.ts", "*adapter.ts"],
        "go": ["*client.go", "*adapter.go"],
        "rust": ["*client.rs", "*adapter.rs"],
        "csharp": ["*Client.cs", "*Adapter.cs"]
    }
    
    language = detect_language(project_root)["primary"]
    adapter_files = patterns.get(language, [])
    
    result = []
    for pattern in adapter_files:
        files = list(project_root.rglob(pattern))
        for file in files:
            result.append({
                "file": str(file.relative_to(project_root)),
                "type": "adapter"
            })
    
    return result


def scan_middleware(project_root: Path) -> List[Dict]:
    """
    扫描中间件配置
    
    Returns:
        中间件配置文件列表
    """
    config_patterns = ["*.yml", "*.yaml", "*.json", "*.toml", ".env"]
    
    result = []
    for pattern in config_patterns:
        files = list(project_root.rglob(pattern))
        for file in files:
            # 排除 node_modules 等目录
            if "node_modules" not in str(file) and "target" not in str(file):
                result.append({
                    "file": str(file.relative_to(project_root)),
                    "type": "config"
                })
    
    return result


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
    project_path = input_data.get("project_path", ".")
    
    # 执行扫描
    result = scan_project_structure(project_path)
    
    # 输出结果到 stdout
    print(json.dumps(result, ensure_ascii=False, indent=2))