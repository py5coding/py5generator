import numpy as np

import py5


uk = None
uk_children = None


def settings():
    py5.size(640, 360, py5.P2D)


# def setup():
#     global uk
#     uk = py5.load_shape('uk.svg')


def setup():
    global uk
    global uk_children
    uk = py5.load_shape('uk.svg')
    uk_children = uk.get_children()

# def draw():
#     py5.background(0)

#     py5.translate((py5.width - uk.width) / 2, (py5.height - uk.height) / 2)
#     children = uk.get_child_count()
#     for i in range(children):
#         child = uk.get_child(i)
#         total = child.get_vertex_count()

#         for j in range(total):
#             x, y = child.get_vertex_x(j), child.get_vertex_y(j)
#             py5.stroke((py5.frame_count + (i + 1) * j) % 255)
#             py5.point(x, y)


def draw():
    py5.background(0)

    py5.translate((py5.width - uk.width) / 2, (py5.height - uk.height) / 2)
    frame_count = py5.frame_count
    for i, child in enumerate(uk_children):
        total = child.get_vertex_count()

        v = np.zeros(2, dtype=np.float32)
        for j in range(total):
            # v = child.get_vertex(j)
            child.get_vertex(j, v)
            # print(v)
            # x, y = child.get_vertex_x(j), child.get_vertex_y(j)
            py5.stroke((frame_count + (i + 1) * j) % 255)
            # py5.point(x, y)
            py5.point(v[0], v[1])


py5.run_sketch(block=False)
