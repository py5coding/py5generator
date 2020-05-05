from pathlib import Path
from setuptools import setup

with open('README.md') as f:
    readme = f.read()


with open(Path('py5_tools', '__init__.py')) as f:
    for line in f.readlines():
        if line.startswith('__version__'):
            break
    VERSION = line.split("'")[-2]


setup(
    name='py5_tools',
    version=VERSION,
    packages=['py5_tools'],
    description='Auxiliary tools for the py5 library',
    long_description=readme,
    author='Jim Schmitz',
    author_email='jim@ixora.io',
    entry_points={
        'console_scripts': [
            'run_sketch = py5_tools.tools.run_sketch:main'
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ],
)
