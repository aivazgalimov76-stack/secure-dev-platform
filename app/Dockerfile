FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

# Устанавливаем зависимости с зеркалом Aliyun
RUN pip install --no-cache-dir -r requirements.txt \
    -i http://mirrors.aliyun.com/pypi/simple/ \
    --trusted-host mirrors.aliyun.com

COPY . .

EXPOSE 5001

CMD ["python", "run.py", "--port=5001"]
