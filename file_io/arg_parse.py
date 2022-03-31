#!/usr/bin/env python3
# coding=utf-8
"""
@author: feng.luo
@time: 2022/3/30
@File: arg_parse.py

需求：
使用python实现shell的ls命令功能：-l、 -a和--all、 -h选项
# ls [path] [-l] [-h] [-a]
要求：
    1、实现显示路径下的文件列表
    2、-a、--all显示包含.开头的文件
    3、-l显示详细列表,例如：
           mode   硬链接    属主 属组 字节         时间             文件名
        -rw-rw-r--  1    root:root   5   2022-03-30 20：00:07 test.py
    4、-h和-l配合，任性化显示文件大小，例如：1k、1G等
    5、按文件名排序输出，时间按“年-月-日 时：分：秒”格式显示


argparse模块：
    一个可执行文件或脚本都可以接收参数，例如：ls -l /etc
        /etc 是位置参数
        -l   是短选项
    argparse模块就可以构造解析器，定义参数，并解析传入模块的参数；还可以自动生成帮助信息。
    尤其是usage，可以看到现在定义的参数是否是自己想要的。

    1、参数分类：
        位置参数：参数本身就对应一个参数位置
        选项参数：分短选项-和长选项--，然后后面的才算它的参数，短选项后面也可以没有参数
    2、解析器参数 parse=argparse.ArgumentParser()：
        prog:程序的名称，缺省使用sys.args[0]
        add_help:自动为解析器增加-h和--help选项，默认为True
        description：为程序功能添加描述
    3、增加参数parse.add_argument():
        解决位置参数：
            parse.add_argument('path', nargs='?', default='.', help='path help')
            nargs:给位置参数path传入多少个参数值，？表示可有可无；也可明确多少个参数值，填数字
            default：参数缺省值, '.' 表示当前路径
        解决选项参数：
            parse.add_argument('-l', action='store_true', help='-l help')
            action: 给选项参数-l指定一个默认的存储值；当调用脚本传入参数中有此选项-l时，命名空间保存True，否则保存False
                    action还可设置为const等

    4、参数解析：args = parse.parse_args('/etc'):
        返回一个命名空间Namespace，可通过Namespace对象访问




"""
import argparse
import pathlib
import datetime
import stat

from tool.logger_define import LoggerDefine


logger = LoggerDefine(__name__).get_logger


def _parse_args(params):
    parse = argparse.ArgumentParser(prog='ls', add_help=False, description='list all files')  # 获得参数解析器
    parse.add_argument('path', nargs='?', default='.', help='path help')  # 增加位置参数
    parse.add_argument('-l', action='store_true')
    parse.add_argument('-a', action='store_true')
    parse.add_argument('-h', action='store_true')
    _args = parse.parse_args(params)  # 解析参数,返回命名空间Namespace对象，可通过Namespace访问，例如Namespace.path
    print(_args)
    parse.print_help()  # 打印帮助
    print(_args.path, _args.h)  # 访问命名空间的值
    return _args


def show_dir(path, al=False, detail=False, human=False):
    p = pathlib.Path(path)
    for file in p.iterdir():
        if not al and str(file.name).startswith('.'):
            # 解决all
            continue
        if detail:
            # 解决-l
            # todo yield xxx
            stat_info = file.stat()
            # -rw-rw-r--  1    root:root   5   2022-03-30 20：00:07 test.py
            t = datetime.datetime.fromtimestamp(stat_info.st_atime).strftime('%Y-%m-%d %H:%M:%S')
            file.owner(), file.group()  # windows不支持，因为没有grp和pwd
            yield _improve_get_mode(stat_info), stat_info.st_nlink, stat_info.st_uid, stat_info.st_gid, stat_info.st_size, t, file.name
        else:
            yield file.name


def _get_mode(path: pathlib.Path):
    """
    mode
    drw-rw-r--
    """
    res_mode = ''
    if path.is_char_device():
        file_type = 'c'
    elif path.is_dir():
        file_type = 'd'
    elif path.is_symlink():
        file_type = 'l'
    elif path.is_block_device():
        file_type = 'b'
    elif path.is_socket():
        file_type = 's'
    elif path.is_fifo():
        file_type = 'p'
    else:
        file_type = '-'
    res_mode += file_type
    mode_lst = ['r', 'w', 'x', 'r', 'w', 'x', 'r', 'w', 'x']
    mode = bin(path.stat().st_mode)[-9:]
    for i, x in enumerate(mode):
        if x == '1':
            res_mode += mode_lst[i]
        else:
            res_mode += '-'
    return res_mode


