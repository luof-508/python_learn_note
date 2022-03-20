# coding=utf-8

__author__ = 'fg.luo'

import logging
import os


class LoggerDefine:
    def __init__(self):
        self.fmt = '[{{asctime}}]{{process}}-{{thread}}-{name}-{{levelname}}: {{message}}'.format(name=__name__)
        self.fn = logging.Formatter(self.fmt, style='{',  datefmt="%Y-%m-%d-%H:%M:%S")
        logging.basicConfig(level=logging.INFO, format=self.fmt, style='{', datefmt="%Y-%m-%d-%H:%M:%S")

    def get_logger(self, file=None, _level=logging.INFO, prop=False):
        """

        :param file: 日志文件
        :param _level: 日志文件级别
        :param prop: 是否向父log传递
        :return:
        """
        _logger = logging.getLogger(__name__)
        _logger.setLevel(logging.INFO)
        _logger.propagate = prop

        if not file:
            fmt = '[{asctime}]process:{process}-thread:{threadName}-function:{funcName}-{levelname}: {message}'
        else:
            fmt = '[{{asctime}}]{{process}}-{{threadName}}-{name}-function:{{funcName}}-{{levelname}}: {{message}}'.format(
                name=os.path.basename(file)
            )
        fn = logging.Formatter(fmt, style='{',  datefmt="%Y-%m-%d-%H:%M:%S")

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(fn)
        _logger.addHandler(ch)

        if file:
            self._set_logger_file(_logger, file, fn, _level)
        return _logger

    @staticmethod
    def _set_logger_file(_logger, file, fn, _level=logging.INFO):
        logger_file = os.path.splitext(file)[0] + '.log'
        f = logging.FileHandler(filename=logger_file)
        f.setLevel(_level)
        f.setFormatter(fn)
        _logger.addHandler(f)
