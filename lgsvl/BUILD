package(default_visibility = ["//visibility:public"])

py_library(
  name = "geometry",
  deps = [],
  srcs = ["geometry.py"],
)

py_library(
  name = "remote",
  deps = [],
  srcs = ["remote.py"],
)

py_library(
  name = "utils",
  deps = [":geometry"],
  srcs = ["utils.py"],
)


py_library(
  name = "controllable",
  deps = [":geometry",
          ":utils"],
  srcs = ["controllable.py"],
)

py_library(
  name = "sensor",
  deps = [":geometry",
          ":utils"],
  srcs = ["sensor.py"],
)

py_library(
  name = "agent",
  deps = [":geometry",
          ":utils",
          ":sensor"],
  srcs = ["agent.py"],
)

py_library(
  name = "simulator",
  deps = [":geometry",
          ":utils",
          ":sensor",
          ":remote",
          ":agent",
          ":controllable"],
  srcs = ["simulator.py"],
)

