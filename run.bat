@echo off
title Mock DDoS Guard

echo Stopping old uvicorn instances...
taskkill /IM python.exe /F >nul 2>&1

cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload

pause