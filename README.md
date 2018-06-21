# Air Mozilla Frontend

The code to actually call the API and refresh the Event model is in the
`refresh_events` management command.

Run `./manage.py refresh_events` to download the list of events.

## Deployment

This application requires python >= 3.4. All the python dependencies are
specified in `requirements.txt`.

The WSGI entry point is `airmozilla/wsgi.py:application`. You will need to set
these environment variables:

- `DJANGO_SETTINGS_MODULE` (you probably want to set this to `airmozilla.settings_live`)
- `DATABASE_URL`. postgres >= 9.4 is required.
- `STATIC_ROOT` (set to a directory that is made available at `STATIC_URL`
  (`/static/`). Static files will be collected here when you run `manage.py
  collectstatic` during deployment.)
- `SECRET_KEY`

`settings_live` assumes that memcached is listening at `127.0.0.1:11211`.

django-compressor is used to compile static files, which requires that the user
running the application has permission to write to `$STATIC_ROOT/CACHE/`.

`manage.py refresh_events` needs to be run on a cron-like schedule. The exact
frequency is not important. I've been doing every hour. The task is built to be
robust no matter when it's scheduled, even if they end up overlapping. On
average the task takes only about 15 seconds though.

To enable HSTS, set `SECURE_HSTS_SECONDS` in `settings_live.py`. See
<https://docs.djangoproject.com/en/1.11/ref/middleware/#http-strict-transport-security>
for more information.

To enable redirects to HTTPS, set `SECURE_SSL_REDIRECT = True` in
`settings_live.py`. See
<https://docs.djangoproject.com/en/2.0/ref/middleware/#ssl-redirect> for more
information.
