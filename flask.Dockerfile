FROM ghcr.io/nationalarchives/tna-python:latest

COPY --chown=app . .

RUN tna-build

CMD ["tna-run", "test.flask:app"]