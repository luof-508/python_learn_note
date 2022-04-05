#!/usr/bin/env python3
# coding=utf-8
"""
@author: feng.luo
@time: 2022/3/20
@File: chapter3_file_io.py

一、冯诺依曼体系架构
    输入设备 --> 存储器  --> 输出设备；存储器 <--> cpu（运算器、控制器）
    运算器：完成各种算数运算、逻辑运算、数据传输等数据加工处理
    控制器：控制程序的执行。控制总线，把数据（脉冲信号）加载到运算器，经运算器输出到内存，然后由内存到IO设备（硬盘）内存：高速访问的晶片
    存储器：用于记忆程序和数据，即内存
    输入设备：将数据或程序输入到计算机中，鼠标、键盘
    输出设备：将数据或程序的处理结构展示给用户，例如显示器、打印机

    windows encoding='cp936'
    linux encoding='utf-8'
    一般来说，IO操作，默认是文件IO，如果是网络IO，都直接说网络IO


二、文件打开读取操作
    1、打开文件：
        打开文件常用的操作就是读和写，访问模式有文本模式和二进制模式。文本是TextIO，字节是BufferIO
        字符流、字节流。f.read(1), f.read(1)
        打开文件：open(file, mode='r', buffering=None, encoding=None, errors=None, newline=None, closefd=True)
            打开一个文件，返回一个文件对象(流对象)和文件描述符。打开失败返回异常
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
                文本模式下，支持从开头向后偏移的方式，whence=0。因为偏移量offset是字节数，文本模式一个中文字包含多少个节数不确定，负向偏移
                    或其他方式很容易就乱码报错。
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

    6、stringIO和BytesIO
    stringI0:
        io模块中的类。可以在内存中，开辟一个文本模式的buffer，可以像文件一样操作它。当调用close方法的时候，这个buffer被释放。
        stringI0（）．getvalue（）：无视指针，输出全部内容
        一般来说，内存足够的情况下，一般的优化思路就是少落地，减少磁盘IO的过程，可以大大提高程序的运行效率。磁盘操作比内存操作要慢得多
        单机stringI0，多机redis
    BytesIO:
        在内存中开辟一个二进制的buffer。操作与stringIO一样。
    file-like:
        类文件对象，可以像文件对象一样操作。socket对象、输入输出对象（stdin、stdout）都是类文件对象


三：python的系统操作--代替shell
    一、目录及路径操作
        3.4版本之前：os.path
            os.path.split
            os.path.splitext
            os.listdir()
            os.path.splitdrive(path): 将路径分割为尾部和驱动器。驱动器是安装点或空字符串，其余路径组件是尾部。在不使用驱动器规范的系统上，
                                      驱动器将始终为空字符串。示例：UNIX

        3.4开始：pathlib.Path()类：
        初始化：p = path('a', 'b', 'c/d')当前目录下的a/b/c/d
              p = Path('/etc')根下的etc目录
              p = Path()当前目录
        操作符/： Path对象/Path对象
                Path对象/字符串 或 字符串/Path
        分解parts：可以返回路径中的每一个部分
        joinpath(＊other)：连接多个字符串到Path对象中

        获取路径：str(Path()), bytes(Path()))

        父目录，parent：目录的逻辑父目录
        父目最序列，parents：索引0是最近一层父目录

    二、文件权限、创建、拷贝、删除操作：
        元数据信息：os.stat（path， follow＿symlinks＝True）
                  follow_symlinks-True:	返回文件本身信息，如果是状僵楼。
        创建文件、目最相关：
            pathlib.Path().touch
            pathlib.Path().mkdir
            pathlib.Path（）.iterdir（） 迭代当前目录
            pathlib.Path（）.rmdir（） 删除空目录
            pathlib.Path（）.exist（） 路径是否存在
            pathlib.Path().is_dir()
            pathlib.Path(). is_file()
            pathlib.Path(). resolve()
            pathlib.Path().absolute()
        改变属主、属组：
            os.chmod()
            os.chown(path, uid, gid)
        拷贝文件： shutil模块
            shutil.copyfileobj（src， dst）：仅复制文件内容，元数据、权限丢失。dst要求可写。src／dst为打开的文件对象
            shutil.copyfile（src， dst）：复制文件内容，元数据、权限丢失。src／dst为文件路径字符串 -- 本质上是调用copyfileobj
            shutil.copymode（src， dst）：仅仅复制权限
            shutil.copystat（src，dts） ：复制权限和其他元数据信息
            shutil.copy（scr，dts）：复制文件内容、权限和部分元数据信息，但是不包括创建时间ctime和修改时间mtime
                --本质上是调用 copyfile和copymode
            shutil．copy2（src，dts）：比copy多了复制全部原数据信息，但需要平台支持
                --本质上是调用 copyfile和copystat
            shutil．copytree（src， dts， symlinks＝False， ignore＝None， copy＿function＝copy2）：递归复制目录，默认使用copy2
            注意：递归复制，symlinks＝False，因为复制目录，如果追踪软连接，会破坏目录结构，出问题。复制单个文件symlinks=True
                src必须是目录且存在，dts必须不存在
                ignore＝func：提供一个callable（src， names） -＞ignored＿names。
            shutil.rmtree（path， ignore＿error＿False）：递归删除	等同于rm -rfo
                不是原子操作，10个文件删了5个后，失败，删除的5个不会恢复
            shutil．move（src， dts， copy＿function＝copy2）：递归的移动文件、目录到目标，返回目标
                实质是使用os.rename方法
            shutil还支持打包功能。可以生产tar包并压缩。支持格式；zip／gz／bz／xz

＊＊文件类型：
    结构化：数据库--结构化存储，有很强模式定义数据每一行每一列是干什么的
    半结构化：json｜xmal，按一定规格
    非结构化：视频、图片、音频。二进制数据
四、csv文件：半结构化数据
    csv文件是一个按行分隔符和列分割符划分成的行和列的文本文件。不需要指定字符编码每一行成为一条记录record

    表头：非必要，与字段列对齐就行
    列分割：csv文件，按逗号分割值 Comma-Separated values
    行分割：lrln. 最后一行可以没有换行符
    特殊符号处理：
    字段可以用双引号括起来，也可以不用。
    如果字段中有特殊符号，如双引号、逗号、换行符、空格，则整个字段必须使用双引号括起来。
    如果字段的值中有双引号，使用两个双引号表示一个转义
    优点：
        1、可以exce1直接打开，另存为excel,则可直接用excel公式。相比直接编辑excel,轻量化得多
        2、高低版本excel切换，有兼容性问题，csv文件则可以避免这种问题用着数据交换工具。
        3、甚至可以当数据库得表来处理。
    python csv类：
        csv.writer(fileobj).writerow()
        csv.reader(iterable)
五、ini文件处理：
    作为配置文件，ini文件格式很流行。
    中括号里面的部分成为section，每一个section内都是key＝value形成得键值对，key称为option选项
    可见：不同section下可以有相同的option
    ini文件解析：configparser模块的ConfigParser类
    cfg = ConfigParser()
    cfg.read（filename）：读取之后就常驻内存的，因为系统运行起来后，很多ini配置参数值都是常驻内存的，这里的设计考虑了ini文件的应用场景
    cfg.sections（）：返回section列表
    cfg.add＿section（section＿name）：增加一个section，存在抛错
    cfg.has_section(section_name)
    cfg.options（section）：返回section的所有option
    cfg.has_option(section, option)

    cfg.get（section， option）：从指定的section选项上去值，如果没有找到，则去DEFAULT section找。没有返回默认值
    cfg.getint()
    cfg.getfloat()
    cfg.getboolean()
    cfg.items（section）：返回指定section的键值对组成的二元组。没有section返回所有section名字及其
    cfg.set(section, opt, value): section存在，则写入键值对，要求opt、value必须是字符串cfg.remove(section)
    cfg.remove(section)
    cfg.remove_option(section, option)

    cfg.write(fileobj): 将当前cfg中的所有内容写如fileobj中。




"""
import configparser
import os.path
import pathlib
import re
import csv


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


