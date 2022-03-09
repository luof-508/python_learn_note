# coding=utf-8

__author__ = 'fg.luo'

import logging


class LoggerDefine:
    def __init__(self, file_name='name'):
        self.fn = logging.Formatter(
            '[{{asctime}}]{name}-{{levelname}}: {{message}}'.format(name=file_name), style='{'
        )

    def logger_define(self, file='', _level=logging.INFO):
        """

        :param file: 日志文件
        :param _level: 日志文件级别
        :return:
        """
        _logger = logging.getLogger(__name__)
        _logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()

        ch.setLevel(logging.INFO)
        ch.setFormatter(self.fn)
        _logger.addHandler(ch)
        if file:
            self._set_logger_file(_logger, file, _level)
        return _logger

    def _set_logger_file(self, _logger, file, _level=logging.INFO):
        f = logging.FileHandler(filename=file)
        f.setLevel(_level)
        f.setFormatter(self.fn)
        _logger.addHandler(f)
