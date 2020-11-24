load("@rules_python//python:defs.bzl", "py_library")
# load("@pip//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "geometry",
    srcs = ["geometry.py"],
    deps = [],
)

py_library(
    name = "remote",
    srcs = ["remote.py"],
    deps = [
        # requirement("websockets"),
        # requirement("asyncio"),
    ],
)

py_library(
    name = "utils",
    srcs = ["utils.py"],
    deps = [
        ":geometry",
    ],
)

py_library(
    name = "controllable",
    srcs = ["controllable.py"],
    deps = [
        ":geometry",
        ":utils",
    ],
)

py_library(
    name = "sensor",
    srcs = ["sensor.py"],
    deps = [
        ":geometry",
        ":utils",
    ],
)

py_library(
    name = "agent",
    srcs = ["agent.py"],
    deps = [
        ":geometry",
        ":sensor",
        ":utils",
    ],
)

py_library(
    name = "simulator",
    srcs = ["simulator.py"],
    deps = [
        ":agent",
        ":controllable",
        ":geometry",
        ":remote",
        ":sensor",
        ":utils",
    ],
)

py_library(
    name = "dreamview",
    srcs = ["dreamview.py"],
    deps = [
        ":simulator",
        # requirement("websocket")
    ],
)
