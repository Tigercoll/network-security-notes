---
title: Week 07：客户端攻击进阶 - 周度总结
tags:
  - 学习总结
  - 阶段复盘
categories:
  - 网络安全
date: 2026-03-14
---

# Week 07：客户端攻击进阶 (XSS & CSRF) - 周度总结

## 📅 本周学习概览

本周我们进入了 Web 安全中最具“艺术性”的领域——客户端攻击。如果说 SQL 注入是简单粗暴的“正面破门”，那么 XSS 和 CSRF 就是优雅的“借刀杀人”。

我们不再满足于简单的 `<script>alert(1)</script>`，而是深入研究了在各种防御措施（WAF、CSP、过滤）下的绕过技巧。我们学会了如何利用 SVG、DOM 特性乃至浏览器的解析差异来执行恶意代码。同时，我们也掌握了 CSRF 漏洞，理解了如何利用用户的身份悄无声息地完成转账或改密操作。

这两类漏洞常年霸榜 OWASP Top 10，理解它们的核心原理——**信任边界的混淆**（浏览器信任了来自服务器的恶意脚本，或者服务器信任了来自浏览器的伪造请求），是成为高级渗透测试人员的关键。

<!--more-->

---

## 📚 每日核心知识回顾

### Day 038：XSS 编码与绕过基础
- **核心逻辑**：当明文关键字（如 `script`, `alert`, `onerror`）被过滤时，利用浏览器解析顺序（HTML实体 -> URL解码 -> JS执行）进行混淆。
- **常见编码**：
  - **HTML 实体编码**：`&#60;` (<), `&#x3c;` (<)。利用点：在 HTML 属性值中（如 `<img src=x onerror=&#97;lert(1)>`）。
  - **URL 编码**：`%3c` (<)。利用点：在 URL 参数中。
  - **JS Unicode 编码**：`\u0061` (a)。利用点：在 `<script>` 标签内部。
- **绕过技巧**：
  - **大小写混淆**：`<ScRiPt>`。
  - **双写绕过**：`<scr<script>ipt>`（对抗简单的 `replace`）。
  - **利用注释**：`javascript:/*--></title></style>alert(1)//`。

### Day 039：SVG 与事件属性利用
- **SVG 黑魔法**：SVG 遵循 XML 标准，解析规则与 HTML 不同，常用于绕过 HTML 过滤。
  - Payload: `<svg/onload=alert(1)>`（无需空格）。
  - 嵌套利用: `<svg><script>alert(1)</script>`（在某些老版本过滤器中有效）。
- **冷门事件属性**：
  - `onfocus` / `autofocus`：`<input onfocus=alert(1) autofocus>`（自动触发，无需交互）。
  - `onmouseover` / `onmouseleave`：鼠标滑过触发。
  - `details` 标签：`<details open ontoggle=alert(1)>`。

### Day 040：DOM XSS 深度挖掘
- **原理**：不经过后端服务器，完全由前端 JS 逻辑处理输入并输出到页面，导致的 XSS。
- **关键概念**：
  - **Source (污染源)**：`location.hash`, `location.search`, `document.referrer`, `window.name`。
  - **Sink (执行点)**：`innerHTML`, `document.write`, `eval()`, `setTimeout()`, `location.href`。
- **挖掘方法**：不仅要看页面源码，更要使用开发者工具（F12）动态调试，跟踪变量的流向。

### Day 041：CSRF 原理与 POC 编写
- **CSRF (跨站请求伪造)**：攻击者诱导受害者访问恶意页面，利用受害者浏览器中残留的 Cookie，向目标网站发起伪造请求。
- **核心条件**：
  1.  目标网站没有任何 CSRF 防御（如 Token）。
  2.  利用 Cookie 进行身份认证（而非 Header 中的 Token）。
  3.  浏览器自动携带 Cookie。
- **POC 编写**：使用 Burp Suite 的 "Generate CSRF PoC" 功能，生成自动提交的 HTML 表单。

### Day 042：CSRF 防御与绕过
- **防御机制**：
  - **CSRF Token**：最有效。在表单中加入随机不可预测的 Token，服务端验证。
  - **Referer / Origin 校验**：检查请求来源域名。
  - **SameSite Cookie**：设置 `Strict` 或 `Lax`，限制第三方 Cookie 发送。
- **绕过思路**：
  - **Token 泄露**：Token 出现在 URL 中或通过 XSS 窃取。
  - **Referer 绕过**：空 Referer（`meta name="referrer" content="never"`），或正则匹配缺陷（如 `site.com.attacker.com`）。
  - **请求方法篡改**：后端只校验 POST 请求的 Token，改为 GET 请求可能绕过。

### Day 043：BeEF 框架入门
- **BeEF (Browser Exploitation Framework)**：专注于客户端（浏览器）攻击的框架。
- **核心原理**：Hook（钩子）。通过让受害者加载 `hook.js`，使受害者浏览器与 BeEF 服务器建立长连接。
- **功能模块**：
  - **信息收集**：浏览器版本、插件、内网 IP。
  - **社工攻击**：伪造 Flash 更新提示、伪造登录框窃取密码。
  - **内网扫描**：利用受害者浏览器作为代理，扫描其内网端口。

### Day 044：周末闯关 - XSS+CSRF 组合拳
- **实战场景**：
  1.  利用存储型 XSS 窃取管理员 Cookie。
  2.  利用 Self-XSS 配合 CSRF 将其转化为存储型 XSS。
  3.  利用 XSS 读取页面源码，获取 CSRF Token，从而实施 CSRF 攻击（绕过 Token 防御）。

---

## 📝 巩固练习题 (Level 7)

### 一、 概念速查（单选/简答）

