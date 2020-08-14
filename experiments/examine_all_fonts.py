import py5
from py5 import Py5Font


fonts = Py5Font.list()
font_index = 0
font_name = fonts[font_index]
good_fonts = []


def settings():
    py5.size(600, 300)


def setup():
    py5.text_align(py5.CENTER, py5.CENTER)
    py5.fill(0)
    pick_font()


def draw():
    py5.background(255)
    py5.text('py5', py5.width / 2, py5.height / 2)


def exiting():
    print(good_fonts)


def key_pressed():
    if py5.key == 's':
        good_fonts.append(font_name)
    elif py5.key == py5.CODED:
        global font_index
        if py5.key_code == py5.RIGHT:
            font_index = (font_index + 1) % len(fonts)
        if py5.key_code == py5.LEFT:
            font_index = (len(fonts) + font_index - 1) % len(fonts)
        pick_font()


def pick_font():
    global font_name
    font_name = fonts[font_index]
    print(font_name)
    font = py5.create_font(font_name, 128)
    py5.text_font(font)


py5.run_sketch()
