from pathlib import Path
from setuptools import setup

with open('README.md') as f:
    readme = f.read()


with open(Path('py5', '__init__.py')) as f:
    for line in f.readlines():
        if line.startswith('__version__'):
            break
    VERSION = line.split("'")[-2]


setup(
    name='py5',
    version=VERSION,
    packages=['py5'],
    py_modules=['py5_tools', 'setup'],
    package_data={
        "py5": ['jars/*.jar', 'py.typed']
    },
    description='CPython wrapper for the Java Processing library',
    long_description=readme,
    author='Jim Schmitz',
    author_email='jim@ixora.io',
    entry_points={
        'console_scripts': [
            'run_sketch = py5_tools.tools.run_sketch:main',
            'py5cmd = py5_tools.tools.py5cmd:main',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ],
)
