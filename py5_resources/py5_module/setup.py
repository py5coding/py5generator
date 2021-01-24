from pathlib import Path
from setuptools import setup

with open('README.rst') as f:
    README = f.read()


with open(Path('py5', '__init__.py')) as f:
    for line in f.readlines():
        if line.startswith('__version__'):
            break
    VERSION = line.split("'")[-2]


INSTALL_REQUIRES = [
    'jpype1>=1.2',
    'line_profiler>=2.1.2',
    'noise>=1.2',
    'nptyping>=1.4',
    'numpy>=1.19',
    'pandas>=1.0',
    'pillow>=8.1',
    'requests>=2.25',
    'stackprinter>=0.2.4',
]

setup(
    name='py5',
    version=VERSION,
    packages=['py5', 'py5.mixins', 'py5_tools', 'py5_tools.tools'],
    py_modules=['setup'],
    package_data={
        "py5": ['jars/*.jar', 'jars/*/*.jar', '*.pyi', 'py.typed']
    },
    python_requires='>3.8',
    install_requires=INSTALL_REQUIRES,
    description='Processing for CPython',
    long_description=README,
    author='Jim Schmitz',
    author_email='jim@ixora.io',
    entry_points={
        'console_scripts': [
            'run_sketch = py5_tools.tools.run_sketch:main',
            'py5cmd = py5_tools.tools.py5cmd:main',
            'py5utils = py5_tools.tools.py5utils:main',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Artistic Software',
        'Topic :: Multimedia :: Graphics',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Java',
    ],
)
