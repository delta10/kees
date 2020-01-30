# UI build container
FROM node:12.13.1-alpine AS ui-build
WORKDIR /app

ENV CI=true

COPY package.json \
     package-lock.json \
     ./

RUN npm ci --no-progress --color=false --quiet

COPY assets/js/ assets/js/
COPY webpack.config.js webpack.config.js

RUN INLINE_RUNTIME_CHUNK=false npm run build

# API build container
FROM python:3.7-slim AS api-build
WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential

RUN python -m venv /app/venv && /app/venv/bin/pip install --upgrade pip

COPY requirements.txt /app
RUN /app/venv/bin/pip3 install -r requirements.txt


# Final container
FROM python:3.7-slim
WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y \
    mime-support \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

COPY --from=api-build /app/venv /app/venv
ENV PATH="/app/venv/bin:${PATH}"

COPY --from=ui-build /app/assets/bundles /app/assets/bundles
COPY --from=ui-build /app/webpack-stats.json /app/webpack-stats.json

COPY docker/config.py /app/kees/config.py
COPY docker/start.sh /start.sh
RUN chmod +x /start.sh

RUN mkdir -p /app/static /app/media && chown www-data:www-data /app/static /app/media

ENV PYTHONUNBUFFERED 1
ENV KEES_ENVIRONMENT production

EXPOSE 8000
CMD ["/start.sh"]
USER www-data
