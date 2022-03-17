#!/usr/bin/env python3
# coding=utf-8
"""
@author: feng.luo
@time: 2022/3/13
@File: 1_thread_security.py

六、线程安全：
    多线程中，不同线程的函数，一个线程中的函数未执行完，被暂停插入执行另一个线程。
        例如：print输出日志，函数分两步,先打印字符串，然后再换行。多线程中，就在这之间发生了线程切换，这就说明print函数是线程不安全。
            解决办法：1、print打印的字符串，作为不可变类型，作为一个整体不可分割输出。就不让print输出换行符，在字符串末尾加上换行符
                    2、使用logging模块

七、daemon线程和non-daemon线程
    * python程序在没有活着的non-daemon线程时退出。也就是剩下的都是daemon线程，主线程直接退出，否则只能等待non-daemon线程执行完。
    * 主线程执行完，还有daemon线程和non-daemon线程，则都继续进行。当non-daemon都执行完时，如果还有daemon，则会杀掉daemon程序退出。
    * 可见：如果要一个线程从头到尾执行完成，一定要是一个non-daemon线程。
           可有可无的线程，如果主线程退出，就可以退出的线程，放到daemon线程中
    daemon属性：
        daemon属性必须在start()之前设置。
        线程具有一个daemon属性，可以设置为True或False，也可以不设置，则去默认值None
        主线程一定是daemon=False，也就是主线程是non-daemon线程。子线程如果不设置daemon属性，就取当前线程的daemon来设置它。
        从主线程创建的所有线程都不设置daemon属性时，则默认都是daemon=False，也就是non-daemon线程。

    想要切换线程：time.sleep()就可以了。
    这里的daemon不是linux中的守护进程
    父线程：如果线程A启动了一个线程B，A就是B的父线程
    子线程：B就是A的子线程

八、join方法：
    join(timeout=None)，是线程的标准方法之一。
    一个线程中调用另一个线程的join方法，调用者将被阻塞，直到被调用线程终止。
    一个线程可以被join多次。
    timeout参数指定调用者等待多久，没有设置超时，就一直等到被调用线程结束。
    调用谁的join方法，就是join谁，就是要等谁。
    上述当没有活着的non-daemon线程时，主线程不等daemon线程，程序直接退出了。
    想要等daemon线程执行完后再退出，则可以用join方法。

daemon线程应用场景：
    daemon唯一的作用就是：当你把一个线程设置为daemon时，它会随主线程的退出而退出。简化了程序员手动关闭线程的工作。
    主要应用场景：
        1、后台任务。如发送心跳包、监控。
        2、主线程工作才有用的线程。如主线程中维护的公共资源，主线程清掉后，准备退出，工作线程使用这些资源工作也没有意义了，一起退出合适。
        3、随时可以被终止的线程。
    如果在non-daemon线程A中，对另外一个线程B使用了join方法，则线程B设置成daemon就没什么意义了。因为线程A总是要等线程B完成后才退出；
    如果两个都是daemon线程，即使使用了join方法，主线程退出，这两个daemon现在不管结束与否，都要退出

九、threading.local:解决前面的疑问，多线程使用全局变量，怎么做到线程隔离、线程安全
    python提供threading.local类，将这个类实例化得到一个全局对象，可以实现不同线程使用这个对象存储的数据其他线程看不见。
    原理：threading.local类构件了一个大字典，其元素是每一个线程实例的地址为key，和线程对象引用的线程单独的字典的映射：
        {id(Thread): (ref(Thread), thread-local dict)}
    通过threading.local实例，就可以在不同线程中，安全的使用线程独有的数据，做到了线程间数据隔离，如本地变量一样安全。

"""
import logging
import threading
import time


def worker(nums):
    for num in range(nums):
        # print('{} is running\n'.format(threading.current_thread().name), end='')
        logging.info(threading.enumerate())
        msg = '{}{} is running'.format(num, threading.current_thread())
        logging.info(msg)
        # print(threading.enumerate())


def worker1(nums):
    for num in range(nums):
        # print('{} is running\n'.format(threading.current_thread().name), end='')
        logging.info(threading.enumerate())
        msg = '$$${}{} is running'.format(num, threading.current_thread())
        logging.info(msg)
        # print(threading.enumerate())


def test_join():
    time.sleep(5)
    logging.info('This is test join')


x = threading.local()


def test_local():
    x = 0
    for i in range(100):
        x += 1
    logging.info('{} x: {}'.format(threading.current_thread(), x))


def test_no_hash(x: list):
    for i in range(10):
        x.append(i)
    logging.info('{} x: {}'.format(threading.current_thread(), x))


def test_local():
    a.x = 0
    for _ in range(10):
        a.x += 1
    # a.all = 123
    logging.info('{} x: {}'.format(threading.current_thread(), a.x))
    logging.info('a: {}, a.all:{}, b:{}， __dict__:{}'.format(a, a.all, b, a.__dict__))


if __name__ == '__main__':
    # fn = '[{asctime}]{name}-{threadName}-{level}:{message}'
    logging.basicConfig(level=logging.INFO)
    # for x in range(5):
    #     t = threading.Thread(target=worker, name='work_{}'.format(x))
    #     t.start()
    # # daemon=True时，会发现部分子线程还未执行完，程序已经退出了。
    # threading.Thread(target=worker, args=(10, ), name='worker-{}'.format(0), daemon=False).start()
    # time.sleep(2)
    # threading.Thread(target=worker1, args=(20, ), name='worker-{}'.format(2), daemon=True).start()
    # print('ending')
    # t = threading.Thread(target=test_join, name='test_join', daemon=True)
    # t.start()
    # print(threading.enumerate())
    # t.join()
    # for i in range(10):
    #     # 函数有自己的栈，这里每个线程调用函数，函数变量都存在每一个线程栈内，因此是完全不同的变量
    #     t = threading.Thread(target=test_local)
    #     t.start()
    # no_hash_lst = []
    # for i in range(5):
    #     threading.Thread(target=test_no_hash, args=(no_hash_lst,)).start()
    # a = threading.local()
    # a.all = 'aaa'
    # b = 'abc'
    #
    # for i in range(5):
    #     threading.Thread(target=test_local).start()
    # logging.info('all a:{}'.format(a))


