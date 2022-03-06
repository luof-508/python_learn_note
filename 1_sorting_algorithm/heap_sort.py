class Solution:
        @staticmethod
        def restore_array(pairs: list) -> list:
            """
            nums是n个不同元素组成的数组
            在pairs中，首位的元素一定只出现一次；其余元素一定也只出现两次
            :param pairs:
            :return:
            """
            #  [[2,1],[3,4],[3,2]]
            # 找出首尾元素
            # 遍历pairs，存放到字典中，key=元素，values = [索引]
            import collections
            # 记录了每一个元素出现的索引
            idx_dic = collections.defaultdict(list)
            for idx, item in enumerate(pairs):
                idx_dic[item[0]].append(idx)
                idx_dic[item[1]].append(idx)

            start, start_idx = None, None
            for k, v in idx_dic.items():
                if len(v) == 1:
                    start = k
                    start_idx = v[0]
                    break
            n = len(pairs) + 1
            res = [start]
            nex = sum(pairs[start_idx]) - start
            res.append(nex)
            # 循环查找下一个元素：
            for i in range(1, n-1):
                idx_lst = idx_dic.get(nex)
                idx_1, idx_2 = idx_lst[0], idx_lst[1]
                if res[i-1] not in pairs[idx_1]:
                    cur = sum(pairs[idx_1]) - nex
                    res.append(cur)
                else:
                    cur = sum(pairs[idx_2]) - nex
                    res.append(cur)
                nex = cur
            return res


if __name__ == '__main__':
    # inputs = [[2, 1], [3, 4], [3, 2]]
    inputs = [[4,-2],[1,4],[-3,1]]
    result = Solution.restore_array(inputs)
    print(result)
