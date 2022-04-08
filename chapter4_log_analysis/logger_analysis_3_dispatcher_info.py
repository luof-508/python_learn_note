#!/usr/bin/env python3
# coding=utf-8
"""
@author: feng.luo
@time: 2022/4/7
@File: logger_analysis_3_dispatcher_info.py
生产者-消费者模型：编程中凡是有上下级关系的，都可以称为生产者消费者模型。
    这种模型，速度很难做到统一，因此有了消息队列，起到缓冲作用。
    水库，干涸期和**期，但是水库蓄洪也有能力的，所以消息队列也有上限。
    消费者能力一般要大于生产者，略大于都不行，万一有一个消费者挂了呢。

queue模块：

"""
import random
from queue import Queue

q = Queue()
q.put(random.randint(1, 100))
q.put(random.randint(1, 100))
print(q.get())
print(q.get())
print(q.get(timeout=3))

if __name__ == '__main__':
    pass
