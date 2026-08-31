@echo off
setlocal enabledelayedexpansion

echo ============================================
echo   Delete GitHub Release and Tag
echo ============================================
echo.

REM ============================================================
REM  Config
REM ============================================================
REM  OWNER / REPO : 目标仓库
REM  TAG          : 要删除的标签（Release 和 Tag）
REM ============================================================
set "OWNER=starmcc"
set "REPO=qs-beanfun-5"
set "TAG=v5.7.8"
REM ============================================================
REM  Token 从环境变量 GH_TOKEN 读取，请勿硬编码到脚本中！
REM  设置方式（Windows CMD）：
REM     set GH_TOKEN=你的token
REM  设置方式（PowerShell）：
REM     $env:GH_TOKEN="你的token"
REM  永久设置（CMD）：
REM     setx GH_TOKEN "你的token"
REM ============================================================

REM 从环境变量读取 Token
if not defined GH_TOKEN (
    echo [ERROR] Environment variable GH_TOKEN is not set.
    echo Please set it first, e.g.:
    echo   set GH_TOKEN=your_token
    exit /b 1
)
set "TOKEN=%GH_TOKEN%"

echo Target repo: %OWNER%/%REPO%
echo Target tag : %TAG%
echo.

REM ===== 使用 PowerShell 执行删除逻辑（支持草稿 release 和 JSON 解析）=====
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ErrorActionPreference='Stop';" ^
  "$owner='%OWNER%';" ^
  "$repo='%REPO%';" ^
  "$tag='%TAG%';" ^
  "$token='%TOKEN%';" ^
  "$headers=@{Authorization='token '+$token;Accept='application/vnd.github+json'};" ^
  "$base='https://api.github.com/repos/'+$owner+'/'+$repo;" ^
  "Write-Host '[1/2] Searching release with tag: '$tag' ...';" ^
  "$releases=Invoke-RestMethod -Uri ($base+'/releases?per_page=100') -Headers $headers -Method Get;" ^
  "$rel=$releases | Where-Object { $_.tag_name -eq $tag } | Select-Object -First 1;" ^
  "if ($rel) {" ^
  "  Write-Host ('Found release id: '+$rel.id+' (draft='+$rel.draft+', prerelease='+$rel.prerelease+')');" ^
  "  Invoke-RestMethod -Uri ($base+'/releases/'+$rel.id) -Headers $headers -Method Delete;" ^
  "  Write-Host '[DONE] Release deleted.';" ^
  "} else {" ^
  "  Write-Host '[INFO] No release found with tag: '$tag'.' ;" ^
  "};" ^
  "Write-Host '';" ^
  "Write-Host '[2/2] Checking tag: '$tag' ...';" ^
  "try {" ^
  "  $ref=Invoke-RestMethod -Uri ($base+'/git/refs/tags/'+$tag) -Headers $headers -Method Get;" ^
  "  Invoke-RestMethod -Uri ($base+'/git/refs/tags/'+$tag) -Headers $headers -Method Delete;" ^
  "  Write-Host '[DONE] Tag deleted.';" ^
  "} catch {" ^
  "  Write-Host '[INFO] Tag not found or already deleted.';" ^
  "}"

echo.
echo ============================================
echo   Done. Please verify on GitHub Releases page.
echo ============================================
pause
