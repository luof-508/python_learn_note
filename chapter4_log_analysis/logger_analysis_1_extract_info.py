#!/usr/bin/env python3
# coding=utf-8
"""
@author: feng.luo
@time: 2022/4/5
@File: logger_analysis_1_extract_info.py
"""
import datetime
import re

from tool.logger_define import LoggerDefine


logger = LoggerDefine(__name__).get_logger

_log_test_strs = '123.125.71.36 - - [06/Apr/2017:18:09:25 +0800] "GET /o2o/media.html?menu=3 HTTP/1.1" 200 8642 "-" ' \
                 '"Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"'


class LoggerAnalysisDemo:
    def __init__(self, log_path: str):
        self.log_path = log_path
        self.extract_fields = None

    def extract_info_by_split(self):
        """按空格分割提取信息

        time： [06/Apr/2017:18:09:25 +0800]
        request： "GET / HTTP/1.1"
        需处理time和request被分割的问题,以及其他双引号中内容被分割的问题
        """
        fields = []
        tmp_info = ''
        catch_flag, time_flag, quote_flag = False, False, False
        for field in self.log_path.split():
            if not catch_flag and field.startswith("["):
                catch_flag, time_flag = True, True
                if field.endswith("]"):
                    fields.append(field.strip("[]"))
                    catch_flag, time_flag = False, False
                else:
                    tmp_info += field.strip('[') + " "
                continue
            elif catch_flag and time_flag:
                if field.endswith("]"):
                    fields.append(tmp_info + field.strip("]"))
                    tmp_info = ''
                    catch_flag, time_flag = False, False
                else:
                    tmp_info += field + " "
                continue
            if not catch_flag and field.startswith('"'):
                catch_flag, quote_flag = True, True
                if field.endswith('"'):
                    fields.append(field.strip('"'))
                    catch_flag, quote_flag = False, False
                else:
                    tmp_info += field.strip('"') + " "
                continue
            elif catch_flag and quote_flag:
                if field.endswith('"'):
                    fields.append(tmp_info + field.strip('"'))
                    tmp_info = ''
                    catch_flag, quote_flag = False, False
                else:
                    tmp_info += field + " "
                continue
            fields.append(field)
        self.extract_fields = fields

    def convert_fields(self):
        """转换time、request、status、size类型
        """
        con_res = dict()
        names = ['remote', None, None, 'datatime', 'request',
                 'status', 'size', None, 'useragent']
        ops_lst = [None, None, None, self._convert_time, self._convert_request,
                   int, int, None, None]
        for idx, ops in enumerate(ops_lst):
            name = names[idx]
            if name:
                if ops:
                    con_res[name] = ops(self.extract_fields[idx])
                else:
                    con_res[name] = self.extract_fields[idx]
        return con_res

    @staticmethod
    def _convert_time(time_str: str):
        return datetime.datetime.strptime(time_str, "%d/%b/%Y:%H:%M:%S %z")

    @staticmethod
    def _convert_request(request_str: str):
        return dict(zip(('method', 'url', 'protocol'), request_str.split()))


class RegularExtract:
    """
    数据提取
    """
    def __init__(self):
        self.pattern = r'(?P<remote>[\d.]{7,}) - - \[(?P<datetime>[^\[\]]+)\] "(?P<request>[^"]+)" ' \
              r'(?P<status>\d+) (?P<size>\d+) "-" "(?P<useragent>[^"]+)"'
        self.regex = re.compile(self.pattern)
        self.ops = {
            'datetime': lambda time_str: datetime.datetime.strptime(time_str, "%d/%b/%Y:%H:%M:%S %z"),
            'request': lambda request_str: dict(zip(('method', 'url', 'protocol'), request_str.split())),
            'status': int,
            'size': int
        }

    def extract_info_by_regular_expression(self, line: str) -> dict:
        """考虑异常处理，当没匹配到的时候return None
        """
        re_obj = self.regex.match(line)
        if re_obj:
            return dict((k, self.ops.get(k, lambda x: x)(v)) for k, v in re_obj.groupdict().items())

    def extract_file(self, path: str):
        res_lst = []
        with open(path, encoding='utf8') as f:
            for line in f:
                res_lst.append(self.extract_info_by_regular_expression(line))
        return res_lst


if __name__ == '__main__':
    demo_obj = LoggerAnalysisDemo(_log_test_strs)
    demo_obj.extract_info_by_split()
    convert_res = demo_obj.convert_fields()
    logger.info('convert result by split  :{}'.format(convert_res))
    regular_demo = RegularExtract()
    con_regular_res = regular_demo.extract_info_by_regular_expression(_log_test_strs)
    logger.info('Convert result by regular:{}'.format(con_regular_res))
