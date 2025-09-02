FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


COPY . .

EXPOSE 9001

# ENV FASTAPI_RELOAD="false"  # можно по умолчанию
#ENV FASTAPI_RELOAD="false"

ENV PYTHONPATH=/app

CMD ["python", "main.py"]
