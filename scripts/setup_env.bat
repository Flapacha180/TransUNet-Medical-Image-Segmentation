@echo off
REM setup_env.bat -- Install TransUNet dependencies into active venv
REM Run from project root: scripts\setup_env.bat

setlocal

cd /d "%~dp0\.."

echo === TransUNet Dependency Installation ===

REM Check uv is available
where uv >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: uv is not installed or not in PATH.
    echo Install from: https://docs.astral.sh/uv/getting-started/installation/
    exit /b 1
)

REM Check venv is activated
python -c "import sys; assert sys.prefix != sys.base_prefix, 'No venv active'" 2>nul
if %errorlevel% neq 0 (
    echo ERROR: No virtual environment is active.
    echo Run: uv venv
    echo Then: .venv\Scripts\activate
    exit /b 1
)

echo Installing PyTorch (compatible with modern GPUs)...
uv pip install torch torchvision

echo Installing remaining dependencies...
uv pip install numpy tqdm tensorboard tensorboardX ml-collections medpy SimpleITK scipy h5py

echo Installing gdown for dataset downloads...
uv pip install gdown

echo.
echo === Setup Complete ===
echo All dependencies installed in active venv.

endlocal
