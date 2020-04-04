"""
Simple test of exec function with a managed user namespace.
"""

USER_CODE = """
y = 10


def setup():
    print('in setup')
    global y
    y = 42


def draw():
    print('in draw')
    print(f'x = {x}')
    print(f'y = {y}')
"""


user_ns = dict()
exec(USER_CODE, user_ns)

exec("setup()", user_ns)
for x in range(10):
    user_ns['x'] = x
    exec("draw()", user_ns)
