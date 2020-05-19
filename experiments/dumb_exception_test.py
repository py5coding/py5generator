

def foo():
    raise RuntimeError('test')


def bar():
    foo()


def test():
    bar()


test()
