@echo off
echo ========================================
echo      BodyTune AI - Starting Server
echo ========================================
echo.

cd /d "c:\Users\abhis\OneDrive\Desktop\BodyTune AI"

echo Activating virtual environment...
call ".venv\Scripts\activate"

echo.
echo Installing/updating packages...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo Testing application components...
python test_final_fix.py

echo.
echo Testing InBody score calculation...
python test_inbody_score.py

echo.
echo Running complete test suite...
python test_complete.py

echo.
echo ========================================
echo Starting Flask application...
echo Open your browser to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py

pause
