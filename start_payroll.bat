@echo off
echo Starting Payroll Management System...

:: Navigate to the script directory
cd /d "%~dp0"

:: Start Streamlit
echo Launching Streamlit interface...
streamlit run main.py

pause
