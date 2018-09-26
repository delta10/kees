# Stage 1 - Compile needed Python dependencies
FROM alpine
RUN apk --no-cache add \
    linux-headers \
    build-base \
    python3 \
    python3-dev \
    musl-dev \
    pcre-dev \
    jpeg-dev \
    zlib-dev && \
  pip3 install virtualenv && \
  virtualenv /app/env

WORKDIR /app
COPY requirements.txt /app
RUN /app/env/bin/pip install -r requirements.txt

# Stage 2 - Build docker image suitable for execution and deployment
FROM alpine
RUN apk --no-cache add \
    ca-certificates \
    mailcap \
    musl \
    pcre \
    zlib \
    jpeg \
    python3

COPY . /app
COPY --from=0 /app/env /app/env

COPY ./docker/start.sh /start.sh

ENV PATH="/app/env/bin:${PATH}"
WORKDIR /app
EXPOSE 8000
CMD ["/start.sh"]
