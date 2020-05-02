def settings():
    size(500, 500, JAVA2D)


def setup():
    background(255)
    rect_mode(CENTER)


def draw():
    if is_key_pressed():
        print('frameRate', get_frame_rate())
    fill(random(255), random(255), random(255), 50.0)
    rect(mouse_x, mouse_y, 40, 40)


def mouse_entered():
    print('mouse entered')


def mouse_exited():
    print('mouse exited')
