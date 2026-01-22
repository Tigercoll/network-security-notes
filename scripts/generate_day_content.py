"""Generate detailed content for Day033-Day090."""
from __future__ import annotations

from pathlib import Path

DAY_TEMPLATES = {
    "Day033": {
        "title": "日志规范与字段统一",
        "week": 5,
        "date": "2026-01-26",
        "objective": "- 将不同来源日志统一字段\n- 形成规范文档",
        "content": """### 1️⃣ 日志规范化的重要性

#### 1.1 为什么需要统一字段？

**问题场景：**

```
系统A日志格式：
[2026-01-26 10:30:45] [INFO] user=admin action=login ip=192.168.1.100

系统B日志格式：
{"timestamp": "2026-01-26T10:30:45Z", "level": "info", "user": "admin", "event": "login", "src_ip": "192.168.1.100"}

系统C日志格式：
Jan 26 10:30:45 server01 auth[1234]: login_success admin from 192.168.1.100
```

**统一规范的好处：**

| 方面 | 不统一的问题 | 统一后的好处 |
|------|-------------|-------------|
| **查询效率** | 需要编写多个不同查询语句 | 一套查询语句覆盖所有来源 |
| **关联分析** | 无法关联同一用户的跨系统行为 | 可以追踪用户在多系统的行为链 |
| **告警规则** | 需要为每种格式单独配置 | 统一告警规则，降低维护成本 |
| **合规审计** | 证据收集复杂，容易遗漏 | 标准化证据，易于审计追踪 |
| **存储成本** | 索引冗余，浪费存储 | 统一字段映射，优化存储 |

---

### 2️⃣ 统一日志字段规范

#### 2.1 必选字段（Common Fields）

| 字段名 | 说明 | 数据类型 | 示例 |
|--------|------|---------|------|
| **timestamp** | 时间戳（UTC） | datetime | 2026-01-26T10:30:45.123Z |
| **level** | 日志级别 | string | "info", "warning", "error", "critical" |
| **source** | 来源系统 | string | "nginx", "apache", "mysql", "ssh" |
| **host** | 主机名/IP | string | "web-server-01", "192.168.1.10" |
| **event_type** | 事件类型 | string | "login", "logout", "file_access", "network" |
| **user** | 用户标识 | string | "admin", "user@example.com", "uid:1001" |
| **action** | 动作 | string | "read", "write", "execute", "delete" |

#### 2.2 可选字段（Optional Fields）

| 字段名 | 说明 | 数据类型 | 示例 |
|--------|------|---------|------|
| **status** | 操作状态 | string | "success", "failure", "partial" |
| **ip_address** | 源/目标IP | string | "192.168.1.100", "203.0.113.5" |
| **port** | 端口号 | integer | 22, 443, 3306 |
| **protocol** | 协议 | string | "tcp", "udp", "http", "ssh" |
| **object** | 操作对象 | string | "/etc/passwd", "database:users" |
| **bytes** | 数据大小 | integer | 1024, 51200 |
| **duration_ms** | 持续时间（毫秒） | integer | 125, 5000 |
| **correlation_id** | 关联ID | string | "req-abc123-def456" |

---

### 3️⃣ 字段映射策略

#### 3.1 映射规则

**原则：**

1. **时间标准化**：所有时间转换为 UTC ISO 8601 格式
2. **级别归一化**：映射到统一级别（debug/info/warning/error/critical）
3. **命名规范**：使用 snake_case（小写+下划线）
4. **数据类型**：确保字段类型一致

**示例映射表：**

| 原系统 | 原字段 | 目标字段 | 转换规则 |
|--------|--------|---------|---------|
| **Nginx** | $time_local | timestamp | 转为UTC ISO格式 |
| **Nginx** | $status | status_code | 保留整数 |
| **Apache** | %h | ip_address | 客户端IP |
| **Apache** | %u | user | 用户名 |
| **MySQL** | user | user | 数据库用户 |
| **MySQL** | command | action | Query, Connect, Quit |
| **SSH** | from | ip_address | 客户端IP |
| **SSH** | user | user | 登录用户 |

#### 3.2 实践：Nginx 日志映射

**原始 Nginx 日志：**

```
192.168.1.100 - admin [26/Jan/2026:10:30:45 +0800] "GET /admin/dashboard HTTP/1.1" 200 1234 "https://example.com/login" "Mozilla/5.0"
```

**Nginx 日志格式定义：**

```nginx
log_format unified_json escape=json '{'
    '"timestamp": "$time_iso8601",'
    '"level": "info",'
    '"source": "nginx",'
    '"host": "$server_addr",'
    '"ip_address": "$remote_addr",'
    '"user": "$remote_user",'
    '"method": "$request_method",'
    '"uri": "$request_uri",'
    '"protocol": "$server_protocol",'
    '"status": $status,'
    '"bytes": $body_bytes_sent,'
    '"referer": "$http_referer",'
    '"user_agent": "$http_user_agent"'
'}';
```

**映射后 JSON：**

```json
{
    "timestamp": "2026-01-26T02:30:45.123Z",
    "level": "info",
    "source": "nginx",
    "host": "192.168.1.10",
    "ip_address": "192.168.1.100",
    "user": "admin",
    "method": "GET",
    "uri": "/admin/dashboard",
    "protocol": "HTTP/1.1",
    "status": 200,
    "bytes": 1234,
    "referer": "https://example.com/login",
    "user_agent": "Mozilla/5.0"
}
```

---

### 4️⃣ 日志收集与传输

#### 4.1 Filebeat 配置示例

**filebeat.yml 示例：**

```yaml
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/nginx/*.log
    fields:
      source: nginx
      environment: production
    fields_under_root: true
    json.keys_under_root: true
    json.add_error_key: true

  - type: log
    enabled: true
    paths:
      - /var/log/auth.log
    fields:
      source: ssh
      environment: production
    fields_under_root: true

output.elasticsearch:
  hosts: ["http://elasticsearch:9200"]
  index: "logs-%{+yyyy.MM.dd}"

setup.template.settings:
  index.number_of_shards: 1
```

#### 4.2 Logstash 过滤与规范化

**logstash.conf 示例：**

```conf
filter {
  # 统一时间格式
  date {
    match => ["timestamp", "ISO8601"]
    timezone => "UTC"
    target => "@timestamp"
  }

  # 统一日志级别
  mutate {
    rename => { "severity" => "level" }
  }

  # 添加缺失字段默认值
  mutate {
    add_field => {
      "environment" => "production"
      "cluster" => "cluster-01"
    }
  }

  # 移除调试信息
  mutate {
    remove_field => [ "message", "agent", "ecs", "log" ]
  }
}
```

---

### 5️⃣ 日志规范落地清单

#### 5.1 规范文档结构

**`log-specification.md`：**

```markdown
# 日志规范化规范

## 1. 字段定义

### 1.1 必选字段
...

### 1.2 可选字段
...

## 2. 映射规则

### 2.1 时间格式
...

### 2.2 级别映射
...

## 3. 各系统配置

### 3.1 Nginx
...

### 3.2 Apache
...

### 3.3 MySQL
...

## 4. 验证方法
```

#### 5.2 验证脚本

**validate_logs.py：**

```python
#!/usr/bin/env python3
"""验证日志格式是否符合规范。"""
import json
import sys
from pathlib import Path

REQUIRED_FIELDS = ["timestamp", "level", "source", "host", "event_type", "user", "action"]

def validate_log_entry(entry: dict) -> tuple[bool, list[str]]:
    """验证单条日志。"""
    errors = []

    for field in REQUIRED_FIELDS:
        if field not in entry:
            errors.append(f"Missing required field: {field}")

    if "timestamp" in entry:
        try:
            import datetime
            datetime.datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            errors.append(f"Invalid timestamp format: {entry['timestamp']}")

    if "level" in entry and entry["level"] not in ["debug", "info", "warning", "error", "critical"]:
        errors.append(f"Invalid level: {entry['level']}")

    return len(errors) == 0, errors

def main() -> int:
    """主函数。"""
    if len(sys.argv) < 2:
        print("Usage: validate_logs.py <log_file.json>")
        return 1

    log_file = Path(sys.argv[1])

    with open(log_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            try:
                entry = json.loads(line)
                valid, errors = validate_log_entry(entry)
                if not valid:
                    print(f"Line {line_num}: FAILED")
                    for error in errors:
                        print(f"  - {error}")
            except json.JSONDecodeError as e:
                print(f"Line {line_num}: Invalid JSON - {e}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
```
""",
        "tasks": """#### 🎯 任务 1: 分析现有日志格式

**执行以下步骤：**

1. 选择 2 个不同的系统（如 Nginx 和 SSH）
2. 各收集 10 条日志样本
3. 分析字段差异
4. 设计统一映射方案

**输出：** 一份字段映射表

---

#### 🎯 任务 2: 配置日志规范化

**选择一个系统进行配置：**

- 修改日志格式为统一格式
- 配置 JSON 输出
- 验证输出正确性

**输出：** 配置文件 + 5 条规范化日志样本

---

#### 🎯 任务 3: 验证日志格式

**使用验证脚本：**

```bash
python validate_logs.py /path/to/normalized.log
```

**输出：** 验证结果截图
""",
        "practice": """### 📝 练习 1: 字段映射设计

**题目：** 以下两个系统的日志格式，设计统一映射方案

**系统 A（Web 服务器）：**
```
[2026-01-26 10:30:45] admin GET /api/users 200 123ms 192.168.1.100
```

**系统 B（数据库）：**
```
2026-01-26 10:30:45.123 UTC | user=admin | query=SELECT * FROM users | time=50ms | rows=10
```

**要求：**
- 列出统一字段列表
- 为每个系统设计映射规则
- 写出映射后的 JSON 格式示例

---

### 📝 练习 2: 级别映射

**题目：** 设计日志级别映射表

将以下来源的日志级别映射到统一规范：

| 来源 | 原级别 | 目标级别 | 理由 |
|------|--------|---------|------|
| Nginx | 200 | info | 正常HTTP响应 |
| Nginx | 404 | warning | 资源未找到 |
| Nginx | 500 | error | 服务器错误 |
| MySQL | ERROR | error | 数据库错误 |
| MySQL | Warning | warning | 警告 |
| SSH | Failed | warning | 登录失败 |
| SSH | Accepted | info | 登录成功 |

---

### 📝 练习 3: 时间格式转换

**题目：** 编写脚本转换不同时间格式到 UTC ISO 8601

**输入格式：**
- `26/Jan/2026:10:30:45 +0800` (Nginx)
- `2026-01-26 10:30:45` (MySQL)
- `Jan 26 10:30:45` (Syslog)

**输出格式：**
- `2026-01-26T02:30:45.000Z`

**要求：** 提供 Python 或 Shell 脚本实现
""",
        "criteria": """- ✅ 提交规范文档（字段定义 + 映射规则）
- ✅ 至少 2 个系统的映射配置
- ✅ 验证脚本运行成功
- ✅ 输出规范化日志样本
"""
    }
}


def generate_day_content(day_num: str) -> str:
    """Generate content for a specific day."""
    if day_num not in DAY_TEMPLATES:
        return ""

    template = DAY_TEMPLATES[day_num]

    return template["content"]


if __name__ == "__main__":
    for day in ["Day033"]:
        print(f"=== {day} ===")
        print(generate_day_content(day))
        print()
