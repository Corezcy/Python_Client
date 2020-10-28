from absl import flags
from absl import app
from absl import logging as absl_logging
import logging

from choose_the_scene import chooseTheScene
from check_report import checkReport
from start_simulation import startSimulation
from logger import LoggerInstance
from scenario_run import SimConnection


log = LoggerInstance()


FLAGS = flags.FLAGS
flags.DEFINE_integer("t", None, "simulation time limit")


simconnection = SimConnection()


def main(args):

    # 终端是否显示log信息的关键.注释，不显示；不注释，显示。
    logging.root.removeHandler(absl_logging.get_absl_handler())

    print("\n*---------Welcome to Python Client!----------*")
    print("|                 --Menu--                   |")
    print("|              1.Choose the Scene            |")
    print("|              2.Start Simulation            |")
    print("|              3.Check Report                |")
    print("|              4.Exit                        |")
    print("*--------------------------------------------*\n")
    choice = input("Please enter your option :")
    print()
    # choice = FLAGS.option
    while choice != "4":

        # 选择场景
        if choice == "1":
            chooseTheScene(log, simconnection)

        # 开始仿真
        elif choice == "2":
            startSimulation(log, simconnection, FLAGS.t)

        # 查勘报告
        elif choice == "3":
            checkReport(log)

        else:
            log.warning("Invalid input !")

        print("\n*---------Welcome to Python Client!----------*")
        print("|                 --Menu--                   |")
        print("|              1.Choose the Scene            |")
        print("|              2.Start Simulation            |")
        print("|              3.Check Report                |")
        print("|              4.Exit                        |")
        print("*--------------------------------------------*\n")
        choice = input("Please enter your option :")
        print()

    print("bye\n")


if __name__ == '__main__':
    # app.run(main, argv=['program_name', '--option=1'])
    app.run(main)
