@echo off
setlocal enabledelayedexpansion

echo ============================================
echo   Delete GitHub Release and Tag
echo ============================================
echo.

REM ===== Config =====
set "OWNER=starmcc"
set "REPO=qs-beanfun-5"
set "TAG=v5.7.8"
REM 在此填入你的 GitHub Personal Access Token (需 repo 权限)
set "TOKEN=在此填入你的token"
REM ===================

REM 若上方 TOKEN 未填写，则尝试从环境变量获取
if "%TOKEN%"=="在此填入你的token" (
    if defined GH_TOKEN (
        set "TOKEN=%GH_TOKEN%"
    ) else if defined GITHUB_TOKEN (
        set "TOKEN=%GITHUB_TOKEN%"
    )
)

if "%TOKEN%"=="" (
    echo [ERROR] No GitHub Token configured.
    echo Please fill in the TOKEN in the Config section of this script.
    exit /b 1
)

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
