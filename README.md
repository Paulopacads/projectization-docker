# projectization-docker

Students:
- `paul.galand`
- `temano.frogier`

Dockerization of an OCR for DEVI course at EPITA.\
The goal is to dockerize a Python server to do character recognition.\
Stage 4 is the most advanced docker setup. You can follow the following steps to run my project.

**Python scripts are mainly (if not entirely) written by teacher [Joseph Chazalon](https://github.com/jchazalon).**

## STAGE 1

### Goal

Running a simple Python server on port 5000 on host machine using Flask.

### Run

Saying you are in `solution/stage1`:
```sh
docker-compose up
```

### Expected behaviour

Method: POST\
Path: `imgshape`\
Goal: get depth, height and width of a given image\
Needed: jpg file

Use example:
```sh
$ curl -X POST --header "Content-type: image/jpeg" --url http://localhost:5000/imgshape -T path/to/image.jpg
{
  "content": {
    "depth": 3,
    "height": 1080,
    "width": 1920
  }
}
```

## STAGE 2

### Goal

Running a simple Python server on port 8000 on host machine using Gunicorn.

### Run

Saying you are in `solution/stage2`:
```sh
docker-compose up
```

### Expected behaviour

Same as Stage 1 on port 8000.

## STAGE 3

### Goal

Running a synchronous OCR server on port 8000 on host machine using Gunicorn.

### Run

Saying you are in `solutions/stage3`:
```sh
(cd sources \
    && wget https://www.lrde.epita.fr/~jchazalo/SHARE/pero_eu_cz_print_newspapers_2020-10-09.tar.gz \
    && wget https://download.pytorch.org/models/vgg16-397923af.pth) \
    && docker-compose up
```

### Expected behaviour

Method: GET\
Path: `check`\
Goal: check if server is running\
Needed:

Use example:
```sh
$ curl --url http://localhost:8000/check
Hello
```

---

Method: POST\
Path: `ocr`\
Goal: run ocr on a given image\
Needed: jpg image

Use example:
```sh
$ curl -X POST --header "Content-type: image/jpeg" --url http://localhost:8000/ocr -T path/to/image.jpg
{
  "content": "Text written on my given image"
}
```

## STAGE 4

### Goal

Running an asynchronous OCR and a web server with task queuing on port 8000 on host machine using Celery.\
You should expect three different services running:
- ocr server
- web server
- rabbitmq

### Run

Saying you are in `solutions/stage4`:
```sh
(cd sources-ocr \
    && wget https://www.lrde.epita.fr/~jchazalo/SHARE/pero_eu_cz_print_newspapers_2020-10-09.tar.gz \
    && wget https://download.pytorch.org/models/vgg16-397923af.pth) \
    && docker-compose up
```

### Expected behaviour

Method: GET\
Path: `check`\
Goal: check if server is running\
Needed:

Use example:
```sh
$ curl --url http://localhost:8000/check
Hello
```

---

Method: POST\
Path: `ocr`\
Goal: run ocr on a given image\
Needed: jpg image

Use example:
```sh
$ curl -X POST --header "Content-type: image/jpeg" --url http://localhost:8000/ocr -T path/to/image.jpg
{
  "submitted": "1202243e-4c2e-4cf2-b399-69a2ce04635f"
}
```

---

Method: GET\
Path: `results/{UUID}`\
Goal: get result of a given task id\
Needed:

Use example:
```sh
$ curl --url http://localhost:8000/results/1202243e-4c2e-4cf2-b399-69a2ce04635f
{
  "content": {
    "content": "Text written on my given image"
  }
}
```
(You may get a "PENDING" answer if your image has not been treated yet)
