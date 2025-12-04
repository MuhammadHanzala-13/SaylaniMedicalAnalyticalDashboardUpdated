@echo off
echo ============================================================
echo Saylani Medical Help Desk - Data Pipeline
echo Real-World Data Processing
echo ============================================================
echo.

echo [1/5] Cleaning Data...
python src/data_cleaning.py
if errorlevel 1 (
    echo ERROR: Data cleaning failed!
    pause
    exit /b 1
)
echo.

echo [2/5] Generating JSON Knowledge Base...
python src/json_kb_generator.py
if errorlevel 1 (
    echo ERROR: JSON KB generation failed!
    pause
    exit /b 1
)
echo.

echo [3/5] Running Enhanced EDA...
python src/eda_enhanced.py
if errorlevel 1 (
    echo WARNING: EDA failed, but continuing...
)
echo.

echo [4/5] Starting API Server (Port 8000)...
start "Saylani API Server" cmd /k "python -m uvicorn src.app:app --reload --port 8000"
timeout /t 5 /nobreak >nul
echo.

echo [5/5] Starting Dashboard (Port 8501)...
start "Saylani Dashboard" cmd /k "streamlit run src/dashboard.py"
timeout /t 3 /nobreak >nul
echo.

echo ============================================================
echo Pipeline Complete!
echo ============================================================
echo.
echo Access your system at:
echo   Dashboard: http://localhost:8501
echo   API Docs:  http://localhost:8000/docs
echo.
echo NOTE: Do not close the two new terminal windows that opened.
echo They are running the API Server and Dashboard.
echo.
echo Press any key to exit this launcher...
pause >nul
