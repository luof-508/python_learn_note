#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/5/8
@File: object_oriented_test4.py

面向对象-魔术方法之高级玩法1：将链表封装成容器，实现负向索引操作。
    魔术方法的容器方法有：__len__、__getitem__、__iter__、__setitem__
    `__getitem__(self, item)`：该方法实现了通过`lst[key]`方式访问容器元素的功能，对于字典，item就是key，对于序列对象item就是索引index，序列对象还切片功能也是通过该方法实现。
    `__setitem__(self, key, value)`: 该方法实现了通过`lst[key] = value`方法修改容器元素的功能，对于字典key、value就是键值对，序列对象就是在指定索引处插入的元素值.
    `__iter__`: 必须返回一个可迭代对象。
    `__len__`: 容器必须实现该方法。对于一个类的实例，如果位于逻辑表达式位置或bool(instance)，如果类中未实现bool，则会调用`__len__`。这也是为什么容器位于逻辑表达式位置时可以等效布尔。

"""


class Node:
    def __init__(self, value):
        self.value = value
        self.next_node = None
        self.front_node = None

    def __repr__(self):
        return str(self.value)

    __str__ = __repr__


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def __len__(self):
        num = 0
        for _ in self.__iter__():
            num += 1
        return num

    def __iter__(self, reverse=False):
        current = self.tail if reverse else self.head
        while current:
            yield current
            current = current.front_node if reverse else current.next_node

    def __getitem__(self, idx):
        """获取索引为idx的节点；支持负向索引

        通过lst[key]实现访问，字典item就是key，序列对象就是索引index ，序列对象还要能切片
        """
        reverse, real_idx = (False, idx) if idx >= 0 else (True, abs(idx)-1)
        for i, node in enumerate(self.__iter__(reverse=reverse)):
            if i == real_idx:
                return node
        raise IndexError('Index out of range')

    def __setitem__(self, idx, value):
        """指定索引插入节点, 超界尾部插入

        通过lst[key] = value实现修改，字典就是key、value对，序列对象就是在指定索引处插入元素
        """
        # 链表为空
        if self.head is None:
            self.append(value)
            return
        current_node = None
        reverse, real_idx = (False, idx) if idx >= 0 else (True, abs(idx)-1)
        for i, node in enumerate(self.__iter__(reverse)):
            if i == real_idx:
                current_node = node
                break
        # 正向索引超界，尾部插入;负向索引超界，头部插入
        if current_node is None:
            if idx >= 0:
                self.append(value)
                return
            current_node = self.head
        node = Node(value)
        prev = current_node.front_node
        # 头部插入,更新head
        if prev is None:
            self.head = node
        else:
            prev.next_node = node
        node.front_node = prev
        node.next_node = current_node
        current_node.front_node = node

    def append(self, value):
        """尾部追加节点"""
        node = Node(value)
        # 节点数为0
        if self.head is None:
            self.head = node
        else:
            self.tail.next_node = node
            node.front_node = self.tail
        self.tail = node

    def pop(self):
        """从尾部移除节点"""
        if self.tail is None:
            return
        ret_node = self.tail
        prev = self.tail.front_node
        if prev is None:
            # 只有一个节点
            self.head = None
        else:
            prev.next_node = None
        self.tail = prev
        return ret_node

    def remove(self, idx):
        """移除指定索引位置的节点"""
        current_node = self.__getitem__(idx)
        prev = current_node.front_node
        next_ = current_node.next_node
        # 尾部移除
        if next_ is None:
            self.pop()
            return
        # 头部移除，更新头部
        if prev is None:
            self.head = next_
        else:
            prev.next_node = next_
        next_.front_node = prev


if __name__ == '__main__':
    lst = LinkedList()
    lst.append(Node('start'))
    for j in range(1, 5):
        lst.append(Node(j))
    lst.append(Node('mid'))
    for j in range(5, 11):
        lst.append(Node(j))
    lst.append(Node('end'))
    # 测试迭代
    for cur_node in lst:
        print(cur_node, end=', ')
    print(), print('~~~~~~~~~~~~~')

    # 测试负向索引
    print(lst[-len(lst)], lst[-1])
    # print(lst[18])  # 测试索引超界异常
    print('~~~~~~~~~~~~~~~~~~~')

    # 测试__setitem__
    lst[len(lst)] = 'insert15'
    lst[0] = 'insert0'
    lst[3] = 'insert3'
    print(len(lst), lst[0], lst[3])
    print('~~~~~~~~~~~')

    # 测试负向索引操作
    lst[-1] = 'insert16'
    print(lst[-2])
    lst[-20] = 'insert_start'
    print(lst[0])
    print('*************')
    print(lst[0], lst[1], lst[-2], lst[-1])
    lst.remove(-len(lst)), lst.remove(-1)
    print(lst[0], lst[-1])

