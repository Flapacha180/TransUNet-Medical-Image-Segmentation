@echo off
REM run_train.bat -- Launch TransUNet training on Synapse dataset
REM Run from project root: scripts\run_train.bat

setlocal

cd /d "%~dp0\.."

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Verify dataset exists
if not exist "data\Synapse" (
    echo ERROR: Dataset not found at data\Synapse\
    echo Run 'python scripts\download_data.py --dataset Synapse' first.
    exit /b 1
)

REM Verify pre-trained weights exist
set WEIGHT_PATH=model\vit_checkpoint\imagenet21k\R50-ViT-B_16.npz
if not exist "%WEIGHT_PATH%" (
    echo ERROR: Pre-trained weights not found at %WEIGHT_PATH%
    echo Run 'python scripts\download_weights.py' first.
    exit /b 1
)

echo === Starting TransUNet Training on Synapse ===
echo Pre-trained weights: %WEIGHT_PATH%
echo Dataset: data\Synapse\
echo.

python train.py --dataset Synapse --vit_name R50-ViT-B_16 %*

endlocal