# # 一、os.path路径操作：
def test_os_path():
    p = 'D:\\repository\\notes_scripts\\python_learn_note\\chapter3_file_io\\chapter3_file_io.py'
    print(os.path.basename(p))
    print(os.path.relpath(p))
    print(os.path.abspath(p))
    print(os.path.split(p))
    print(os.path.splitdrive(p))
    print(os.path.dirname(p))
    print(os.path.curdir)
    print(os.path.exists(p))
    print(os.path.join('abc', 'python.py'))


# # 二、pathlib.Path
def test_pathlib():

    # 1.初始化
    p1 = pathlib.Path()  # 当前目录
    p2 = pathlib.Path('a', 'b', 'c/d')   # 当前目录下的a/b/c/d
    p3 = pathlib.Path('/etc')  # 根下的etc目录
    print(p1, p2, p3)

    # 2.操作符/
    # Path对象/Path对象；Path对象/字符串；字符串/Path对象
    p4 = p1/'a'
    p5 = 'b'/p1
    p6 = p3/p2
    print(p4, p5, p6)
    # 3.分解parts:可以返回路径中的每一个部分
    print(p6.parts)
    # 4.joinpath，连接多个字符串到Path对象中
    print(p6.joinpath('a', 'abc', 'fusion', pathlib.Path('http')))
    # 获取路径 str(Path对象) 或bytes(Path对象)
    print(type(p6), type(str(p6)))

    # # 5.父目录：parent；
    # # 父目录序列：parents，索引0是最近的父目录
    p = pathlib.Path('abc/etc/sys/config/network/eth0')
    print(type(p.parent), p.parent)
    print(list(p.parents))

    # # 6.目录操作
    # name，目录的最后一部分，文件全名
    print(p.name, type(p.name))
    # suffix，后缀，文件的最后一个扩展名
    p = pathlib.Path('/home/admin/test.tar.gz')
    print(p.suffix)
    # stem，目录的最后一部分，没有后缀。及文件名
    print(p.stem)
    print(p.stem + p.suffix == p.name)
    # suffixes 返回多个扩展名
    print(p.suffixes)
    # with_suffix(suffix) 补充扩展名到路径尾部，返回新的路径，扩展名存在则不进行任何操作
    print(p.with_suffix('.zip'), p.with_suffix('.gz'), p.with_suffix('.asc'))
    # with_name(name) 替换目录最后一部分，返回一个新的路径
    print(p.with_name('ll.log'))

    # #7. 获取与判断操作
    p = pathlib.Path()
    qq = pathlib.Path('/chapter3_file_io\\腾讯QQ.lnk')
    print('---' * 5)
    print(p.cwd())  # 返回当前目录
    print(p.home())  # 返回家目录
    print(qq.resolve())  # 返回当前Path的绝对路径，如果当前Path是软链接，则软链接被解析，返回真实路径
    print(qq.absolute())  # 返回绝对路径
    print(p.is_dir())
    print(p.is_file())
    print(p.is_absolute())
    print(p.is_symlink())
    print(p.exists())

    # # 8、创建文件与目录
    print(list(pathlib.Path().iterdir()))  # 跌带当前目录
    pathlib.Path('test.log').touch()  # 创建一个新文件
    pathlib.Path('test/').mkdir(exist_ok=True)  # 创建一个目录
    # pathlib.Path('test/').mkdir(mode=0o777, parents=False, exist_ok=False)
    # parents,是否创建父目录，parents=True等同于mkdir -p；False时，父母了不存在将抛FileNotFoundError错
    # exist_ok=True时，文件存储不抛出错

    # # 9.通配符glob(pattern) 通配给定的模式
    print('---' * 5)
    p = pathlib.Path()
    print(list(p.glob('test*')))  # 返回当前目录下所有以test开头的文件
    print(list(p.glob('**/*.py')))  # 递归当前目录下的所有目录及文件，返回所有py文件
    print(list(p.rglob('*.py')))  # 同上

    # # 10.匹配match(pattern) 模式匹配，成功返回True
    print(pathlib.Path('a/b.py').match('*.py'))
    print(pathlib.Path('a/b/c/d.py').match('a/*/*.py'))
    print(pathlib.Path('a/b/c/d.py').match('a/**/*.py'))
    print(pathlib.Path('a/b/c/d.py').match('**/*.py'))

    # # 11. 文件操作
    # open，打开文件，操作与内建函数open一致
    p = pathlib.Path('test.log')
    with p.open(mode='w', encoding='utf8') as f:
        f.write('abc')
    # 读写文件
    p.write_text('abc')
    p.write_bytes(b'abc')  # 这里的write_bytes每次都是重新创建，慎用
    p.read_text()


