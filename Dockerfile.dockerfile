FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["gunicorn", "Telegram_bot:app", "--bind", "0.0.0.0:$PORT"]