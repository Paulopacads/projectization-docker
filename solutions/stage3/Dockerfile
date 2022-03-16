FROM python:3.7-slim

WORKDIR /app

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y ffmpeg libsm6 libxext6 libglib2.0-0
COPY requirements.txt .

RUN pip3 install -r requirements.txt
RUN pip3 install https://github.com/jchazalon/pero-ocr/archive/refs/heads/master.zip

# Joseph autorise pour des raisons d'optimisation la copy
# de ces fichiers lourds plutot que la recuperation via
# internet qui peut prendre beaucoup de temps a chaque
# `docker-compose up`.
# Nous aurions pu cependant faire :
# ADD https://www.lrde.epita.fr/~jchazalo/SHARE/pero_eu_cz_print_newspapers_2020-10-09.tar.gz ./
# RUN mkdir pero_config_dir && \
#     tar -xvf pero_eu_cz_print_newspapers_2020-10-09.tar.gz -C pero_config_dir --strip-components 1
# ADD https://download.pytorch.org/models/vgg16-397923af.pth /root/.cache/torch/hub/checkpoints/
ADD pero_eu_cz_print_newspapers_2020-10-09.tar.gz ./
RUN mv pero_eu_cz_print_newspapers_2020-10-07 pero_config_dir
COPY weights.pth /root/.cache/torch/hub/checkpoints/vgg16-397923af.pth

ENV PERO_CONFIG_DIR='/app/pero_config_dir'

EXPOSE 8000
COPY OCR_routes.py app.py
COPY pero_ocr_driver.py .

CMD ["gunicorn", "-b :8000", "app:app"]