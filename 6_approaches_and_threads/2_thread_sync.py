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
        wait（timeout=None）：设置等等标记为True的时长，None为无线等待。等到返回True。未等到超时了返回False
        ***使用场景：老板雇佣了一个工人，等工人生产杯子。---等待工作线程完成，实现线程间通信

    二、threading.Lock类: 锁，凡是存在共享资源争抢的地方都可以使用锁，从而保证只有一个使用者可以完全使用这个资源。当前线程在读共享的资源的时候，锁住，让其他线程看不了.
        获取：lock.acquire（blocking=True, timeout=-1），成功获取锁，返回True，否则返回False
            blocking=True:默认阻塞锁，阻塞可以设置超时时间。非阻塞锁blocking=False，禁止设置timeout.
        释放：lock.release（）
            即使任务完成，退出，退出之前也要释放。否则其他线程一直在获取锁，一直卡死

        锁可以解决共享资源，但要特别注意死锁。
        死锁：所有线程都在等释放，使用锁的过程中，导致所有线程都在相互等待，都没人释放，都出现阻塞状态。

        锁保证原子性，金融局点，特别敏感，关心的正确的结果，结果正确比效率更重要，所以一定要加锁，保证数据保证完整性，如生产100个杯子，分10个线程，
        每个线程生产10个，作为局部变量返回。但是有的线程忙，一生产不完怎么办？即木桶原理

        加锁、解锁语句：
            加锁和解锁之间的代码实现有可能因为异常，线程异常退出，而未解锁，导致死锁。因此，加解锁非常重要。
            1、使用try．．．finally．．．语句，保证锁释放
            2、with上下文管理，锁对象支持上下文管理。有enter和exist魔术方法的对象都支持上下文管理

        ***应用场景：适用于访问和修改同一个共享资源的时候，即读写同一个资源的时候。如果全都是读取同一个资源不需要锁

        注意事项：
            1、少用锁，必要时用锁。使用了锁，多线程访问被锁的资源时，就成了串行，要么排队执行，要么争抢执
            2、加锁时间越短越好，不需要就立即释放
            3、一定要避免死锁
    三、threading.Rlock类：可重入锁,是线程相关的锁。
        线程A获得可重复锁，并可以多次成功获取，不会阻塞。最后要在线程A中做和acquire次数相同的release。
        获取：threading.Rlock().acquire()
        释放：threading.Rlock.release()

    四、threading.Condition(lock=None)类：可传入一个Lock或Rlock对象，不传默认是RLock
        方法：
        acquire():获取锁
        wait(timeout=None):可设置超时时间
        notify(n=1)：唤醒至多指定数目个线程，没有等待的线程就不做任何操作
        notify_all()：唤醒所有等待的线程
        ***使用场景：用于生产者、消费者模型，为了解决生产者和消费者速度匹配同步问题。
        注意：因为Condition内部默认使用了Rlock，因此必须先acquire，用完要release。最好使用with上下文。
             消费者wait；生产者生产好消息后，对消费者发通知，使用notify或notify_all方法
        一个生产者对多个消费者时，实现了消息的一对多，这其实就是广播。
        本例只做演示用，线程不安全.消费者再读的时候可能生产者又在生产新的

    五、threading.Barrier(parties, action=None, timeout=None)类：栅栏、屏障。
        理解：将线程分组，parities为一组，当达到parities个时，放行，循环下一组进入等待
        n_waiting属性: 返回栅栏中处于等待的线程数
        parities: 指定的等待数目
        wait(timeout=None)方法:设置等待,返回0-parities数字。可以设置超时时间，超时后栅栏被打破abort，等待中的线程或调用等待方法的线程中，
                           都会抛出BrokenBarrierError异常，直到reset方法恢复栅栏
        broken属性：如果栅栏处于打破状态，返回True
        abort()方法：打破栅栏
        reset()方法：恢复栅栏

        执行逻辑：所有线程冲到barrier前等待，直到达到parities数目的线程，栅栏打开，所有线程继续执行。再有线程wait，继续循环
        例如：赛马比赛，所有马匹达到栅栏就位，开闸放马，再关闸。下一批马匹陆续就位后再开闸

        应用：并发初始化。所有线程都必须初始化完成后，才能继续工作。例如：运行程序前，加载数据、检查，如果这些工作没完成，就开始运行将不能正常工作。
            又如：启动一个程序，需要先加载磁盘文件、缓存预热、初始化连接池等工作，这些工作齐头并进，不过只有都准备好了，程序才能继续向后执行；
            假设数据库连接失败，则初始化工作失败，就要abort，屏障broken，所有线程收到异常退出

    六、信号量：
        threading.Semaphore(value=1):信号量，类似锁，信号量对象内部维护一个倒计数器，每acquire一次，减1，当acquire方法发现计数器为0时，
                                     就阻塞请求的线程，直到其他线程对信号量release后，计数大于0，恢复阻塞的线程。
            acquire()方法：获取信号量，计数器减1，获取成功返回True
            release()方法：释放信号量，计数器加1
            计数器永远不会低于0，acquire的时候发现是0，都会被阻塞
        应用场景：使用信号量semaphore解决资源有限的问题。
            实例：创建连接池
            池有最多连接数
            可以从池中取连接
            连接返回到池
            线程安全

        threading.BoundedSemaphore(value=1): 有界信号量
            应用：Semaphore类，在未acquire，直接release时，会超上界。BoundedSemaphore，不允许超出初始值范围，否则抛出ValueError异常

    信号量和锁：
        锁，只允许同一时间一个线程独占资源。它是特殊的信号量，即信号量计数器初值为1.
        信号量，允许多个线程访问共享资源，但这个共享资源数量有限
        锁可以看做特殊的信号量

