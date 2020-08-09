package py5.core;

import java.util.HashSet;
import java.util.Set;

import com.jogamp.newt.event.KeyListener;
import com.jogamp.newt.event.MouseListener;
import com.jogamp.newt.event.WindowListener;

import processing.core.PApplet;
import processing.event.MouseEvent;

public class Py5Applet extends PApplet {

  protected Py5Methods py5Methods;
  protected Set<String> py5RegisteredEvents;

  public static final char CODED = PApplet.CODED;

  public static final String HIDDEN = "py5.core.hidden.HiddenPGraphicsJava2D";

  public void usePy5Methods(Py5Methods py5Methods) {
    this.py5Methods = py5Methods;
    this.py5RegisteredEvents = new HashSet<String>();
    for (String f : py5Methods.get_function_list())
      this.py5RegisteredEvents.add(f);
  }

  @Override
  public void settings() {
    if (py5RegisteredEvents.contains("settings")) {
      boolean success = py5Methods.run_method("settings");
      if (!success) {
        throw new RuntimeException("py5 method failure in settings");
      }
    }
  }

  @Override
  public void setup() {
    if (py5RegisteredEvents.contains("setup")) {
      boolean success = py5Methods.run_method("setup");
      if (!success) {
        throw new RuntimeException("py5 method failure in setup");
      }
    }
  }

  @Override
  public void draw() {
    if (py5RegisteredEvents.contains("draw")) {
      boolean success = py5Methods.run_method("draw");
      if (!success) {
        throw new RuntimeException("py5 method failure in draw");
      }
    } else {
      noLoop();
    }
  }

  @Override
  public void mousePressed() {
    if (py5RegisteredEvents.contains("mouse_pressed")) {
      boolean success = py5Methods.run_method("mouse_pressed");
      if (!success) {
        throw new RuntimeException("py5 method failure in mouse_pressed");
      }
    }
  }

  @Override
  public void mouseReleased() {
    if (py5RegisteredEvents.contains("mouse_released")) {
      boolean success = py5Methods.run_method("mouse_released");
      if (!success) {
        throw new RuntimeException("py5 method failure in mouse_released");
      }
    }
  }

  @Override
  public void mouseClicked() {
    if (py5RegisteredEvents.contains("mouse_clicked")) {
      boolean success = py5Methods.run_method("mouse_clicked");
      if (!success) {
        throw new RuntimeException("py5 method failure in mouse_clicked");
      }
    }
  }

  @Override
  public void mouseDragged() {
    if (py5RegisteredEvents.contains("mouse_dragged")) {
      boolean success = py5Methods.run_method("mouse_dragged");
      if (!success) {
        throw new RuntimeException("py5 method failure in mouse_dragged");
      }
    }
  }

  @Override
  public void mouseMoved() {
    if (py5RegisteredEvents.contains("mouse_moved")) {
      boolean success = py5Methods.run_method("mouse_moved");
      if (!success) {
        throw new RuntimeException("py5 method failure in mouse_moved");
      }
    }
  }

  @Override
  public void mouseEntered() {
    if (py5RegisteredEvents.contains("mouse_entered")) {
      boolean success = py5Methods.run_method("mouse_entered");
      if (!success) {
        throw new RuntimeException("py5 method failure in mouse_entered");
      }
    }
  }

  @Override
  public void mouseExited() {
    if (py5RegisteredEvents.contains("mouse_exited")) {
      boolean success = py5Methods.run_method("mouse_exited");
      if (!success) {
        throw new RuntimeException("py5 method failure in mouse_exited");
      }
    }
  }

  @Override
  public void mouseWheel(MouseEvent event) {
    if (py5RegisteredEvents.contains("mouse_wheel")) {
      boolean success = py5Methods.run_method("mouse_wheel", event);
      if (!success) {
        throw new RuntimeException("py5 method failure in mouse_wheel");
      }
    }
  }

  @Override
  public void keyPressed() {
    if (py5RegisteredEvents.contains("key_pressed")) {
      boolean success = py5Methods.run_method("key_pressed");
      if (!success) {
        throw new RuntimeException("py5 method failure in key_pressed");
      }
    }
  }

  @Override
  public void keyReleased() {
    if (py5RegisteredEvents.contains("key_released")) {
      boolean success = py5Methods.run_method("key_released");
      if (!success) {
        throw new RuntimeException("py5 method failure in key_released");
      }
    }
  }

  @Override
  public void keyTyped() {
    if (py5RegisteredEvents.contains("key_typed")) {
      boolean success = py5Methods.run_method("key_typed");
      if (!success) {
        throw new RuntimeException("py5 method failure in key_typed");
      }
    }
  }

  @Override
  public void exitActual() {
    if (py5RegisteredEvents.contains("exiting")) {
      py5Methods.run_method("exiting");
      // if the exiting method was not successful we still need to run the below
      // shutdown code.
    }

    py5Methods.shutdown();

    // TODO: why do I need all of this? I know `dispose()` by itself isn't good
    // enough.
    // it gets called by the exit() function before exitActual()
    final Object nativeWindow = surface.getNative();
    if (nativeWindow instanceof com.jogamp.newt.opengl.GLWindow) {
      com.jogamp.newt.opengl.GLWindow window = (com.jogamp.newt.opengl.GLWindow) nativeWindow;
      for (int i = 0; i < window.getGLEventListenerCount(); i++) {
        window.disposeGLEventListener(window.getGLEventListener(i), true);
      }
    }
    if (nativeWindow instanceof com.jogamp.newt.Window) {
      com.jogamp.newt.Window window = (com.jogamp.newt.Window) nativeWindow;
      // remove the listeners before destroying window to prevent a core dump
      for (WindowListener l : window.getWindowListeners()) {
        window.removeWindowListener(l);
      }
      for (KeyListener l : window.getKeyListeners()) {
        window.removeKeyListener(l);
      }
      for (MouseListener l : window.getMouseListeners()) {
        window.removeMouseListener(l);
      }
      window.destroy();
    } else if (nativeWindow instanceof processing.awt.PSurfaceAWT.SmoothCanvas) {
      processing.awt.PSurfaceAWT.SmoothCanvas window = (processing.awt.PSurfaceAWT.SmoothCanvas) nativeWindow;
      window.getFrame().dispose();
    } else {
      // TODO: remove this statement
      System.out.println("Making window invisible but not actually destroying it.");
      surface.setVisible(false);
    }
  }

  public float getFrameRate() {
    return frameRate;
  }

  public boolean isKeyPressed() {
    return keyPressed;
  }

  public boolean isMousePressed() {
    return mousePressed;
  }

}
