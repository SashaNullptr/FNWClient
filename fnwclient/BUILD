package(default_visibility = ["//visibility:public"])

py_library(
    name = "fnwclient",
    srcs = glob([
        "fnwclient/*.py",
        "fnwclient/**/*.py",
    ]),
    srcs_version = "PY3",
    deps = [
      "@fnwclient_deps//numpy",
      "@fnwclient_deps//scipy",
      "@fnwclient_deps//pandas",
      "@fnwclient_deps//textblob",
      "@fnwclient_deps//injector",
      "@fnwclient_deps//telethon",
      "@fnwclient_deps//flask",
      "@fnwclient_deps//flask_cors",
      "@fnwclient_deps//waitress",
      "@fnwclient_deps//prometheus_client",
    ],
)

load("@io_bazel_rules_docker//python3:image.bzl", "py3_image")

py3_image(
    name = "server",
    srcs = ["server.py"],
    base = "python_3_5_image",
    main = "server.py",
    visibility = ["//visibility:public"],
    python_version = "PY3",
    deps = [":fnwclient"],
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
   registry = "fopshub.net",
   repository = "/fnw_client",
   tag = "latest",
)
