from absl import flags
from absl import app
import logging
from absl import logging as absl_logging

from gui.choose_the_scene import chooseTheScene
from gui.check_report import checkReport
from gui.start_simulation import startSimulation
from gui.logger import LoggerInstance


log = LoggerInstance()

FLAGS = flags.FLAGS
flags.DEFINE_string("name", None, "Your name.")


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
            chooseTheScene(log)
        elif choice == "2":
            '''
            开始仿真(加入暂停功能)
            '''
            log.info("Simulation is starting")
            startSimulation(log)
            log.info("Simulation is finished")
        elif choice == "3":
            '''
            查看报告
            '''
            log.info("Please check the report")
            checkReport(log)
        else:
            log.warning("Invalid input")
        choice = input("Please give your choice :")

    print("bye")


if __name__ == '__main__':
    # app.run(main,argv=['program_name', '--name=tom'])
    app.run(main)