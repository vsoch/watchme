FROM continuumio/miniconda

# docker build -t vanessa/watchme .

RUN apt-get update && apt-get install -y git gcc && \
    mkdir -p /code
ADD . /code
WORKDIR /code
RUN pip install .[all]
ENTRYPOINT ["watchme"]
