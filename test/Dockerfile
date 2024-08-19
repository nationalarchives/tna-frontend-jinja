FROM ghcr.io/nationalarchives/tna-python:latest

COPY --chown=app test .
COPY --chown=app ../tna_frontend_jinja /home/app/tna_frontend_jinja

RUN tna-build

CMD ["tna-run", "app:app"]