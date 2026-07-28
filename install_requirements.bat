@echo off
setlocal

cd /d "%~dp0"

set "PROJECT_PYTHON=%LocalAppData%\Programs\Python\Python313\python.exe"

if exist "%PROJECT_PYTHON%" (
    "%PROJECT_PYTHON%" -m pip install -r requirements.txt
) else (
    python -m pip install -r requirements.txt
)

if errorlevel 1 (
    echo.
    echo Failed to install project dependencies.
    exit /b 1
)

echo.
echo Project dependencies installed successfully.
endlocal
