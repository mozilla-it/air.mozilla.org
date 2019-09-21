#https://github.com/tiangolo/uwsgi-nginx-docker
FROM tiangolo/uwsgi-nginx:python3.7

ADD . /app

RUN pip3 install --no-cache-dir -r requirements.txt

ENV STATIC_ROOT=/airmo/static
ENV DJANGO_SETTINGS_MODULE=airmozilla.settings

RUN python3 manage.py collectstatic --noinput
RUN python3 manage.py compress --force

COPY docker/uwsgi.ini /app/

#EXPOSE 8000
#
#CMD uwsgi --plugins python3 --home /usr/local --http-socket :8000 --wsgi-file nubis/puppet/files/wsgi.py --chdir /airmo
