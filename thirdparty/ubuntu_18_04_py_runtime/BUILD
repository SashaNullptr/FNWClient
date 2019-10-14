package(default_visibility = ["//visibility:public"])

load("@rules_python//python:defs.bzl", "py_runtime_pair")

py_runtime(
    name = "ubuntu_18_04_py2_runtime",
    interpreter_path = "/usr/bin/python2",
    python_version = "PY2",
)

py_runtime(
    name = "ubuntu_18_04_py3_runtime",
    interpreter_path = "/usr/bin/python3",
    python_version = "PY3",
)

py_runtime_pair(
    name = "ubuntu_18_04_py_runtime_pair",
    py2_runtime = ":ubuntu_18_04_py2_runtime",
    py3_runtime = ":ubuntu_18_04_py3_runtime",
)

toolchain(
    name = "ubuntu_18_04_toolchain",
    toolchain = ":ubuntu_18_04_py_runtime_pair",
    toolchain_type = "@rules_python//python:toolchain_type",
)
