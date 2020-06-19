import numpy as np
from PIL import Image
import py5


def settings():
    py5.size(512, 512)


def draw():
    py5.image_mode(py5.CENTER)
    py5.background(0)
    # img = np.zeros((50, 20, 4), dtype=np.uint8)
    # img[:, :, 3] = 255
    # img[:30, :, 2] = 255
    # img[10:40, :, 1] = 255
    # img[20:, :, 0] = 255

    img = Image.open('/mnt/readynas_data/DataBackup/ffhq_dataset/00000.png').resize((500, 500)).convert("RGBA")

    pimg = py5.get_py5applet().convertBytesToPImage(img.tobytes(), img.width, img.height, pass_by_reference=False)
    py5.image(pimg, py5.width / 2, py5.height / 2)
    py5.no_loop()


py5.run_sketch(block=False)