def _improve_get_mode(st: stat):
    """
    使用stat库
    """
    return stat.filemode(st.st_mode)


class LSSolution:
    def __init__(self):
        self.args = self._args_parser()

    @staticmethod
    def _args_parser():
        parser = argparse.ArgumentParser(
            prog='ls',
            add_help=False,
            description='List the file information in the dictionary')  # 获得一个参数解析器
        parser.add_argument('path', help='The path')  # 添加位置参数
        parser.add_argument('-a', '--all', default=False, dest='a', help='List all files, including .')  # 添加关键字参数
        parser.add_argument('-l', help='List the details info of files')
        parser.add_argument('-h', help='A more readable list of files')
        args = parser.parse_args([__file__.split()])  # 解析参数
        # parser.print_help()
        logger.info('args:{}'.format(args.path))
        return args

    def procedure(self):
        path = self.args.path[0]
        if not self.args.a:
            ig_files = self._ignore_file(pathlib.Path(path).parent)
        else:
            ig_files = set()
        file_info_lst = list()
        for p in pathlib.Path(path).parent.iterdir():
            f = p.name
            if f in ig_files:
                continue
            if self.args.l:
                stat_obj = p.stat()
                cur_mode = self._get_mode(p)
                n_link = str(stat_obj.st_nlink)
                u, g = str(stat_obj.st_uid), str(stat_obj.st_gid)
                s = stat_obj.st_size
                if self.args.h:
                    s = self._get_size(s)
                t = datetime.datetime.fromtimestamp(stat_obj.st_ctime).replace(microsecond=0)
                f = ' '.join([cur_mode, n_link, u, g, s, t, f])
            file_info_lst.append(f)
        res = sorted(file_info_lst, key=lambda x: x.split()[-1])
        # logger.info('res:\n{}'.format('\n'.join(res)))
        logger.info('finally:{}'.format(res))
        return res

    @staticmethod
    def _ignore_file(path: pathlib.Path):
        ig_file = set()
        for f in path.iterdir():
            s_file = str(f)
            if s_file.startswith('.'):
                ig_file.add(s_file)
        logger.info('ignore file:{}'.format(ig_file))
        return ig_file

    def _get_size(self, size, res=None, idx=0, suffix='KMGTP'):
        if res is None:
            res = '{:.2f}{}'.format(size, suffix[idx])
        if size > 1024:
            idx += 1
            size = size / 1024
            res = '{:.2f}{}'.format(size, suffix[idx])
            return self._get_size(size, res, idx)
        return res

    @staticmethod
    def _get_mode(path: pathlib.Path):
        """
        mode
        drw-rw-r--
        """
        res_mode = ''
        if path.is_char_device():
            file_type = 'c'
        elif path.is_dir():
            file_type = 'd'
        elif path.is_symlink():
            file_type = 'l'
        elif path.is_block_device():
            file_type = 'b'
        elif path.is_socket():
            file_type = 's'
        elif path.is_fifo():
            file_type = 'p'
        else:
            file_type = '-'
        res_mode += file_type

        mode = oct(path.stat().st_mode)[-3:]
        for x in mode:
            if x == '7':
                res_mode += 'rwx'
            elif x == '6':
                res_mode += 'rw-'
            elif x == '5':
                res_mode += 'r-x'
            elif x == '4':
                res_mode += 'r--'
            elif x == '3':
                res_mode += '-wx'
            elif x == '2':
                res_mode += '-w-'
            elif x == '1':
                res_mode += '--x'
            else:
                res_mode += '---'
        return res_mode


if __name__ == '__main__':
    # result = LSSolution().procedure()
    # time.sleep(0.2)
    # for file in result:
    #     print(file)
    args = _parse_args(['.', '-l'])
    print('***' * 10)
    for f in show_dir(args.path, args.a, args.l, args.h):
        print(f)
