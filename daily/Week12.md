---
title: Week 12：域渗透与 C2 协同 - 周度总结
tags:
  - 学习总结
  - 阶段复盘
categories:
  - 网络安全
date: 2026-04-14
---

# Week 12：域渗透与 C2 协同 (AD & Command Control) - 周度总结

## 📅 本周学习概览

本周我们深入了企业内网的核心腹地——**Windows 域 (Active Directory)**。如果说 Week 11 是“进门”，那么 Week 12 就是“夺权”。我们学习了 Kerberos 协议的运作机制，以及如何利用其设计缺陷进行攻击（Kerberoasting, 黄金票据）。

此外，我们从“单兵作战”升级到了“团队协同”。通过 Cobalt Strike (CS) 这样的 C2 框架，我们学会了如何管理多个 Beacon，如何进行派生会话，以及如何通过 SMB Beacon 在内网中隐蔽地横向移动。

拿到域控（Domain Controller）权限，通常意味着一次内网渗透测试的通关。

<!--more-->

---

## 📚 每日核心知识回顾

### Day 068：Kerberos 协议详解
- **三头犬模型**：Client, Server, KDC (Key Distribution Center)。
- **认证流程**：
  1.  **AS-REQ**: Client -> AS (KDC)，请求 TGT (Ticket Granting Ticket)。
  2.  **AS-REP**: AS -> Client，返回 TGT（由 `krbtgt` 密码加密）。
  3.  **TGS-REQ**: Client -> TGS (KDC)，出示 TGT，请求 ST (Service Ticket)。
  4.  **TGS-REP**: TGS -> Client，返回 ST。
  5.  **AP-REQ**: Client -> Server，出示 ST，访问服务。

### Day 069：域渗透攻击向量 (Kerberoasting)
- **原理**：TGS-REP 返回的 ST 是由服务账号的 NTLM Hash 加密的。如果请求了某个服务（如 MSSQL）的票据，攻击者可以在本地离线暴力破解这个加密块，还原出服务账号的明文密码。
- **利用步骤**：
  1.  `GetUserSPNs.ps1` 或 Rubeus 查找注册了 SPN 的用户。
  2.  请求该 SPN 的票据。
  3.  导出 Hash 到 hashcat 破解。
- **防御**：给服务账号设置强密码。

### Day 070：黄金票据与白银票据
- **黄金票据 (Golden Ticket)**：
  - **条件**：拥有域控权限，拿到了 `krbtgt` 用户的 NTLM Hash。
  - **效果**：伪造 TGT，可以以任意用户身份（如域管）访问域内任意服务。有效期可设为 10 年，相当于域内的“免死金牌”。
- **白银票据 (Silver Ticket)**：
  - **条件**：拿到了服务账号（如 SQLService）的 Hash。
  - **效果**：伪造 ST，只能访问该特定服务。不经过 KDC，隐蔽性更高。

### Day 071：Cobalt Strike 基础安装与配置
- **TeamServer**：服务端，运行在 Linux VPS 上。`./teamserver <IP> <password> <profile>`。
- **Client**：客户端，攻击者操作界面。
- **Listener**：监听器。HTTP/HTTPS/DNS 等协议，用于接收 Beacon 的回连。
- **Beacon**：Payload。分 Staged (小，分段加载) 和 Stageless (大，全功能)。

### Day 072：CS 插件与上线操作
- **上线方式**：PowerShell 命令, Windows Executable, HTA, Office Macro。
- **Aggressor Script (.cna)**：CS 的插件脚本。
  - **Ladon**：大型内网扫描插件。
  - **Taowu**：后渗透提权插件集。
- **常用命令**：`sleep 60` (设置心跳), `shell whoami` (执行 CMD), `upload/download`。

### Day 073：使用 C2 进行横向移动
- **SMB Beacon**：
  - **原理**：不直接连外网，通过 SMB 管道 (`named pipe`) 连接已经上线的父 Beacon。流量封装在 SMB 协议中，防火墙通常允许。
  - **命令**：`link <target_ip>`（需要已建立 IPC$ 连接或有凭证）。
- **WMI / WinRM**：
  - `jump psexec64 <target> <listener>`
  - `jump winrm64 <target> <listener>`

### Day 074：周末闯关 - 模拟小型域环境渗透
- **实战场景**：
  1.  WebShell 上线 CS。
  2.  提权到 System。
  3.  Dump Hash 发现域用户凭证。
  4.  扫描发现域控 (DC)。
  5.  利用 SMB Beacon 横向移动到 DC。
  6.  导出 `krbtgt` Hash，制作黄金票据。

---

## 📝 巩固练习题 (Level 12)

### 一、 概念速查（单选/简答）

