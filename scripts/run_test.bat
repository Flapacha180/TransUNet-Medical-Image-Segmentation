@echo off
REM run_test.bat -- Launch TransUNet evaluation on Synapse dataset
REM Run from project root: scripts\run_test.bat

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

echo === Starting TransUNet Evaluation on Synapse ===
echo Dataset: data\Synapse\
echo Note: Pancreas = label 6 in Synapse dataset
echo Paper reference - Pancreas Dice: 55.86%%
echo.

python test.py --dataset Synapse --vit_name R50-ViT-B_16 %*

endlocal
