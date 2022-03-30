# coding=utf-8

__author__ = 'fg.luo'

import logging
import os


class LoggerDefine:
    def __init__(self, file=None, prop=False, level=logging.INFO):
        self.fmt = '[{{asctime}}]{{process}}-{{thread}}-{name}-{{levelname}}: {{message}}'.format(name=__name__)
        self.fn = logging.Formatter(self.fmt, style='{',  datefmt="%Y-%m-%d-%H:%M:%S")
        self.file = file
        self.prop = prop
        self._level = level
        logging.basicConfig(level=logging.INFO, format=self.fmt, style='{', datefmt="%Y-%m-%d-%H:%M:%S")

    @property
    def get_logger(self):
        """
        工厂方法获取日志对象
        """
        _logger = logging.getLogger(__name__)
        _logger.setLevel(logging.INFO)
        _logger.propagate = self.prop

        if not self.file:
            fmt = '[{asctime}]process:{process}-thread:{threadName}-function:{funcName}-{levelname}: {message}'
        else:
            fmt = '[{{asctime}}]process:{{process}}-{{threadName}}-{name}-function:{{funcName}}-{{levelname}}: ' \
                  '{{message}}'.format(name=os.path.basename(self.file))
        fn = logging.Formatter(fmt, style='{',  datefmt="%Y-%m-%d-%H:%M:%S")

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(fn)
        _logger.addHandler(ch)

        if self.file:
            self._set_logger_file(_logger, fn)
        return _logger

    def _set_logger_file(self, _logger, fn):
        logger_file = os.path.splitext(self.file)[0] + '.log'
        f = logging.FileHandler(filename=logger_file)
        f.setLevel(self._level)
        f.setFormatter(fn)
        _logger.addHandler(f)
