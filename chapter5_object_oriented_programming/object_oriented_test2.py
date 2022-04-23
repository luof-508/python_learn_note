#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/23
@File: object_oriented_test2.py
用面向对象实现链表LinkedList
单向链表实现append,iter_nodes
双向链表实现append,pop,insert,remove,iter_nodes


链表：
表头head：记录起始位置
节点node：记录元素、指向下一个节点位置；最后一个节点指向为None
双向链表节点：记录元素，以及上一个节点和下一个节点位置


分析：
根据链表特征，及需求，
节点抽象为一个类：记录节点元素信息，以及下一个节点id
链表抽象为一个类：保存每一个节点，用字典保存，key作为节点实例id，value为节点
如何遍历链表，列表，id记录索引，下一个节点放进来，自动更新上一个节点的指针。
"""


class LinkedNode:
    def __init__(self, info, next_seek, back_seek=None):
        self.info = info
        self.next_seek = next_seek
        self.back_seek = back_seek


class LinkedList:
    def __init__(self):
        self.__linked_list = []

    def append(self, node: LinkedNode):
        if self.__linked_list:
            self.__linked_list[-1].next_seek = id(node)
        self.__linked_list.append(node)

    def iter_nodes(self):
        yield from self.__linked_list


class DoubleLinkedList(LinkedList):
    def __init__(self):
        super(DoubleLinkedList, self).__init__()
        self.__linked_list = []

    def append(self, node: LinkedNode):
        if self.__linked_list:
            self.__linked_list[-1].next_seek = id(node)
            node.back_seek = id(self.__linked_list[-1])
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
        next_node.back_seek = id(back_node)
        return self.__linked_list.pop(node_idx)

    def remove(self, node: LinkedNode):
        node_id = id(LinkedNode)
        for idx, cur_node in enumerate(self.__linked_list):
            if id(cur_node) == node_id:
                # todo 考虑起点、终点、以及节点不存在情况
                self.__linked_list[idx-1].next_seek = id(self.__linked_list[idx+1])
                self.__linked_list[idx+1].back_seek = id(self.__linked_list[idx-1])
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
                self.__linked_list[idx+1].back_seek = node_id
                node.back_seek = id(self.__linked_list[idx])
                node.next_seek = id(self.__linked_list[idx+1])
                break
        self.__linked_list.insert(insert_idx, node)


if __name__ == '__main__':
    pass
