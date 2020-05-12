import py5

MouseEvent = py5.autoclass('processing.event.MouseEvent')


def settings():
    py5.size(500, 500, py5.P2D)


def setup():
    py5.background(255)
    py5.rect_mode(py5.CENTER)
    py5.frame_rate(30)


def draw():
    if py5.is_key_pressed():
        print('frameRate', py5.get_frame_rate())
    py5.fill(py5.random(255), py5.random(255), py5.random(255), 50.0)
    py5.rect(py5.mouse_x, py5.mouse_y, 40, 40)


def key_pressed():
    print(f'pressed {ord(py5.key)} {py5.key_code}')


def key_typed():
    print(f'typed {ord(py5.key)} {py5.key_code}')


def key_released():
    print(f'released {ord(py5.key)} {py5.key_code}')


def mouse_entered():
    print('mouse entered')


def mouse_exited():
    print('mouse exited')


def mouse_clicked():
    print('mouse clicked')


def mouse_dragged():
    print('mouse dragged')


# def mouse_moved():
#     # print('mouse moved')
#     print('frameRate', py5.get_frame_rate())


def mouse_pressed():
    print('mouse pressed')


def mouse_released():
    print('mouse released')


def mouse_wheel(event):
    print(f'mouse wheel {event.getCount()}')


py5.run_sketch(block=False)
