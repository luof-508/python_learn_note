# 无参装饰器
# 是一个函数
# 函数作为形参
# 返回值必须是一个函数
# 可使用@functionname，简化调用
import datetime
import time


def logger(func):
    def wrapper(*args, **kwargs):
        print("args = {}, kwargs = {}".format(args, kwargs))
        start = datetime.datetime.now()
        ret = func(*args, **kwargs)
        end = datetime.datetime.now() - start
        print("function {} took {}s.".format(func.__name__, end.total_seconds()))
        return ret
    return wrapper


@logger
def add(*args, **kwargs):
    print("====call add====")
    time.sleep(2)
    return sum(args) + sum(kwargs.values())


print(add(1, 2, 3, x=4, y=5))
