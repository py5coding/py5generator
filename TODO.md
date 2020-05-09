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

docstrings
----------

add docstrings to all methods, pulling docs from wherever the website documentation comes from.

It seems to have been generated with JavaDocs and this code:

https://github.com/processing/processing-docs/tree/master/java_generate

These are the xml files referenced in the `PApplet.java` comments. Most have not been updated in a while. Do I want to use this at all? Do these xml files precede the comments in the *.java files or are they the output of `GenerateDescriptions.py`?

https://github.com/processing/processing-docs/tree/master/content/api_en

It would be great if I could feed these through a translator to make this multi-linqual. Then perhaps I could do something like this:

`import py5.es as py5`

And all the docstrings would be in Spanish.

If I did this, how would I keep everything in sync? I will certainly add new functions, especially in the short term. Those new functions will be in Python so their docstrings will come from another source.

performance
-----------

Can I batch commands together and get a performance improvement? It is slower to go back and forth between Python and Java. The py5 methods can have a second "mode" that collects all the commands together and executes them all at once at the end? Should there be a flush command to manually force everything through? Perhaps I can use a context manager for a performance improvement of one part of the code.

libraries
---------

camera3D and colorblindness need to call the preDraw and postDraw methods with an Interface in the same way PApplet calls the setup and draw methods.

other
-----


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
