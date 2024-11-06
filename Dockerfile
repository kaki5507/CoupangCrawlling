# 파이썬 3.10.15-slim
FROM python:3.10.15-slim

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 생성
WORKDIR /app

# requirements.txt 복사 및 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 크롤러 스크립트 복사
COPY crawlling.py .

# 환경 변수 설정
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# 크롤러 실행
CMD ["python", "crawlling.py"]