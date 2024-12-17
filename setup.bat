@echo off
setlocal

REM Try pythonw directly first
pythonw --version >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    start /b "" pythonw "%~dp0main.pyw" %*
    exit /b 0
)

REM Check if Python is installed
python --version >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    REM Python exists but pythonw not in PATH, try to find it
    for /f "delims=" %%i in ('where python') do (
        set PYTHON_PATH=%%i
        set PYTHONW_PATH=%%~dpiPythonw.exe
        if exist "!PYTHONW_PATH!" (
            start /b "" "!PYTHONW_PATH!" "%~dp0main.pyw" %*
            exit /b 0
        )
    )
)

echo Python not found! Please install Python or add it to PATH.
pause
exit /b 1