---
title: Week 09：系统提权与后渗透 - 周度总结
tags:
  - 学习总结
  - 阶段复盘
categories:
  - 网络安全
date: 2026-03-28
---

# Week 09：系统提权与后渗透 (Privilege Escalation) - 周度总结

## 📅 本周学习概览

本周我们跨越了 Web 与系统的边界。在之前的学习中，我们的目标是拿到 WebShell（通常是低权限的 `www-data` 或 `IIS APPPOOL`）。但在这个阶段，我们要回答一个关键问题：**拿到 Shell 之后做什么？**

系统提权是渗透测试中至关重要的一环。只有获得了 Root（Linux）或 System/Administrator（Windows）权限，我们才能读取哈希、安装持久化后门、或以此为跳板进攻内网其他机器。

我们学习了如何利用系统内核的“老毛病”（Kernel Exploit），如何抓住管理员配置失误的“小辫子”（SUID, Sudo, 服务权限），以及如何使用 Metasploit 和自动化脚本让提权变得更高效。

<!--more-->

---

## 📚 每日核心知识回顾

### Day 052：Linux 提权基础与 SUID
- **提权核心思路**：收集信息 -> 寻找利用点 -> 执行利用 -> 获取 Root。
- **SUID 提权**：
  - **原理**：如果一个文件（如 `/usr/bin/find`）设置了 SUID 位（`chmod u+s`），那么普通用户执行它时，进程将暂时拥有该文件所有者（通常是 root）的权限。
  - **利用**：利用该程序的功能（如 `find ... -exec /bin/sh \;`）来生成一个 Root Shell。
  - **查找命令**：`find / -perm -u=s -type f 2>/dev/null`。

### Day 053：Linux 内核漏洞与 Sudo 滥用
- **内核漏洞 (Kernel Exploits)**：
  - **Dirty COW (CVE-2016-5195)**：竞态条件写入只读文件（修改 `/etc/passwd`）。
  - **CVE-2021-4034 (PwnKit)**：利用 `pkexec` 环境变量处理缺陷。
- **Sudo 滥用**：
  - **配置错误**：检查 `/etc/sudoers` 或运行 `sudo -l`。
  - **NOPASSWD**：如果某个命令（如 `vim`）被允许无密码 sudo 运行，可通过 `:!/bin/sh` 提权。
  - **LD_PRELOAD**：如果 sudo 配置保留了此环境变量，可注入恶意 .so 文件提权。

### Day 054：Windows 提权基础与服务权限
- **服务权限漏洞**：
  - **不安全的服务权限**：普通用户对某个服务（Service）有配置权限（`SERVICE_CHANGE_CONFIG`），可修改其 `binPath` 为恶意 exe，重启服务即提权。
  - **未引用的服务路径 (Unquoted Service Path)**：如果路径 `C:\Program Files\My App\service.exe` 没有引号，Windows 会尝试执行 `C:\Program.exe`。
- **AlwaysInstallElevated**：注册表策略允许普通用户以 System 权限安装 MSI 文件。

### Day 055：Windows 令牌窃取与内核漏洞
- **令牌 (Token)**：Windows 的身份凭证。
- **令牌窃取 (Token Impersonation)**：
  - 如果攻击者拥有 `SeImpersonatePrivilege`（常见于 IIS Service 账户），可以使用工具（如 Potato 系列：JuicyPotato, RoguePotato, SweetPotato）模拟 System 令牌。
- **内核漏洞**：
  - **MS17-010 (EternalBlue)**：SMB 漏洞。
  - **CVE-2020-0796 (SMBGhost)**。

### Day 056：Metasploit 后渗透提权实战
- **Meterpreter**：MSF 的强大 Payload。
- **常用命令**：
  - `getuid`：看当前是谁。
  - `getsystem`：尝试自动化提权（利用命名管道模拟等技术）。
  - `background`：挂起会话。
- **Local Exploit Suggester**：
  - `use post/multi/recon/local_exploit_suggester`。
  - 自动对比补丁库，推荐可用的提权模块。

### Day 057：自动化提权脚本 (PEAS系列)
- **LinPEAS / WinPEAS**：目前最流行的提权枚举脚本。
  - **功能**：全自动扫描系统信息、用户、进程、网络、软件版本、配置错误等。
  - **输出**：高亮显示高危项（红色/黄色背景），极大节省人工排查时间。
- **其他脚本**：
  - Linux: `linux-exploit-suggester.sh`, `GTFOBins` (网站查询)。
  - Windows: `PowerUp.ps1`, `Sherlock.ps1` (较老)。

### Day 058：周末闯关 - 提权综合练习
- **实战场景**：
  1.  通过 Web 漏洞（RCE）获得反弹 Shell。
  2.  上传 LinPEAS 发现 `sudo` 版本过低或存在 `SUID` 的 `nmap`。
  3.  利用 GTFOBins 查询 `nmap` 的提权参数，成功拿到 Root Flag。

---

## 📝 巩固练习题 (Level 9)

### 一、 概念速查（单选/简答）

1.  **在 Linux 中，命令 `chmod u+s file` 的作用是什么？**
    A) 给文件添加执行权限
    B) 设置 SUID 位，执行时拥有文件所有者的权限
    C) 锁定文件，禁止修改
    D) 允许任何人读取文件
