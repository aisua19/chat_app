#セキュリティ最適化
FROM python:3.10-slim as builder

WORKDIR /app

# 環境変数抑制
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt ./

#キャッシュを使わず最小限に
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt


FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY ./app ./app

#FastAPIアプリケーションをUvicornで起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
