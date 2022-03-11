FROM python:3.9-slim

WORKDIR /app

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y ffmpeg libsm6 libxext6 libglib2.0-0
COPY sources/requirements.txt .

RUN pip3 install -r requirements.txt
RUN pip3 install https://github.com/jchazalon/pero-ocr/archive/refs/heads/master.zip

COPY sources/pero_config_dir pero_config_dir
COPY sources/weights.pth /root/.cache/torch/hub/checkpoints/vgg16-397923af.pth

ENV PERO_CONFIG_DIR=/app/pero_config_dir

EXPOSE 8000
COPY sources/OCR_routes.py app.py
COPY sources/pero_ocr_driver.py .

CMD ["gunicorn", "-b :8000", "app:app"]