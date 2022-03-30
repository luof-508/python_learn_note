#!/usr/bin/env python3
# coding=utf-8
"""
@author: feng.luo
@time: 2022/3/25
@File: serialization_deserialization.py

内存中的字典、链表、列表如何保存到文件中？
自定义的类的实例，如何保存到文件中？
又怎么读取才能让他们在内存中再次变成自己对应的类的实例？
这就是序列化和反序列化

一、理解（serialization）：
    *序列化和反序列化		-- 设计一套协议，按协议规则读取、保存数据到文件中；
        文件是一个字节序列，所以必须把数据转换成字节序列，输出到文件
    *协议也分版本。用同样版本的协议，保证读取没有问题。

二、序列化和反序列化定义：
    序列化就是把数据变成可存储或可传输的过程的，只有序列化后的数据才可以写入到磁盘或者通过网络传输到Spark集群的其他节点上。
    反序列化则相反，反序列就是把序列化的变量重新转到内存里。
    由于模块shelve的Shelf方法依赖于pickle模块，所以使用模块shelve的Shelf方法加载不可信来源的数据也是不安全的。


序列化：将内存中的对象存储下来，变成一个个字节-->二进制
反序列化：将文件中的一个个字节恢复成内存中的对象。
持久化：序列化保存到文件就是持久化
可以将数据序列化后持久化，或网络传输；也可以将从文件或网络接收的字节序列反序列化。

三、目的：1、落地，2、传输

四、python序列化标准库：pickle
    dump: 转储
    仅限于python内部序列化的问题，跨语言或网络传输就不行了
    pickle.dump()  # 对象序列化到文件对象，就是将python数据类型、对象以python特定格式的二进制，并存入文件
    pickle.load()  # 对象反序列化，从文件读取python特定格式的二进制数据格式，转换为python数据类型

    pickle.dumps()  # 对象序列化， 将python数据类型、对象转换为python特定格式的二进制
    pickle.loads()  # 对象反序列化 将python特定格式的二进制数据格式转换为python数据类型

五、自定义对象序列化理解序列化、反序列化过程：
    通过分析序列化文件test.bin可见：
        1、对象序列化，会保存对象所在的模块标识serialization_deserialization，以及对象本身的标识AA。
        2、类方法show、类属性TEST都没有被序列化
        3、对象属性self.name则被序列化：因为每一个对象属性都是不同的
        4、被序列化的对象，通过网络传输到其他节点，反序列化后对象实例能够运行的前提是其他节点必须有同样的模块定义，以及模块内有相同标识符AA的
           类定义，否则执行将失败，报找不到这个模块或方法。 如果其他节点的类方法、类属性被重写了，则得到不预期的结果，相当于偷梁换柱了。

    反序列化的过程：类是模子，二进制序列就是铁水。

六、应用：
    本地序列化应用较少。大多数常见都应用在网络中。将数据序列化后通过网络传输到远程节点，远程服务器上的服务将接收到的数据反序列化后，就可以使用了。
    但是：远程接收端，反序列化时必须有对应的数据类型，否则就会报错。尤其是自定义类，必须远程得有。

rpc的基本原则：序列化 <---> 反序列化
远程过程调用：序列化 <---> 反序列化
序列化 整数传输大小端问题：网络传输一般都是大端模式

七、公共协议：
    跨平台、跨语言的公共的序列化、反序列化协议：XML(易懂，但是废数据太多)、Json(网络传输)、Protocol Buffer(分布式场景)等。
    不同的协议，效率不同，适用不同场景。讲究效率，接近二进制比较合适；
    慢数据交换系统（比如内网），可能XML或Json方案比较合适。但是都不应该用先落地再读取的方案

八、Json： JavaScript Object Notation，JS对象标记、是一种轻量级的数据交换格式。
    它基于ECMAscript的一个子集，采用完全独立于编程语言的文本格式来存储和表示数据
    **文本格式来存储和表示数据
    Json数据类型value：
        string：字符串。由双引号包围起来的任意字符的组合，可以有转移字符
        number：数值。整数、浮点数，可正负
        object：无序的键值对集合，key必须是双引号包围的字符串，value可以是任意合法的值
        array：列表
        false:
        true:
        null:None

    AJAX：异步传输数据

    python类型	json类型
    True		true
    False   false
    None			null
    str			string
    int		integer
    float		float
    list		array
    dict    object
    常用方法：
        dumps json编码
        dump json编码并存入文件
        loads	json解码
        load	json解码，从文件读取数据

    一般json编码的数据很少落地，数据都是通过网路传输，传输的时候要考虑压缩它-key值映射，减少网络传输流量浪费

    本质上json就是个文本、字符串，几乎语言编程都支持json。

    九、三方插件MessagePack：一个基于二进制高效的对象序列化类库，可用于跨语言通信
        可以像json那样，在多种语言之间交换结构对象用法和jso、pickle一样。

        pip install msgpack-python
        import msgpack
        msgpack.dumps
        msgpack.dump
        msgpack.loads
        msgpack.load

    MessagePack简单易用，高效压缩，效率比json更高。	--二进制格式存储和表示数据
    json应该更加广泛，简单-文本格式来存储和表示数据
"""
import pickle


class AA:
    TEST = 'ABC'

    def __init__(self):
        self.name = 'AAAA'

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


def obj_serialization_test():
    """
    自定义对象序列化
    通过分析序列化文件test.bin可见：
        1、对象序列化，会保存对象所在的模块标识serialization_deserialization，以及对象本身的标识AA。
        2、类方法show、类属性TEST都没有被序列化
        3、对象属性self.name则被序列化：因为每一个对象属性都是不同的
        4、被序列化的对象，通过网络传输到其他节点，反序列化后对象实例能够运行的前提是其他节点必须有同样的模块定义，以及模块内有相同标识符AA的
           类定义，否则执行将失败，报找不到这个模块或方法。 如果其他节点的类方法、类属性被重写了，则得到不预期的结果，相当于偷梁换柱了。
    """
    a1 = AA()
    with open('test.bin', 'wb') as f:
        pickle.dump(a1, f)


def obj_deserialization_test():
    # test.bin传到另一个节点，反序列化。直接测试运行看会怎么样；
    # 然后创建模块serialization_deserialization，并重新对象AA，或不写AA，测试运行
    with open('test.bin', 'rb') as f:
        res = pickle.load(f)
        res.show()
        print(res.TEST)


if __name__ == '__main__':
    # serialization_test()
    obj_serialization_test()
