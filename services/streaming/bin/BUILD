package(default_visibility = ["//visibility:public"])
py_binary(
    name = "bootstrap_session",
    srcs = glob([
        "bootstrap_session.py",
    ]),
    srcs_version = "PY3",
    deps = [
        "@fnw_streaming_deps//telethon",
         "//services/streaming/config:config"
    ],
)

load("@io_bazel_rules_docker//python3:image.bzl", "py3_image")

py3_image(
    name = "train_sentiment_model",
    srcs = ["train_sentiment_model.py"],
    base = "//thirdparty/containers:cuda_10_1_image_base",
    main = "train_sentiment_model.py",
    visibility = ["//visibility:public"],
    deps = [
        "@fnw_streaming_deps//torch",
        "@fnw_streaming_deps//allennlp",
        "@fnw_streaming_deps//flair"
    ]
)

load("@io_bazel_rules_docker//container:container.bzl", "container_bundle")

container_bundle(
    name = "model_training",
    images = {
        "flair-model-training:latest": ":train_sentiment_model",
    },
)

load("@io_bazel_rules_docker//container:container.bzl", "container_push")

container_push(
    name = "push",
    format = "Docker",
    image = ":train_sentiment_model",
    registry = "index.docker.io",
    repository = "sashanullptr/flair-model-training",
    tag = "latest",
)