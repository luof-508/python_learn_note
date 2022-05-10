#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/5/9
@File: exception_handle_01.py

异常Exception：
    错误：逻辑错误，算法写错了，加法写成了减法；笔误，变量名写错，语法错误等；总之，错误是可以避免的（美好的愿望）。
    异常：程序本身没有错误，但在某些情况下，会出现一些意外，导致程序无法正常执行下去。比如访问网络过程中，突然断网，这就是异常。异常是不可避免的。异常处理甚至占据了程序的大部分。
    在高级编程语言中，一般都有错误和异常的概念。异常可以捕获并被处理，但是错误不能被捕获。一个健壮的程序，尽可能的避免错误，尽可能的捕获、处理各种异常。

产生异常：
    通过raise语句显式的抛出异常。没有raise语句，python解释器自己检测到异常也将引发它。通过traceback，可以跟踪异常栈
    程序会在异常抛出的地方中断执行，如果不捕获，就会提前结束程序。raise语句：raise后要求应该抛出一个BasException类的子类或实例，如果raise的是异常类，这个异常类将被解释器自动无参实例化后抛出，这样的缺点是无法带出信息，不利于显示分析定位问题。

异常类及继承层次：
    BaseException  # 所有异常的基类
     +-- SystemExit  # 解释器请求退出
     +-- KeyboardInterrupt  # 用户中断执行(通常是输入^C)
     +-- GeneratorExit  # 生成器(generator)发生异常来通知退出
     +-- Exception  # 常规异常的基类

BasException及其子类：
    BasException是所有内建异常类的祖先类。
    SystemExit：sys.exit()函数引发的异常，异常不捕获处理，就直接交给python解释器，解释器退出。sys.exit(1), sys.exit(0)
    KeyBoardInterrupt：对应的捕获用户中断行为Ctrl+C

Exception及其子类：
    所有内建的、非系统退出的异常的基类，自定义异常也应该继承自它.
异常捕获：
    except可以捕获多个异常。捕获规则从上到下异常比较，如果匹配不到，则该异常向外抛出；如果匹配到，则执行匹配的except语句盘，其他except语句就不会再次捕获。
    捕获原则：越具体的异常应该往更靠前放，越宽泛的异常应该往后面写；同一层级的异常，前后顺序没关系(从小大大，从具体到宽泛)

as子句：
    被抛出的异常是异常的实例，as子句把捕获的异常实例与子句后的标识符绑定。`as e：print(e)`相当于调用异常实例e的`__str__`

finally:
    最终，即最后一定要执行的，不管有没有异常。
    根因：函数返回值被压在栈顶，字节码去拿返回值拿的栈顶的值。进入try执行return 3，3被压在栈顶，虽然函数要返回，但是finally语句块最后还要执行，在finally中执行了return 5,5又被压在栈顶。
    所以，函数的返回值取决于最后一个执行的return语句，finally内一般不要有return，否则将覆盖正常的return值。
    finally中一般放置资源的清理、释放工作的语句。所以，也可以在finally语句中再次捕获异常。

异常的传递：
    异常总是向外层抛出，如果外层没有处理这个异常，就会继续向外抛出。如果内层捕获并处理了异常，外部就不能捕获到了。如果到了最外层还是没有被处理，就会中断异常所在的线程执行。可以通过traceback追溯异常传递路径，定位问题发生根因。

    异常一旦不处理，造成的后果非常严重，可能造成主线程直接退出，业务中断。所以一些业务代码，把它放到子线程中跑更安全，在主线程监控子线程是否活着就行了，没有活着重新拉一把。

