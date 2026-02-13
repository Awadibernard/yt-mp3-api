FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg

RUN pip install yt-dlp flask gunicorn

COPY server.py /app/server.py
WORKDIR /app

EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "server:app"]
