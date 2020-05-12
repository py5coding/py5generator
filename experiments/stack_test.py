import inspect


def draw():
    print('in draw method')


def get_parent_stack():
    foo = 42
    for level in inspect.stack():
        print(level.frame.f_locals.keys())


bar = 10


def dummy_function():
    asdf = 100
    get_parent_stack()

