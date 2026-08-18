@echo off
chcp 65001 >nul
echo ============================================
echo   打包 GGM 拦截器 ggm_interceptor.exe
echo ============================================
echo.

pyinstaller --clean --onefile --noconsole ^
--name="ggm_interceptor" ^
--distpath="dist" ^
--workpath="build/ggm_interceptor" ^
ggm_interceptor.py -y

echo.
if exist "dist\ggm_interceptor.exe" (
    echo 打包成功: dist\ggm_interceptor.exe
) else (
    echo 打包失败，请检查上方错误信息。
)
echo.
pause
