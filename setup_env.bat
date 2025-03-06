@echo off
set VENV_DIR=venv

:: Check if virtual environment already exists
if exist %VENV_DIR% (
    echo Virtual environment '%VENV_DIR%' already exists.
) else (
    echo Creating virtual environment in '%VENV_DIR%'...
    python -m venv %VENV_DIR%
    echo Virtual environment created successfully.
)

:: Activate virtual environment and install dependencies
call %VENV_DIR%\Scripts\activate

echo Installing required packages...
pip install numpy matplotlib tk
echo Packages installed successfully.

echo Setup complete! To activate the environment manually, run:
echo   call %VENV_DIR%\Scripts\activate
