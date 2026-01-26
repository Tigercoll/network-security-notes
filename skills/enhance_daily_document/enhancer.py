from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

@dataclass
class TopicInfo:
    name: str
    domain: str
    concept_1: str
    concept_2: str
    tools: str

TOPICS = {
    "network": TopicInfo("Network Protocol", "Network", "Network Model", "Protocol Stack", "Wireshark, tcpdump, curl"),
    "security": TopicInfo("Network Security", "Security", "CIA Triad", "Threats and Vulnerabilities", "Nessus, OpenVAS"),
    "web": TopicInfo("Web Security", "Web", "OWASP Top 10", "Input Validation", "Burp Suite, OWASP ZAP"),
    "cryptography": TopicInfo("Cryptography", "Encryption", "Symmetric/Asymmetric", "Hash and Signatures", "OpenSSL, Keytool"),
    "penetration": TopicInfo("Penetration Testing", "Pentest", "Pentest Methodology", "Info Gathering", "Nmap, Metasploit"),
    "system": TopicInfo("System Security", "OS", "Access Control", "Logging and Monitoring", "Usermod, Auditd"),
    "analysis": TopicInfo("Security Analysis", "Analysis", "Traffic Analysis", "Log Analysis", "Wireshark, Splunk")
}

class ContentGenerator:
    def __init__(self):
        pass
    
    def _detect_topic(self, content: str) -> TopicInfo:
        keywords = {
            "network": ["network", "protocol", "TCP", "UDP", "IP", "OSI", "HTTP", "DNS"],
            "security": ["security", "encryption", "auth", "authorization", "vulnerability", "attack", "defense"],
            "web": ["Web", "SQL injection", "XSS", "CSRF", "OWASP", "API"],
            "cryptography": ["crypto", "hash", "encryption", "certificate", "TLS", "SSL", "PKI"],
            "penetration": ["penetration", "exploit", "privilege", "lateral", "internal"],
            "system": ["system", "Linux", "Windows", "permission", "user", "process"],
            "analysis": ["analysis", "log", "monitoring", "forensics", "traffic", "Wireshark"]
        }
        for category, kw_list in keywords.items():
            if any(kw in content for kw in kw_list):
                return TOPICS[category]
        return TOPICS["network"]
    
    def _has_complete_section(self, sections_dict: Dict[str, str], keywords: list, min_lines: int = 10) -> bool:
        for name, content in sections_dict.items():
            for kw in keywords:
                if kw in name and len(content.split('\n')) >= min_lines:
                    return True
        return False
    
    def generate(self, analyzer, verbose: bool = False) -> str:
        analysis = analyzer.analyze()
        score = analyzer.get_completeness_score()
        
        if score >= 90:
            if verbose:
                print(f"Document already complete (score: {score:.1f}%)")
            return None
        
        enhanced_content = analyzer.content
        existing_sections = analyzer.sections
        
        if not self._has_complete_section(existing_sections, ["Practice Tasks", "实践任务", "Task 1"]):
            enhanced_content += """

## Practice Tasks (实践任务 - Authorized Scope Only)

> Security Notice: All tasks must be performed in authorized environments.

### Task 1: Environment Setup (Required)
Verify tools and network connectivity.

### Task 2: Core Experiment (Required)
Complete main technical practices.

### Task 3: Advanced Challenge (Optional)
Deep dive into principles.

---
"""
            if verbose:
                print("  - Added Practice Tasks")
        elif verbose:
            print("  - Practice Tasks already complete")
        
        if not self._has_complete_section(existing_sections, ["Exercises", "巩固练习", "Questions"], min_lines=15):
            enhanced_content += """

## Exercises and Review (巩固练习与复盘)

### Exercise Categories

| Type | Purpose | Weight |
|------|---------|--------|
| Concept Questions | Test understanding | 20% |
| Practical Tasks | Test technical skills | 40% |
| Case Studies | Test knowledge transfer | 40% |

### Part 1: Concept Questions (20 points)
Explain core concepts learned today.

### Part 2: Practical Tasks (40 points)
Complete operations and analyze results.

### Part 3: Case Studies (40 points)
Analyze scenarios and solve problems.

---

### Reference Answers

| Question | Points |
|----------|--------|
| 1 | 10 |
| 2 | 10 |
| 3 | 20 |
| 4 | 20 |
| 5 | 40 |

**Total Score**: 90-100 Excellent, 80-89 Good, 60-79 Satisfactory

---
"""
            if verbose:
                print("  - Added Exercises")
        elif verbose:
            print("  - Exercises already complete")
        
        if not self._has_complete_section(existing_sections, ["Evaluation", "评估标准", "Criteria"], min_lines=15):
            enhanced_content += """

## Evaluation Criteria (评估标准)

### Assessment Dimensions

| Dimension | Weight | Description |
|-----------|---------|-------------|
| Concept Understanding | 30% | Core concept comprehension |
| Technical Skills | 40% | Tool usage and operations |
| Problem Solving | 20% | Analysis capability |
| Security Awareness | 10% | Security boundary awareness |

### Achievement Levels

| Score | Level | Description |
|-------|-------|-------------|
| 90-100 | Excellent | Fully achieved learning objectives |
| 80-89 | Good | Mostly achieved, review weak areas |
| 60-79 | Satisfactory | Partially achieved, supplement missing |
| Below 60 | Needs Retake | Not achieved, relearning required |

---

### Self-Checklist

#### Concept Understanding
- [ ] Can explain core concepts in your own words?
- [ ] Can give real-world examples?

#### Technical Operations
- [ ] Is environment ready?
- [ ] Can use core tools correctly?

#### Security Awareness
- [ ] Are authorization boundaries clear?
- [ ] Are operation risks understood?

---
"""
            if verbose:
                print("  - Added Evaluation Criteria")
        elif verbose:
            print("  - Evaluation Criteria already complete")
        
        if not self._has_complete_section(existing_sections, ["Learning Outcomes", "学习成果", "Results"], min_lines=15):
            enhanced_content += """

## Learning Outcomes (学习成果达成情况)

### Learning Information

| Item | Content |
|------|---------|
| Date | YYYY-MM-DD |
| Duration | ____ hours |

### Screenshots & Evidence

- Task 1: [ ]
- Task 2: [ ]

### Key Findings

| ID | Finding | Risk Level |
|----|---------|------------|
| 1 | | |

### Self-Assessment

| Skill | Rating (1-5) |
|-------|--------------|
| Concepts | ⭐⭐⭐⭐⭐ |
| Tools | ⭐⭐⭐⭐⭐ |
| Analysis | ⭐⭐⭐⭐⭐ |

---

**Congratulations on completing today's learning!**

```bash
git add daily/DayXXX/
git commit -m "DayXXX: Completed learning and records"
```

---
"""
            if verbose:
                print("  - Added Learning Outcomes")
        elif verbose:
            print("  - Learning Outcomes already complete")
        
        return enhanced_content
