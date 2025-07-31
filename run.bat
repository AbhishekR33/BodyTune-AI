@echo off
title BodyTune AI - Quick Start
echo ========================================
echo      BodyTune AI - Starting Server
echo ========================================
echo.

cd /d "c:\Users\abhis\OneDrive\Desktop\BodyTune AI"

REM Activate virtual environment
echo Activating virtual environment...
call ".venv\Scripts\activate"

REM Set environment variables
set FLASK_ENV=development
set FLASK_DEBUG=True

echo.
echo ========================================
echo Starting Flask application...
echo Open your browser to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start the Flask application
python app.py

echo.
echo Application stopped.
pause

pause
