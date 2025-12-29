# ========================================
# GitHub 多账号 SSH 配置脚本
# ========================================

Write-Host "=== GitHub 多账号 SSH 配置向导 ===" -ForegroundColor Cyan
Write-Host ""

# 步骤 1：生成新的 SSH 密钥
Write-Host "步骤 1：生成新的 SSH 密钥（为 tigercoll-zsh 账号）" -ForegroundColor Yellow
Write-Host "命令：ssh-keygen -t ed25519 -C 'your-email@example.com' -f ~/.ssh/id_ed25519_zsh"
Write-Host ""

$generateKey = Read-Host "是否现在生成密钥？(y/n)"
if ($generateKey -eq 'y') {
    $email = Read-Host "请输入您的邮箱地址"
    ssh-keygen -t ed25519 -C $email -f "$HOME\.ssh\id_ed25519_zsh"
    Write-Host "✅ 密钥已生成" -ForegroundColor Green
}

# 步骤 2：添加到 ssh-agent
Write-Host ""
Write-Host "步骤 2：添加 SSH 密钥到 ssh-agent" -ForegroundColor Yellow

# 确保 ssh-agent 正在运行
$sshAgent = Get-Service ssh-agent -ErrorAction SilentlyContinue
if ($sshAgent.Status -ne 'Running') {
    Write-Host "正在启动 ssh-agent..." -ForegroundColor Gray
    Start-Service ssh-agent
}

ssh-add "$HOME\.ssh\id_ed25519_zsh"
Write-Host "✅ 密钥已添加到 ssh-agent" -ForegroundColor Green

# 步骤 3：配置 SSH config
Write-Host ""
Write-Host "步骤 3：配置 SSH config 文件" -ForegroundColor Yellow

$sshConfigPath = "$HOME\.ssh\config"
$configContent = @"

# Tigercoll 账号（原有账号）
Host github.com-tigercoll
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519

# tigercoll-zsh 账号（新账号）
Host github.com-zsh
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_zsh
"@

if (Test-Path $sshConfigPath) {
    Add-Content -Path $sshConfigPath -Value $configContent
    Write-Host "✅ 已追加到现有 config 文件" -ForegroundColor Green
} else {
    New-Item -Path $sshConfigPath -ItemType File -Force
    Set-Content -Path $sshConfigPath -Value $configContent
    Write-Host "✅ 已创建新的 config 文件" -ForegroundColor Green
}

# 步骤 4：显示公钥
Write-Host ""
Write-Host "步骤 4：复制公钥到 GitHub" -ForegroundColor Yellow
Write-Host "公钥内容：" -ForegroundColor Gray
Write-Host "----------------------------------------" -ForegroundColor Gray
Get-Content "$HOME\.ssh\id_ed25519_zsh.pub"
Write-Host "----------------------------------------" -ForegroundColor Gray
Write-Host ""
Write-Host "✅ 公钥已复制到剪贴板" -ForegroundColor Green
Get-Content "$HOME\.ssh\id_ed25519_zsh.pub" | Set-Clipboard

Write-Host ""
Write-Host "请按以下步骤操作：" -ForegroundColor Cyan
Write-Host "1. 登录 tigercoll-zsh GitHub 账号"
Write-Host "2. 访问：https://github.com/settings/keys"
Write-Host "3. 点击 'New SSH key'"
Write-Host "4. 粘贴公钥（已在剪贴板）并保存"
Write-Host ""

Read-Host "完成后按 Enter 继续"

# 步骤 5：更新 Git 远程仓库 URL
Write-Host ""
Write-Host "步骤 5：更新 Git 远程仓库 URL" -ForegroundColor Yellow

Set-Location "D:\projects\Network Security"
git remote set-url origin git@github.com-zsh:tigercoll-zsh/network-security-learning.git

Write-Host "✅ 远程仓库 URL 已更新" -ForegroundColor Green
Write-Host ""
Write-Host "当前远程仓库配置：" -ForegroundColor Gray
git remote -v

# 步骤 6：测试连接
Write-Host ""
Write-Host "步骤 6：测试 SSH 连接" -ForegroundColor Yellow
ssh -T git@github.com-zsh

Write-Host ""
Write-Host "=== 配置完成！===" -ForegroundColor Green
Write-Host ""
Write-Host "现在您可以推送到 tigercoll-zsh 仓库：" -ForegroundColor Cyan
Write-Host "git push origin main" -ForegroundColor White
