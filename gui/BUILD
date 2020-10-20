py_library(
  name = "logger",
  deps = [],
  srcs = ["logger.py"],
)

py_library(
  name = "scenario_run",
  deps = [],
  srcs = ["scenario_run.py"],
)

py_library(
  name = "choose_the_scene",
  deps = [":scenario_run"],
  srcs = ["choose_the_scene.py"],
)

py_binary(
  name = "main",
  deps = [":logger",":choose_the_scene"],
  srcs = ["main.py"],
)
