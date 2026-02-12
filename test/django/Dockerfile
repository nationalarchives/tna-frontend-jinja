FROM ghcr.io/nationalarchives/tna-python-dev:latest

COPY ./test/django/pyproject.toml /app/pyproject.toml
COPY ./test/django/poetry.lock /app/poetry.lock
COPY ./package.json /app/package.json
COPY ./package-lock.json /app/package-lock.json
COPY ./test/django/manage.py /app/manage.py

RUN . tna-nvm; \
    npm i; \
    tna-build

COPY ./test/django/app /app/app

CMD ["tna-wsgi", "app.wsgi:application"]
