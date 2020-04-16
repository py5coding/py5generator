import sys
import time
import jnius_config
jnius_config.set_classpath(
    '.', '/home/jim/Projects/git/processing/core/library/*')
from jnius import autoclass  # noqa

PythonTaskBlockerTest = autoclass('processing.core.PythonTaskBlockerTest')


def setup():
    print("Running Python Setup Method", file=sys.stderr, flush=True)
    # time.sleep(0.1)


def draw():
    print("Running Python Draw Method", file=sys.stderr, flush=True)
    # time.sleep(0.1)


useBlocker = True
blockerTest = PythonTaskBlockerTest()
if useBlocker:
    blockerTest.activatePythonTaskBlocker()
    signaller = blockerTest.getPythonTaskBlocker()

PythonTaskBlockerTest.run(blockerTest)

if useBlocker:
    while True:
        task = signaller.getPythonTask()
        if not task:
            time.sleep(0.001)
            continue
        if task == "setup":
            setup()
        elif task == "draw":
            draw()
        elif task == "exit":
            break
        signaller.continueJava()


###############################################################################
# PythonTaskBlocker.java
###############################################################################
"""
package processing.core;

public class PythonTaskBlocker {

  private String task;

  public PythonTaskBlocker() {
    task = "";
  }

  public String getPythonTask() {
    return task;
  }

  public synchronized void continueJava() {
    task = "";
    notifyAll();
  }

  public synchronized void setPythonTask(String task) {
    this.task = task;

    try {
      wait();
    } catch (InterruptedException e) {
      Thread.currentThread().interrupt();
    }
  }
}
"""

###############################################################################
# PythonTaskBlockerTest.java
###############################################################################
"""
package processing.core;

public class PythonTaskBlockerTest {

  private PythonTaskBlocker pythonTaskBlocker;

  public PythonTaskBlockerTest() {

  }

  public void activatePythonTaskBlocker() {
    pythonTaskBlocker = new PythonTaskBlocker();
  }

  public PythonTaskBlocker getPythonTaskBlocker() {
    return pythonTaskBlocker;
  }

  public void setup() {
    if (pythonTaskBlocker != null) {
      pythonTaskBlocker.setPythonTask("setup");
    } else {
      System.err.println("Running Java Setup Method");
    }
  }

  public void draw() {
    if (pythonTaskBlocker != null) {
      pythonTaskBlocker.setPythonTask("draw");
    } else {
      System.err.println("Running Java Draw Method");
    }
  }

  private void runLoop() {
    System.err.println("Pre-Setup Phase");
    setup();
    System.err.println("Post-Setup Phase");

    for (int i = 0; i < 20; i++) {
      System.err.println("Pre-Draw Phase");
      draw();
      System.err.println("Post-Draw Phase");
    }
    if (pythonTaskBlocker != null) {
      pythonTaskBlocker.setPythonTask("exit");
    }
  }

  public static void run(PythonTaskBlockerTest obj) {
    new Thread() {
      @Override
      public void run() {
        obj.runLoop();
      }
    }.start();
  }

}
"""
