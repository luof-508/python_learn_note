"""
需求： 将字典扁平化
"""

src_dict = {"a": {"b": 1, "c": 2}, "d": {"e": 3, "f": {"g": 4}}}
dst_dict = {"a.b": 1, "a.c": 2, "d.e": 3, "d.f.g": 4}


class MyFlatMethod(object):
    def __init__(self):
        self.destination = {}

    def primary_method(self, dic, key=''):
        for k, v in dic.items():
            if isinstance(v, dict):
                self.primary_method(v, key=key+k+'.')  # 递归调用
            else:
                self.destination[key+k] = v

    def prove_method(self, dic, dst=None, key=''):
        if dst is None:
            dst = {}
        for k, v in dic.items():
            if isinstance(v, dict):
                self.prove_method(v, dst, key=key+k+'.')
            else:
                dst[key+k] = v
        return dst

    def flat_map(self, src):
        def _flatmap(src1, dst1=None, key=''):
            for k, v in src1.items():
                if isinstance(v, dict):
                    _flatmap(v, dst1, key=key+k+".")
                else:
                    dst1[key+k] = v
        dst = {}
        _flatmap(src, dst)
        return dst


res = MyFlatMethod()
res.primary_method(src_dict)
print(res.destination)

print(res.prove_method(src_dict))

print(res.flat_map(src_dict))

