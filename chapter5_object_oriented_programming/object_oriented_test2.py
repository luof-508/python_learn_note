#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/23
@File: object_oriented_test2.py
用面向对象实现链表LinkedList
单向链表实现append,iter_nodes
双向链表实现append,pop,insert,remove,iter_nodes


## 需求分析
**根据链表结构特征进行抽象，需要设计两个类**：
- 节点类：记录节点元素信息，包括节点value，节点指针seek，上一个节点和下一个节点位置
- 容器类：保存每一个节点，记录链表头head、尾tail；因为数据在容器，因此还需在容器实现链表的增、闪、改、查。

head、tail：记录起始、终止位置
"""


class LinkedNode:
    def __init__(self, info, next_seek=None, front_seek=None):
        self.info = info
        self.next_seek = next_seek
        self.front_seek = front_seek


class LinkedList:
    def __init__(self):
        # 所谓的链表无序，是指链表的一个个节点在内存中存在任何地方，不是在堆栈中有序保存的，通过指针，指向下一个节点在内存中的位置。
        # 这里的用列表只是一个容器，节点总要保存吧，与链表无序是两回事,而且列表保存的是链表的引用，只是一个个ID。
        self.__linked_list = []  # 不需要插入的列表来说，检索方便，但是插入、remove不合适

    def append(self, node: LinkedNode):
        if self.__linked_list:
            self.__linked_list[-1].next_seek = id(node)
        self.__linked_list.append(node)

    def iter_nodes(self, reverse=False):
        n = len(self.__linked_list)
        while n > -1:
            yield self.__linked_list[n]
            n -= 1


class DoubleLinkedList(LinkedList):
    """使用列表索引，暴力解法
    优点：检索方便
    缺点：对于频繁插入、remove的运用场景，效率太低，不合适"""
    def __init__(self):
        super(DoubleLinkedList, self).__init__()
        self.__linked_list = []

    def append(self, node: LinkedNode):
        if self.__linked_list:
            self.__linked_list[-1].next_seek = id(node)
            node.front_seek = id(self.__linked_list[-1])
        self.__linked_list.append(node)

    def pop(self, node_seek):
        node_idx = None
        for idx, cur_node in enumerate(self.__linked_list):
            if id(cur_node) == node_seek:
                node_idx = idx
                break
        # todo 考虑起点、终点、以及节点不存在情况
        back_node = self.__linked_list[node_idx-1]
        next_node = self.__linked_list[node_idx + 1]
        back_node.next_seek = id(next_node)
        next_node.front_seek = id(back_node)
        return self.__linked_list.pop(node_idx)

    def remove(self, node: LinkedNode):
        node_id = id(LinkedNode)
        for idx, cur_node in enumerate(self.__linked_list):
            if id(cur_node) == node_id:
                # todo 考虑起点、终点、以及节点不存在情况
                self.__linked_list[idx-1].next_seek = id(self.__linked_list[idx+1])
                self.__linked_list[idx+1].front_seek = id(self.__linked_list[idx - 1])
                break
        return self.__linked_list.remove(node)

    def insert(self, node: LinkedNode, insert_seek):
        node_id = id(LinkedNode)
        insert_idx = None
        for idx, cur_node in enumerate(self.__linked_list):
            if id(cur_node) == insert_seek:
                # todo 考虑起点、终点、以及节点不存在情况
                insert_idx = idx+1
                self.__linked_list[idx].next_seek = node_id
                self.__linked_list[idx+1].front_seek = node_id
                node.front_seek = id(self.__linked_list[idx])
                node.next_seek = id(self.__linked_list[idx+1])
                break
        self.__linked_list.insert(insert_idx, node)


# 不带列表解法
class Item:
    def __init__(self, val, next_node=None, front_node=None):
        self.val = val
        self.next_node = next_node
        self.front_node = front_node

    def __repr__(self):
        return str(self.val)

    def __str__(self):
        return str(self.val)


class LinkedListImprove:
    """
    容器，记录节点，实现迭代、append、pop、insert、remove、getitem
    append:增加节点
    pop:从尾部弹出节点
    insert:在指定索引处插入节点，超界头部或尾部插入
    remove:移除指定索引处的节点，超界移除尾部
    getitem:获取指定索引节点
    """
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, val):
        """尾部增加节点"""
        node = Item(val)
        # 更新head、tail
        # 0个节点、1个节点、2个节点情况
        if self.head is None:
            self.head = node
        else:
            self.tail.next_node = node
            node.front_node = self.tail
        self.tail = node

    def iter_items(self, reverse=False):
        # 支持正反迭代
        current = self.tail if reverse else self.head
        while current:
            yield current
            current = current.front_node if reverse else current.next_node

    def getitem(self, idx):
        """获取指定索引处的节点"""
        current = None
        for i, tmp_node in enumerate(self.iter_items()):
            if i == idx:
                current = tmp_node
                break
        if current is None:
            raise IndexError('Index out of range')
        return current

    def pop(self):
        """从尾部弹出节点"""
        if self.head is None:  # 没有节点
            raise Exception('Empty')

        ret_node = self.tail
        prev = ret_node.front_node
        if prev is None:  # 只有1个节点
            self.head = None
        else:  # 两个或以上
            prev.next_node = None
        self.tail = prev
        return ret_node

    def insert(self, idx, val):
        """在指定索引处插入节点,超界尾部追加"""
        node = Item(val)
        current = None
        for i, tmp_node in enumerate(self.iter_items()):
            if i == idx:
                current = tmp_node
                break
        # 超界尾部追加
        if current is None:
            self.append(val)
            return
        # 头部插入，处理head
        prev = current.front_node
        if prev is None:
            node.next_node = current
            current.front_node = node
            self.head = node
        else:
            # 中间插入
            prev.next_node = node
            node.front_node = prev
            node.next_node = current
            current.front_node = node

    def remove(self, idx):
        """移除指定索引处的节点，超界return"""
        current = None
        for i, tmp_node in enumerate(self.iter_items()):
            if i == idx:
                current = tmp_node
                break
        if current is None:
            return
        prev = current.front_node
        next_node = current.next_node
        # 只有一个节点
        if prev is None and next_node is None:
            self.head = None
            self.tail = None
        # 头部移除，两个以上节点
        elif prev is None and next_node:
            next_node.front_node = None
            self.head = next_node
        # 尾部移除，两个以上节点
        elif prev and next_node is None:
            prev.next_node = None
            self.tail = prev
        else:
            prev.next_node = next_node
            next_node.front_node = prev
        del current


if __name__ == '__main__':
    lst = LinkedListImprove()
    item = Item('start')
    lst.append(item)
    item = Item(1)
    lst.append(item)
    item = Item(2)
    lst.append(item)
    item = Item(3)
    lst.append(item)
    item = Item(4)
    lst.append(item)
    item = Item(5)
    lst.append(item)
    item = Item(6)
    lst.append(item)
    item = Item('mid')
    lst.append(item)
    item = Item(7)
    lst.append(item)
    item = Item(8)
    lst.append(item)
    item = Item('end')
    lst.append(item)
    for n in lst.iter_items():
        print(n)
    print('~~~~~~~~~~~~~~~~~~~~~')
    lst.pop()
    lst.pop()
    lst.pop()
    for n in lst.iter_items():
        print(n)
    print('~~~~~~~~~~~~~~~~~~~~~')
    lst.insert(1, 0)
    lst.insert(0, 'enter')
    lst.insert(15, 'exit')
    for n in lst.iter_items():
        print(n)
    print('~~~~~~~~~~~~~~~~~~~~~')
    lst.remove(0)
    lst.remove(8)
    lst.remove(8)
    lst.remove(8)
    for n in lst.iter_items():
        print(n)
    print('~~~~~~~~~~~~~~~~~~~~~')

