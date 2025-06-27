@echo off
title 🚀 Building SpaceLoginGUI Executable
echo ============================================
echo     BUILDING SpaceLoginGUI WITH PyInstaller
echo ============================================

cd /d %~dp0

REM Build .exe with icon
python -m PyInstaller --name SpaceLoginGUI --onefile --noconsole --add-data "assets;assets" --icon=space-logo.ico main.py

echo.
echo ✅ Done! Check the "dist" folder for SpaceLoginGUI.exe
pause