数据结构和GIL
    queue模块：
        标准库queue模块，提供FIFO的queue、LIFO的队列、有限队列。
        queue类是线程安全的，适用于多线程间安全的交换数据。内部使用了Lock和Condition
    GIL全局解释器锁：
        Cpython在解释器进程级别有一把锁，叫GIL全局解释器锁。
        GIL保证Cpython进程中，只有一个线程执行字节码。甚至在多核cpu的情况下，也是如此。
        因此Cpython中，严格意义上没有多线程，同一时刻只有一个线程。Cpython中，多线程适用于：
            IO密集型，由于线程阻塞，就会调度其他线程；
            cpu密集型，当前线程可能会连续的获得GIL，导致其他线程几乎无法使用CPU，因为处于等待的线程重新激活，相比正在跑的线程，需要更多的时间，导致一直抢不到锁。
            因此：IO密集型，使用多线程；CPU密集型，使用多进程，绕开GIL。

            IO密集型：写的程序大量访问网络、访问文件。
            CPU密集型：写的程序大量的计算，就是CPU密集型。

    由于GIL的存在，Cpython中，绝大多数内置数据结构的读写（append、add）都是原子操作，在多线程中都是线程安全的。但是，实际上它们本身不是线程安全的类型。

python线程同步总结：
    因为GIL全局解释器锁的存在，看到python内置数据结构读写都是原子操作，如果真的要实现线程安全，可以读queue原码，如何去加锁实现线程安全的
    Event：简单的wait，等一个状态的变化，就可以用Event。boss--worker杯子模型
    Lock应用场景：访问和修改同一个共享资源的时候，即读写同一个资源的时候；默认阻塞锁。RLock可重入锁。   食堂窗口打饭模型
    Barrier：等等等，等大家都到齐了，并行初始化问题，就用barrier
    Condition要怎么用：做一对多通知，生产者消费者场景的时候，解决生产者---消费者速度不同步
    Semaphore怎么用：信号量，倒计数，资源池使用的时候；控制边界用BoundedSemaphore

