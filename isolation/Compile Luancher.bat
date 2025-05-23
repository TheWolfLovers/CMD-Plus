@echo off
echo Compiling CMD+ Launcher
pyinstaller --onefile --icon=CMD+.ico CMD+.py
if %errorlevel% neq 0 (
    echo Compilation failed.
    pause
    exit /b %errorlevel%
)
echo Done
echo Exe generated in dist\ btw
pause