package processing.core;

import com.jogamp.newt.event.KeyListener;
import com.jogamp.newt.event.MouseListener;
import com.jogamp.newt.event.WindowListener;

import processing.event.MouseEvent;

public class Py5Applet extends PApplet {

  protected Py5Methods py5Methods;

  public void usePy5Methods(Py5Methods py5Methods) {
    this.py5Methods = py5Methods;
  }

  @Override
  public void settings() {
    py5Methods.run_method("settings");
  }

  @Override
  public void setup() {
    py5Methods.run_method("setup");
  }

  @Override
  public void draw() {
    py5Methods.run_method("draw");
  }

  @Override
  public void mousePressed() {
    py5Methods.run_method("mouse_pressed");
  }

  @Override
  public void mouseReleased() {
    py5Methods.run_method("mouse_released");
  }

  @Override
  public void mouseClicked() {
    py5Methods.run_method("mouse_clicked");
  }

  @Override
  public void mouseDragged() {
    py5Methods.run_method("mouse_dragged");
  }

  @Override
  public void mouseMoved() {
    py5Methods.run_method("mouse_moved");
  }

  @Override
  public void mouseEntered() {
    py5Methods.run_method("mouse_entered");
  }

  @Override
  public void mouseExited() {
    py5Methods.run_method("mouse_exited");
  }

  @Override
  public void mouseWheel(MouseEvent event) {
    py5Methods.mouse_wheel(event);
  }

  @Override
  public void keyPressed() {
    py5Methods.run_method("key_pressed");
  }

  @Override
  public void keyReleased() {
    py5Methods.run_method("key_released");
  }

  @Override
  public void keyTyped() {
    py5Methods.run_method("key_typed");
  }

  @Override
  public void exitActual() {
    py5Methods.run_method("exit_actual");

    final Object nativeWindow = surface.getNative();
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
    } else {
      surface.setVisible(false);
    }
  }

  public float getFrameRate() {
    return frameRate;
  }

  public boolean isKeyPressed() {
    return keyPressed;
  }

}
