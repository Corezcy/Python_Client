from absl import logging as absl_logging
import logging

class LoggerInstance():
    logger = None

    def __init__(self) :

        self.logger = absl_logging.get_absl_logger()
        self.logger.setLevel(absl_logging.FATAL)
        # 控制日志输出到文件

        file_handler_all = logging.FileHandler('./log/output.log')
        file_handler_all.setLevel(absl_logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - PyClient - %(name)s - %(levelname)s - %(message)s')

        file_handler_all.setFormatter(formatter)

        self.logger.addHandler(file_handler_all)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)