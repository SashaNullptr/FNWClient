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

