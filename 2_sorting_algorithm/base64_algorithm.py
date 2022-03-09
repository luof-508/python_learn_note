# coding = utf-8
"""
位运算实现base64编码和解码，运用AOP思想，运用类装饰器，分析算法实现的正确性。

base64编码核心算法：
    1、将输入每3个字节分为一组，每组按6个bit断开分为4个段 -->  2**6=64, 因此有了base64编码表。
    2、新的4段，每一段当成新的8bit，这个8bit对应的值就是base64编码表对应的索引，并根据索引找到对应的字符。
    3、不足3字节的处理：不足三字节后面填充0，全部为填充的0而产生的数据，用’=’来替代。

base64解码核心算法：
    1、根据字节，找到base64索引，通过移位运算，重新组成3字节的24bit的，再通过大端模式，转换成bytes。
    2、补0处理：编码中，末尾补0被替换成=号，将无法在base64编码表中找到索引数字，在这里判断是否需要移位运算。

涉及概念：大、小端模式，位运算
"""

__author__ = 'fg.luo'

import re
import base64
import string
import os

from tool.logger_define import LoggerDefine


base_name = os.path.basename(__file__)
logger = LoggerDefine(base_name).logger_define()


class ResultCheck:
    def __init__(self, func):
        logger.info('first step')
        self.func = func

    def __get__(self, instance, own):
        def _res_analysis(*args):
            logger.info('Third step')
            if re.search('decode', self.func.__name__):
                builtins_res = base64.b64decode(*args)
            else:
                builtins_res = base64.b64encode(*args)
            res = self.func(instance, *args)
            if builtins_res == res:
                logger.info('OK!, res:{}'.format(res))
            else:
                logger.error('Error, builtin:{}, your method:{}'.format(builtins_res, res))
            return res
        logger.info('second step')
        return _res_analysis


class Base64Demo(object):
    def __init__(self):
        self.alfa = (string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/').encode()
        self.alfa_dic = dict(zip(range(64), self.alfa))
        self.str_dic = dict(zip(range(64), string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'))
        self.decode_dic = dict(zip(self.alfa, range(64)))

    def procedure(self, src: bytes):
        logger.info("Original str: {}".format(src))
        # encode_ret = self.my_encode_method(src.decode())
        encode_res = self.bit_encode_base64(src)
        decode_ret = self.bit_decode_base64(encode_res)

    def my_encode_method(self, src: str):
        """
        暴力法
        :return: str
        """
        dst_lst = []
        j = 0
        for _ in range(len(src)):
            team = src[j: j+3]
            if not team:
                break
            n = len(team)
            # 取每一组的二进制字符串
            bit_team = ''
            for i in range(n):
                bit_str = bin(ord(team[i])).replace("0b", "")
                bit_team += '0' * (8 - len(bit_str)) + bit_str
            bit_team += '0' * (24 - len(bit_team))
            # 按6位划分为四组，并转换为整数，求base64对应的字符
            i = 0
            for x in range(4):
                encode_bit = bit_team[i: i+6]
                if n == 1 and x >= 2:
                    dst_lst.append('=')
                    continue
                elif n == 2 and x == 3:
                    dst_lst.append('=')
                    continue
                num = int(encode_bit, 2)
                base_str = self.str_dic.get(num)
                dst_lst.append(base_str)
                i += 6
            if n < 3:
                break
            j += 3
        return "".join(dst_lst)

    @ResultCheck
    def bit_encode_base64(self, src: bytes):
        """
        移位位运算编码
        3个字节一组，分四段，然后每一段当做8bit，计算8bit对应的值。不足3位的末尾补0，全补0的段用=号代替
        =的ASCII码：0x3D
        """
        res = bytearray()
        n = len(src)
        add_zero_num = 0
        for i in range(0, n, 3):
            if i + 3 <= n:
                sub_src = src[i: i+3]
            else:
                sub_src = src[i:]
                add_zero_num = 3 - len(sub_src)
                sub_src = sub_src + b'\x00' * add_zero_num
            b = int.from_bytes(sub_src, 'big')
            for j in range(18, -1, -6):
                idx = b >> j & 0x3F
                res.append(self.alfa_dic[idx])
        for s in range(1, add_zero_num+1):
            res[-s] = 0x3D
        return bytes(res)

    @ResultCheck
    def bit_decode_base64(self, src: bytes):
        """
        移位运算解码
        4个字节一组，找到对应的base64索引，移位运算组成24位，末尾的=strip(b'\x00')
        """
        res = bytearray()
        for offset in range(0, len(src), 4):
            sub_src = src[offset: offset+4]
            b = 0x00
            for i, s in enumerate(sub_src):
                idx = self.decode_dic.get(s)
                if idx is not None:
                    b += idx << (3 - i) * 6
            res.extend(b.to_bytes(3, 'big'))
        return bytes(res).strip(b'\x00')


if __name__ == '__main__':
    base = Base64Demo()
    for origin in ['abcd'.encode(), 'ab'.encode(), 'abc'.encode(), 'abcd'.encode(), b'']:
        base.procedure(origin)
