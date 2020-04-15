support dynamic variables like frameRate and mouseX, mouseY, skip deprecated, objects that don't change, height, width, etc that don't change
have animation thread be in its own thread that can be stopped

command line py5 generator util
command line run_sketch util

run_sketch function from py5 module: needs to have event functions passed in. can I
write a function to pull them  out of the local() or global() namespaces? can I combine
it with what I am doing in the exec_test2.py file? I should also be able to create a class and run the class. That will make it easier to pass in the event methods.

fork and edit PApplet class instead of duplicating code in the PythonPApplet class
don't hardcode the classpath in py5generator or py5. or should the jars be part of the project? YES!
** jars should be a part of the project because otherwise there could be versioning issues.
ability to set JVM options like heap size

support key and mouse events
support Processing libraries

build magic functions for screen grabs and making good documentation

add docstrings to all methods, pulling docs from website
is there anything to be gained from using type hinting?

rather than require users to install libraries through the PDE, I can download and install
them directly using the same download mechanism. There is a text file with links to all
the zip files, which I can open up and pull out the jar files.

skip over @Deprecated constants
skip over all protected constants, variables, and methods
possible solution: parse the output of javap
javap -classpath /home/jim/Projects/git/processing/core/library/core.jar -public processing.core.PApplet
javap -classpath /home/jim/Projects/git/processing/core/library/core.jar -public processing.core.PConstants


loadPixels => pixels should be a numpy array, not a list. unsigned ints? something to help with colors? perhaps can make utility functions in addition to the standard py5 stuff, to faciliate working with other numpy libraries.

pixels = np.array(py5.pixels, dtype=np.uint32)

(pixels & 0x000000FF)
(pixels & 0x0000FF00) >> 8
(pixels & 0x00FF0000) >> 16



How to get this working for P2D and P3D in addition to JAVA2D renderers
=======================================================================

The PSurfaceJOGL class has a DrawListener class that calls sketch.handleDraw.
That DrawListener gets passed to window.addGLEventListener and that object calls
a display method. I can't cut that method apart so I need to use a lock
somewhere to call handleDraw or draw myself.

Why not use semaphors for all the renderers? It would simplify the
implementation a bit. I would not need to split up the handleSettings and
handleDraw methods. Those are the only places where settings, setup, or draw are
called, outside of libraries like Camera3D that also call those methods.

Inside the default settings, setup, and draw methods in PApplet, I can use a
signaller to block and resume Python execution. That can then run the Python
methods. I can do this for the keyboard and mouse event methods also.

Only Py5 will not be able to call the subclassed methods in a sketch! The Java
Processing sketches will override those methods.
