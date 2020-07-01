TODOS
=====

INFO
----

Building py5:

$ make clean
$ make processing_dir=../sam_processing4

The Processing jars need to exist and be built. If I am using Processing3 I need to compile with java 1.8. I can use it with a command like this:

(JAVA_HOME="/usr/lib/jvm/jdk1.8.0_74"; ant -f /home/jim/Projects/ITP/pythonprocessing/processing/core/build.xml)

Processing4 integration branch:
[repo](https://github.com/sampottinger/processing4)
[builds](https://www.datadrivenempathy.com/processing)

management
----------

Move all of these todos and notes to Notion. Use one of their templates for easy management. Should I share this with the public?

packaging and deployment
------------------------

get pypi package process working

Windows problems

* tab complete in py5cmd doesn't work on windows, I will need to implement with prompt_toolkit instead
* when using an opengl renderer, window doesn't close after hitting ESC unless the thread stopped because of an error

error messages
--------------

Add helpful messages for when the function parameter types are not correct or other `JavaException` / `Py5Exception` problems. For any exception, add a helpful explanation for what that error is and how to proceed with the debugging.

I can get each function's parameter types with the `signatures()` method.

`javap -classpath /home/jim/Projects/git/processing/core/library/core.jar -public processing.core.PApplet`

type hinting
------------

Use [type hinting](https://docs.python.org/3/library/typing.html) for Processing functions. Refer to [PEP-0484](https://www.python.org/dev/peps/pep-0484/) for more info.

Should I use stub files? Here are some packages that use them:

* [pyrsistent](https://github.com/tobgu/pyrsistent)
* [attrs](https://github.com/python-attrs/attrs)

The `NewType` types I added should be replaced with something that gives the methods for those classes.

Should the type hints make it clear that these are [position only parameters](https://www.python.org/dev/peps/pep-0570/)? This would require Python 3.8.

library functions
-----------------

I need the same error handling on those numpy wrapper functions I made. A good approach might be to move them from the Sketch class to a new `Extras` class, then parameterize the method templates so they can call something `Extras` instead of `_Py5Applet`.

The PMatrix methods should be skipped and replaced with numpy backed functions.

The JSON and XML functions should be replaced with Python library tools.

Review skipped functions to see what should be re-implemented.

There are undocumented functions like frameResized with no apparent purpose.

docstrings
----------

add docstrings to all methods, pulling docs from wherever the website documentation comes from.

It seems to have been generated with [JavaDocs and some Python code](https://github.com/processing/processing-docs/tree/master/java_generate). The repo contains the [xml files](https://github.com/processing/processing-docs/tree/master/content/api_en) referenced in the `PApplet.java` comments. The `GenerateDescriptions.py` inserts those xml descriptions into the Java source. The `processingrefBuild.sh` script just calls `javadoc` using a custom doclet to use particular templates and other customizations.

[Doclet documentation](https://docs.oracle.com/javase/9/docs/api/jdk/javadoc/doclet/package-summary.html)

It would be great if I could feed these through a translator to make this multi-linqual. Then perhaps I could do something like `import py5.es as py5` to make all the docstrings in Spanish. If I did this, how would I keep everything in sync? I will certainly add new functions, especially in the short term. Those new functions will be in Python so their docstrings will be written by me.

For Py5 documentation I should use Sphinx to generate my own docfiles after everything has been compiled together.

Py5Image and Py5Shape
---------------------

I should also Py5Image and Py5Shape classes that will really be backed by Cairo and Pillow but provide more accessible functionality, along with multi-lingual comments.

The custom image and shape functions will need a cache to store the images and shapes after they have been converted into PImage or PShape objects.

performance
-----------

Can I batch commands together and get a performance improvement? It is slower to go back and forth between Python and Java. The py5 methods can have a second "mode" that collects all the commands together and executes them all at once at the end? Should there be a flush command to manually force everything through? Perhaps I can use a context manager for a performance improvement of one part of the code.

PDE mode
--------

[Build a PDE mode](https://github.com/processing/processing/wiki/Mode-Overview)?

libraries
---------

need to add [Processing's non-core jars](https://processing.org/reference/libraries/) for other libraries like PDF, SVG, Video, Sound.

Should all Java Processing libraries be wrapped in a Python package? Should I bundle multiple libraries together?

camera3D and colorblindness need to call the preDraw and postDraw methods with an Interface in the same way PApplet calls the setup and draw methods.

Ability to make Python library extensions. Might as well make them installable Python packages. Deployment can be through pypi, just like any other Python package. Here are some ideas:

* py5-AR - build an AR framework that tracks the Processing camera to a surface.
* py5-slides - presentation framework, read a markdown file and show one slide after another. Support complex animations on each slide, including embedded sketches.
* py5-vj - can I do live coding for a VJ event? I can get inputs from a music stream for the beats, notes, etc. It is possible to replace the `draw()` method at will with `hot_reload_draw()`. Perhaps I can use the ControlP5 textarea object for editing the code.
* py5-audio - use librosa to animate audio or music.
* py5-cloud - can I use cloud computing to build a renderfarm for rendering a lot of frames? they don't have to be done sequentially if I code it correctly. also, it would be interesting to build a generative work that can be streamed over twitch from the cloud.

other
-----

test and document packaging and deployment with pyinstaller

build magic functions for screen grabs and making good documentation

bugs
----

when an error is thrown I can call run_sketch again to continue the sketch. neat trick, but it opens a new window, which perhaps it should not do.
