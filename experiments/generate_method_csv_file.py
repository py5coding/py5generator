import sys
import re
from pathlib import Path

import xmltodict
from pandas import DataFrame, Series


###############################################################################
# TEMPLATES
###############################################################################

METHOD_REGEX = re.compile(r'(@\w+)?\s*def (.*?)\((cls|self),?\s*(.*?)\)\s*-?>?\s*(.*?):$', re.MULTILINE | re.DOTALL)

###############################################################################
# REFERENCE AND LOOKUPS
###############################################################################


skip_user_methods = {
    'settings', 'setup', 'draw'
    'keyPressed', 'keyTyped', 'keyReleased',
    'mouseClicked', 'mouseDragged', 'mouseMoved', 'mouseEntered',
    'mouseExited', 'mousePressed', 'mouseReleased', 'mouseWheel',
    'exitActual',
}

skip_builtin_python_functions = {
    'print', 'exec', 'exit', 'str', 'set', 'map', 'sort',
}

skip_user_should_use_python_instead = {
    'append', 'arrayCopy', 'arraycopy', 'concat', 'expand', 'reverse', 'shorten',
    'splice', 'subset', 'binary', 'boolean', 'byte', 'char', 'float', 'hex',
    'int', 'unbinary', 'unhex', 'join', 'match', 'matchAll', 'nf', 'nfc', 'nfp',
    'nfs', 'split', 'splitTokens', 'trim', 'debug', 'delay', 'equals', 'println',
    'printArray',
}

skip_user_should_use_numpy_instead = {
    'min', 'max', 'round', 'map', 'abs', 'pow', 'sqrt', 'ceil', 'floor', 'log',
    'exp', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'atan2', 'degrees',
    'radians', 'sq', 'lerp', 'constrain', 'norm', 'mag', 'dist'
}

skip_public_methods_that_should_be_skipped = {
    'runSketch', 'main', 'handleDraw', 'handleSettings', 'usePy5Methods',
    'registerMethod', 'unregisterMethod',
    'showDepthWarning', 'showDepthWarningXYZ', 'showMethodWarning',
    'showVariationWarning', 'showMissingWarning',
    'checkAlpha', 'setSize', 'die',
}

skip_methods_that_are_not_part_of_the_framework = {
    'attrib', 'attribColor', 'attribNormal', 'attribPosition', 'beginPGL', 'endPGL',
    'exitCalled', 'flush', 'focusGained', 'focusLost', 'frameMoved', 'frameResized',
    'isLooping', 'orientation', 'sketchDisplay', 'sketchFullScreen',
    'sketchHeight', 'sketchOutputPath' 'sketchPath', 'sketchPixelDensity', 'sketchRenderer',
    'sketchSmooth', 'sketchSmooth', 'sketchWidth', 'sketchWindowColor', 'blendColor',
}

skip_methods_that_should_be_done_in_python = {
    'createInput', 'createInputRaw', 'createOutput', 'createPath', 'createReader',
    'createWriter', 'dataFile', 'dataPath', 'link', 'listFiles', 'listPaths',
    'loadJSONArray', 'loadJSONObject', 'parseJSONArray', 'parseJSONObject',
    'saveJSONArray', 'saveJSONObject',
    'loadBytes', 'saveBytes', 'loadXML', 'parseXML', 'saveXML', 'launch',
    'loadStrings', 'saveStrings', 'loadTable', 'saveTable', 'saveStream',
    'saveFile', 'savePath', 'checkExtension', 'getExtension', 'desktopFile',
    'desktopPath', 'shell', 'urlDecode', 'urlEncode', 'sketchFile', 'sketchOutputStream',
}

skip_parsing_methods_that_should_be_done_in_python = {
    'parseBoolean', 'parseByte', 'parseChar', 'parseInt', 'parseFloat',
}

skip_internal_methods = {
    'postEvent', 'style', 'hideMenuBar', 'saveViaImageIO',
    'getClass', 'hashCode', 'wait', 'notify', 'notifyAll', 'toString',
    'setAndUpdatePixels', 'loadAndGetPixels', 'convertBytesToPImage',
}

skip_methods_implemented_by_me = {
    'image', 'createImage', 'loadImage', 'requestImage', 'texture',
    'shape', 'loadShape'
}

PAPPLET_SKIP_METHODS = (skip_user_methods
                        | skip_builtin_python_functions
                        | skip_user_should_use_python_instead
                        | skip_user_should_use_numpy_instead
                        | skip_public_methods_that_should_be_skipped
                        | skip_methods_that_are_not_part_of_the_framework
                        | skip_methods_that_should_be_done_in_python
                        | skip_parsing_methods_that_should_be_done_in_python
                        | skip_internal_methods
                        | skip_methods_implemented_by_me)


PAPPLET_SKIP_PARAM_TYPES = {
    'processing/core/PMatrix3D', 'processing/core/PMatrix2D',
    'processing/core/PMatrix', 'java/io/File'
}

DEPRECATED = {
    'firstMouse', 'mouseEvent', 'keyEvent', 'MACOSX'
}

