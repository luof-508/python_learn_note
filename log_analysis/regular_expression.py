#!/usr/bin/env python3
# coding=utf-8
"""
@author: feng.luo
@time: 2022/4/2
@File: regular_expression.py
正则匹配：
    特殊字符在[]方括号内不用转义也可匹配
    连字符‘-’在字符集[]中作为普通中划线匹配时，只能在字符集开始或字符集末尾，否则抛re.error
    中划线被作为连字符‘-’处理，匹配ascii码w到.之间的字符。

"""
import collections
import re


def regular_exp_test():
    # 匹配邮箱
    p0 = r"\b\w[\w.+-]*@[\w.-]+\.[a-zA-Z]{2,6}\b"
    mail = 'v-ip@hot-mail.com.cn'
    if re.match(p0, mail):
        print(mail)

    # html提取
    p1 = r"(?<=>)\w+(?=<)"

    # 匹配url
    p2 = r"(\w+)://([\S]+)"

    # 匹配身份证
    p3 = r"\d{17}[\dxX]|\d{15}"


def check_passwd(passwd):
    """
    强密码校验：数字、大小写字母、下划线
    :param passwd:
    :return:
    """
    if len(passwd) < 6 or len(passwd) > 12:
        return False
    if re.search(r"\W", passwd):
        return False
    if not re.search(r"_", passwd):
        return False
    if not re.search(r"[A-Z]", passwd):
        return False
    if not re.search(r"[0-9]", passwd):
        return False
    if not re.search(r"[a-z]", passwd):
        return False
    return True


def word_count(file_path: str):
    """
    统计文章中单词数量
    :return:
    """
    words_dic = collections.defaultdict(lambda : 0)
    re_obj = re.compile(r"[^\w-]")
    with open(file_path, encoding='utf8') as f:
        for line in f:
            for word in re_obj.split(line):
                if len(word) > 0:
                    words_dic[word.upper()] += 1
    return sorted(words_dic.items(), key=lambda x: x[1], reverse=True)[:10]


if __name__ == '__main__':
    regular_exp_test()
    passwds = "Aluo_f1212"
    print(check_passwd(passwds))
    print(word_count('word_count.txt'))
