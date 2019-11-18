# FNW (Fox n' Wolf) Client

[build-badge](https://travis-ci.org/SashaNullptr/FNWClient.svg?branch=master)

## What is this project?

A Prometheus client that generates conversation/interpersonal interaction analytics
from various platforms.

## Building from Source

This project relies on [Bazel](https://docs.bazel.build/versions/master/install.html)
for building and container deployment.


## Building

```shell
bazel build //...
```

## Running Locally

```shell
bazel run //services/streaming:server
```

## Getting Started

You'll need a Telegram API ID and Hash to get started. These can be obtained by visiting https://my.telegram.org/apps and filling out the
form therein.

## Example Set Up

### Config Files

#### Grafan Provisioning File

`./monitoring/grafana/provisioning/datasources/prometheus.yml`

```yaml
# config file version
apiVersion: 1

# list of datasources that should be deleted from the database
deleteDatasources:
  - name: Prometheus
    orgId: 1

# list of datasources to insert/update depending
# whats available in the database
datasources:
  # <string, required> name of the datasource. Required
- name: Prometheus
  # <string, required> datasource type. Required
  type: prometheus
  # <string, required> access mode. direct or proxy. Required
  access: proxy
  # <int> org id. will default to orgId 1 if not specified
  orgId: 1
  # <string> url
  url: http://prometheus:9090
  # <string> database password, if used
  password:
  # <string> database user, if used
  user:
  # <string> database name, if used
  database:
  # <bool> enable/disable basic auth
  basicAuth: true
  # <string> basic auth username
  basicAuthUser: admin
  # <string> basic auth password
  basicAuthPassword: foobar
  # <bool> enable/disable with credentials headers
  withCredentials:
  # <bool> mark as default datasource. Max one per org
  isDefault: false
  # <map> fields that will be converted to json and stored in json_data
  jsonData:
     graphiteVersion: "1.1"
     tlsAuth: false
     tlsAuthWithCACert: false
  # <string> json object of data that will be encrypted.
  secureJsonData:
    tlsCACert: "..."
    tlsClientCert: "..."
    tlsClientKey: "..."
  version: 1
  # <bool> allow users to edit datasources from the UI.
  editable: true
```

#### Prometheus Config

`./monitoring/prometheus.yml`

```yaml
---
global:
  evaluation_interval: 15s
  external_labels:
    monitor: codelab-monitor
  scrape_interval: 15s
rule_files: ~
scrape_configs:
  -
    job_name: prometheus
    scrape_interval: 5s
    static_configs:
      -
        targets:
          - "localhost:9090"
  -
    job_name: fnw
    scrape_interval: 5s
    static_configs:
      -
        targets:
          - "fnw-client:8080"

```

### Docker Compose File

```yaml
version: '3.6'

services:

  # Container needs to be able to communicate with Telegram server via port 443
  # Since the gateway is using port 443 we need to remap this port to something
  # unused (and not exposed to the outside world)
  #
  # This also implies that we need to be on an external facing network
  fnw-client:
    image: fnw-streaming-client:latest
    # Container needs to communicate with Telegram server via port 443
    ports:
      - '4040:443'
    expose:
      - 8080
    networks:
      - monitoring_network
      - default

  prometheus:
    image: quay.io/prometheus/prometheus:v2.0.0
    volumes:
     - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    command: "--config.file=/etc/prometheus/prometheus.yml --storage.tsdb.path=/prometheus"
    expose:
      - 9090
    depends_on:
      - fnw-client
    networks:
      - monitoring_network

  grafana:
    image: grafana/grafana:6.3.3
    depends_on:
      - prometheus
    ports:
      - '3000:3000'
    volumes:
      - ./monitoring/grafana/provisioning/:/etc/grafana/provisioning/
      - ./grafana/dashboards/:/var/lib/grafana/dashboards/
    environment:
      - GF_AUTH_BASIC_ENABLED=false
      - GF_AUTH_ANONYMOUS_ENABLED=true
      - GF_AUTH_ANONYMOUS_ORG_ROLE=Admin
    networks:
      - monitoring_network
      - default

networks:
  monitoring_network:
    internal: true

```

### Run Example

Run `docker-compose up` and navigate to `localhost:3000`. You'll need to set up
a Dashboard that uses the `Promteus` Datasource we specified.
