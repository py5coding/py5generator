from typing import overload


class A:
    def f1(self, x: float, y: float) -> float: ...
    def f2(self, x: float) -> float: ...
    def f4(self, x: float) -> float: ...

    @overload
    def f5(self, x: float) -> float:
        """this is the f5 docstring 2

        more stuff
        """
        pass

    @overload
    def f5(self, x: float, y: float) -> float:
        """this is the f5 docstring 3

        more stuff
        """
        pass

    @overload
    def f5(self, x: float, y: float, z: float) -> float:
        """this is the f5 docstring 4

        more stuff
        """
        pass


testvar1 = 10  # type: float
testvar2 = None  # type: A


def gen() -> A: ...
def foo() -> A: ...
