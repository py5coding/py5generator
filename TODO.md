support all dynamic variables like frameRate and mouseX, mouseY

command line py5 generator util
command line run_sketch util

fork and edit PApplet class instead of duplicating code in the PythonPApplet class
don't hardcode the classpath in py5generator or py5. or should the jars be part of the project?
** jars should be a part of the project because otherwise there could be versioning issues.
ability to set JVM options like heap size

support key and mouse events
support Processing libraries

add docstrings to all methods, pulling docs from website
is there anything to be gained from using type hinting?


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
