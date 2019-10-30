load("@io_bazel_rules_docker//container:container.bzl", "container_bundle")

container_bundle(
    name = "fnwclient_container",
    images = {
        "/fnwclient_streaming:latest": "//services/streaming:server",
    },
)
