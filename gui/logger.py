from absl import logging as absl_logging
import logging
import os


class LoggerInstance():
    logger = None

    def __init__(self):
        report_path = "./log/"  # 文件保存路径，如果不存在就会被重建
        if not os.path.exists(report_path):  # 如果路径不存在
            os.makedirs(report_path)
        filename = "./log/output.log"  # 文件保存路径，如果不存在就会被重建

        if not os.path.exists(filename):
            os.system(r"touch {}".format(filename))  # 调用系统命令行来创建文件

        self.logger = absl_logging.get_absl_logger()
        self.logger.setLevel(absl_logging.FATAL)
        # 控制日志输出到文件

        # logging_stream_handler = logging.StreamHandler()
        # formatter = logging.Formatter('%(asctime)s - %(message)s')
        # logging_stream_handler.setFormatter(formatter)
        # self.logger.addHandler(logging_stream_handler)

        '''
        bazel和python运行路径的区别:
        bazel以workspace文件为根目录
        python以main文件所在的文件夹为根目录
        '''
        # bazel目录
        file_handler_all = logging.FileHandler('./log/output.log')
        # python run目录
        # file_handler_all = logging.FileHandler('./log/output.log')

        file_handler_all.setLevel(absl_logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s - PyClient - %(name)s - %(levelname)s - %(message)s')

        file_handler_all.setFormatter(formatter)

        self.logger.addHandler(file_handler_all)

        logging.root.removeHandler(absl_logging.get_absl_handler())

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)
