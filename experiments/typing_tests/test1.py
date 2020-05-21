from typing import overload


class A:

    def f1(self, x: float, y: float) -> float:
        return x + y

    def f2(self, x: float) -> float:
        return x * x

    def f3(self, x, y, z):
        return x + y + z

    @property
    def p1(self) -> int:
        """this is the p1 property

        stuff
        """
        return 42

    foobar: float = 42

    @overload
    def f5(self, x: int) -> int:
        """ this is the f5 function 1

        stuff
        """
        pass

    @overload
    def f5(self, x: float) -> float:
        """ this is the f5 function 2

        stuff
        """
        pass

    def f5(self, x):
        """ this is the f5 function 3

        stuff
        """
        return 2 * x

    @overload
    def f6(self, x: int) -> int:
        """ docstring for f6 1

        stuff
        """
        pass

    @overload
    def f6(self, x: int, y: int) -> int:
        """ docstring for f6 2

        stuff
        """
        pass

    @overload
    def f6(self, x: int, y: int, z: int) -> int:
        """ docstring for f6 3

        stuff
        """
        pass

    def f6(self, *args):
        return sum(args)


def gen() -> A:
    return A()


def foo() -> A:
    return gen()
