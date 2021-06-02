# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2021 Jim Schmitz
#
#   This library is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 2.1 of the License, or (at
#   your option) any later version.
#
#   This library is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
#   General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this library. If not, see <https://www.gnu.org/licenses/>.
#
# *****************************************************************************
import time
import re
import base64
from io import BytesIO

from IPython.core.magic_arguments import MagicHelpFormatter
import PIL


class CellMagicHelpFormatter(MagicHelpFormatter):

    def add_usage(self, usage, actions, groups, prefix="::\n\n  %%"):
        super(MagicHelpFormatter, self).add_usage(usage, actions, groups, prefix)


def make_zmq_streamer(shell):
    display_pub = shell.display_pub
    parent_header = display_pub.parent_header

    def zmq_shell_send_stream(name, text):
        content = dict(name=name, text=text)
        msg = display_pub.session.msg('stream', content, parent=parent_header)
        display_pub.session.send(display_pub.pub_socket, msg, ident=b'stream')

    return zmq_shell_send_stream

def make_zmq_image_display(shell):
    display_pub = shell.display_pub
    parent_header = display_pub.parent_header

    def zmq_shell_send_image(frame, init_display, display_id, quality, scale):
        msg_type = 'display_data' if init_display else 'update_display_data'
        height, width, _ = frame.shape
        img = PIL.Image.fromarray(frame)
        if scale != 1.0:
            img = img.resize(tuple(int(scale * x) for x in img.size))
        b = BytesIO()
        img.save(b, format='JPEG', quality=quality)
        data = {'image/jpeg': base64.b64encode(b.getvalue()).decode('ascii')}
        metadata = {'image/jpeg': {'height': img.size[0], 'width': img.size[1]}}
        content = dict(data=data, metadata=metadata, transient=dict(display_id=display_id))
        msg = display_pub.session.msg(msg_type, content, parent=parent_header)
        display_pub.session.send(display_pub.pub_socket, msg, ident=bytes(msg_type, encoding='utf8'))

    return zmq_shell_send_image


def fix_triple_quote_str(code):
    for m in re.finditer(r'\"\"\"[^\"]*\"\"\"', code):
        code = code.replace(
            m.group(), m.group().replace('\n    ', '\n'))
    return code


def wait(wait_time, sketch):
    end_time = time.time() + wait_time
    while time.time() < end_time and sketch.is_running:
        time.sleep(0.1)


__all__ = ['CellMagicHelpFormatter', '_make_zmq_streamer', 'make_zmq_image_display', 'fix_triple_quote_str', 'wait']
