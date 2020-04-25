TODOS
=====

clean up generator.py
---------------------

remove hardcoded path to py5.jar from jnius_setup and get rid of the Modifier stuff if it can be done more simply.

should generate_py5 really be a command? why not make it into a regular script so the paths to py5.jar and the py5 resources can be simpler.

test with Processing4 integration branch
https://github.com/sampottinger/processing4
https://www.datadrivenempathy.com/processing

design sketch execution
-----------------------

command line run_sketch util

is it possible to make a py5 reset function to create a new _papplet? I just need the run_sketch function to create a new PApplet instance. I should also add something to not re-import pyjnius if the jvm is already running.

run_sketch function from py5 module: needs to have event functions passed in. can I write a function to pull them out of the local() or global() namespaces? can I combine it with what I am doing in the exec_test2.py file? I should also be able to create a class and run the class. That will make it easier to pass in the event methods.

the two main execution methods should be inheriting from a class and `from py5 import *`. for the second one there should be command line tool to run the sketch. the third is the current one where someone types `import py5` but does
not create a class but passes the methods to a run method.

_update_vars slowing this down. I make it faster with on-demand updates

Can I batch commands together and get a performance improvement? It is slower to go back and forth between Python and Java and I already saw that Camera3D has a problem. The py5 methods can have a second "mode" that collects all the commands together and executes them all at once at the end? Should there be a flush command to manually force everything through? Perhaps I can use a context manager for a performance improvement of one part of the code.

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

integrate debugging

test and document packaging and deployment with pyinstaller

have animation thread be in its own thread that can be stopped or paused

build magic functions for screen grabs and making good documentation

add docstrings to all methods, pulling docs from website

loadPixels => pixels should be a numpy array, not a list. unsigned ints? something to help with colors? perhaps can make utility functions in addition to the standard py5 stuff, to faciliate working with other numpy libraries.

    ```
    pixels = np.array(py5.pixels, dtype=np.uint32)
    (pixels & 0x000000FF)
    (pixels & 0x0000FF00) >> 8
    (pixels & 0x00FF0000) >> 16
    ```

headless mode that grabs keyboard events from the terminal. this can be done in java and would be useful for sound and text sketches.

can I use terminal graphics to display the output? there are terminal image viewers. some ideas:
https://docs.python.org/3/library/curses.html
http://urwid.org/index.html  https://github.com/urwid/urwid
https://github.com/peterbrittain/asciimatics
https://pypi.org/project/PySixel/

bugs
----

is the type of key and keyCode correct? Key is not supposed to be a number

fullScreen mode causes crazy errors with the `key` variable in camera3D_test?

camera3D is slower than it should be

camera3D and colorblindness need to call the preDraw and postDraw methods with an Interface in the same way PApplet calls the setup and draw methods.
