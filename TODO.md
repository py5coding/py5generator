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

what happened to code completion? it worked before.

get pypi package process working

error messages
--------------

Stack traces are a combination of Java and Python, which will be scary for beginners. Can I optionally hide the Java part? Can I improve the JavaException errors?

Need to add validation to make sure the parameter types are correct. I can add some type checking and helpful error messages to better support beginners. I can get the types from javap:

`javap -classpath /home/jim/Projects/git/processing/core/library/core.jar -public processing.core.PApplet`

is there anything to be gained from using type hinting?

performance
-----------

Can I batch commands together and get a performance improvement? It is slower to go back and forth between Python and Java. The py5 methods can have a second "mode" that collects all the commands together and executes them all at once at the end? Should there be a flush command to manually force everything through? Perhaps I can use a context manager for a performance improvement of one part of the code.

libraries
---------

the run_sketch command should be in a separate package (py5_tools) so it can properly set the classpath with jnius_config and then import py5. it should have params for libraries and search for the appropriate jars by getting information out of ~/.processing/preferences.txt

Processing library install process with py5_tools

rather than require users to install libraries through the PDE, I can download and install them directly using the same download mechanism. There is a text file with links to all the zip files, which I can open up and pull out the jar files.

camera3D and colorblindness need to call the preDraw and postDraw methods with an Interface in the same way PApplet calls the setup and draw methods.

other
-----

add docstrings to all methods, pulling docs from website

can the python debugger work with this?

test and document packaging and deployment with pyinstaller

build magic functions for screen grabs and making good documentation

loadPixels => pixels should be a numpy array, not a list. unsigned ints? something to help with colors? perhaps can make utility functions in addition to the standard py5 stuff, to faciliate working with other numpy libraries.

    ```
    pixels = np.array(py5.pixels, dtype=np.uint32)
    (pixels & 0x000000FF)
    (pixels & 0x0000FF00) >> 8
    (pixels & 0x00FF0000) >> 16
    ```

bugs
----
