import re
from pathlib import Path

from pandas import DataFrame


core_jar_path = Path('../processing4/core/library/core.jar')

import jnius_config  # noqa
jnius_config.set_classpath(str(core_jar_path))
from jnius import autoclass, JavaStaticMethod, JavaMethod, JavaMultipleMethod, JavaStaticField, JavaField  # noqa


def snake_case(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()


class_types = {
    JavaStaticField: 'static field',
    JavaField: 'dynamic variable',
    JavaStaticMethod: 'static method',
    JavaMethod: 'method',
    JavaMultipleMethod: 'method'
}


def make_dataframe(cls_):
    df = DataFrame(columns=['processing_name', 'py5_name', 'type'])
    for i, (processing_name, v) in enumerate(cls_.__dict__.items()):
        if processing_name.startswith('_'):
            continue
        type_ = class_types.get(type(v), 'unknown')
        py5_name = processing_name if type_ == 'static field' else snake_case(processing_name)
        df.loc[i, :] = (processing_name, py5_name, type_)

    df.set_index('py5_name', inplace=True, drop=True)

    return df


PShape = autoclass('processing.core.PShape', include_protected=False, include_private=False)
make_dataframe(PShape).to_csv('/tmp/pshape.csv')

PShader = autoclass('processing.opengl.PShader', include_protected=False, include_private=False)
make_dataframe(PShader).to_csv('/tmp/pshader.csv')

PGraphics = autoclass('processing.core.PGraphics', include_protected=False, include_private=False)
make_dataframe(PGraphics).to_csv('/tmp/pgraphics.csv')

PSurface = autoclass('processing.core.PSurface', include_protected=False, include_private=False)
make_dataframe(PSurface).to_csv('/tmp/psurface.csv')

PFont = autoclass('processing.core.PFont', include_protected=False, include_private=False)
make_dataframe(PFont).to_csv('/tmp/pfont.csv')
