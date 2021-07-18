![py5 logo](py5_docs/images/logo.png)

# py5

![py5 PyPI Downloads](https://img.shields.io/pypi/dm/py5?label=py5%20PyPI%20downloads) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/hx2A/py5examples/HEAD?urlpath=lab)

py5 is a new version of [**Processing**][processing] for Python 3.8+. It makes the Java [**Processing**][processing] jars available to the CPython interpreter using [**JPype**][jpype]. It can do just about everything [**Processing**][processing] can do, except with Python instead of Java code.

The goal of py5 is to create a new version of Processing that is integrated into the Python ecosystem. Built into the library are thoughtful choices about how to best get py5 to work with other popular Python libraries such as [numpy](https://www.numpy.org/) or [Pillow](https://python-pillow.org/).

Here is a simple example of a working py5 Sketch:

```
import py5


def setup():
    py5.size(200, 200)
    py5.rect_mode(py5.CENTER)


def draw():
    py5.square(py5.mouse_x, py5.mouse_y, 10)


py5.run_sketch()
```

If you have Java 11 installed on your computer, you can install py5 using pip:

```
pip install py5
```

py5generator is a meta-programming project that creates the py5 library. To view the actual installed py5 library code, look at the [py5 repository][py5_repo]. All py5 library development is done through py5generator.

[Detailed installation instructions](http://py5.ixora.io/install/) are available on the documentation website. There are some [Special Notes for Mac Users](http://py5.ixora.io/tutorials/mac-users/) that you should read if you use OSX.

The documentation website, [http://py5.ixora.io/](http://py5.ixora.io/), is very much a work in progress. The [reference documentation](http://py5.ixora.io/reference/) is solid but the how-to's and tutorials need a lot of work. See the [py5 examples repository][py5_examples_repo] for some working examples.

[py5_repo]: https://github.com/hx2A/py5
[py5_examples_repo]: https://github.com/hx2A/py5examples
[processing]: https://github.com/processing/processing4
[jpype]: https://github.com/jpype-project/jpype