# 三、csv
dst = """num,name,age,comm
1,luof,20,
2,jerry,33,male
3,tom,30,
4,Lily,3,"""
def test_csv():
    with open('test.csv', mode='w', encoding='utf8') as f:
        for line in dst.splitlines():
            f.write(line + '\n')
        csv.writer(f).writerow([2, 'll', 23])
        csv.writer(f).writerows([(6, 'hh', 5), (7, 'cle', 56, 'female')])
    with open('test.csv', encoding='utf8') as f:
        print(next(csv.reader(f)))
        print(next(csv.reader(f)))


# 四、ini
def test_ini():
    cfg = configparser.ConfigParser()
    cfg.read('test.ini')
    print(cfg.sections())
    for section in cfg.sections():
        for opt in cfg.options(section):
            print(section, opt)
        for k, v in cfg.items(section):
            print(k, v)
    print(cfg.items('mysql'))
    print(cfg.options('mysql'))
    for k, v in cfg.items():
        print(k, v)
    # cfg.set('test_section', 'opt', 'True')
    cfg.add_section('test_section')
    cfg.set('test_section', 'opt', 'True')
    print(cfg.get('test_section', 'opt'))
    print(cfg.getboolean('test_section', 'opt'))
    with open('test_ini', mode='w') as f:
        cfg.write(f)


if __name__ == '__main__':
    # copy_file()
    # find_top_word()
    # print(os.path.abspath(__file__))
    # test_pathlib()
    # print(os.listdir())
    # test_csv()
    test_ini()
