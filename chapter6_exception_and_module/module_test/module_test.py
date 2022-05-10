__all__ = ['_x', '__y']


print('This is module_test module')

_x = '_x'
__y = '__y'
z = 'zzz'


class A:
    def show_module(self):
        print('{}.a={}'.format(self.__module__, self))
        print(self.__class__.__name__)


def imp_test():
    pass


a = A()
a.show_module()

if __name__ == '__main__':
    pass
