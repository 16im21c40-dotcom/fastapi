#!/bin/bash

# 1. 가상환경 활성화 (있으면)
source antenv/bin/activate

# 2. FastAPI 앱 실행
uvicorn main:app --host 0.0.0.0 --port 8000

chmod +x startup.sh