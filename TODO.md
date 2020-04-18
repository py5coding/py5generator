TODOS
=====

clean up generator.py
---------------------

jars should be a part of the python module, otherwise there could be versioning issues.

ability to set JVM options like heap size

command line py5 generator util, need a clean build process that runs ant, copies the jar, runs the generator, and puts the result into the py5 directory.

dynamic variables
-----------------

support dynamic variables like frameRate and mouseX, mouseY

skip anything @Deprecated

skip objects that don't change like height, width, etc

skip over all protected constants, variables, and methods

design sketch execution
-----------------------

command line run_sketch util

run_sketch function from py5 module: needs to have event functions passed in. can I
write a function to pull them  out of the local() or global() namespaces? can I combine
it with what I am doing in the exec_test2.py file? I should also be able to create a class and run the class. That will make it easier to pass in the event methods.

libraries
---------

Processing library install process

rather than require users to install libraries through the PDE, I can download and install them directly using the same download mechanism. There is a text file with links to all the zip files, which I can open up and pull out the jar files.

other
-----

have animation thread be in its own thread that can be stopped

support key and mouse events

build magic functions for screen grabs and making good documentation

add docstrings to all methods, pulling docs from website

is there anything to be gained from using type hinting? I can get the types from javap:

`javap -classpath /home/jim/Projects/git/processing/core/library/core.jar -public processing.core.PApplet`

loadPixels => pixels should be a numpy array, not a list. unsigned ints? something to help with colors? perhaps can make utility functions in addition to the standard py5 stuff, to faciliate working with other numpy libraries.

    ```
    pixels = np.array(py5.pixels, dtype=np.uint32)
    (pixels & 0x000000FF)
    (pixels & 0x0000FF00) >> 8
    (pixels & 0x00FF0000) >> 16
    ```
