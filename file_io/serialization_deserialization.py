#!/usr/bin/env python3
# coding=utf-8
"""
@author: feng.luo
@time: 2022/3/25
@File: serialization_deserialization.py

序列化和反序列化：
序列化就是把数据变成可存储或可传输的过程的，只有序列化后的数据才可以写入到磁盘或者通过网络传输到Spark集群的其他节点上。
反序列化则相反，反序列就是把序列化的变量重新转到内存里。
由于模块shelve的Shelf方法依赖于pickle模块，所以使用模块shelve的Shelf方法加载不可信来源的数据也是不安全的。


定义（serialization）：
*序列化和反序列化		-- 设计一套协议，按协议规则读取、保存数据到文件中；
    文件是一个字节序列，所以必须把数据转换成字节序列，输出到文件
*协议也分版本。用同样版本的协议，保证读取没有问题。

内存中的字典、链表、列表如何保存到文件中？
自定义的类的实例，如何保存到文件中，-
又怎么读取才能让他们在内存中再次变成自己对应的类的实例？
这就是序列化和反序列化

序列化：将内存中的对象存储下来，变成一个个字节-->二进制
反序列化：将文件中的一个个字节恢复成内存中的对象。
持久化：序列化保存到文件就是持久化
可以将数据序列化后持久化，或网络传输；也可以将从文件或网络接收的字节序列反序列化。

目的：1、落地，2、传输

序列化 整数传输大小端问题：网络传输一般都是大端模式
二、python序列化标准库：pickle
    dump: 转储
    仅限于python内部序列化的问题，跨语言或网络传输就不行了
    pickle.dump()  # 对象序列化到文件对象，就是将python数据类型、对象以python特定格式的二进制，并存入文件
    pickle.load()  # 对象反序列化，从文件读取python特定格式的二进制数据格式，转换为python数据类型

    pickle.dumps()  # 对象序列化， 将python数据类型、对象转换为python特定格式的二进制
    pickle.loads()  # 对象反序列化 将python特定格式的二进制数据格式转换为python数据类型



"""
import pickle


class AA:
    TEST = 'ABC'

    @staticmethod
    def show():
        print('abc')


def serialization_test():
    # dump: 转储
    a = {'name': 'qiang', 'age': 11}
    b = 'abc'
    c = ['a', 'b', ['c', 'd']]
    with open('test.log', 'wb') as f:
        pickle.dump(a, f)
        pickle.dump(b, f)
        pickle.dump(c, f)

    with open('test.log', 'rb') as f:
        s = []
        for _ in range(3):
            s.append(pickle.load(f))
        print(s)


def obj_ser_test():
    """
    对象序列化
    """
    a1 = AA()

    sr = pickle.dumps(a1)
    print('sr = {}'.format(sr))

    a2 = pickle.loads(sr)
    print(a2.TEST)
    a2.show()


if __name__ == '__main__':
    serialization_test()
    obj_ser_test()