1.  **在 DOM XSS 中，`location.search` 属于哪一类？**
    A) Sink (执行点)
    B) Source (污染源)
    C) Filter (过滤器)
    D) Output (输出)
2.  **以下哪个标签通常用于在不允许使用空格的情况下执行 XSS？**
    A) `<img>`
    B) `<script>`
    C) `<svg>`
    D) `<div>`
3.  **CSRF 攻击的本质是什么？它利用了浏览器的什么机制？**
4.  **SameSite Cookie 的 `Lax` 模式和 `Strict` 模式有什么区别？**
5.  **为什么 JSONP 经常会导致 XSS 漏洞？**

### 二、 场景分析与安全实践（实战模拟）

6.  **场景：WAF 绕过**
    你发现一个搜索框存在反射型 XSS，但是输入 `<script>` 会被 WAF 拦截并提示 "Illegal Tag"。输入 `javascript:` 也会被拦截。
    *   你会尝试哪些替代标签？（列举 2 个）
    *   你会尝试哪些替代伪协议或事件？
    *   如果 `<` 和 `>` 被转义成了 `&lt;` 和 `&gt;`，XSS 还有机会吗？为什么？

7.  **场景：DOM XSS 审计**
    你看到如下一段 JS 代码：
    ```javascript
    var lang = location.hash.substring(1);
    document.write("<select value='" + lang + "'>");
    ```
    *   这里存在漏洞吗？如果有，Sink 是什么？
    *   构造一个 Payload 来触发弹窗。
    *   如何修复这段代码？

8.  **场景：CSRF 防御评估**
    某网站的修改密码接口如下：`POST /api/changepwd`，参数为 `new_password`。请求头中包含 Cookie。开发者声称他们校验了 Referer 必须包含 `example.com`。
    *   这种防御足够安全吗？
    *   攻击者可能用什么域名来绕过这个正则匹配（假设正则写得不好，如 `/example.com/`）？
    *   如果攻击者能控制该网站下的一个子域（如 `blog.example.com`），能否绕过 Referer 保护？

### 三、 深度思考与综合分析

9.  **XSS 和 CSRF 经常被结合使用。请描述一个场景，攻击者如何利用 XSS 漏洞来攻破一个部署了 CSRF Token 防御的敏感操作接口（如转账）？**（提示：关键在于 Token 是如何获取的）

10. **现代前端框架（如 React, Vue）默认都对数据进行了转义，大大减少了 XSS。那么在使用这些框架时，通常在什么情况下还会产生 XSS 漏洞？**（列举 2 种情况，例如 `dangerouslySetInnerHTML`）

---

## 🔑 参考答案

### 一、 概念速查
1.  **B) Source (污染源)**。它是攻击者可控的输入源。
2.  **C) `<svg>`**。例如 `<svg/onload=alert(1)>`，在 XML 解析规则下 `/` 可以作为分隔符，不需要空格。
3.  **本质是利用了浏览器自动发送 Cookie 的机制**（隐式身份验证）。服务器无法区分请求是用户自愿发起的，还是被恶意页面诱导发起的。
4.  **Lax**：允许部分第三方链接（如 `<a>` 标签跳转、GET 表单）携带 Cookie，但 POST 请求不带。**Strict**：任何第三方发起的请求都不带 Cookie（体验较差，但最安全）。
5.  **JSONP 回调函数名未过滤**。如果 URL 是 `callback=<script>...`，服务器直接返回 `<script>...({data})`，就会导致 XSS。

### 二、 场景分析
6.  **WAF 绕过**。
    *   标签：`<img>`, `<body>`, `<svg>`, `<details>`, `<iframe>`。
    *   事件/伪协议：`onload`, `onerror`, `onfocus`, `autofocus`。
    *   **没有机会**。如果 `< >` 被正确转义，浏览器会将其视为文本而非标签结构，无法构建 HTML 元素，除非存在极其特殊的 DOM 库二次渲染问题。
7.  **DOM XSS**。
    *   存在。Sink 是 `document.write`。
    *   Payload: `#'><script>alert(1)</script>` 或者更简单的 `#'><img src=x onerror=alert(1)>`。闭合前面的 `<select>` 标签。
    *   修复：使用 `innerText` 或 `textContent`，或者对 `lang` 变量进行严格的白名单校验（如只允许 `en`, `zh`）。
8.  **CSRF 防御**。
    *   不安全。Referer 容易被伪造（在某些情况下）或绕过，且可能因隐私设置不发送。
    *   绕过域名：`example.com.attacker.com`, `attacker.com/example.com`, `attacker-example.com`。
    *   能。子域通常被认为是可信来源，Referer 校验通常允许子域。

### 三、 深度思考
9.  **XSS 破 CSRF Token**。
    *   攻击者利用 XSS 漏洞在受害者浏览器执行 JS 脚本。
    *   脚本发起一个 AJAX/Fetch 请求（同域请求），访问包含 CSRF Token 的页面（如转账页面的 HTML）。
    *   脚本解析响应内容，提取出 Token 值。
    *   脚本带上这个 Token 和转账参数，发起真正的转账 POST 请求。
    *   **结论**：XSS 破坏力高于 CSRF，因为 XSS 可以读取页面内容（包括 Token），从而击穿 CSRF 防御。
10. **框架 XSS**。
    *   **显式使用危险函数**：React 的 `dangerouslySetInnerHTML`，Vue 的 `v-html`。
    *   **URL 注入**：`href` 属性直接绑定用户输入，如 `<a href={userInput}>`，用户输入 `javascript:alert(1)`。
    *   **服务端渲染 (SSR) 注水问题**：服务端拼接字符串时未转义。
