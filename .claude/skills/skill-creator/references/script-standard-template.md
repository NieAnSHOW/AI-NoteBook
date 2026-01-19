# 标准 Python 脚本模板

Infrastructure 层脚本的标准模板。

## 完整模板

```python
#!/usr/bin/env python3
"""
Script Name: script_name.py
Description: Brief description of what this script does
"""

import sys
import json
from typing import Dict, Any


def process(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main processing function.
    
    Args:
        data: Input data dictionary
        
    Returns:
        Processed result dictionary
        
    Raises:
        ValueError: When input validation fails
    """
    # Validate input
    required_fields = ['field1', 'field2']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    # Process data
    result = {
        "status": "success",
        "processed_field": data["field1"] + data["field2"]
    }
    
    return result


def main():
    """Main execution function."""
    try:
        # Read JSON from stdin
        data = json.loads(sys.stdin.read())
        
        # Validate & Process
        result = process(data)
        
        # Output JSON to stdout
        print(json.dumps(result, indent=2))
        
    except ValueError as e:
        error_result = {
            "status": "error",
            "error_type": "ValueError",
            "message": str(e)
        }
        print(json.dumps(error_result, indent=2), file=sys.stderr)
        sys.exit(1)
        
    except Exception as e:
        error_result = {
            "status": "error",
            "error_type": type(e).__name__,
            "message": str(e)
        }
        print(json.dumps(error_result, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
```

## 模板说明

| 部分 | 说明 |
|------|------|
| Shebang | `#!/usr/bin/env python3` 确保跨平台兼容 |
| Docstring | 脚本名称和功能描述 |
| process() | 核心处理逻辑，便于单元测试 |
| main() | 入口函数，处理 I/O 和异常 |
| 输入验证 | 检查必需字段 |
| 错误处理 | 统一的错误输出格式 |
