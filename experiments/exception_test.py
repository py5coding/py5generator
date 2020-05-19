import py5_tools


if not py5_tools.py5_started:
    py5_tools.add_options('-Xrs', '-Xmx4096m')
import py5  # noqa


pixels = []


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

    if py5.frame_count == 100:
        # print(10 / 0)
        cause_error('garbage')

    #     print('calling exit_sketch')
    #     # py5.exit_sketch()
    #     py5.fill('garbage input', 4, 5, 32)

    # if py5.frame_count == 100:
    #     global pixels
    #     py5.load_pixels()
    #     pixels.extend(py5.pixels[:])
    #     print('copied pixels')
    #     print(len(pixels))


def cause_error(junk):
    # try:
    py5.fill(junk, 4, 5, 32)
    # except Exception:
    #     print(10 / 0)
        # x = y + 10


print('this is file', __file__)

py5.run_sketch(block=True)
