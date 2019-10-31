package(default_visibility = ["//visibility:public"])

py_library(
    name = "streaming_config",
    srcs = glob([
        "config/*.py",
    ]),
    srcs_version = "PY3",
)

py_library(
    name = "streaming",
    srcs = glob([
        "backend/*.py",
        "lib/*.py",
    ]),
    srcs_version = "PY3",
    deps = [
        "streaming_config",
        "@fnw_streaming_deps//flask",
        "@fnw_streaming_deps//flask_cors",
        "@fnw_streaming_deps//injector",
        "@fnw_streaming_deps//prometheus_client",
        "@fnw_streaming_deps//python_dateutil",
        "@fnw_streaming_deps//telethon",
        "@fnw_streaming_deps//textblob",
        "@fnw_streaming_deps//waitress",
    ],
)

load("@io_bazel_rules_docker//python3:image.bzl", "py3_image")

py3_image(
    name = "server",
    srcs = ["server.py"],
    base = "//thirdparty/containers:python_3_7_image_base",
    main = "server.py",
    visibility = ["//visibility:public"],
    deps = [":streaming"],
)

filegroup(
    name = "srcs",
    srcs = ["BUILD"] + glob(["**/*.py"]),
)

load("@io_bazel_rules_docker//container:container.bzl", "container_push")

container_push(
    name = "push",
    format = "Docker",
    image = ":server",
    registry = "index.docker.io",
    repository = "sashanullptr/fnw_client",
    tag = "latest",
)
