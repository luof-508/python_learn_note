#!/usr/bin/env python3
# coding=utf-8
"""
@author: feng.luo
@time: 2022/3/20
@File: file_IO_1.py

一、冯诺依曼体系架构
    输入设备 --> 存储器  --> 输出设备；存储器 <--> cpu（运算器、控制器）
    运算器：完成各种算数运算、逻辑运算、数据传输等数据加工处理
    控制器：控制程序的执行
    存储器：用于记忆程序和数据，即内存
    输入设备：将数据或程序输入到计算机中，鼠标、键盘
    输出设备：将数据或程序的处理结构展示给用户，例如显示器、打印机

    一般来说，IO操作，默认是文件IO，如果是网络IO，都直接说网络IO

二、文件IO常用操作
    1、打开文件：open(file, mode='r', buffering=None, encoding=None, errors=None, newline=None, closefd=True)
        打开一个文件，返回一个文件对象(流对象)和文件描述符。打开失败返回异常
        打开文件常用的操作就是读和写，访问模式有文本模式和二进制模式
        mode:
            r、w、x、a、b、t、+
            r -- 只读打开
            w、x、a -- 只写打开。w：文件存在清空原内容、不存在创建新文件。 x：创建新文件，文件存在报错。 a：追加内容，文件不存在报错。
            + -- 为r、w、x、a提供缺失的读写功能，但获取的文件对象依然按r、w、x、a自己的特征。例如r+，如果文件不存在将报错。
            t -- 字符模式读写，字符流，将文件按某种字符编码理解。open默认rt。编码模式encoding：windows下缺省GBK(0xB0A1),linux下缺省utf8
            b -- 二进制模式读写，字节流，将文件按字节理解，与字符编码无关了。类型为bytes。

    2、文件指针操作：
        文件指针，指向当前字节位置。mode=r,指针起始在0，mode=a，指针起始在EOF。
        f.tell():返回当前指针位置
        f.seek(offset, whence):移动文件指针位置。
            offset：偏移多少个字节。
            whence：从什么位置开始。缺省值0：表示从头开始。1：表示从当前位置开始。2：表示从EOF开始。
                文本模式下，支持从开头向后偏移的方式，whence=0。因为偏移量offset是字节数，文本模式一个中文字包含多少个节数不确定，负向偏移或其他方式很容易就乱码报错。
                二进制模式下，支持任意起点的偏移，向后seek支持超界，向前不能超界，否则抛异常。

    3、指定缓存区：
        缓冲区buffering。是一个内存空间，一般来说一个FIFO队列，直到缓冲区满了或达到阈值，数据才会flush到磁盘。
            buffering=-1:默认缓存模式。
            buffering=0:关闭缓存，文本模式不支持
            buffering=1:文本模式，按行缓冲，遇到换行符flush；二进制就是1个字节
            buffering>1:文本模式，是io.DEFAULT_BUFFER_SIZE；二进制就是字节数。
            f.flush():将缓存数据写入磁盘
            f.close()前会调用flush()
            一般来说：
                1、文本模式，都用默认缓冲区大小。且不支持关闭缓冲
                2、二进制模式，是一个个字节的操作，可以指定buffer的大小
                3、编程中，明确知道要写磁盘了，都会手动调用一次flush，而不是等到自动flush或close的时候。

    4、读写文件：
        f.read(size=-1):默认读取所有文件
            size：读取多少个字节或字符
        f.readline():行读取
        f.readlines():读取所有行的列表，每一行是列表中一个元素。
        f.write(s):把字符串s或字节写入文件

    5、上下文管理：
        lsof 列出打开的文件
        ulimit -a 查看所有限制
        with open(file) as f:
        上下文管理的语句块并不会开启新的作用域。
        OI被打开的时候，会获得一个文件描述符。计算机资源是有限的，所以操作系统都会做限制，保护计算机资源不要被完全耗尽。

"""
import re


def copy_file():
    with open('test.txt', encoding='utf8') as f1:
        with open('test1.txt', 'w', encoding='utf8') as f2:
            f2.write(f1.read())


def find_top_word():
    dic = dict()
    with open('test.txt', encoding='utf8') as f:
        for word in f:
            words = re.split('[^a-z]', word.strip().lower())
            for s in words:
                if not s.strip().isalpha():
                    continue
                dic[s.strip()] = dic.get(s.strip(), 0) + 1
    res = sorted(dic.items(), key=lambda x: x[1], reverse=True)
    print(res[:10])


if __name__ == '__main__':
    copy_file()
    find_top_word()
