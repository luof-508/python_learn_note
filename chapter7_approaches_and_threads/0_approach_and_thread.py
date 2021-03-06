#!/usr/bin/env python3
# coding=utf-8
"""
@author: feng.luo
@time: 2022/3/13
@File: 0_approach_and_thread.py

一、并行和并发
并行，parallel：同一个时间点，不同任务同时进行，互不干扰
并发，concurrency:需要同时做某些事，强调的是需要处理多项事务，不一定同时进行
    ---> 并行解决的是并发需求的一种方式。
    --->队列、缓冲区，也是解决并发的方式。

高并发怎么解决：嗯，并行怎么样，队列怎么样，争抢怎么样？
    1、队列、缓冲区：排队是天然解决并发需求的方法。
        * 缓冲区：排成的队列，就是一个缓冲地带，就是 缓冲区。
        * 优先队列：假设女生优先，食堂只有一个窗口，需要排两个队列，女生排女生的队列，只要有女生来，就优先打饭。
    2、争抢：谁先抢到窗口，谁先吃饭。缺点是有可能有人很长时间抢不到
        * 锁机制：食堂无序打饭发生争抢，只有一个窗口，当有一个人占据窗口，可视为锁定窗口，窗口就不能为其他人提供服务了。这是一种锁机制
    3、预处理：提前加载用户需要的数据。预处理思想，缓存常用。
        排队，排在后面的人很可能想吃的菜没了，怎么办，提前统计，多少人想吃热菜，多少人想吃冷菜，按比例提前做好。这样即使有人锁住了窗口，也可以很快释放，不至于卡死
    4、并行：上千个人同时吃饭，一个队伍搞不定，多开几个窗口，形成多个队列。
        * 水平扩展思想：通过购买更多服务器、或多开进程，来解决并发问题
        有多少个cpu，就可以开多少个线程：如果线程在单个cpu上处理，就不能并行了。
        缺点：多个窗口就得扩大食堂，多雇人，成本上升。
    5、提速：提高单个窗口的打饭速度，也是解决并发的方式
        * 垂直扩展思想：提高单个cpu的性能，或单个服务器安装更多cpu。 垂直提升很容易遇到天花板，成本急速上升
    6、消息中间件：景区检票口，通过隔离带设计成九曲回肠的走廊，缓冲人流，再设置多个检票口检票。
        常见的消息中间件有RabbitMQ，ActiveMQ(Apache)、RocketMQ(阿里Apache)、kafka(Apache，大数据领域分布式系统)等。
        * 分布式：多个服务之间要相互协调

    以上是高并发最常用地解决方案，一般来说，不同的高并发场景用不同的策略，而且可能是多种方式的优化组合。例如，多开食堂，食堂建到宿舍生活区

服务端：提供服务的，打菜的师傅
客户端：用户，吃饭的人

高速公路收费站思想：串、并行。
串行快还是并行快：看场景，到达cpu的上限了，什么方式都只能一个一个来（高速路收费站出站口只有一个闸门，无论多少车道，一次只能出一辆车）。因此不能厚此薄彼

二、进程和线程
进程和线程：
    * 在实现了线程的操作系统中，线程是操作系统能够进行运算调度的最小单位。它被包含在进程之中，是进程中的实际运作单位。一个程序的执行实例就是一个进程
    * 进程（process）是系统进行资源分配和调度的基本单位，是操作系统结构的基础

进程和程序的关系
    * 程序是源代码编译后的文件，这些文件存放在磁盘上。当程序被操作系统加载到内存中，就是进程，进程中存放着指令和数据（资源），它也是线程的容器。
    * linux进程有父进程和子进程，windows的进程是平等关系。
    * 线程，有时被称为轻量级进程，是程序执行流的最小单元。一个标准的线程由线程ID，当前指令指针(PC),寄存器集合和堆栈组成。

进程、线程的理解
    * 现代操作系统提出进程的概念，每一个进程都认为自己独占所有的计算机资源（因此现代操作系统一开始就有虚拟化的概念）。
    * 进程就是独立的王国，进程间不可以随便的共享数据。
    * 线程就是省份，同一个进程内的线程可以共享进程的资源，每一个线程拥有自己独立的堆栈。

三、线程的状态
    1、运行态(run)：该时刻，该进程正在占用cpu
    2、就绪态(Ready)：线程能够运行，但在等待被调度
    3、阻塞态：线程等待外部事件发生而无法运行，如I/O操作
    4、终止：线程完成，或退出，或被取消


四、python中的进程和线程
    * python进程会启动一个解释器进程，线程共享一个解释器进程。
    * 多线程：一个进程中如果有多个线程，就是多线程，实现一种并发。线程的优先级是由操作系统决定的，不用太过关心
        多线程不是同时跑几个线程，而是这个线程跑一会儿，那个线程跑一会儿，操作系统调度
    * 主线程：一个进程中至少有一个线程，并作为程序的入口，这个线程就是主线程。其他线程称为工作线程。

五、python中的线程开发
    标准库/模块：threading
    threading模块的属性和方法：
        current_thread():返回当前线程对象
        main_thread():返回主线程对象
        active_count():返回正在执行的线程数量，非零整数
        enumerate():返回所有活着的线程列表

    threading.Thread类：threading.Thread(target, name, daemon=None, *args, **kwargs)
        target：线程调用的对象，就是目标函数
        name：为线程起个名字(不同线程可重名) --- 线程是按线程ID区分的
        args：为目标函数传递实参，元组
        kwargs：为目标函数关键字传参，字典
        Thread()实例的属性和方法：
            ident: 线程ID，它是非零整数。线程启动后才有ID，否则为None。线程退出，此ID依旧可以访问。此ID可以重复使用。
            is_alive(): 返回线程是否活着
            start(): 启动线程，启动了一个新的线程，一个线程只能启动一次
            run(): 执行线程函数target # 在当前线程(不一定是主线程)中执行函数顺序调用,就是一个普通函数调用

    python没有为线程退出,没有优先级、没有线程组，不能被销毁、停止、挂起，程序执行完线程自动终止。

问题：多线程，不可hash变量，不同线程可以同时操作这个变量吗？


"""
import threading
import time


class MyThread(threading.Thread):
    def run(self) -> None:
        print('run')
        super().run()

    def start(self) -> None:
        print('start')
        return super().start()


def show_thread_info():
    print(threading.main_thread())
    print(threading.current_thread())
    print(threading.active_count())
    print('%s: %s' % (threading.current_thread(), threading.current_thread().is_alive()))


def worker(x, **kwargs):
    count = 1
    # show_thread_info()
    print(threading.current_thread())
    while True:
        print('welcome chengdu, res:{}'.format(x))
        time.sleep(0.1)
        if count > 3:
            print('Thread over')
            break
        count += 1


if __name__ == '__main__':
    t = MyThread(target=worker, name='w1', args=(5,), kwargs={'a': 5})
    # t.start()
    t.run()
    print('==================')
    t1 = MyThread(target=worker, name='w2', args=(5,), kwargs={'a': 5})
    t1.run()

    thread_lst = threading.enumerate()
    show_thread_info()
    time.sleep(2)
    for cur_th in thread_lst:
        print('%s: %s' % (cur_th.ident, cur_th.is_alive()))