"""
import datetime
import random
import threading
import time

from tool.logger_define import LoggerDefine


logger = LoggerDefine(__name__).get_logger


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


class Task:
    def __init__(self, name):
        self.name = name
        self.lock = threading.Lock()


class NotBlockLockDemo:
    """
    构造10个任务，即10把非阻塞锁，起5个线程去争抢任务。通过time.sleep强制线程切换，且获取到锁的线程不释放锁，演示非阻塞锁争抢到任务的不确定性
    """
    def __init__(self):
        self.task_lst = [Task('task-{}'.format(x)) for x in range(10)]

    def worker(self):
        for task in self.task_lst:
            time.sleep(0.01)
            if task.lock.acquire(False):
                logger.info('{} {} begin to start'.format(threading.current_thread(), task.name))
            else:
                logger.info('{} {} is working'.format(threading.current_thread(), task.name))

    def run_thread(self):
        for i in range(5):
            threading.Thread(target=self.worker, name='worker={}'.format(i)).start()


def sub(lock: threading.RLock):
    """
    可重入锁，获取了几次，就要释放几次，多释放会报错
    :param lock:
    :return:
    """
    lock.acquire()
    lock.acquire()
    lock.release()
    lock.release()
    lock.release()


class Dispatcher:
    """
    threading.Condition(lock=None)类：可传入一个Lock或Rlock对象，不传默认是RLock
        方法：
        acquire():获取锁
        wait(timeout=None):可设置超时时间
        notify(n=1)：唤醒至多指定数目个线程，没有等待的线程就不做任何操作
        notify_all()：唤醒所有等待的线程
        ***使用场景：用于生产者、消费者模型，为了解决生产者和消费者速度匹配同步问题。
        注意：因为Condition内部默认使用了Rlock，因此必须先acquire，用完要release。最好使用with上下文。
             消费者wait；生产者生产好消息后，对消费者发通知，使用notify或notify_all方法
        一个生产者对多个消费者时，实现了消息的一对多，这其实就是广播。
        本例只做演示用，线程不安全.消费者再读的时候可能生产者又在生产新的
    """
    def __init__(self):
        # 生产者线程、消费者线程
        # 生产者生产数字完成后，叫醒消费者；消费者排队等待产品，进入等待池
        # 数字要被上锁
        self.con = threading.Condition()
        self.ev = threading.Event()
        self.num = None

    def produce(self):
        # while not self.ev.is_set():
        for _ in range(10):
            with self.con:
                self.num = random.randrange(0, 100)
                logger.info('{} make the num:{}'.format(threading.current_thread().name, self.num))
                self.con.notify(2)  # 生产者生产完成，通知等待池的线程取产品
            self.ev.wait(1)  # 模拟生产速度
        logger.info('{} product over'.format(threading.current_thread().name))

    def costumer(self):
        while not self.ev.is_set():
            with self.con:
                self.con.wait()  # 消费者排队等产品，进入等待线程池
                # 当生产者使用while语句时，此处线程不安全，例如，当线程进入wait池，但是在这之前，执行了self.ev.set()，则生产者不获取锁，直接停止生产，wait池中的线程一直等待产品,进入死锁
                logger.info("{} get the num:{}".format(threading.current_thread().name, self.num))
                self.num = None
            self.ev.wait(0.5)  # 模拟消费速度
        logger.info('{} consumer completed'.format(threading.current_thread().name))

    def set_ev(self):
        self.ev.set()
        logger.info('finish')


class BarrierDemo:
    """
    threading.Barrier(parties, action=None, timeout=None)类：栅栏、屏障。
        理解：将线程分组，parities为一组，当达到parities个时，放行，循环下一组进入等待
        n_waiting属性: 返回栅栏中处于等待的线程数
        parities: 指定的等待数目
        wait(timeout=None)方法:设置等待,返回0-parities数字。可以设置超时时间，超时后栅栏被打破abort，等待中的线程或调用等待方法的线程中，
                           都会抛出BrokenBarrierError异常，直到reset方法恢复栅栏
        broken属性：如果栅栏处于打破状态，返回True
        abort()方法：打破栅栏
        reset()方法：恢复栅栏

        执行逻辑：所有线程冲到barrier前等待，直到达到parities数目的线程，栅栏打开，所有线程继续执行。再有线程wait，继续循环
        例如：赛马比赛，所有马匹达到栅栏就位，开闸放马，再关闸。下一批马匹陆续就位后再开闸

        应用：并发初始化。所有线程都必须初始化完成后，才能继续工作。例如：运行程序前，加载数据、检查，如果这些工作没完成，就开始运行将不能正常工作。
            又如：启动一个程序，需要先加载磁盘文件、缓存预热、初始化连接池等工作，这些工作齐头并进，不过只有都准备好了，程序才能继续向后执行；
            假设数据库连接失败，则初始化工作失败，就要abort，屏障broken，所有线程收到异常退出

    """
    @staticmethod
    def worker(barrier: threading.Barrier, x: int):
        logger.info('waiting for {} threads'.format(barrier.n_waiting))
        try:
            logger.info('Broken status:{}'.format(barrier.broken))
            if x < 3:
                barrier_id = barrier.wait(1)
            else:
                if x == 6:
                    barrier.reset()
                barrier_id = barrier.wait()
            logger.info('after barrier:{}'.format(barrier_id))
        except threading.BrokenBarrierError as e:
            logger.error('broken barrier, {}'.format(e))

    def run_barrier(self):
        barrier = threading.Barrier(3)
        for i in range(9):
            # if i == 2:
            #     barrier.abort()
            # elif i == 6:
            #     barrier.reset()
            threading.Event().wait(2)
            threading.Thread(target=self.worker, args=(barrier, i), name='worker_{}'.format(i)).start()


class SemaphoreDemo:
    @staticmethod
    def worker(s: threading.Semaphore):
        logger.info('in sub')
        s.acquire()
        logger.info('end sub')

    def run_s(self):
        s = threading.Semaphore(3)
        logger.info(s.acquire())
        logger.info(s.acquire())
        logger.info(s.acquire())
        logger.info('----------------')
        logger.info(s.acquire(False))
        logger.info(s.acquire(timeout=3))
        threading.Thread(target=self.worker, args=(s,)).start()
        s.release()


class Conn:
    def __init__(self, name):
        self.name = name


class ConnPoolLockDemo:
    """
    使用锁方法 创建一个连接池
    限制：
        池有最多连接数
        可以从池中取连接
        连接返回到池
        线程安全
    """
    def __init__(self, count):
        self.count = count
        self.lock = threading.Lock()
        self.pool = [Conn('pool_{}'.format(i)) for i in range(count)]

    def get_conn(self):
        self.lock.acquire()
        if self.pool:
            res_conn = self.pool.pop()
            self.lock.release()
            return res_conn
        return None

    def return_conn(self, conn):
        self.lock.acquire()
        if len(self.pool) < self.count:
            self.pool.append(conn)
            self.lock.release()
        else:
            logger.warning('exceed the threshold value: {}'.format(self.count))


class ConnPoolSemaphoreDemo:
    """
    信号量：
        threading.Semaphore(value=1):信号量，类似锁，信号量对象内部维护一个倒计数器，每acquire一次，减1，当acquire方法发现计数器为0时，
                                     就阻塞请求的线程，直到其他线程对信号量release后，计数大于0，恢复阻塞的线程。
            acquire()方法：获取信号量，计数器减1，获取成功返回True
            release()方法：释放信号量，计数器加1
            计数器永远不会低于0，acquire的时候发现是0，都会被阻塞
        应用场景：使用信号量semaphore解决资源有限的问题。
            实例：创建连接池
            池有最多连接数
            可以从池中取连接
            连接返回到池
            线程安全

        threading.BoundedSemaphore(value=1): 有界信号量
            应用：Semaphore类，在未acquire，直接release时，会超上界。BoundedSemaphore，不允许超出初始值范围，否则抛出ValueError异常

    信号量和锁：
        锁，只允许同一时间一个线程独占资源。它是特殊的信号量，即信号量计数器初值为1.
        信号量，允许多个线程访问共享资源，但这个共享资源数量有限
        锁可以看做特殊的信号量

    """
    def __init__(self, count):
        self.count = count
        self.sema = threading.Semaphore(3)
        self.pool = [Conn('pool_{}'.format(i)) for i in range(count)]

    def get_conn(self):
        self.sema.acquire()
        res_conn = self.pool.pop()
        return res_conn

    def return_conn(self, conn):
        self.pool.append(conn)
        self.sema.release()


class CanUesConnPoolSemaphoreDemo:
    def __init__(self, count: int):
        self.count = count
        self.sem = threading.BoundedSemaphore(count)
        self.conn_pool = [Conn('conn_{}'.format(i)) for i in range(count)]

    def get_conn(self):
        self.sem.acquire()
        return self.conn_pool.pop()

    def return_conn(self, conn):
        """
        异常场景：线程A/B/C都执行到第一句append，利用BoundedSemaphore超界抛ValueError异常，使用try...except...
        """
        try:
            self.conn_pool.append(conn)
            self.sem.release()
        except ValueError:
            self.conn_pool.pop(conn)


class RunPoolSemaphore:
    def __init__(self):
        self.pool = ConnPoolSemaphoreDemo(3)

    @staticmethod
    def semaphore_worker(pool: ConnPoolSemaphoreDemo):
        conn = pool.get_conn()
        logger.info(conn)
        # 模拟使用了一段时间
        threading.Event().wait(random.randint(1, 4))
        pool.return_conn(conn)

    def run_worker(self):
        for i in range(6):
            threading.Thread(target=self.semaphore_worker, args=(self.pool,)).start()


class MultiThreadEfficiency:
    def __init__(self):
        self.num = 1000000000

    @staticmethod
    def calc(num):
        res = 0
        for i in range(num):
            res += i

    def calc_thread_run(self):
        st = datetime.datetime.now()
        t1 = threading.Thread(target=self.calc, args=(self.num,))
        t2 = threading.Thread(target=self.calc, args=(self.num,))
        t3 = threading.Thread(target=self.calc, args=(self.num,))
        t4 = threading.Thread(target=self.calc, args=(self.num,))
        t5 = threading.Thread(target=self.calc, args=(self.num,))
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        logger.info('thread time:{}'.format((datetime.datetime.now() - st).total_seconds()))

    def not_thread_calc(self):
        start = datetime.datetime.now()
        self.calc(self.num)
        self.calc(self.num)
        self.calc(self.num)
        self.calc(self.num)
        self.calc(self.num)
        logger.info('not thread, time:{}'.format((datetime.datetime.now() - start).total_seconds()))


if __name__ == '__main__':
    # CupDemo().run_demo()
    # TimerDemo(1, lambda x, y: x+y, 3, 4).start()
    # LockDemo(cup_num=100, workers=10).run_product()
    # co = CounterLockDemo(threading.Lock())
    # for i in range(10):
    #     threading.Thread(target=run_counter, args=(co,)).start()
    # while True:
    #     if threading.active_count() == 1:
    #         logger.info('thread:{},res:{}'.format(threading.enumerate(), co.value))
    #         break
    #     logger.info('current value:{}'.format(co.value))
    # NotBlockLockDemo().run_thread()
    # disp = Dispatcher()
    # threading.Thread(target=disp.produce, name='produce').start()
    # threading.Thread(target=disp.costumer, name='costumer1').start()
    # threading.Thread(target=disp.costumer, name='costumer2').start()
    # time.sleep(3)
    # disp.set_ev()
    # BarrierDemo().run_barrier()
    # SemaphoreDemo().run_s()
    # RunPoolSemaphore().run_worker()
    # sem = threading.Semaphore(3)
    # sem.release()
    # sem.release()
    # print(sem.__dict__)

    MultiThreadEfficiency().not_thread_calc()
    # not_thread_calc-INFO: not thread, time:385.343603
    MultiThreadEfficiency().calc_thread_run()
    # calc_thread_run-INFO: thread time:354.982785
