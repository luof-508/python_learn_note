"""
切片操作
1、切片返回的是一个列表，左闭右开
2、切片和.copy()都是浅拷贝，只拷贝最外层元素，内层元素都是拷贝的引用
3、lst[start_index:end_index:step]中，三个参数都是可选的:
    start_index: 切片操作起始索引
    end_index: 切片操作终止索引
    step:步长, step的符号，决定了正向切片还是负向切片
（一）start_index、end_index、step三者可同为正、同为负，或正负混合。 但必须遵循一个原则，即：
    当start_index表示的实际位置在end_index的左边时，从左往右取值，此时step必须是正数（同样表示从左往右）；
    当start_index表示的实际位置在end_index的右边时，表示从右往左取值，此时step必须是负数（同样表示从右往左），即两者的取值顺序必须相同。
    当start_index或end_index省略时，取值的起始索引和终止索引由step的正负来决定，这种情况不会有取值方向矛盾（即不会返回空列表[]），
    但正和负取到的结果顺序是相反的，因为一个向左一个向右。

（二）step的正负是必须要考虑的，尤其是当step省略时。
     比如 a[-1:] ，很容易就误认为是从“终点”开始一直取到“起点”，即 a[-1:]= [9, 8, 7, 6, 5, 4, 3, 2, 1, 0] ，
     但实际上 a[-1:]=[9] （注意不是9），原因在于step省略时step=1表示从左往右取值，
     而起始索引start_index=-1本身就是对象的最右边元素了，再往右已经没数据了，因此结果只含有 a[-1] 一个元素。

4、start_index和end_index可以是正索引，也可以是负索引，切片是在[start_index, end_index)包含的元素内，按照步长step进行操作
例如：lst = [0, 1, 2, 3, 4, 5, 6, 7, 8]
     res = lst[-1:-3:-1] ->
     因为step为负，为负向切片，[-1，-3)负向取值区间内有元素， next_index = start_index = -1 ->
     res[0]=lst[-1]，next_index = next_index + step = -2 ->
     res[1]=lst[-2]，next_index = next_index + step = -3 ，超出范围了，直接返回
"""
lst = [0, 1, 2, 3, 4, 5, 6, 7, 8]
print(lst[-1::1])
