"""
需求：实现base64编码和解码
"""
import string


class Base64Method(object):
    def __init__(self, original_str):
        self.original_str = original_str
        self.alfa_dic = {}
        self.alfa = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
        for i, alfa in enumerate(self.alfa):
            self.alfa_dic[i] = alfa

    def procedure(self):
        print("Original str: {}".format(self.original_str))

        encode_ret = self.encode_method(self.original_str)
        print("encode result: {}".format(encode_ret))

        decode_ret = self.decode_method(encode_ret)
        print("decode result: {}".format(decode_ret))

    def encode_method(self, src):
        """
        base64编码，每3个字符为一组，取这3个字数据的ASCII码的8位二进制为一组，然后以6位为一组组成4个新的base64数据。对于不足3字节的处理：
        1.不足三字节后面填充0；
        2.对于包含编码前的数据产生的6位，如果为0，则索引到的字符为‘A’；
        3.全部为填充的0而产生的数据，用’=’来替代。

        :param src: str
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
                base_str = self.alfa_dic.get(num)
                dst_lst.append(base_str)
                i += 6
            if n < 3:
                break
            j += 3
        return "".join(dst_lst)

    def decode_method(self, src):
        dst = ''
        return dst


be_encode = 'ABCD'
base = Base64Method(be_encode)
base.procedure()