异常的捕获时机：
    1、立即捕获：在异常发生出立即捕获。
        运用场景：对于给用户的接口、函数等，对于用户来说，应该是越方便越好。当发生异常时，接口应该立即捕获，并给出友好性提示或返回异常时的默认值，用户一目了然。
    2、边界捕获：
        运用场景：封装产生了边界。
        例如，写了一个函数注册接口，用户调用该接口注册函数，接口内部不需要捕获、处理异常，一旦内部处理了，外部调用者就无法感知了，不知道注册成功还是失败。
        又如，自定义一个open模块，掉用者使用这个模块读取文件时可能会发生异常，比如调用者想创建文件但文件已经存在了，这个时候模块内部做处理就不合适了，
        因为无法预测用户最终的意图（删除重新创建还是直接打开已存在的文件），最好的处理方式就继续向外层抛出，一般来说最外层也是边界，由边界来处理这个异常。
    无论是立即捕获还是边界捕获，都不是绝对的，在具体项目场景使用最合适的异常处理方式即可。

总结；
    try:
        <语句>  # 运行正常代码
    except <异常类>:
        <语句>  # 捕获某种类型的异常
    except <异常类> as <变量名>:
        <语句>  # 捕获某种类型的异常并获得对象
    else:
        <语句>  # 如果没有任何异常执行
    finally:
        <语句>  # 退出try时总会执行

try的工作原理
1、如果try中语句执行时发生异常，搜索except子句，并执行第一个匹配该异常的except子句
2、如果try中语句执行时发生异常，却没有匹配的except子句，异常将被递交到外层的try，如果外层不处理这个异常，异常将继续向外层传递。如果都不处理该异常，则会传递到最外层，如果还没有处理，就终止异常所在的线程
3、如果在try执行时没有发生异常，将执行else子句中的语句
4、无论try中是否发生异常，finally子句最终都会执行

"""
import threading
import time
import traceback


# def 0a():  # 产生异常
#     pass


class MyException(Exception):  # Exception是所有内建的、非系统退出的异常的基类，自定义异常也应该继承自它
    def __init__(self, code='', msg=''):  # 为了避免raise无参异常时，解释器自动无参实例化引起TypeError，最好给参数给一个默认值
        self.code = code
        self.msg = msg


def exp_test():
    try:  # 异常传递：异常总是向外层抛出，如果外层没有处理这个异常，就会继续向外抛出。如果内层捕获并处理了异常，外部就不能捕获到了
        f = None  # finally中出现的变量f，在try语句块外定义是好的习惯。否则有可能引发NameError。
        try:
            f = open('test')
            return 'true'
        except MyException as e:  # 被抛出的异常是异常的实例，as子句把捕获的异常实例与子句后的标识符绑定
            print('MyException={}'.format(e))
            raise MyException('My error')  # 通过raise语句显式的抛出异常;没有raise语句，python解释器自己检测到异常也将引发它。
        except TypeError as e:  # except可以捕获多个异常；越具体的异常应该往更靠前放，同一层级的异常，前后顺序没有关系。
            print('TypeError={}'.format(e))
            raise TypeError('type error')
        except FileExistsError('Not exist') as e:
            print('FileExistsError={}'.format(e))
            raise e
        except Exception as e:  # 越宽泛的异常，应该往后放
            print(e)
            print(traceback.format_exc())  # 通过traceback，可以跟踪异常栈
        finally:  # 最终，即最后一定要执行的，不管有没有异常。
            print('final')
            if f:
                f.close()
            return 'final'  # 函数返回值被压在栈顶，字节码去拿返回值拿的栈顶的值。所以，函数的返回值取决于最后一个执行的return语句
    finally:
        print()


# 看似小小的错误引发的异常，可能导致严重的事故，甚至业务中断
def exp_demo():
    time.sleep(3)
    try:
        1/0
    except FloatingPointError as e:  # 立即捕获。运用场景：对于给用户的接口、函数等，对于用户来说，应该是越方便越好。当发生异常时，接口应该立即捕获，并给出友好性提示，用户一目了然。
        raise e
    except OverflowError as e:
        raise e
    except ZeroDivisionError as e:
        raise e
    finally:
        print('exit')


t = threading.Thread(target=exp_demo)
t.start()
while True:
    if t.is_alive():  # 业务代码放到子线程中跑更安全，主线程监控子线程是否活着就行了，子线程异常导致整个线程退出，也不会影响主线程。异常的天花板就是线程。
        print('alive')
    else:
        print('dead')
    time.sleep(1)


if __name__ == '__main__':
    print(exp_test())

