# absl库下面的四个模块
from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_string("name", None, "Your name.")


# Required flag.
flags.mark_flag_as_required("name")


def main(argv):
    del argv  # Unused.
    print('Hello, %s!' % FLAGS.name)


if __name__ == '__main__':
    app.run(main)
