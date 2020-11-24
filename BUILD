package(default_visibility = ["//visibility:public"])

load("@rules_pkg//:pkg.bzl", "pkg_tar")

pkg_tar(
    name = "Python_Client_v0.0.1",
    srcs = [
        "config.yaml",
        "setup.py",
    ],
    extension = "tar.gz",
    deps = [
        "//gui:Python_Client",
    ],
)
