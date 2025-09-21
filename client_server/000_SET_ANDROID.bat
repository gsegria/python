@echo off
:: -------------------------------
:: Android SDK 檢查與授權自動化
:: -------------------------------

:: 設定你的 SDK 根目錄
set SDK_ROOT=C:\Users\gs\Downloads\Tools\develop\android_sdk

:: 設定環境變數
set ANDROID_SDK_ROOT=%SDK_ROOT%
set PATH=%SDK_ROOT%\platform-tools;%SDK_ROOT%\cmdline-tools\latest\bin;%PATH%

:: 檢查 cmdline-tools 目錄
if not exist "%SDK_ROOT%\cmdline-tools\latest\bin\sdkmanager.bat" (
    echo ERROR: cmdline-tools\latest\bin\sdkmanager.bat 不存在！
    echo 請確認 cmdline-tools 已下載並解壓到 %SDK_ROOT%\cmdline-tools\latest\
    pause
    exit /b 1
)

:: 檢查平台工具
if not exist "%SDK_ROOT%\platform-tools\adb.exe" (
    echo ERROR: platform-tools\adb.exe 不存在！
    echo 請確認 platform-tools 已下載
    pause
    exit /b 1
)

:: 測試 sdkmanager 是否可用
sdkmanager --version
if errorlevel 1 (
    echo ERROR: sdkmanager 無法運行
    pause
    exit /b 1
)

:: 接受所有授權
echo 接受所有 Android SDK 授權...
sdkmanager --licenses

:: 完成
echo.
echo ✅ Android SDK 環境檢查完成
echo 你可以再執行: flutter doctor -v
pause
