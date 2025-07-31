#!/usr/bin/env pwsh
# BodyTune AI - One Command Startup
Set-Location "c:\Users\abhis\OneDrive\Desktop\BodyTune AI"
& ".venv\Scripts\activate"
Write-Host "🚀 Starting BodyTune AI..." -ForegroundColor Green
Write-Host "📱 Open: http://localhost:5000" -ForegroundColor Cyan
Write-Host "⏹️  Press Ctrl+C to stop" -ForegroundColor Yellow
python app.py
