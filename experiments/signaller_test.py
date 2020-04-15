import sys
import time
import jnius_config
jnius_config.set_classpath(
    '.', '/home/jim/Projects/git/processing/core/library/*')
from jnius import autoclass  # noqa

SignallerTest = autoclass('processing.core.SignallerTest')


def setup():
    print("Running Python Setup Method", file=sys.stderr, flush=True)
    # time.sleep(0.1)


def draw():
    print("Running Python Draw Method", file=sys.stderr, flush=True)
    # time.sleep(0.1)


useSignaller = True
signallerTest = SignallerTest()
if useSignaller:
    signallerTest.useSignaller()
    signaller = signallerTest.getSignaller()

SignallerTest.run(signallerTest)

if useSignaller:
    while True:
        task = signaller.getTask()
        if not task:
            time.sleep(0.001)
            continue
        signaller.clearTask()
        if task == "setup":
            setup()
        elif task == "draw":
            draw()
        elif task == "exit":
            break
        signaller.resumeJava()


###############################################################################
# PythonBlocker.java
###############################################################################
"""
package processing.core;

public class PythonBlocker {

  private String task;

  private boolean block;

  public PythonBlocker() {
    task = "";
    block = true;
  }

  public String getTask() {
    return task;
  }

  public void clearTask() {
    task = "";
  }

  public synchronized void resumeJava() {
    block = false;
    notifyAll();
  }

  public synchronized void pythonTask(String task) {
    this.task = task;

    while (block) {
      try {
        wait();
      } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
      }
    }

    block = true;
  }
}
"""

###############################################################################
# SignallerTest.java
###############################################################################
"""
package processing.core;

public class SignallerTest {

  private PythonBlocker signaller;

  public SignallerTest() {

  }

  public void useSignaller() {
    signaller = new PythonBlocker();
  }

  public PythonBlocker getSignaller() {
    return signaller;
  }

  public void setup() {
    if (signaller != null) {
      signaller.pythonTask("setup");
    } else {
      System.err.println("Running Java Setup Method");
    }
  }

  public void draw() {
    if (signaller != null) {
      signaller.pythonTask("draw");
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
    if (signaller != null) {
      signaller.pythonTask("exit");
    }
  }

  public static void run(SignallerTest obj) {
    new Thread() {
      @Override
      public void run() {
        obj.runLoop();
      }
    }.start();
  }

}
"""
