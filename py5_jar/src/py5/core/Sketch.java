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

import jogamp.newt.driver.macosx.WindowDriver;
import jogamp.opengl.macosx.cgl.MacOSXOnscreenCGLDrawable;
import processing.core.PApplet;
import processing.core.PMatrix2D;
import processing.core.PShape;
import processing.core.PSurface;
import processing.event.MouseEvent;
import processing.opengl.PGraphicsOpenGL;
import processing.opengl.PJOGL;
import py5.util.OpenSimplex2S;

public class Sketch extends PApplet {

  protected Py5Methods py5Methods;
  protected Set<String> py5RegisteredEvents;
  protected boolean success = false;
  protected int exitActualCallCount = 0;
  protected String py5IconPath;
  protected int[] pixelCapture = null;
  protected OpenSimplex2S osNoise = new OpenSimplex2S(0);

  public static final char CODED = PApplet.CODED;

  public static final String HIDDEN = "py5.core.graphics.HiddenPy5GraphicsJava2D";

  public void setPy5IconPath(String py5IconPath) {
    this.py5IconPath = py5IconPath;
  }

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

  public void py5Println(String text) {
    py5Methods.py5_println(text, false);
  }

  public void py5Println(String text, boolean stderr) {
    py5Methods.py5_println(text, stderr);
  }

  public String getRendererName() {
    switch (sketchRenderer()) {
    case JAVA2D:
      return "JAVA2D";
    case P2D:
      return "P2D";
    case P3D:
      return "P3D";
    case HIDDEN:
      return "HIDDEN";
    case FX2D:
      return "FX2D";
    case PDF:
      return "PDF";
    case SVG:
      return "SVG";
    case DXF:
      return "DXF";
    default:
      return null;
    }
  }

