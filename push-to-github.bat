@echo off
echo ========================================
echo    BodyTune AI - GitHub Push Script
echo ========================================
echo.

REM Check if Git repository exists
if not exist ".git" (
    echo ERROR: Not a Git repository. Run 'git init' first.
    pause
    exit /b 1
)

echo Current Git status:
git status

echo.
echo ========================================
echo Instructions for pushing to GitHub:
echo ========================================
echo.
echo 1. Create a new repository on GitHub (github.com)
echo    - Repository name: BodyTune-AI
echo    - Description: Professional Health Analysis Platform
echo    - Make it Public or Private (your choice)
echo    - Do NOT initialize with README (we already have one)
echo.
echo 2. Copy the repository URL from GitHub
echo    - It will look like: https://github.com/yourusername/BodyTune-AI.git
echo.
echo 3. Run these commands in order:
echo.
echo    git remote add origin YOUR_REPOSITORY_URL
echo    git branch -M main
echo    git push -u origin main
echo.
echo ========================================
echo Example commands (replace with your URL):
echo ========================================
echo.
echo git remote add origin https://github.com/AbhishekR33/BodyTune-AI.git
echo git branch -M main  
echo git push -u origin main
echo.
echo ========================================
echo Your project is ready for GitHub!
echo ========================================
echo.
echo Features included in this commit:
echo - Professional InBody analysis system
echo - Medical report processing
echo - Personalized recommendations  
echo - Bootstrap 5 responsive UI
echo - Print-ready professional reports
echo - Complete Flask web application
echo.

pause
