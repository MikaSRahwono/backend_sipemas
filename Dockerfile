FROM python:3.11.8
RUN apt-get update -qq && apt-get install -y -qq \
    gdal-bin binutils libproj-dev libgdal-dev cmake &&\
    apt-get clean all &&\
    rm -rf /var/apt/lists/* &&\
    rm -rf /var/cache/apt/*
ENV PYTHONUNBUFFERED 1
WORKDIR /backend_sipemas
COPY . /backend_sipemas
RUN pip install -r requirements.txt
COPY entrypoint.sh backend_sipemas/entrypoint.sh
RUN chmod +x backend_sipemas/entrypoint.sh