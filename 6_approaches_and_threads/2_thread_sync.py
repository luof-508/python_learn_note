#!/usr/bin/env python3
# coding=utf-8
"""
@author: feng.luo
@time: 2022/3/18
@File: 2_thread_sync.py

十一、线程同步
    线程间协同，通过某种技术，让一个线程访问某些数据的时候，其他线程不能访问这些数据，直到该线程完成对数据的操作。
    ＊脏读：一个线程操作的半成品数据，其他线程又来用。
        脏读就是指当一个事务正在访问数据，并且对数据进行了修改，而这种修改还没有提交到数据库中，这时，另外一个事务也访问这个数据，然后使用了这个数据。
        因为这个数据是还没有提交的数据，那么另外一个事务读到的这个数据是脏数据，依据脏数据所做的操作可能是不正确的。
            1、如果都未更新你就读取了，或者都更新完才读取，这都不是脏读，因为得到的是更新前的有效值，或完全更新后的值。
            2、如果那个用户更新一半你就读取了，也就是说更新了A，正打算要更新B但尚未更新时，就读取了，此时得到的就是脏数据。

    **线程同步重要概念：临界区Critical Section、互斥量Mutex、信号量Semaphore、事件event

    一、threading.Event类：使用一个内部的标记flag，通过flag的True或False的变化来进行操作
        set（）：标记设置为True
        clear（）：标记设置为False
        is_set（）：标记是否为True
        wait（timeout=None）：设置等等标记为True的时长，None为无线等待。等到返回True。未等到超时了返回Fa

    二、threading.Lock类: 锁，凡是存在共享资源争抢的地方都可以使用锁，从而保证只有一个使用者可以完全使用这个资源。
        当前线程在读共享的资源的时候，锁住，让其他S线程看不了.
        获取：lock.acquire（）
            锁可以解决共享资源，但要特别注意死锁。死锁：所有线程都在等释放，使用锁的过程中，导致所有线程者
        释放：lock.release（）
            即使任务完成，退出，退出之前也要释放。否则其他线程一直在获取锁，一直卡死

        锁保证原子性，金融局点，特别敏感，关心的正确的结果，结果正确比效率更重要，所以一定要加锁，保证数据保证完整性，如生产100个杯子，分10个线程，
        每个线程生产10个，作为局部变量返回。但是有的线程忙，一生产不完怎么办？即木桶原理

        加锁、解锁语句：
            加锁和解锁之间的代码实现有可能因为异常，线程异常退出，而未解锁，导致死锁。因此，加锁解锁。
            1、使用try．．．finally．．．语句，保证锁释放
            2、with上下文管理，锁对象支持上下文管理。有enter和exist魔术方法的对象都支持上下文管理
        注意事项：
            1、少用锁，必要时用锁。使用了锁，多线程访问被锁的资源时，就成了串行，要么排队执行，要么争抢执
            2、加锁时间越短越好，不需要就立即释放
            3、一定要避免死锁

"""
import datetime
import threading
import time

from tool.logger_define import LoggerDefine


logger = LoggerDefine().get_logger()


class CupDemo:
    """
    # 案例1、老板雇佣了一个工人生产杯子，一直等工人，直到生产了10个杯子
    """
    def __init__(self):
        self.cups = []
        self.ev = threading.Event()

    def boss(self):
        while True:
            if self.ev.wait():
                logger.info('{}:Good job'.format(threading.current_thread().name))
                return
            time.sleep(1)

    def worker(self, num):
        cur_name = threading.current_thread().name
        logger.info("{}:I'm working for you.".format(cur_name))
        while True:
            logger.info('{}:make 1'.format(cur_name))
            time.sleep(0.1)
            self.cups.append(1)
            if len(self.cups) == num:
                self.ev.set()
                break
        logger.info('{}:I finished my job'.format(cur_name))

    def run_demo(self):
        threading.Thread(target=self.boss, name='boss').start()
        threading.Thread(target=self.worker, args=(10,), name='worker').start()


