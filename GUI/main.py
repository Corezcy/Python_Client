from gui.logger import LoggerInstance
from absl import flags
from absl import app
import logging
from absl import logging as absl_logging

log = LoggerInstance()

FLAGS = flags.FLAGS
flags.DEFINE_string("name", None, "Your name.")
flags.mark_flag_as_required("name")

def chooseTheScene():
    pass


def startSimulation():
    pass


def checkReport():
    pass


def main(args):
    print(FLAGS.name)

    logging.root.removeHandler(absl_logging.get_absl_handler())

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
            '''
            选择场景
            '''
            log.info("Please choose the scene")
            chooseTheScene()
            log.info("The scene is choosed")
        elif choice == "2":
            '''
            开始仿真
            '''
            log.info("Simulation is starting")
            startSimulation()
            log.info("Simulation is finished")
        elif choice == "3":
            '''
            查看报告
            '''
            log.info("Please check the report")
            checkReport()
        else:
            log.warning("Invalid input")
        choice = input("Please give your choice :")

    print("bye")


if __name__ == '__main__':
    app.run(main)
