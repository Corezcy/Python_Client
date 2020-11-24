load("@rules_python//python:defs.bzl", "py_binary", "py_library")

# load("@pip//:requirements.bzl", "requirement")
load("@rules_pkg//:pkg.bzl", "pkg_tar")
load("@subpar//:subpar.bzl", "par_binary")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "logger",
    srcs = ["logger.py"],
    deps = [
        # requirement("absl-py")
    ],
)

py_library(
    name = "scenario_run",
    srcs = ["scenario_run.py"],
    deps = [
        "//lgsvl:agent",
        "//lgsvl:dreamview",
        "//lgsvl:geometry",
        "//lgsvl:simulator",
        # requirement("pyyaml"),
    ],
)

py_library(
    name = "choose_the_scene",
    srcs = ["choose_the_scene.py"],
    deps = [
        ":scenario_run",
        # requirement("pymongo"),
        # requirement("pyyaml"),
    ],
)

py_library(
    name = "check_report",
    srcs = ["check_report.py"],
    deps = [
    ],
)

py_library(
    name = "start_simulation",
    srcs = ["start_simulation.py"],
    deps = [
        "//lgsvl:agent",
        # requirement("absl-py"),
        # requirement("pynput"),
    ],
)

# py_binary(
#     name = "main",
#     srcs = [
#         "main.py",
#     ],
#     imports = [""],
#     main = "main.py",
#     deps = [
#         ":check_report",
#         ":choose_the_scene",
#         ":logger",
#         ":scenario_run",
#         ":start_simulation",
#         # requirement("absl-py"),
#     ],
# )

par_binary(
    name = "main",
    srcs = [
        "main.py",
    ],
    imports = [""],
    main = "main.py",
    deps = [
        ":check_report",
        ":choose_the_scene",
        ":logger",
        ":scenario_run",
        ":start_simulation",
        # requirement("absl-py"),
    ],
)

pkg_tar(
    name = "Python_Client",
    srcs = [
        ":main.par",
    ],
    mode = "0755",
)
