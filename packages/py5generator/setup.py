from distutils.core import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name='py5generator',
    version='0.1',
    packages=['py5generator'],
    description='Generate py5 project',
    long_description=readme,
    author='Jim Schmitz',
    author_email='jim@ixora.io',
    # TODO: fix this
    # install_requires=[
    #     '???'
    # ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ],
)
