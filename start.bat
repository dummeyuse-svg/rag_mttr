 One-click launcher (Windows)Created a file, read a fileCreated a file, read a fileWindows batch file to start Ollama and the FastAPI server together




@echo off
title MTDR AI Assistant

echo Starting Ollama...
start "" "ollama" serve

timeout /t 3 /nobreak >nul

echo Starting MTDR backend...
start "" cmd /k "uvicorn app:app --host 127.0.0.1 --port 8000"

timeout /t 3 /nobreak >nul

echo Opening browser...
start http://127.0.0.1:8000

echo.
echo MTDR AI Assistant is running at http://127.0.0.1:8000
echo Close this window to leave the servers running.
pause
