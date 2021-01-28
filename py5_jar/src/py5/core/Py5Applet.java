/******************************************************************************

  Part of the py5 library
  Copyright (C) 2020-2021 Jim Schmitz

  This library is free software: you can redistribute it and/or modify it
  under the terms of the GNU Lesser General Public License as published by
  the Free Software Foundation, either version 2.1 of the License, or (at
  your option) any later version.

  This library is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
  General Public License for more details.

  You should have received a copy of the GNU Lesser General Public License
  along with this library. If not, see <https://www.gnu.org/licenses/>.

******************************************************************************/
package py5.core;

import java.util.HashSet;
import java.util.Set;

import com.jogamp.newt.Window;
import com.jogamp.newt.Screen;
import com.jogamp.newt.Display;
import com.jogamp.newt.event.KeyListener;
import com.jogamp.newt.event.MouseListener;
import com.jogamp.newt.event.WindowListener;
import com.jogamp.newt.opengl.GLWindow;

import processing.core.PApplet;
import processing.event.MouseEvent;

public class Py5Applet extends PApplet {

  protected Py5Methods py5Methods;
  protected Set<String> py5RegisteredEvents;
  protected boolean success = false;

  public static final char CODED = PApplet.CODED;

  public static final String HIDDEN = "py5.core.graphics.HiddenPy5GraphicsJava2D";

  /*
   * The below methods are how Java makes calls to the Python implementations of
   * the Processing methods.
   */

  public void usePy5Methods(Py5Methods py5Methods) {
    this.py5Methods = py5Methods;
    this.py5RegisteredEvents = new HashSet<String>();
    for (String f : py5Methods.get_function_list())
      this.py5RegisteredEvents.add(f);
    this.success = true;
  }

  public boolean getSuccess() {
    return success;
  }

  @Override
  public void settings() {
    if (success) {
      if (py5RegisteredEvents.contains("settings")) {
        success = py5Methods.run_method("settings");
      } else {
        // parent method doesn't do anything but that might change
        super.settings();
      }
    }
  }

  @Override
  public void setup() {
    if (success) {
      if (py5RegisteredEvents.contains("setup")) {
        success = py5Methods.run_method("setup");
      } else {
        // parent method doesn't do anything but that might change
        super.setup();
      }
    }
  }

  @Override
  public void draw() {
    if (success) {
      if (py5RegisteredEvents.contains("draw")) {
        success = py5Methods.run_method("draw");
      } else {
        super.draw();
      }
    }
  }

  public void preDraw() {
    if (success && py5RegisteredEvents.contains("pre_draw")) {
      success = py5Methods.run_method("pre_draw");
    }
  }

  public void postDraw() {
    if (success && py5RegisteredEvents.contains("post_draw")) {
      success = py5Methods.run_method("post_draw");
    }
  }

  @Override
  public void mousePressed() {
    if (success && py5RegisteredEvents.contains("mouse_pressed")) {
      success = py5Methods.run_method("mouse_pressed");
    }
  }

  @Override
  public void mouseReleased() {
    if (success && py5RegisteredEvents.contains("mouse_released")) {
      success = py5Methods.run_method("mouse_released");
    }
  }

  @Override
  public void mouseClicked() {
    if (success && py5RegisteredEvents.contains("mouse_clicked")) {
      success = py5Methods.run_method("mouse_clicked");
    }
  }

  @Override
  public void mouseDragged() {
    if (success && py5RegisteredEvents.contains("mouse_dragged")) {
      success = py5Methods.run_method("mouse_dragged");
    }
  }

  @Override
  public void mouseMoved() {
    if (success && py5RegisteredEvents.contains("mouse_moved")) {
      success = py5Methods.run_method("mouse_moved");
    }
  }

  @Override
  public void mouseEntered() {
    if (success && py5RegisteredEvents.contains("mouse_entered")) {
      success = py5Methods.run_method("mouse_entered");
    }
  }

  @Override
  public void mouseExited() {
    if (success && py5RegisteredEvents.contains("mouse_exited")) {
      success = py5Methods.run_method("mouse_exited");
    }
  }

  @Override
  public void mouseWheel(MouseEvent event) {
    if (success && py5RegisteredEvents.contains("mouse_wheel")) {
      success = py5Methods.run_method("mouse_wheel", event);
    }
  }

