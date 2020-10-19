from gui.logger import LoggerInstance
from absl import flags
from absl import app

FLAGS = flags.FLAGS
flags.DEFINE_string("name", None, "Your name.")
flags.DEFINE_integer("num_times", 1,
                     "Number of times to print greeting.")
flags.mark_flag_as_required("name")

def main(args):
    print(FLAGS.name)
    del args
    log = LoggerInstance()
    print(" ---------Welcome to Python Client!----------")
    print("|                 --Menu--                   |")
    print("|              1.Choose the Scene            |")
    print("|              2.Start Simulation            |")
    print("|              3.Check Report                |")
    print("|              4.Exit                        |")
    print(" --------------------------------------------")
    choice = input("Please give your choice :")
    while choice != "4":
        if choice == "1":
            log.info("1")
            break
        elif choice == "2":
            pass
            log.info("2")
            break
        elif choice == "3":
            pass
            log.info("3")
            break
        else:
            break
    print("bye")


if __name__ == '__main__':
    app.run(main)


