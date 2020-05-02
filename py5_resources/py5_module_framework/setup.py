from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='py5',
    version='0.1',
    packages=['py5'],
    description='CPython wrapper for the Java Processing library',
    long_description=readme,
    author='Jim Schmitz',
    author_email='jim@ixora.io',
    entry_points={
        'console_scripts': [
            'py5_sketch = py5.tools.run_sketch:main'
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ],
)
