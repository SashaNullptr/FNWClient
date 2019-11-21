package(default_visibility = ["//visibility:public"])

load("@io_bazel_rules_docker//container:container.bzl", "container_image")

container_image(
    name = "python_3_6_image_base",
    base = "@dockerhub_python_3_6_image_base//image",
    symlinks = {
        "/usr/bin/python": "/usr/local/bin/python",
        "/usr/bin/python3": "/usr/local/bin/python",
    },
)

container_image(
    name = "python_3_7_image_base",
    base = "@dockerhub_python_3_7_image_base//image",
    symlinks = {
        "/usr/bin/python": "/usr/local/bin/python",
        "/usr/bin/python3": "/usr/local/bin/python",
    },
)

container_image(
    name = "cuda_10_1_image_base",
    base = "@model_training_base//image:dockerfile_image.tar",
    symlinks = {
        "/usr/bin/python": "/usr/bin/python3",
    },
    env = {
        "NVIDIA_VISIBLE_DEVICES":"all",
    }
)


container_image(
    name = "streaming_analytics_base",
    base = "cuda_10_1_image_base",
)

filegroup(
    name = "srcs",
    srcs = ["BUILD"]
)
