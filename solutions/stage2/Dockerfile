FROM python:3.9-slim

WORKDIR /app
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y ffmpeg libsm6 libxext6 libglib2.0-0
COPY sources/requirements.txt .
RUN pip3 install -r requirements.txt
EXPOSE 8000
COPY sources/OCR_routes.py app.py
CMD ["gunicorn", "-b :8000", "app:app"]