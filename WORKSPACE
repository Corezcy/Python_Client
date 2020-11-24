load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

http_archive(
    name = "rules_python",
    sha256 = "b6d46438523a3ec0f3cead544190ee13223a52f6a6765a29eae7b7cc24cc83a0",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.1.0/rules_python-0.1.0.tar.gz",
)

load("@rules_python//python:repositories.bzl", "py_repositories")

py_repositories()

http_archive(
    name = "rules_pkg",
    sha256 = "352c090cc3d3f9a6b4e676cf42a6047c16824959b438895a76c2989c6d7c246a",
    url = "https://github.com/bazelbuild/rules_pkg/releases/download/0.2.5/rules_pkg-0.2.5.tar.gz",
)

load("@rules_pkg//:deps.bzl", "rules_pkg_dependencies")

rules_pkg_dependencies()

git_repository(
    name = "subpar",
    remote = "https://github.com/google/subpar",
    tag = "2.0.0",
)

# load("@rules_python//python:pip.bzl", "pip_install")

# pip_install(
#     # (Optional) You can provide extra parameters to pip.
#     # Here, make pip output verbose (this is usable with `quiet = False`).
#     #extra_pip_args = ["-v"],

#     # (Optional) You can exclude custom elements in the data section of the generated BUILD files for pip packages.
#     # Exclude directories with spaces in their names in this example (avoids build errors if there are such directories).
#     #pip_data_exclude = ["**/* */**"],

#     # (Optional) You can provide a python_interpreter (path) or a python_interpreter_target (a Bazel target, that
#     # acts as an executable). The latter can be anything that could be used as Python interpreter. E.g.:
#     # 1. Python interpreter that you compile in the build file (as above in @python_interpreter).
#     # 2. Pre-compiled python interpreter included with http_archive
#     # 3. Wrapper script, like in the autodetecting python toolchain.
#     #python_interpreter_target = "@python_interpreter//:python_bin",

#     # (Optional) You can set quiet to False if you want to see pip output.
#     quiet = False,

#     # Uses the default repository name "pip"
#     requirements = "//:requirements.txt",
# )
