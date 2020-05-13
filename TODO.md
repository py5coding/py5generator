TODOS
=====

INFO
----

Building py5:

$ make clean
$ make processing_dir=../sam_processing4 py5_dir=../py5build

The Processing jars need to exist and be built. If I am using Processing3 I need to compile with java 1.8. I can use it with a command like this:

(JAVA_HOME="/usr/lib/jvm/jdk1.8.0_74"; ant -f /home/jim/Projects/ITP/pythonprocessing/processing/core/build.xml)

Processing4 integration branch:
[repo](https://github.com/sampottinger/processing4)
[builds](https://www.datadrivenempathy.com/processing)

packaging and deployment
------------------------

get pypi package process working

properly include stub files and show that they work. Here are some packages that use them:

* [pyrsistent](https://github.com/tobgu/pyrsistent)
* [attrs](https://github.com/python-attrs/attrs)

error messages
--------------

Stack traces are a combination of Java and Python, which will be scary for beginners. Can I optionally hide the Java part? Can I improve the JavaException errors?

Need to add validation to make sure the parameter types are correct. I can add some type checking and helpful error messages to better support beginners. I can get the types from javap:

`javap -classpath /home/jim/Projects/git/processing/core/library/core.jar -public processing.core.PApplet`

Or I can use Java reflection to get the information.

use [type hinting](https://docs.python.org/3/library/typing.html) for Processing functions. I can use `@overload` for overloaded functions. [PEP-0484](https://www.python.org/dev/peps/pep-0484/) explains in more detail.

Can I use *.pyi files (stub files) to help VSCode with code completion? According to [stackoverflow](https://stackoverflow.com/questions/53578365/does-vscode-support-python-pyi-files-for-intellisense), it should. Can that replace the need for what I did to get the code completion to work? How well does this work if Jedi is turned on?

docstrings
----------

add docstrings to all methods, pulling docs from wherever the website documentation comes from.

It seems to have been generated with [JavaDocs and some Python code](https://github.com/processing/processing-docs/tree/master/java_generate).

The repo also contains the [xml files](https://github.com/processing/processing-docs/tree/master/content/api_en) referenced in the `PApplet.java` comments. Most have not been updated in a while. Do I want to use this at all? Do these xml files precede the comments in the *.java files or are they the output of `GenerateDescriptions.py`?

It would be great if I could feed these through a translator to make this multi-linqual. Then perhaps I could do something like `import py5.es as py5` to make all the docstrings in Spanish.

If I did this, how would I keep everything in sync? I will certainly add new functions, especially in the short term. Those new functions will be in Python so their docstrings will come from another source.

performance
-----------

Can I batch commands together and get a performance improvement? It is slower to go back and forth between Python and Java. The py5 methods can have a second "mode" that collects all the commands together and executes them all at once at the end? Should there be a flush command to manually force everything through? Perhaps I can use a context manager for a performance improvement of one part of the code.

libraries
---------

need to add [Processing's non-core jars](https://processing.org/reference/libraries/) for other libraries like PDF, SVG, Video, Sound.

camera3D and colorblindness need to call the preDraw and postDraw methods with an Interface in the same way PApplet calls the setup and draw methods.

other
-----

can the python debugger work with this?

test and document packaging and deployment with pyinstaller

build magic functions for screen grabs and making good documentation

bugs
----
