load("@rules_python//python:defs.bzl", "py_library")
load("@pip//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "dreamview",
    srcs = ["dreamview.py"],
    deps = [requirement("websocket")],
)
