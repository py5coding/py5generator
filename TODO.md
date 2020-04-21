TODOS
=====

clean up generator.py
---------------------

build process should copy the jars as well as setup all the package files.

ability to set JVM options like heap size, add to classpath

design sketch execution
-----------------------

command line run_sketch util

run_sketch function from py5 module: needs to have event functions passed in. can I write a function to pull them out of the local() or global() namespaces? can I combine it with what I am doing in the exec_test2.py file? I should also be able to create a class and run the class. That will make it easier to pass in the event methods.

the two main execution methods should be inheriting from a class and `from py5 import *`. for the second one there should be command line tool to run the sketch. the third is the current one where someone types `import py5` but does
not create a class but passes the methods to a run method.

error messages
--------------

stack traces are a combination of Java and Python. Need to add validation to make sure the parameter types are correct. I can add some type checking and helpful error messages to better support beginners.

is there anything to be gained from using type hinting? I can get the types from javap:

`javap -classpath /home/jim/Projects/git/processing/core/library/core.jar -public processing.core.PApplet`

I'll need that to validate parameter types.

libraries
---------

Processing library install process

rather than require users to install libraries through the PDE, I can download and install them directly using the same download mechanism. There is a text file with links to all the zip files, which I can open up and pull out the jar files.

other
-----

have animation thread be in its own thread that can be stopped

build magic functions for screen grabs and making good documentation

add docstrings to all methods, pulling docs from website

loadPixels => pixels should be a numpy array, not a list. unsigned ints? something to help with colors? perhaps can make utility functions in addition to the standard py5 stuff, to faciliate working with other numpy libraries.

    ```
    pixels = np.array(py5.pixels, dtype=np.uint32)
    (pixels & 0x000000FF)
    (pixels & 0x0000FF00) >> 8
    (pixels & 0x00FF0000) >> 16
    ```

bugs
----

need way to get public frameRate, fullScreen, pixelDensity, and smooth vars

fullScreen mode causes crazy errors with the `key` variable

camera3D is slower than it should be

camera3D and colorblindness need to call the preDraw and postDraw methods with an Interface in the same way PApplet calls the setup and draw methods.