EXTRA_DIR_NAMES = {
    'run_sketch', 'get_py5applet', 'reset_py5', 'exit_sketch',
    'autoclass', 'Py5Methods', '_Py5Applet', '_py5sketch', '_py5sketch_used',
    '_prune_tracebacks'
}


###############################################################################
# UTIL FUNCTIONS
###############################################################################


def snake_case(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()


def skip_reason(fname):
    if fname in skip_user_methods:
        return 'user method'
    if fname in skip_builtin_python_functions:
        return 'builtin python function'
    if fname in skip_user_should_use_python_instead:
        return 'user should use python instead'
    if fname in skip_user_should_use_numpy_instead:
        return 'user should use numpy instead'
    if fname in skip_public_methods_that_should_be_skipped:
        return 'public methods that should be skipped'
    if fname in skip_methods_that_are_not_part_of_the_framework:
        return 'methods that are not part of the framework'
    if fname in skip_methods_that_should_be_done_in_python:
        return 'methods that should be implemented by me in Python'
    if fname in skip_parsing_methods_that_should_be_done_in_python:
        return 'parsing methods that should be implemented by me in Python'
    if fname in skip_internal_methods:
        return 'internal methods'
    if fname in skip_methods_implemented_by_me:
        return 'methods that should be implemented by me in Python'


###############################################################################
# MAIN
###############################################################################


def generate_py5(repo_dir):
    """Generate an installable py5 library using processing jars
    """
    repo_dir = Path(repo_dir)

    print(f'inspecting processing library...')
    core_jars = list(repo_dir.glob('**/core.jar'))
    if len(core_jars) != 1:
        if core_jars:
            print(f'more than one core.jar found in {repo_dir}', file=sys.stderr)
        else:
            print(f'core.jar not found in {repo_dir}', file=sys.stderr)
        return
    core_jar_path = core_jars[0]

    py5_jar_path = Path('py5_jar', 'dist', 'py5.jar')
    if not py5_jar_path.exists():
        raise RuntimeError(f'py5 jar not found at {str(py5_jar_path)}')
    import jnius_config
    jnius_config.set_classpath(str(py5_jar_path), str(core_jar_path))
    from jnius import autoclass, JavaStaticMethod, JavaMethod, JavaMultipleMethod, JavaStaticField, JavaField

    print('examining Java classes')
    Py5Applet = autoclass('py5.core.Py5Applet',
                          include_protected=False, include_private=False)

    class_types = {
        JavaStaticField: 'static field',
        JavaField: 'dynamic variable',
        JavaStaticMethod: 'static method',
        JavaMethod: 'method',
        JavaMultipleMethod: 'method'
    }

    df = DataFrame(columns=['processing_name', 'py5_name', 'type', 'included', 'reason'])

    for i, (processing_name, v) in enumerate(Py5Applet.__dict__.items()):
        if processing_name.startswith('_'):
            continue
        type_ = class_types.get(type(v), 'unknown')
        py5_name = processing_name if type_ == 'static field' else snake_case(processing_name)
        included = True
        reason = ''
        if processing_name in DEPRECATED:
            included = False
            reason = 'deprecated'
        if processing_name in PAPPLET_SKIP_METHODS:
            included = False
            reason = skip_reason(processing_name)
        df.loc[i, :] = (processing_name, py5_name, type_, included, reason)

    df.set_index('py5_name', inplace=True, drop=True)

    # add the methods in the mixin classes as functions in the __init__.py module
    mixin_dir = Path('py5_resources', 'py5_module', 'py5', 'mixins')
    for filename in mixin_dir.glob('*.py'):
        if filename.stem == '__init__':
            continue
        with open(filename) as f:
            code = f.read()
            code = code.split('*** BEGIN METHODS ***')[1].strip()

        for decorator, fname, arg0, args, rettypestr in METHOD_REGEX.findall(code):
            if fname.startswith('_'):
                continue
            elif decorator == '@overload':
                continue
            else:
                type_ = 'static method' if decorator == '@classmethod' else 'method'
                df.loc[fname, :] = ('', type_, True, f'from mixin file {filename.name}')

    # add the webrefs from the xml file
    filename = 'py5_docs/docfiles/javadocs.xml'
    with open(filename, 'r') as f:
        root = xmltodict.parse(f.read())
    webrefs = DataFrame(columns=['category', 'subcategory'])
    for commenttree in root['commenttrees']['commenttree']:
        processing_name = commenttree['@name']
        blocktags = commenttree['blocktags']
        if blocktags:
            tags = blocktags['blocktag']
            webref = list(map(lambda x: x[8:], filter(lambda x: x.startswith('@webref'), tags)))
            if webref and webref[0].strip():
                tokens = webref[0].strip().split(':')
                cat = tokens[0]
                subcat = '' if len(tokens) == 1 else tokens[1]
                print(webref)
                webrefs.loc[processing_name] = cat, subcat

    df = df.join(webrefs, on='processing_name')

    df.to_csv('/tmp/datafile.csv')

    print('done!')


def main():
    generate_py5(repo_dir='../sam_processing4/')


if __name__ == '__main__':
    main()
