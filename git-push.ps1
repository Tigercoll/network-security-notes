# ========================================
# Git 多仓库推送脚本
# ========================================

param(
    [Parameter(Mandatory=$false)]
    [string]$Message = "Update notes",
    
    [Parameter(Mandatory=$false)]
    [switch]$All,
    
    [Parameter(Mandatory=$false)]
    [switch]$Origin,
    
    [Parameter(Mandatory=$false)]
    [switch]$Backup
)

Write-Host "=== Git 多仓库推送工具 ===" -ForegroundColor Cyan
Write-Host ""

# 检查是否有未提交的更改
$status = git status --porcelain
if ($status) {
    Write-Host "发现未提交的更改：" -ForegroundColor Yellow
    git status --short
    Write-Host ""
    
    $commit = Read-Host "是否提交这些更改？(y/n)"
    if ($commit -eq 'y') {
        git add .
        
        if ($Message -eq "Update notes") {
            $customMessage = Read-Host "请输入提交信息（直接回车使用默认）"
            if ($customMessage) {
                $Message = $customMessage
            }
        }
        
        git commit -m $Message
        Write-Host "✅ 已提交更改" -ForegroundColor Green
    } else {
        Write-Host "⚠️ 取消推送，请先提交更改" -ForegroundColor Yellow
        exit
    }
}

Write-Host ""
Write-Host "当前远程仓库配置：" -ForegroundColor Cyan
git remote -v
Write-Host ""

# 推送逻辑
if ($All) {
    # 推送到所有仓库
    Write-Host "推送到 origin (tigercoll-zsh)..." -ForegroundColor Yellow
    git push origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ origin 推送成功" -ForegroundColor Green
    } else {
        Write-Host "❌ origin 推送失败" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "推送到 backup (Tigercoll)..." -ForegroundColor Yellow
    git push backup main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ backup 推送成功" -ForegroundColor Green
    } else {
        Write-Host "❌ backup 推送失败" -ForegroundColor Red
    }
} elseif ($Origin) {
    # 只推送到 origin
    Write-Host "推送到 origin (tigercoll-zsh)..." -ForegroundColor Yellow
    git push origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ 推送成功" -ForegroundColor Green
    } else {
        Write-Host "❌ 推送失败" -ForegroundColor Red
    }
} elseif ($Backup) {
    # 只推送到 backup
    Write-Host "推送到 backup (Tigercoll)..." -ForegroundColor Yellow
    git push backup main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ 推送成功" -ForegroundColor Green
    } else {
        Write-Host "❌ 推送失败" -ForegroundColor Red
    }
} else {
    # 交互式选择
    Write-Host "请选择推送目标：" -ForegroundColor Cyan
    Write-Host "1. origin (tigercoll-zsh/network-security-learning)"
    Write-Host "2. backup (Tigercoll/network-security-notes)"
    Write-Host "3. 两个都推送"
    Write-Host ""
    
    $choice = Read-Host "请输入选项 (1/2/3)"
    
    switch ($choice) {
        "1" {
            Write-Host ""
            Write-Host "推送到 origin (tigercoll-zsh)..." -ForegroundColor Yellow
            git push origin main
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ 推送成功" -ForegroundColor Green
            } else {
                Write-Host "❌ 推送失败" -ForegroundColor Red
            }
        }
        "2" {
            Write-Host ""
            Write-Host "推送到 backup (Tigercoll)..." -ForegroundColor Yellow
            git push backup main
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ 推送成功" -ForegroundColor Green
            } else {
                Write-Host "❌ 推送失败" -ForegroundColor Red
            }
        }
        "3" {
            Write-Host ""
            Write-Host "推送到 origin (tigercoll-zsh)..." -ForegroundColor Yellow
            git push origin main
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ origin 推送成功" -ForegroundColor Green
            } else {
                Write-Host "❌ origin 推送失败" -ForegroundColor Red
            }
            
            Write-Host ""
            Write-Host "推送到 backup (Tigercoll)..." -ForegroundColor Yellow
            git push backup main
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ backup 推送成功" -ForegroundColor Green
            } else {
                Write-Host "❌ backup 推送失败" -ForegroundColor Red
            }
        }
        default {
            Write-Host "❌ 无效的选项" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "=== 完成 ===" -ForegroundColor Green
