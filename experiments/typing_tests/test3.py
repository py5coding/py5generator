class A:

    def f1(self, x, y):
        return x + y

    def f2(self, x):
        return x * x

    def f3(self, x, y, z):
        return x + y + z


def gen():
    return A()


def foo():
    return gen()
