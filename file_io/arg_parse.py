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
import platform
import stat

from tool.logger_define import LoggerDefine


logger = LoggerDefine(__name__).get_logger


def parse_args():
    parse = argparse.ArgumentParser(prog='ls', add_help=False, description='list all files')  # 获得参数解析器
    # parse.add_argument('path', nargs='?', default='.', help='path help')  # 增加位置参数, ？表示可有可无，0或1
    parse.add_argument('path', nargs='*', default='.', help='path help')  # *表示0个或多个位置参数；+代表至少1个
    parse.add_argument('-l', action='store_true')
    parse.add_argument('-a', action='store_true')
    parse.add_argument('-h', action='store_true')
    _args = parse.parse_args()  # 解析参数,返回命名空间Namespace对象，可通过Namespace访问，例如Namespace.path
    print(_args)
    parse.print_help()  # 打印帮助
    print(_args.path, _args.h)  # 访问命名空间的值
    return _args


class LSSolution:
    def ls_dir(self, path, al=False, detail=False, human=False):
        yield from sorted(self._show_dir(path, al, detail, human), key=lambda x: x[-1])

    def _show_dir(self, path, al=False, detail=False, human=False):
        cur_p = pathlib.Path(path)
        for file in cur_p.iterdir():
            if not al and str(file.name).startswith('.'):  # 解决all
                continue
            if detail:  # 解决-l
                # todo -rw-rw-r--  1    root:root   5   2022-03-30 20：00:07 test.py
                st = file.stat()
                m = self._get_type(file) + self._get_mode_by_bit(st)
                # stat.filemode(st.st_mode)  # 使用stat库获取文件mode
                uid, gid = self._get_uid_gid(file)
                t = datetime.datetime.fromtimestamp(st.st_atime).strftime('%Y-%m-%d %H:%M:%S')
                sz = self._get_size(st.st_size) if human else str(st.st_size)
                yield m, str(st.st_nlink), str(uid), str(gid), sz, t, file.name
            else:
                yield file.name

    @staticmethod
    def _get_mode(path: pathlib.Path):
        """
        mode
        drw-rw-r--
        """
        mode_lst = ['r', 'w', 'x', 'r', 'w', 'x', 'r', 'w', 'x']
        mode = bin(path.stat().st_mode)[-9:]
        res_mode = ''
        for i, x in enumerate(mode):
            if x == '1':
                res_mode += mode_lst[i]
            else:
                res_mode += '-'
        return res_mode

    @staticmethod
    def _get_mode_by_bit(st: stat):
        """
        位运算获取文件权限
        :param st:
        :return:
        """
        st_m = st.st_mode & 0o777
        mode_lst = ['r', 'w', 'x', 'r', 'w', 'x', 'r', 'w', 'x']
        re_md = ''
        for x in range(8, -1, -1):
            if st_m > x & 1:
                re_md += mode_lst[8-x]
            else:
                re_md += '-'
        return re_md

    @staticmethod
    def _get_type(path: pathlib.Path):
        """
        mode
        drw-rw-r--
        """
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
        return file_type

    @staticmethod
    def _get_uid_gid(path: pathlib.Path):
        """获取属主组
        """
        st = path.stat()
        if platform.system() == 'Windows':
            u, g = st.st_uid, st.st_gid
        else:
            # windows不支持pwd和grp
            # import pwd
            # import grp
            # u, g = pwd.getpwuid(st.st_uid), grp.getgrgid(st.st_gid)
            u, g = path.owner(), path.group()
        return u, g

    def _get_size(self, size, res=None, idx=0, suffix='KMGTP'):
        if res is None:
            res = '{:.1f}{}'.format(size, suffix[idx])
        if size > 1024:
            idx += 1
            size = size / 1024
            res = '{:.1f}{}'.format(size, suffix[idx])
            return self._get_size(size, res, idx)
        return res


if __name__ == '__main__':
    args = parse_args()
    print('***' * 10)
    path_lst = args.path
    for p in path_lst:
        for f in LSSolution().ls_dir(p, args.a, args.l, args.h):
            print(' '.join(f))
