FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

# МЕНЯЕМ НА ALIYUN (самое стабильное зеркало)
RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple/
RUN pip config set global.trusted-host mirrors.aliyun.com

# Устанавливаем зависимости
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "run.py"]
