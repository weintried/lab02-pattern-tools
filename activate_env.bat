@echo off
set VENV_DIR=venv

:: Check if virtual environment exists
if not exist %VENV_DIR% (
    echo Error: Virtual environment '%VENV_DIR%' not found. Run 'setup_env.bat' first.
    exit /b
)

:: Activate virtual environment
echo Activating virtual environment '%VENV_DIR%'...
call %VENV_DIR%\Scripts\activate

:: Keep the terminal open
cmd /k
