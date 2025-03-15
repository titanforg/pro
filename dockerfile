FROM python:3.10-slim

# نصب وابستگی‌های سیستم
RUN apt-get update && apt-get install -y ffmpeg

# نصب پکیج‌های پایتون
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# اجرای برنامه
COPY . .
CMD ["python", "main.py"]
