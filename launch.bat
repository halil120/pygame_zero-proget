@echo off
setlocal

cd /d "%~dp0"

set "PROJECT_PYTHON=%LocalAppData%\Programs\Python\Python313\python.exe"

if exist "%PROJECT_PYTHON%" (
    "%PROJECT_PYTHON%" -m pgzero game.py
) else (
    python -m pgzero game.py
)

if errorlevel 1 (
    echo.
    echo The game stopped with an error.
    pause
    exit /b 1
)

endlocal
