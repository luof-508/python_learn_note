# coding = utf-8
"""
二叉树的性质：
性质1、在二叉树第i层，至多有2^(i-1)个节点
性质2、深度为n的二叉树，最多有2^(n)-1个节点
性质3、任何一棵二叉树，如果其终端节点数为n0，度数为2的节点数为n2，则有n0=n2+1
性质4、含有n个节点的完全二叉树，深度为：int(log2(n))+1或math.ceil(log2(n+1))
性质5、一棵n个节点的完全二叉树：假设根节点序号i=1，则其第m个节点有：
      当2*m <= n,则节点m有左孩子；
      当2*m + 1 <= n,则节点m有右孩子。
其他性质、含有n个节点的二叉树，高度至多为n、至少为math.ceil(log2(n+1))

树的遍历：对树中所有元素不重复的遍历一遍
广度优先：层序遍历
深度优先：前序遍历、中序遍历、后序遍历
遍历序列：将树中所有元素遍历后，得到的元素序列。将层次结构转换为线性结构

二叉树的遍历：左子树必须在右子树的前面。深度优先中的前、中、后是指根节点位于遍历序列中的前面、中间或后面   递归遍历


堆排序：不稳定算法
堆是一个完全二叉树
大顶堆：每一个非叶子节点都要大于等于左右孩子。小顶堆则相反
根节点：一定是大顶堆中的最大值，小顶堆打最小值
稳定：序列中，值相同的不同元素，顺序也是稳定的
核心算法：对堆节点的调整。
        度数为2的节点A，如果其左右孩子的值比它大，将最大值与之交互；
        度数为1的节点A，如果其左孩子比起大，则与之交互；
        如果节点A被调整到其他位置了，还需要和其孩子节点重复上述过程；（递归）
排序过程：1、首先写一个函数，实现对单个叶子进行调整 -- 首次调整为大顶堆；拿走极值后，对根节点进行堆调整
时间复杂度：O(nlog(n)),对原始状态的顺序不敏感
空间复杂度：O(1)
"""
__author__ = 'fg.luo'

import logging
import math
import random
import time


def set_log():
    # 实例化日志
    _logger = logging.getLogger(__name__)
    _logger.setLevel(level=logging.INFO)  # logger等级总开关
    # 创建一个控制台handler
    ch = logging.StreamHandler()
    # 定义handler输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    ch.setFormatter(formatter)
    ch.setLevel(level=logging.INFO)
    _logger.addHandler(ch)
    return _logger


logger = set_log()


class HeapSolution:
    def __init__(self, seq: list):
        self.seq = [0] + seq
        self.num = len(seq)
        self.depth = math.ceil(math.log2(self.num + 1))

    def heap_sort_procedure(self):
        logger.info('Start to change the origin seq as a big heap')
        logger.info('Origin seq:{}'.format(self.seq[1:]))
        self.big_heap()

        logger.info('print big heap>>>>>')
        self.print_tree_tool(self.seq[1:])

        logger.info('Swap the root node with the last leaf node, and re sort the rest of seq as a big heap')
        for i in range(self.num, 0, -1):
            self.seq[1], self.seq[i] = self.seq[i], self.seq[1]
            self.adjust_node(1, i-1)
            logger.info('re sort as a big heap:{}'.format(self.seq[1:i-1]))

        logger.info('sort result: {}'.format(self.seq[1:]))
        return self.seq[1:]

    def big_heap(self):
        """
        构造大顶堆
        :return:
        """
        logger.info('Sort the tree as a big heap')
        start_point = self.num // 2
        for i in range(start_point, 0, -1):
            self.adjust_node(i, self.num)
        logger.info('big heap result:{}'.format(self.seq[1:]))

    def adjust_node(self, point, seq_len):
        """
        实现对堆节点调整
        :param point:
        :param seq_len:
        :return:
        """
        if 2 * point > seq_len:
            return
        max_son_idx = 2*point
        if 2*point + 1 <= seq_len:
            max_son_idx = 2*point if self.seq[2*point] > self.seq[2*point+1] else 2*point+1
        if self.seq[point] < self.seq[max_son_idx]:
            self.seq[point], self.seq[max_son_idx] = self.seq[max_son_idx], self.seq[point]
            self.adjust_node(max_son_idx, seq_len)

    @staticmethod
    def print_tree_tool(seq):
        """
        打印一棵树
        间距规律：高度为n的完全二叉树，节点间的间距为8个字符(包含上一层双亲数字占位),单个数字占位为2个字符串,
                   则 第x层第一个数字的缩进为 节点间的间距 + 字符占位：(2**(n-x) - 1) * 3 + 2**(n-x-1) * 2
                每一层计算方法： 缩进 + 字符占位 + 字符间距
        :param seq:
        :return:
        """
        layer = math.ceil(math.log2(len(seq)+1))
        last_sep = '        '  # 最后一层节点间距8个字符串
        str_sep = len(str(max(seq))) * ' '  # 单个数字占位
        half_sep = '   '  # 半个间距3个字符
        str_lst = []
        logger.info('layer:{}, the seq:{}'.format(layer, seq))
        for i in range(layer, 0, -1):
            all_front_layer = 2**(i-1) - 1
            start_idx = all_front_layer
            cur_num = 2**(i-1)
            cur_print = ''
            if i < layer:
                tuck = (2**(layer-i) - 1) * half_sep + 2**((layer-i)-1) * str_sep
                cur_print = tuck + cur_print
            for _ in range(cur_num):
                cur_print = cur_print + '{:^2}'.format(seq[start_idx]) + 2**(layer-i) * last_sep + (2**(layer-i)-1) * str_sep
                start_idx += 1
                if start_idx == len(seq):
                    break
            str_lst.append(cur_print)
        for s in range(len(str_lst)-1, -1, -1):
            print(str_lst[s])

    @staticmethod
    def print_tree_learn(seq):
        layer = math.ceil(math.log2(len(seq)+1))
        max_node = (2**layer - 1)*layer
        idx = 0
        for i in range(1, layer+1):
            cur_print_str = ''
            for j in range(2**(i-1)):
                cur_print_str = cur_print_str + '{:^{}}'.format(seq[idx], max_node) + ' '
                idx += 1
                if idx == len(seq):
                    break
            print(cur_print_str)
            max_node = max_node // 2


if __name__ == '__main__':
    origin = [random.choice(range(100)) for s in range(int(input('enter the length>>>')))]
    heap_sol = HeapSolution(origin)
    heap_sol.print_tree_learn(origin)
    time.sleep(1)
    heap_sol.heap_sort_procedure()