class TimerDemo:
    """
    案例2、实现threading.Timer 延时器。延时执行一个函数
    1、start后，等待interval后，开启一个新线程执行函数：Event.wait()
    2、cancel功能：Event.set()
    3、run function：not Event.set()
    4、需要的参数：interval，全局的Event

    """
    def __init__(self, interval, func, *args, **kwargs):
        self.ev = threading.Event()
        self.interval = interval
        self.args = args
        self.kwargs = kwargs
        self.func = func

    def start(self):
        self._run()

    def cancel(self):
        self.ev.set()

    def _run(self):
        logger.info('waiting')
        start = datetime.datetime.now()
        self.ev.wait(timeout=self.interval)
        if not self.ev.set():
            logger.info(self.args)
            self.func(*self.args, **self.kwargs)
        logger.info('finished:{}'.format((datetime.datetime.now() - start).total_seconds()))


class LockDemo:
    """
    案例3：锁，10个工人生产100个杯子
    1、杯子总数作为全局变量，必须每次只能一个人修改，避免脏数据。
    2、边界处理，避免生产了99个杯子的时候，每个工人读取还差一个，都去生产
    """
    def __init__(self, cup_num=100, workers=10):
        self.lock = threading.Lock()
        self.cup = []
        self.num = cup_num
        self.workers = workers

    def worker(self):
        while True:
            self.lock.acquire()
            count = len(self.cup)
            logger.info('{}: cup num:{}'.format(threading.current_thread().name, count))
            # self.lock.release()
            if count >= self.num:
                self.lock.release()   # 此处不释放，造成死锁，其余线程一直在等待
                break
            time.sleep(0.01)  # 构造切换线程效果
            # self.lock.acquire()  本行和135行，构造了脏数据的过程。假设生产了99个杯子，线程A刚好读到了99，释放线程；
            # 线程B也读到了99个杯子，在本行获取锁，生产杯子；但是线程A不知道线程B已经生产了第100个杯子，当线程B生产完释放线程后，
            # 线程A接着生产，导致杯子总是大于100.同时本行和135行不应该有锁操作，因为读取和写入，是生产杯子的一个最小原子任务，
            # 分别加锁，破坏了原子任务，导致超出边界。
            logger.info('{}: make 1,res:{}'.format(threading.current_thread().name, count))
            self.cup.append(1)
            self.lock.release()

    def run_product(self):
        for i in range(self.workers):
            threading.Thread(target=self.worker, name='work_{}'.format(i)).start()


class CounterLockDemo:
    """
    案例4、加锁、解锁。实现计数器
    一般来说，加锁、解锁之间，有一段代码实现，当代码异常导致线程异常退出时，锁未释放，造成死锁。
    python避免上述问题的加解锁语句：
    1、try...finally...
    2、with上下文管理：有enter和exist魔术方法的对象支持上下文管理。Lock对象支持上下文管理
    """
    def __init__(self, lock: threading.Lock):
        self.val = 0
        self.lock = lock

    def inc(self):
        try:
            self.lock.acquire()
            self.val += 1
        finally:
            self.lock.release()

    def dec(self):
        with self.lock:
            self.val -= 1

    @property
    def value(self):
        return self.val


def run_counter(c: CounterLockDemo, count=100):
    for _ in range(count):
        for i in range(-50, 50):
            if i < 0:
                c.dec()
            else:
                c.inc()


if __name__ == '__main__':
    # CupDemo().run_demo()
    # TimerDemo(1, lambda x, y: x+y, 3, 4).start()
    # LockDemo(cup_num=100, workers=10).run_product()
    co = CounterLockDemo(threading.Lock())
    for i in range(10):
        threading.Thread(target=run_counter, args=(co,)).start()
    while True:
        if threading.active_count() == 1:
            logger.info('thread:{},res:{}'.format(threading.enumerate(), co.value))
            break
        logger.info('current value:{}'.format(co.value))

