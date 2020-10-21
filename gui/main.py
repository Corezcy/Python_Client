from absl import flags
from absl import app
from absl import logging as absl_logging
import logging

from choose_the_scene import chooseTheScene
from check_report import checkReport
from start_simulation import startSimulation
from logger import LoggerInstance
from scenario_run import SimConnection

# import choose_the_scene
# import check_report
# import start_simulation
# import logger
# import scenario_run

log = LoggerInstance()

FLAGS = flags.FLAGS
flags.DEFINE_string("int", None, "choice")

simconnection = SimConnection()


def main(args):

    logging.root.removeHandler(absl_logging.get_absl_handler())

    print("*---------Welcome to Python Client!----------*")
    print("|                 --Menu--                   |")
    print("|              1.Choose the Scene            |")
    print("|              2.Start Simulation            |")
    print("|              3.Check Report                |")
    print("|              4.Exit                        |")
    print("*--------------------------------------------*")
    # choice = input("Please give your choice :")
    choice = FLAGS.int
    while choice != "4":
        #选择场景
        if choice == "1":
            path = chooseTheScene(log)
            simconnection.address = path

        #开始仿真
        elif choice == "2":
            if simconnection.address != "":
                startSimulation(log,simconnection)
            else:
                print("Failed to choose the scene ... Please get back to step.1")
                log.error("Failed to choose the scene ... Please get back to step.1")

        #查勘报告
        elif choice == "3":
            checkReport(log)

        else:
            log.warning("Invalid input")

        #choice = input("Please give your choice :")

    print("bye")


if __name__ == '__main__':
    app.run(main,argv=['program_name', '--int=1'])
    # app.run(main)