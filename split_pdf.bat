@echo off
setlocal enabledelayedexpansion

if "%~1"=="" (
    echo Please drag and drop a PDF file onto this batch file
    pause
    exit /b 1
)

set "PDF_FILE=%~1"
set "SCRIPT_DIR=%~dp0"
set "OUTPUT_DIR=%~dp1Split"

if not exist "!PDF_FILE!" (
    echo Error: PDF file not found
    pause
    exit /b 1
)

echo.
echo Processing: !PDF_FILE!
echo Output directory: !OUTPUT_DIR!
echo.
echo Please wait while splitting the PDF...
echo.

python "!SCRIPT_DIR!pdf_splitter.py" "!PDF_FILE!" -o "!OUTPUT_DIR!" -s "ΛΟΓΑΡΙΑΣΜΟΣ"

if errorlevel 1 (
    echo.
    echo Error occurred while processing the PDF
) else (
    echo.
    echo PDF splitting completed successfully!
    echo Files are saved in: !OUTPUT_DIR!
    set /a count=0
    for %%f in ("!OUTPUT_DIR!\*.*") do set /a count+=1
    echo Total files created: !count!
)

echo.
echo Press any key to exit...
pause >nul