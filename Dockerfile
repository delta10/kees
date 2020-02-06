# UI build container
FROM node:12.14.1-alpine AS ui-build
WORKDIR /app/frontend

COPY frontend/package.json \
     frontend/package-lock.json \
     /app/frontend/
RUN npm install

COPY frontend /app/frontend
RUN npm run build

# API build container
FROM python:3.8-slim AS api-build
WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential

RUN python -m venv /app/venv && /app/venv/bin/pip install --upgrade pip

COPY requirements.txt /app
RUN /app/venv/bin/pip3 install -r requirements.txt

# Final container
FROM python:3.8-slim
WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y \
    postgresql-client \
    mime-support \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

COPY --from=api-build /app/venv /app/venv
ENV PATH="/app/venv/bin:${PATH}"

COPY --from=ui-build /app/core/static/dist /app/core/static/dist
COPY --from=ui-build /app/frontend/webpack-stats.json /app/frontend/webpack-stats.json

COPY docker/config.py /app/kees/config.py
COPY docker/start.sh /start.sh
RUN chmod +x /start.sh

RUN mkdir -p /app/static /app/media && chown www-data:www-data /app/static /app/media

ENV PYTHONUNBUFFERED 1
ENV KEES_ENVIRONMENT production

EXPOSE 8000
CMD ["/start.sh"]
USER www-data