  @Override
  public void keyPressed() {
    if (success && py5RegisteredEvents.contains("key_pressed")) {
      success = py5Methods.run_method("key_pressed");
    }
  }

  @Override
  public void keyReleased() {
    if (success && py5RegisteredEvents.contains("key_released")) {
      success = py5Methods.run_method("key_released");
    }
  }

  @Override
  public void keyTyped() {
    if (success && py5RegisteredEvents.contains("key_typed")) {
      success = py5Methods.run_method("key_typed");
    }
  }

  @Override
  public void exitActual() {
    // TODO: On Linux, OpenGL sketches that call `no_loop` core dump when
    // terminating via Escape key, and this function has something to do with it.
    // This function needs to be re-written by someone who knows something about
    // Java GUI programming.

    // call exiting even if success == false. user might need to do shutdown
    // activities
    if (py5RegisteredEvents.contains("exiting")) {
      py5Methods.run_method("exiting");
      // if the exiting method was not successful we still need to run the below
      // shutdown code.
    }

    py5Methods.shutdown();

    final Object nativeWindow = surface.getNative();
    if (nativeWindow instanceof GLWindow) {
      GLWindow window = (GLWindow) nativeWindow;
      for (int i = 0; i < window.getGLEventListenerCount(); i++) {
        window.disposeGLEventListener(window.getGLEventListener(i), true);
      }
    }
    if (nativeWindow instanceof Window) {
      Window window = (Window) nativeWindow;

      // first remove the listeners before destroying window
      for (WindowListener l : window.getWindowListeners()) {
        window.removeWindowListener(l);
      }
      for (KeyListener l : window.getKeyListeners()) {
        window.removeKeyListener(l);
      }
      for (MouseListener l : window.getMouseListeners()) {
        window.removeMouseListener(l);
      }

      // get the screen and display and explicitly destroy both
      // this next piece causes the core dump but is necessary for Windows
      Screen screen = window.getScreen();
      Display display = screen.getDisplay();
      display.destroy();
      screen.destroy();

      // finally, destroy the window
      try {
        window.destroy();
      } catch (RuntimeException e) {
        // ignore possible NullPointerException since exiting anyway
      }
    } else if (nativeWindow instanceof processing.awt.PSurfaceAWT.SmoothCanvas) {
      processing.awt.PSurfaceAWT.SmoothCanvas window = (processing.awt.PSurfaceAWT.SmoothCanvas) nativeWindow;
      window.getFrame().dispose();
    } else {
      surface.setVisible(false);
    }
  }

  /*
   * These extra methods are here to get around the name collisions caused by
   * methods and fields that have the same name. That sort of thing is allowed in
   * Java but not in Python.
   */

  public float getFrameRate() {
    return frameRate;
  }

  public boolean isKeyPressed() {
    return keyPressed;
  }

  public boolean isMousePressed() {
    return mousePressed;
  }

  /*
   * New functions to improve performance
   */

  public void points(float[][] coordinates) {
    if (recorder != null)
      Py5GraphicsHelper.points(recorder, coordinates);
    Py5GraphicsHelper.points(g, coordinates);
  }

  public void lines(float[][] coordinates) {
    if (recorder != null)
      Py5GraphicsHelper.lines(recorder, coordinates);
    Py5GraphicsHelper.lines(g, coordinates);
  }

  public void vertices(float[][] coordinates) {
    if (recorder != null)
      Py5GraphicsHelper.vertices(recorder, coordinates);
    Py5GraphicsHelper.vertices(g, coordinates);
  }

  public void bezierVertices(float[][] coordinates) {
    if (recorder != null)
      Py5GraphicsHelper.bezierVertices(recorder, coordinates);
    Py5GraphicsHelper.bezierVertices(g, coordinates);
  }

  public void curveVertices(float[][] coordinates) {
    if (recorder != null)
      Py5GraphicsHelper.curveVertices(recorder, coordinates);
    Py5GraphicsHelper.curveVertices(g, coordinates);
  }

  public void quadraticVertices(float[][] coordinates) {
    if (recorder != null)
      Py5GraphicsHelper.quadraticVertices(recorder, coordinates);
    Py5GraphicsHelper.quadraticVertices(g, coordinates);
  }

}
