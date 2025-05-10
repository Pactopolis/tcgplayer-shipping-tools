@echo off
setlocal

:: Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

:: Call the Python script with the provided arguments
python "%SCRIPT_DIR%main.py" %*

endlocal 