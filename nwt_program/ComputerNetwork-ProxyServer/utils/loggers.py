import logging
import os
import os.path as op


class LoggerV1(object):
    def __init__(self, name, add_file=True, add_console=False, level=logging.INFO):
        # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.Logger(name)
        self.logger.setLevel(level=level)
        if add_console:
            # add log console output
            console = logging.StreamHandler()
            console.setLevel(level=level)
            console.setFormatter(self.formatter)
            self.logger.addHandler(console)
        if add_file:
            # add log file
            handler = logging.FileHandler(op.join(op.abspath(op.dirname(__file__)), r"../log/{}.log".format(name)))
            handler.setLevel(level=level)
            handler.setFormatter(self.formatter)
            self.logger.addHandler(handler)

    def info(self, msg: str) -> None:
        """写入info日志"""
        self.logger.info(msg)

    def debug(self, msg: str) -> None:
        """写入debug日志"""
        self.logger.debug(msg)

    def warning(self, msg: str) -> None:
        """写入warning日志"""
        self.logger.warning(msg)

    def error(self, msg: str) -> None:
        """写入error日志"""
        self.logger.error(msg)


class Logger(object):
    def __init__(self, name, add_file=True, use_name_as_file=False, file_name="default", add_console=False,
                 level=logging.INFO):
        # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.Logger(name)
        self.logger.setLevel(level=level)
        if add_console:
            # add log console output
            console = logging.StreamHandler()
            console.setLevel(level=level)
            console.setFormatter(self.formatter)
            self.logger.addHandler(console)
        if add_file:
            # add log file
            if use_name_as_file:
                handler = logging.FileHandler(op.join(op.abspath(op.dirname(__file__)), r"../log/{}.log".format(name)))
            else:
                handler = logging.FileHandler(
                    op.join(op.abspath(op.dirname(__file__)), r"../log/{}.log".format(file_name)))
            handler.setLevel(level=level)
            handler.setFormatter(self.formatter)
            self.logger.addHandler(handler)

    def info(self, msg: str) -> None:
        """写入info日志"""
        self.logger.info(msg)

    def debug(self, msg: str) -> None:
        """写入debug日志"""
        self.logger.debug(msg)

    def warning(self, msg: str) -> None:
        """写入warning日志"""
        self.logger.warning(msg)

    def error(self, msg: str) -> None:
        """写入error日志"""
        self.logger.error(msg)


if __name__ == '__main__':
    logger1 = Logger("logger1")
    logger2 = Logger("logger2")

    logger1.info("logger1 info1")
    logger2.info("logger2 info2")
