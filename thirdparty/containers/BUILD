package(default_visibility = ["//visibility:public"])

load("@io_bazel_rules_docker//container:container.bzl", "container_image")

container_image(
    name = "python_3_7_image_base",
    base = "@dockerhub_python_3_7_image_base//image",
    symlinks = {
        "/usr/bin/python": "/usr/local/bin/python",
        "/usr/bin/python3": "/usr/local/bin/python",
    },
)

filegroup(
    name = "srcs",
    srcs = ["BUILD"],
)