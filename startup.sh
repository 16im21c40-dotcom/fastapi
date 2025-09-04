#!/bin/bash
# ===========================
# Azure App Service Minimal Startup Script
# No virtual environment required
# ===========================

# 1. 환경 변수
export PORT=${PORT:-8000}
export HOST=${HOST:-0.0.0.0}

# 2. 앱 루트 이동
APP_ROOT="/home/site/wwwroot"
if [ -d "$APP_ROOT" ]; then
    cd "$APP_ROOT" || { echo "Failed to cd to $APP_ROOT"; exit 1; }
else
    echo "App root not found!"
    exit 1
fi

# 3. requirements.txt 설치 (앱 처음 배포 시)
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install --no-cache-dir -r requirements.txt
fi

# 4. FastAPI 실행
if [ -f "main.py" ]; then
    echo "Starting FastAPI app..."
    exec uvicorn main:app --host $HOST --port $PORT
else
    echo "Error: main.py not found!"
    exit 1
fi