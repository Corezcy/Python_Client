from absl import logging as absl_logging

class LoggerInstance:
    logger = None

    def __init__(self) -> None:

        self.logger = absl_logging.get_absl_logger()
        self.logger.setLevel(absl_logging.DEBUG)

        # 控制日志输出到控制台
        logging_stream_handler = absl_logging.get_absl_handler()
        logging_stream_handler.setLevel(absl_logging.DEBUG)


        # 控制日志输出到文件
        file_handler_all = absl_logging.get_absl_handler()
        file_handler_all.use_absl_log_file('loghaha.log')
        file_handler_all.setLevel(absl_logging.DEBUG)

        logging_stream_handler.setFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler_all.setFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.logger.addHandler(logging_stream_handler)
        self.logger.addHandler(file_handler_all)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)
