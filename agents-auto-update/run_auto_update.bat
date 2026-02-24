@echo off
chcp 65001 >nul
echo ========================================
echo    Agents.dm 自动更新工具
echo ========================================
echo.

python -c "import watchdog" 2>nul
if errorlevel 1 (
    echo 正在安装依赖包...
    pip install watchdog
    echo.
)

echo 选择运行模式:
echo 1. 单次更新 (扫描一次并退出)
echo 2. 持续监控 (自动检测变化并更新)
echo.
set /p choice="请输入选项 (1 或 2): "

if "%choice%"=="1" (
    echo.
    echo 执行单次更新...
    python f:\skill\agents-auto-update\auto_update_agents.py once
) else if "%choice%"=="2" (
    echo.
    echo 启动持续监控...
    echo 按 Ctrl+C 停止监控
    echo.
    python f:\skill\agents-auto-update\auto_update_agents.py
) else (
    echo 无效选项，退出
)

echo.
pause
