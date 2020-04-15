import time
import jnius_config
jnius_config.set_classpath(
    '.', '/home/jim/Projects/git/processing/core/library/*')
from jnius import autoclass  # noqa

SignallerTest = autoclass('processing.core.SignallerTest')


def setup():
    print("Running Python Setup Method")


def draw():
    print("Running Python Draw Method")
    time.sleep(1)


useSignaller = True
signallerTest = SignallerTest()
if useSignaller:
    signallerTest.useSignaller()

SignallerTest.run(signallerTest)

if useSignaller:
    signaller = signallerTest.getSignaller()

    while True:
        task = signaller.getTask()
        if task == "setup":
            setup()
        elif task == "draw":
            draw()
        elif task == "exit":
            break
        signaller.resumeJava()


###############################################################################
# Signaller.java
###############################################################################
"""
package processing.core;

public class Signaller {

  private String task;

  private Object python;

  private Object java;

  public Signaller() {
    task = "";
    python = new Object();
    java = new Object();
  }

  public String getTask() {
    return task;
  }

  public void resumeJava() {
    synchronized (java) {
      java.notify();
    }
    synchronized (python) {
      try {
        python.wait();
      } catch (InterruptedException e) {
        e.printStackTrace();
      }
    }
  }

  public void resumePython(String task) {
    this.task = task;
    synchronized (python) {
      python.notify();
    }
    synchronized (java) {
      try {
        java.wait();
      } catch (InterruptedException e) {
        e.printStackTrace();
      }
    }
  }
}
"""

###############################################################################
# SignallerTest.java
###############################################################################
"""
package processing.core;

public class SignallerTest {

  private Signaller signaller;

  public SignallerTest() {

  }

  public void useSignaller() {
    signaller = new Signaller();
  }

  public Signaller getSignaller() {
    return signaller;
  }

  public void setup() {
    if (signaller != null) {
      signaller.resumePython("setup");
    } else {
      System.out.println("Running Java Setup Method");
    }
  }

  public void draw() {
    if (signaller != null) {
      signaller.resumePython("draw");
    } else {
      System.out.println("Running Java Draw Method");
      try {
        Thread.sleep(1000);
      } catch (InterruptedException e) {
        e.printStackTrace();
      }
    }
  }

  private void runLoop() {
    System.out.println("Pre-Setup Phase");
    setup();
    System.out.println("Post-Setup Phase");

    for (int i = 0; i < 20; i++) {
      System.out.println("Pre-Draw Phase");
      draw();
      System.out.println("Post-Draw Phase");
    }
    if (signaller != null) {
      signaller.resumePython("exit");
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