2.  **Windows 提权中，"Unquoted Service Path" 漏洞利用了 Windows 解析文件路径的什么特性？**
3.  **什么是 GTFOBins？它在提权中有什么用？**
4.  **如果 `sudo -l` 显示 `(root) NOPASSWD: /usr/bin/vim`，你应该如何提权？**
5.  **为什么在获得 WebShell 后，通常需要反弹一个交互式 Shell (Reverse Shell) 才能更好地进行提权？**

### 二、 场景分析与安全实践（实战模拟）

6.  **场景：Linux SUID 提权**
    你在靶机上运行 `find / -perm -u=s -type f`，发现 `/usr/bin/systemctl` 有 SUID 权限。
    *   这是一个常见的 SUID 提权程序吗？
    *   你会去哪里查找如何利用它？（除了 Google）
    *   简述利用思路（提示：systemctl 可以管理服务）。

7.  **场景：Windows 烂土豆 (Rotten/Juicy Potato)**
    你拿到了一个 IIS 的 Webshell，权限是 `IIS APPPOOL\DefaultAppPool`。你运行 `whoami /priv` 发现开启了 `SeImpersonatePrivilege`。
    *   这意味着什么？你有机会提权到什么权限？
    *   你需要上传什么工具？
    *   这种提权方式依赖于 Windows 的哪个机制？（DCOM/RPC）

8.  **场景：MSF 后渗透**
    你通过 MSF 的 `exploit/multi/handler` 接收到了一个 meterpreter 会话。但是运行 `getsystem` 失败了。
    *   接下来你会尝试哪个 MSF 模块来寻找提权漏洞？
    *   如果模块推荐了 `exploit/linux/local/cve_2021_4034_pwnkit`，利用它需要什么条件？（如：目标架构、是否需要编译环境）

### 三、 深度思考与综合分析

9.  **内核提权（Kernel Exploit）虽然强大，但在真实渗透测试中往往是“最后手段”。为什么？它有什么风险？**

10. **作为防御者，如何防止 SUID 提权和 Sudo 滥用？请给出至少 2 条具体的加固建议。**

---

## 🔑 参考答案

### 一、 概念速查
1.  **B) 设置 SUID 位**。
2.  **解析空格的特性**。当路径包含空格且未引起来时，Windows 会从左向右尝试执行截断的路径（把空格视为分隔符）。
3.  **GTFOBins 是一个 curated list**（精选列表），列出了各种 Unix 二进制文件如何被滥用（Bypass 安全限制、提权、反弹 Shell）。是 Linux 提权的字典。
4.  **`sudo vim -c ':!/bin/sh'`**。在 Vim 中执行 Shell 命令，由于 Vim 是 root 启动的，Shell 也是 root 权限。
5.  **交互性**。很多提权操作（如 `su`, `sudo` 输入密码，某些 exploit）需要标准输入/输出 (TTY)。WebShell 通常是非交互的，无法处理这些操作。

### 二、 场景分析
6.  **systemctl SUID**。
    *   是。虽然不如 vim 常见，但很危险。
    *   **GTFOBins**。
    *   **思路**：创建一个恶意的 systemd 服务文件（`.service`），其中 `ExecStart=/bin/sh -c 'cat /root/flag > /tmp/flag'`，然后用 `/usr/bin/systemctl link` 链接该文件并启动服务。由于 systemctl 有 SUID，它会以 root 身份解析并运行该服务。
7.  **Windows 土豆提权**。
    *   意味着拥有“身份模拟”特权。有机会提权到 **System**。
    *   上传 **Juicy Potato** 或 **SweetPotato** 等工具，以及一个反弹 Shell 的 exe。
    *   依赖 **COM/DCOM** 组件的协商机制，通过中间人攻击本地 RPC 流量，迫使 System 账户向攻击者控制的端口发起认证，从而窃取 System 的令牌。
8.  **MSF 后渗透**。
    *   `post/multi/recon/local_exploit_suggester`。
    *   条件：目标系统未打补丁，目标架构匹配（x86/x64）。通常 MSF 的模块是编译好的利用代码，不需要目标有 gcc，但需要目标能执行二进制文件（且不被杀软拦截）。

### 三、 深度思考
9.  **内核提权的风险**。
    *   **稳定性差**：内核漏洞利用稍有不慎就会导致**系统崩溃 (Kernel Panic / BSOD)**，导致服务器重启，业务中断。这对生产环境是灾难性的。
    *   **痕迹明显**：系统日志可能记录崩溃信息。
    *   **环境依赖**：对内核版本要求极其严格，差一个小版本都可能导致失败或崩溃。
10. **防御建议**。
    *   **最小化 SUID**：定期扫描 `find / -perm -u=s`，移除不必要的 SUID 位（如 vim, find, nmap 不需要 SUID）。
    *   **严格限制 Sudo**：`/etc/sudoers` 中只授予用户必须的命令权限，尽量避免使用 `ALL`。禁止对允许 Shell 逃逸的程序（如 vim, less, more）授予 sudo 权限。
    *   **使用 NoExec 挂载**：对于 `/tmp` 或 `/dev/shm` 等目录，挂载时使用 `noexec` 选项，防止运行 exploit。
