package(default_visibility = ["//visibility:public"])

py_binary(
    name = "train_sentiment_model",
    srcs = glob([
        "train_sentiment_model.py",
    ]),
    srcs_version = "PY3",
    deps = [
        "@fnw_streaming_deps//flair"
    ],
)

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
    base = "//thirdparty/containers:python_3_6_image_base",
    main = "train_sentiment_model.py",
    visibility = ["//visibility:public"],
    deps = [
        "@fnw_streaming_deps//torch",
        "@fnw_streaming_deps//flair"
    ],
)