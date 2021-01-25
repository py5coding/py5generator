# *****************************************************************************
#
#   Part of the py5generator project; generator of the py5 library
#   Copyright (C) 2020-2021 Jim Schmitz
#
#   This project is free software: you can redistribute it and/or modify it
#   under the terms of the GNU General Public License as published by the
#   Free Software Foundation, either version 3 of the License, or (at your
#   option) any later version.
#
#   This project is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
#   Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program. If not, see <https://www.gnu.org/licenses/>.
#
# *****************************************************************************
import os
import argparse
import logging
import shutil
from pathlib import Path

import pandas as pd

from generator import CodeBuilder, DocstringFinder, CodeCopier
from generator import reference as ref
from generator import templates as templ
from generator import javap


logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)

###############################################################################
# ARGUMENT PARSING
###############################################################################


parser = argparse.ArgumentParser(description="Generate py5 library using processing jars")
parser.add_argument('processing_repo_dir', action='store', help='location of processing code (github repository)')
parser.add_argument('processing_build_dir', action='store', help='location of build directory')


###############################################################################
# MAIN
###############################################################################


def generate_py5(repo_dir, build_dir):
    "Generate an installable py5 library using processing jars"
    repo_dir = Path(repo_dir)
    build_dir = Path(build_dir)

    logger.info('generating py5 library...')

    logger.info('building classpath')

    def find_jar(jar_name):
        jars = list(repo_dir.glob(f'**/{jar_name}.jar'))
        if len(jars) == 1:
            return jars[0]
        else:
            if jars:
                msg = f'more than one {jar_name}.jar found in {repo_dir}'
            else:
                msg = f'{jar_name}.jar not found in {repo_dir}'
            logger.critical(msg)
            raise RuntimeError(msg)

    core_jar_path = find_jar('core')
    svg_jar_path = find_jar('svg')
    dxf_jar_path = find_jar('dxf')
    pdf_jar_path = find_jar('pdf')

    py5_jar_path = Path('py5_jar', 'dist', 'py5.jar')
    if not py5_jar_path.exists():
        msg = f'py5 jar not found at {str(py5_jar_path)}'
        logger.critical(msg)
        raise RuntimeError(msg)

    javap.classpath = f'{py5_jar_path}:{core_jar_path}'

    logger.info('creating Sketch code')
    py5applet_data = pd.read_csv(Path('py5_resources', 'data', 'py5applet.csv')).fillna('').set_index('processing_name')

    # these CodeBuilder objects write the code fragments for the methods and fields.
    py5applet_builder = CodeBuilder('py5.core.Py5Applet', 'Sketch', py5applet_data)
    py5applet_builder.code_module_members('_py5sketch')
    py5applet_builder.run_builder()

    # add the methods in the mixin classes as functions in the __init__.py module
    mixin_dir = Path('py5_resources', 'py5_module', 'py5', 'mixins')
    for filename in mixin_dir.glob('*.py'):
        if filename.stem == '__init__':
            continue
        py5applet_builder.code_extra('Sketch', filename)
    py5applet_builder.code_extra('Sketch', Path('py5_resources', 'py5_module', 'py5', 'sketch.py'))

    # code the extra pre-run steps so the dynamic variables work right
    run_sketch_pre_run_steps = [
        templ.MODULE_PROPERTY_PRE_RUN_TEMPLATE.format(n) for n in sorted(py5applet_builder.dynamic_variable_names)
    ]

    def run_code_builder(name, clsname, class_name=None):
        logger.info(f'creating {name} code')
        class_name = class_name or clsname.split('.')[-1]
        data = pd.read_csv(Path('py5_resources', 'data', f'{class_name.lower()}.csv')).fillna('').set_index('processing_name')

        builder = CodeBuilder(clsname, name, data)
        builder.run_builder()

        return builder

    py5shader_builder = run_code_builder('Py5Shader', 'processing.opengl.PShader')
    py5shape_builder = run_code_builder('Py5Shape', 'processing.core.PShape')
    py5font_builder = run_code_builder('Py5Font', 'processing.core.PFont')
    py5surface_builder = run_code_builder('Py5Surface', 'py5.core.Py5SurfaceDummy', class_name='PSurface')
    py5graphics_builder = run_code_builder('Py5Graphics', 'py5.core.Py5Graphics', class_name='PGraphics')
    py5image_builder = run_code_builder('Py5Image', 'processing.core.PImage')

    # this assembles the code fragments from the builders so it can be
    # inserted into the code templates to complete the py5 module.
    logger.info('joining code fragments')
    sketch_class_members_code = ''.join(py5applet_builder.class_members)
    sketch_module_members_code = ''.join(py5applet_builder.module_members)
    py5shader_class_members_code = ''.join(py5shader_builder.class_members)
    py5shape_class_members_code = ''.join(py5shape_builder.class_members)
    py5font_class_members_code = ''.join(py5font_builder.class_members)
    py5surface_class_members_code = ''.join(py5surface_builder.class_members)
    py5graphics_class_members_code = ''.join(py5graphics_builder.class_members)
    py5image_class_members_code = ''.join(py5image_builder.class_members)
    run_sketch_pre_run_code = ''.join(run_sketch_pre_run_steps)

    # gather method_signatures info so they can be added to the docstrings
    method_signatures_lookup = {
        **py5applet_builder.method_signatures,
        **py5shader_builder.method_signatures,
        **py5shape_builder.method_signatures,
        **py5font_builder.method_signatures,
        **py5surface_builder.method_signatures,
        **py5graphics_builder.method_signatures,
        **py5image_builder.method_signatures,
        **ref.EXTRA_METHOD_SIGNATURES,
    }

    # code the result of the module's __dir__ function and __all__ variable
    py5_dir_names = py5applet_builder.all_names | ref.EXTRA_DIR_NAMES
    py5_dir_str = str(sorted(py5_dir_names, key=lambda x: (x.lower(), x)))[1:-1].replace(', ', ',\n    ')
    # don't want import * to import the dynamic variables because they cannot be updated
    py5_all_str = str(sorted(py5_dir_names - py5applet_builder.dynamic_variable_names, key=lambda x: (x.lower(), x)))[1:-1].replace(', ', ',\n    ')
    py5_dynamic_variables_str = str(sorted(py5applet_builder.dynamic_variable_names))

    def build_signatures(v):
        return [f"({', '.join(params)}) -> {rettype}" for params, rettype in v]
    # build signatures lookup for custom exceptions and do formatting so autopep8 doesn't have to
    method_signatures_lookup_str = '\n    '.join(f'({str(k)}, {build_signatures(v)}),' for k, v in method_signatures_lookup.items())

    # this dictionary of code strings will be inserted into the python code templates
    format_params = dict(sketch_class_members_code=sketch_class_members_code,
                         sketch_module_members_code=sketch_module_members_code,
                         py5shader_class_members_code=py5shader_class_members_code,
                         py5shape_class_members_code=py5shape_class_members_code,
                         py5font_class_members_code=py5font_class_members_code,
                         py5surface_class_members_code=py5surface_class_members_code,
                         py5graphics_class_members_code=py5graphics_class_members_code,
                         py5image_class_members_code=py5image_class_members_code,
                         method_signatures_lookup_str=method_signatures_lookup_str,
                         run_sketch_pre_run_code=run_sketch_pre_run_code,
                         py5_dir_str=py5_dir_str,
                         py5_all_str=py5_all_str,
                         py5_dynamic_variables_str=py5_dynamic_variables_str)

    # build complete py5 module in destination directory
    logger.info(f'building py5 in {build_dir}')
    if build_dir.exists():
        logger.info(f'emptying contents of {build_dir}')
        for c in build_dir.glob('*'):
            if c.name == '.git':
                continue
            if c.is_dir():
                shutil.rmtree(c)
            else:
                os.remove(c)

    # build the docstrings for each method
    docstrings = DocstringFinder(method_signatures_lookup)

    # as the code is copied, the code strings and docstrings will be assembled
    # CodeCopier is callable and is basically a custom version of `shutil.copy`
    copier = CodeCopier(format_params, docstrings)
    try:
        shutil.copytree(Path('py5_resources', 'py5_module'), build_dir, copy_function=copier, dirs_exist_ok=True)
    except shutil.Error:
        # for some reason on WSL this exception will be thrown but the files all get copied.
        logger.error('errors thrown in shutil.copytree, continuing and hoping for the best', exc_info=True)

    # finally, add the jars
    def copy_jars(jar_dir, dest):
        dest.mkdir(parents=True, exist_ok=True)
        for jar in jar_dir.glob('*.jar'):
            shutil.copy(jar, dest)

    copy_jars(core_jar_path.parent, build_dir / 'py5' / 'jars')
    copy_jars(svg_jar_path.parent, build_dir / 'py5' / 'jars' / 'svg')
    copy_jars(dxf_jar_path.parent, build_dir / 'py5' / 'jars' / 'dxf')
    copy_jars(pdf_jar_path.parent, build_dir / 'py5' / 'jars' / 'pdf')
    shutil.copy(py5_jar_path, build_dir / 'py5' / 'jars')

    build_dir.touch()

    logger.info('py5 build complete!')


def main():
    args = parser.parse_args()
    generate_py5(args.processing_repo_dir, args.processing_build_dir)


if __name__ == '__main__':
    main()
