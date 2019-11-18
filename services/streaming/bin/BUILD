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