load("@rules_python//python:defs.bzl", "py_binary")
load("@rules_python//python:defs.bzl", "py_library")
load("@pip//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "logger",
    srcs = ["logger.py"],
    deps = [requirement("absl-py")],
)

py_library(
    name = "scenario_run",
    srcs = ["scenario_run.py"],
    deps = [
        "//lgsvl:simulator",
        requirement("pyyaml"),
    ],
)

py_library(
    name = "choose_the_scene",
    srcs = ["choose_the_scene.py"],
    deps = [
        ":scenario_run",
        requirement("pymongo"),
        requirement("pyyaml"),
    ],
)

py_binary(
    name = "main",
    srcs = ["main.py"],
    deps = [
        ":choose_the_scene",
        ":logger",
        requirement("absl-py"),
    ],
)