  @Override
  public void settings() {
    if (py5IconPath != null) {
      try {
        PJOGL.setIcon(py5IconPath);
      } catch (Exception e) {
      }
    }

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
      PSurface surface = getSurface();
      // This is an ugly hack to make sure the Sketch window opens above all
      // other windows. It alleviates the symptoms of bug #5 but is not a
      // proper fix. When it does get a proper fix, this needs to be removed.
      if ((platform == MACOS || platform == WINDOWS) && sketchRenderer().equals(JAVA2D)) {
        surface.setAlwaysOnTop(true);
        surface.setAlwaysOnTop(false);
      }

      if (py5IconPath != null && !(g instanceof PGraphicsOpenGL)) {
        try {
          surface.setIcon(loadImage(py5IconPath));
        } catch (Exception e) {
        }
      }

      if (py5RegisteredEvents.contains("setup")) {
        success = py5Methods.run_method("setup");
      } else {
        // parent method doesn't do anything but that might change
        super.setup();
      }

      if (platform == WINDOWS && (sketchRenderer().equals(P2D) || sketchRenderer().equals(P3D))) {
        capturePixels(true);
      }
    }
  }

  @Override
  public void draw() {
    if (pixelCapture != null) {
      restorePixels();
    }

    if (success) {
      if (py5RegisteredEvents.contains("draw")) {
        success = py5Methods.run_method("draw");
      } else {
        super.draw();
      }
    }

    if (frameCount == 1 && platform == WINDOWS && (sketchRenderer().equals(P2D) || sketchRenderer().equals(P3D))) {
      capturePixels(false);
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

  // Support the Processing Video library. The passed movie parameter will be a
  // processing.video.Movie object but that won't compile right now because the
  // Processing Video library is not yet a part of py5. Interestingly, jype is
  // able to sort out the actual object type.
  public void movieEvent(Object movie) {
    if (success && py5RegisteredEvents.contains("movie_event")) {
      success = py5Methods.run_method("movie_event", movie);
    }
  }

  @Override
  public void exit() {
    if (platform == MACOS && g.isGL() && !isLooping()) {
      loop();
    }
    super.exit();
  }

  @Override
  public void exitActual() {
    // TODO: This function needs to be re-written by someone who knows something
    // about cross platform Java GUI programming.

    // prevent an endless loop on OSX
    exitActualCallCount += 1;

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
      if (platform == MACOS && exitActualCallCount == 1) {
        final MacOSXOnscreenCGLDrawable drawable = (MacOSXOnscreenCGLDrawable) window.getDelegatedDrawable();
        WindowDriver driver = (WindowDriver) drawable.getNativeSurface();
        driver.destroy();
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
      // this is necessary for Windows but can cause a core dump on Linux for
      // OpenGL sketches that call `no_loop` when terminating via Escape key
      // seems to also be necessary on MACOS to avoid occasional ugly
      // exceptions, but at least there are no core dumps. ;)
      if (platform == WINDOWS || platform == MACOS) {
        Screen screen = window.getScreen();
        Display display = screen.getDisplay();
        display.destroy();
        screen.destroy();
      }

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

    exitActualCallCount -= 1;
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
   * This is to get around an issue with JPype method dispatching. It will always
   * use the second method signature, even when p.length == 0.
   */

  public PShape createShape(int kind, float... p) {
    if (p.length == 0) {
      return super.createShape(kind);
    } else {
      return super.createShape(kind, p);
    }
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

  /*
   * Override 3 print functions to direct the output through py5
   */

  @Override
  public void printMatrix() {
    if (g instanceof PGraphicsOpenGL) {
      py5Println(PrintUtils.toString(((PGraphicsOpenGL) g).modelview));
    } else {
      py5Println(PrintUtils.toString(g.getMatrix((PMatrix2D) null)));
    }
  }

  @Override
  public void printCamera() {
    if (g instanceof PGraphicsOpenGL) {
      py5Println(PrintUtils.toString(((PGraphicsOpenGL) g).camera));
    } else {
      py5Println("print_camera() is not available with this renderer.");
    }
  }

  @Override
  public void printProjection() {
    if (g instanceof PGraphicsOpenGL) {
      py5Println(PrintUtils.toString(((PGraphicsOpenGL) g).projection));
    } else {
      py5Println("print_projection() is not available with this renderer.");
    }
  }

  /*
   * Vectorized Processing noise
   */

  public float[] noiseArray(float[] x) {
    float[] out = new float[x.length];
    for (int i = 0; i < x.length; ++i) {
      out[i] = noise(x[i]);
    }
    return out;
  }

  public float[] noiseArray(float[] x, float[] y) {
    float[] out = new float[x.length];
    for (int i = 0; i < x.length; ++i) {
      out[i] = noise(x[i], y[i]);
    }
    return out;
  }

  public float[] noiseArray(float[] x, float[] y, float[] z) {
    float[] out = new float[x.length];
    for (int i = 0; i < x.length; ++i) {
      out[i] = noise(x[i], y[i], z[i]);
    }
    return out;
  }

  /*
   * Open Simplex noise
   */

  public void osNoiseSeed(long seed) {
    osNoise = new OpenSimplex2S(seed);
  }

  public double osNoise(double x, double y) {
    return osNoise.noise2(x, y);
  }

  public double osNoise(double x, double y, double z) {
    return osNoise.noise3_Classic(x, y, z);
  }

  public double osNoise(double x, double y, double z, double w) {
    return osNoise.noise4_Classic(x, y, z, w);
  }

  public double[] osNoiseArray(double[] x, double[] y) {
    double[] out = new double[x.length];
    for (int i = 0; i < x.length; ++i) {
      out[i] = osNoise.noise2(x[i], y[i]);
    }
    return out;
  }

  public double[] osNoiseArray(double[] x, double[] y, double[] z) {
    double[] out = new double[x.length];
    for (int i = 0; i < x.length; ++i) {
      out[i] = osNoise.noise3_Classic(x[i], y[i], y[i]);
    }
    return out;
  }

  public double[] osNoiseArray(double[] x, double[] y, double[] z, double[] w) {
    double[] out = new double[x.length];
    for (int i = 0; i < x.length; ++i) {
      out[i] = osNoise.noise4_Classic(x[i], y[i], y[i], w[i]);
    }
    return out;
  }

  /*
   * Capture and restore pixel functions, used as a workaround for a Windows
   * problem. It alleviates the symptoms of bug #5 but is not a proper fix.
   */

  protected void capturePixels(boolean alwaysOnTop) {
    surface.setAlwaysOnTop(alwaysOnTop);
    loadPixels();
    pixelCapture = new int[pixels.length];
    System.arraycopy(pixels, 0, pixelCapture, 0, pixels.length);
  }

  protected void restorePixels() {
    loadPixels();
    System.arraycopy(pixelCapture, 0, pixels, 0, pixels.length);
    pixelCapture = null;
    updatePixels();
  }
}
