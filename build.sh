#!/usr/bin/env bash
# 시스템 패키지 업데이트 및 필수 패키지 설치
apt-get update && apt-get install -y wget libnss3 libatk1.0 libatk-bridge2.0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libasound2 libpangocairo-1.0-0 libpango-1.0-0 libcups2

# Python 패키지 설치
pip install -r requirements.txt

# Playwright 브라우저 설치
playwright install
