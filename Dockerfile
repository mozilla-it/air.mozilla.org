#https://github.com/tiangolo/uwsgi-nginx-docker
FROM tiangolo/uwsgi-nginx:python3.7

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    postgresql-client \
 && rm -rf /var/lib/apt/lists/*

COPY . /app
RUN touch /app/.env

RUN pip3 install --no-cache-dir -r requirements.txt

ENV STATIC_ROOT=/app/static
ENV DJANGO_SETTINGS_MODULE=airmozilla.settings_docker

RUN python3 manage.py collectstatic --noinput
RUN python3 manage.py compress --force

COPY docker/legacyurlsmap.map /app/

COPY docker/uwsgi.ini /app/
COPY docker/prestart.sh /app/
COPY docker/wsgi.py /app
