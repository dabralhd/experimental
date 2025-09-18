FROM python:3.12-slim AS build-debug

ENV POETRY_VIRTUALENVS_CREATE=false PIP_NO_CACHE_DIR=1
RUN pip install poetry poetry-plugin-export
RUN python -m venv /venv

WORKDIR /install

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry export --without-hashes | /venv/bin/python -m pip install -r /dev/stdin
RUN poetry export --with build --without-hashes | grep '^python-minifier==\|^python-minifier =' | /venv/bin/python -m pip install -r /dev/stdin

FROM python:3.12-slim AS run-debug
RUN apt-get update && apt-get install -y coreutils

COPY --from=build-debug /venv /venv

RUN useradd --user-group --create-home -u 9001 -s /bin/bash project-api
USER 9001:9001

WORKDIR /app

COPY --chown=9001:9001 . .

ENV FLASK_ENV=development

#RUN /venv/bin/pyminify --remove-literal-statements --remove-asserts --remove-debug ./project_api --in-place

VOLUME /usr/storage
VOLUME /usr/project_api/api-service/app/swagger_server/oidc_provider_test
VOLUME /data

ENV OIDC_CLIENT_SECRETS_PATH=/usr/project_api/api-service/app/swagger_server/oidc_provider_test/client_secrets.json

EXPOSE 9090

ENTRYPOINT ["/bin/bash"]
CMD ["-c", "/venv/bin/python -m project_api --bind 0.0.0.0:9090 --workers \"${GUNICORN_WORKERS:-4}\" 'project_api:main()'"]
# CMD ["tail", "-f", "/dev/null"]
# CMD ["sleep", "infinity"]
# CMD ["python", "-c", "import time; time.sleep(99999999)"]

# Compilation step
FROM python:3.12-alpine AS build-release

ENV POETRY_VIRTUALENVS_CREATE=false POETRY_CACHE_DIR= PIP_NO_CACHE_DIR=1

RUN apk add --no-check-certificate patchelf gcc libc-dev ccache libffi-dev
RUN pip install poetry

WORKDIR /app
WORKDIR /build

COPY ./pyproject.toml ./poetry.lock ./
COPY . .

RUN poetry install --without dev --without debug

#RUN /venv/bin/pyminify --remove-literal-statements --remove-asserts --remove-debug ./project_api --in-place

RUN poetry run nuitka \
    --include-package-data=project_api \
    --include-package=gunicorn \
    --include-package=project_api \
    --follow-imports \
    --standalone \
    --output-dir=/app \
    --remove-output \
    project_api

# Final target image
FROM alpine AS run-release

RUN adduser -D -u 9001 -g 9001 -s /bin/sh project-api
USER 9001:9001
COPY --chown=9001:9001 --from=build-release /app /app

WORKDIR /app

ENV FLASK_ENV=production

VOLUME /usr/storage
VOLUME /usr/project_api/api-service/app/swagger_server/oidc_provider_test
VOLUME /data

ENV OIDC_CLIENT_SECRETS_PATH=/usr/project_api/api-service/app/swagger_server/oidc_provider_test/client_secrets.json

EXPOSE 9090

ENTRYPOINT ["/bin/sh"]
CMD ["-c", "/app/project_api.dist/project_api.bin --bind 0.0.0.0:9090 --workers \"${GUNICORN_WORKERS:-4}\" 'project_api:main()'"]
