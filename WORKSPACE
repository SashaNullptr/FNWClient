workspace(name = "fnwclient")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "io_bazel_rules_docker",
    sha256 = "9ff889216e28c918811b77999257d4ac001c26c1f7c7fb17a79bc28abf74182e",
    strip_prefix = "rules_docker-0.10.1",
    urls = ["https://github.com/bazelbuild/rules_docker/releases/download/v0.10.1/rules_docker-v0.10.1.tar.gz"],
)

load(
    "@io_bazel_rules_docker//repositories:repositories.bzl",
    container_repositories = "repositories",
)
container_repositories()

load("@io_bazel_rules_docker//repositories:deps.bzl", container_deps = "deps")
container_deps()

load("@io_bazel_rules_docker//container:container.bzl","container_pull")

container_pull(
  name = "python_3_5_image",
  registry = "gcr.io",
  repository = "distroless/python3",
  digest = "sha256:9efd7c54d622c1b53a151456527749dd67dbe18ac8d69ac91639509c479abe12", # built on /9/6/2019
)

load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

git_repository(
    name = "com_apt_itude_rules_pip",
    commit = "e5ed5e72bf5a7521244e1d2119821628bbf17263",
    remote = "https://github.com/apt-itude/rules_pip.git",
)

load("@com_apt_itude_rules_pip//rules:dependencies.bzl", "pip_rules_dependencies")

pip_rules_dependencies()

load("@com_apt_itude_rules_pip//rules:repository.bzl", "pip_repository")

pip_repository(
    name = "fnwclient_deps",
    python_interpreter = "python3",
    requirements = "//thirdparty/dependencies:requirements.txt",
)

register_toolchains("//bazel/ubuntu_18_04_py_runtime:ubuntu_18_04_toolchain")
