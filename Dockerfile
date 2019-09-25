#https://github.com/tiangolo/uwsgi-nginx-docker
FROM tiangolo/uwsgi-nginx:python3.7

RUN apt-get update && apt-get install -y \
    postgresql-client \
 && rm -rf /var/lib/apt/lists/*

ADD . /app

RUN pip3 install --no-cache-dir -r requirements.txt

ENV STATIC_ROOT=/airmo/static
ENV DJANGO_SETTINGS_MODULE=airmozilla.settings_docker

RUN python3 manage.py collectstatic --noinput
RUN python3 manage.py compress --force

COPY docker/uwsgi.ini /app/
COPY docker/prestart.sh /app/