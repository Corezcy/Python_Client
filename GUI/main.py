from gui.logger import LoggerInstance
from absl import flags
from absl import app

# FLAGS = flags.FLAGS
# flags.DEFINE_string("name", None, "Your name.")
# flags.DEFINE_integer("num_times", 1,
#                      "Number of times to print greeting.")

def main(log):
    # print(FLAGS.name)
    print("*---------Welcome to Python Client!----------*")
    print("|                 --Menu--                   |")
    print("|              1.Choose the Scene            |")
    print("|              2.Start Simulation            |")
    print("|              3.Check Report                |")
    print("|              4.Exit                        |")
    print("*--------------------------------------------*")
    choice = input("Please give your choice :")
    while choice != "4":
        if choice == "1":
            log.info("1")
        elif choice == "2":
            log.info("2")
        elif choice == "3":
            log.info("3")
        else:
            pass
        choice = input("Please give your choice :")
    print("bye")



if __name__ == '__main__':
    log = LoggerInstance()
    app.run(main(log))

