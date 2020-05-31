# flake8: noqa
import test_import as ti


started = False


def settings():
    size(500, 500, JAVA2D)


def setup():
    background(255)
    rect_mode(CENTER)


def draw():
    if is_key_pressed():
        print('frameRate', get_frame_rate())
    if started:
        fill(random(255), random(255), random(255), 50.0)
        rect(mouse_x, mouse_y, 40, 40)

    if frame_count == 300:
        save_frame('/tmp/frame_###.png')
        cause_error(ti.test_function(10, 30))


def mouse_entered():
    global started
    started = True
    print('mouse entered')


def mouse_exited():
    print('mouse exited')


def cause_error(x):
    print(x / 0)
