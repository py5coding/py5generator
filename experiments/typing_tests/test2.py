class A:

    def f1(self, x, y):
        return x + y

    def f2(self, x):
        return x * x

    def f3(self, x, y, z):
        return x + y + z

    def f5(self, *args):
        """this is the f5 docstring 1

        more stuff
        """
        return sum(args)


def gen():
    return A()


def foo():
    return gen()
