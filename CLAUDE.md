# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI-NoteBook is an AI-driven intelligent content analysis and note-taking product that enables deep parsing of technical articles. It focuses on extracting, analyzing, and enhancing technical knowledge from web content using AI agents and structured analysis frameworks.

## Technology Stack

- **Primary Language**: Python 3.11.0
- **Secondary**: Node.js v22.14.0 (for .opencode dependencies)
- **AI/LLM Integration**: OpenCode AI SDK, Volcengine ARK (GLM-4.7, Doubao models)
- **API Services**: Exa API for code and web search
- **Package Managers**: Bun (for Node.js), pip (for Python)
- **Architecture Pattern**: Domain-Driven Design (DDD) 4-layer architecture

## Common Commands

### Running Python Scripts

All Python scripts use stdin/stdout for JSON I/O:

```bash
# Run any script directly (reads JSON from stdin)
echo '{"description": "analyze repo", "examples": []}' | python3 .opencode/skills/skill-creator/scripts/analyze_requirements.py

# Initialize a new skill
python3 .opencode/skills/skill-creator/scripts/init_skill.py <skill-name> --path <output-directory>

# Validate skill structure
python3 .opencode/skills/skill-creator/scripts/quick_validate.py <skill-directory>

# Package skill for distribution
python3 .opencode/skills/skill-creator/scripts/package_skill.py <skill-path> [output-dir]

# Validate wiki document
python3 .opencode/skills/repo-wiki-generator/scripts/validate_document.py

# Scan project structure
python3 .opencode/skills/repo-wiki-generator/scripts/scan_project_structure.py
```

### Node.js Dependencies

```bash
cd .opencode
bun install
# or
npm install
```

## Project Structure

```
AI-NoteBook/
├── .opencode/                           # OpenCode AI platform configuration
│   ├── skills/                         # AI skill modules (DDD architecture)
│   │   ├── skill-creator/             # Skill creation framework
│   │   ├── repo-wiki-generator/       # Project knowledge base generator
│   │   └── github-repository-analyzer/ # GitHub repo analyzer
│   └── package.json                   # Node.js dependencies
├── gientech/                          # Generated documentation output
├── opencode.json                      # OpenCode AI provider & MCP config
└── 技术文章深度解析系统.md             # Technical article analyzer design doc
```

## High-Level Architecture

### DDD 4-Layer Architecture

All skills follow Domain-Driven Design:

1. **Interface Layer** (YAML Frontmatter in SKILL.md): Trigger mechanism and request handling
2. **Application Layer** (SKILL.md): Scenario recognition and workflow orchestration
3. **Domain Layer** (SKILL.md): Business rules and task execution
4. **Infrastructure Layer** (scripts/references/assets): Deterministic logic, reference materials, and static resources

### Skill Structure Pattern

Each skill follows this structure:
```
skill-name/
├── SKILL.md          # Main skill documentation with YAML frontmatter + 4 DDD layers
├── scripts/          # Python scripts for deterministic logic
├── references/       # Reference materials and business rules
└── assets/           # Static resources (images, templates)
```

### Decision Workflow Pattern

Skills use Mermaid diagrams in the Application Layer to define:
- Scenario recognition
- Path orchestration
- Task execution
- Error handling and validation

## Important Conventions

### Python Code Style

```python
#!/usr/bin/env python3
"""模块文档字符串（中文）"""
import sys
import json
from pathlib import Path
from typing import Dict, Any

def process_data(input_data: Dict[str, Any]) -> tuple[bool, str]:
    """函数文档字符串. 返回: (success_bool, message_string)"""
    return True, "Success message"

# 使用 stdin/stdout 进行 JSON I/O
input_data = json.loads(sys.stdin.read())
print(json.dumps(result, indent=2, ensure_ascii=False))
```

- Use type hints (Python 3.9+ syntax)
- Return tuples for error handling: `(success, message)`
- 4-space indentation, snake_case naming
- File I/O with UTF-8 encoding
- Error messages in Chinese, printed to stderr

### SKILL.md Requirements

1. **YAML Frontmatter** (MUST include):
   ```yaml
   ---
   name: skill-name
   description: What the skill does + when to use it
   ---
   ```
   - `name`: lowercase alphanumeric with hyphens, max 64 chars
   - `description`: complete function + usage scenario

2. **Mermaid Diagrams**: Use for workflows in Application Layer

3. **Emphasis Markers**: **CRITICAL**, **MANDATORY**, **IMPORTANT**, **WARNING**

### Script Input/Output Conventions

- All scripts must use stdin for JSON input and stdout for JSON output
- Handle BOM (byte order mark) in input
- Use UTF-8 encoding
- Always use forward slashes (`/`) for cross-platform paths

### No Auxiliary Documentation

Do NOT create README.md, CHANGELOG.md, or similar files in skill directories. Keep all content in SKILL.md and references/.

## Configuration

### opencode.json

- **AI Providers**: Volcengine (GLM-4.7, Doubao), OpenAI-compatible API
- **MCP Services**: Exa API (code/web search), Sequential thinking
