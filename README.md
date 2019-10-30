# FNW (Fox n' Wolf) Client

[build-badge](https://travis-ci.org/SashaNullptr/FNWClient.svg?branch=master)

## What is this project?

A Prometheus client that generates conversation/interpersonal interaction analytics
from various platforms.

## Building from Source

This project relies on [Bazel](https://docs.bazel.build/versions/master/install.html)
for building and container deployment.


## Building

```shell script
bazel build //...
```

## Running Locally

```shell script
bazel run //services/streaming:server
```

## Getting Started

You'll need a Telegram API ID and Hash to get started. These can be obtained by visiting https://my.telegram.org/apps and filling out the
form therein.

## Example Docker-Compose

```yaml
version: '3.6'

services:

  prometheus:
    image: quay.io/prometheus/prometheus:v2.0.0
    volumes:
     - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    command: "--config.file=/etc/prometheus/prometheus.yml --storage.tsdb.path=/prometheus"
    ports:
     - '9090:9090'
    depends_on:
     - fnw-client

  fnw-client:
    image: sashanullptr/fnw-client:latest
    ports:
     - "8080:8080"
    environment:
     API_ID: '12345'
     API_HASH: '0123456789abcdef0123456789abcdef'

  grafana:
    image: grafana/grafana:6.3.3
    depends_on:
      - prometheus
    networks:
      - monitoring_network
    ports:
      - '3000:3000'
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  grafana_data: {}

networks:
  monitoring_network:
```
