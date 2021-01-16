FROM python:3.9-slim-buster

LABEL maintainer=erdem@erdemuysal.net

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt && \
    mkdir /conf

COPY ./app.py /app
COPY ./config.yml /app
COPY ./docker-entrypoint.sh /docker-entrypoint.sh

EXPOSE 5000
ENTRYPOINT ["/bin/bash"]
CMD ["/docker-entrypoint.sh"]