1.  **Kerberoasting 攻击针对的是 Kerberos 协议的哪一个阶段？**
    A) AS-REQ
    B) TGS-REP
    C) AP-REQ
    D) PAC 验证
2.  **制作黄金票据 (Golden Ticket) 必须要获取哪个用户的 NTLM Hash？**
3.  **Cobalt Strike 中，`Staged` Payload 和 `Stageless` Payload 的主要区别是什么？**
4.  **在 CS 中，为什么建议把 `sleep` 时间设置得长一点（如 60s 或更高）？**
5.  **SMB Beacon 适合在什么网络环境下使用？**

### 二、 场景分析与安全实践（实战模拟）

6.  **场景：Kerberos 错误**
    你在尝试横向移动时，使用了 `dir \\DC01\c$` 命令，收到错误 "Logon Failure: The target account name is incorrect"。
    *   这通常意味着什么？（提示：时间同步或 SPN 问题）
    *   如果收到 "KDC has no support for encryption type"，可能是什么原因？

7.  **场景：CS 隐蔽性**
    你的 CS Beacon 上线后不到 1 分钟就被杀软查杀了，IP 也被封了。
    *   你认为主要暴露点在哪里？（列举 2 点，如流量特征、默认证书）
    *   如何通过配置 Malleable C2 Profile 来改善？

8.  **场景：横向移动被拦**
    你拥有域管账号密码，尝试用 `psexec` 横向移动到一台 Win10 主机，但失败了。防火墙显示拦截了 445 端口。
    *   除了 SMB (445)，你还可以尝试利用什么协议/端口进行横向？（提示：WinRM, WMI, RDP）
    *   如果是 WinRM，默认端口是多少？

### 三、 深度思考与综合分析

9.  **为什么有了 NTLM Hash 就可以直接进行 PTH（哈希传递），而不需要解密出明文密码？这是否意味着 Windows 的认证设计有缺陷？如果是，为什么微软不修复？**

10. **作为防御方，如何检测网络中存在的 Cobalt Strike Beacon 流量？（提示：心跳包规律、JARM 指纹、默认 HTTP Header）**

---

## 🔑 参考答案

### 一、 概念速查
1.  **B) TGS-REP**。攻击者收到加密的 ST。
2.  **krbtgt** 账户。
3.  **Staged**：Payload 分两段，第一段很小（Loader），执行后从服务器下载第二段（Reflective DLL）。适合溢出漏洞利用。**Stageless**：完整包含所有功能，体积大。适合直接执行（exe/dll）。
4.  **隐蔽性**。频繁的心跳（如 1s）会产生大量连续流量，极易被流量分析设备（NTA）或防火墙识别并拦截。
5.  **不出网的内网主机**。该主机无法直接访问外网 VPS，但可以通过 SMB 协议与内网中一台能上网的跳板机通信。

### 二、 场景分析
6.  **Kerberos 错误**。
    *   可能意味着**时间不同步**（超过 5 分钟误差），或者目标机器的 SPN 注册丢失/重复。
    *   **加密类型不支持**。例如攻击机只支持 RC4，而域控强制要求 AES256。
7.  **CS 隐蔽性**。
    *   暴露点：使用了 CS 默认的 SSL 证书（Cobalt Strike Default证书）；流量特征明显（默认的 URI 路径）；Beacon 行为被 EDR 钩挂。
    *   改善：申请合法的 SSL 证书；配置 C2 Profile 伪装成 Amazon/jQuery 流量；使用 Artifact Kit 修改 Payload 特征。
8.  **横向移动被拦**。
    *   **WinRM (5985/5986)**。WMI (135 + 随机高端口，也难过防火墙)。RDP (3389)。
    *   **5985 (HTTP)** 和 **5986 (HTTPS)**。

### 三、 深度思考
9.  **PTH 原理**。
    *   NTLM 协议设计就是用 Hash 做 Challenge/Response 运算。
    *   **不算缺陷，是特性**。这就是“单点登录 (SSO)”的基础。只要凭证（Hash）是正确的，认证就该通过。
    *   **修复**：微软推出了 "Protected Users" 组（禁止 NTLM，强制 Kerberos），以及 "Credential Guard"（虚拟化隔离 LSASS 内存），来缓解 Hash 窃取。
10. **检测 CS 流量**。
    *   **心跳规律**：即使有抖动 (Jitter)，长连接的心跳统计特征依然明显。
    *   **TLS 指纹**：JA3/JARM 指纹，默认 TeamServer 的指纹很固定。
    *   **HTTP 特征**：默认 Profile 中的 User-Agent, Cookie, URL 路径等如果不修改，很容易写规则匹配。
