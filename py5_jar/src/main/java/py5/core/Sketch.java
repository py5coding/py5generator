/******************************************************************************

  Part of the py5 library
  Copyright (C) 2020-2022 Jim Schmitz

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

import java.io.File;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
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
import processing.core.PConstants;
import processing.core.PMatrix2D;
import processing.core.PShape;
import processing.core.PSurface;
import processing.event.Event;
import processing.event.KeyEvent;
import processing.event.MouseEvent;
import processing.opengl.PGraphicsOpenGL;
import processing.opengl.PJOGL;
import py5.util.KeyEventUtilities;
import py5.util.OpenSimplex2S;

public class Sketch extends PApplet {

  protected Py5Bridge py5Bridge;
  protected Set<String> py5RegisteredEvents;
  protected Map<String, Integer> py5RegisteredEventParamCounts;
  protected boolean success = false;
  protected int exitActualCallCount = 0;
  protected String py5IconPath;
  protected int[] pixelCapture = null;
  protected long osNoiseSeed = (long) (Math.random() * Long.MAX_VALUE);
  public Integer lastWindowX;
  public Integer lastWindowY;

  public static final char CODED = PApplet.CODED;

  public static final String HIDDEN = "py5.core.graphics.HiddenPy5GraphicsJava2D";

  public Sketch() {
    Sketch.useNativeSelect = platform == MACOS;
  }

  public void setPy5IconPath(String py5IconPath) {
    this.py5IconPath = py5IconPath;
  }

  public static void setJOGLProperties(String py5Path) {
    if (System.getProperty("jogamp.gluegen.UseTempJarCache") == null) {
      System.setProperty("jogamp.gluegen.UseTempJarCache", "false");
    }

    String variant = PConstants.platformNames[PApplet.platform] + "-" + System.getProperty("os.arch");
    String joglPath = py5Path + File.separator + "natives" + File.separator + variant;
    String javaLibraryPath = System.getProperty("java.library.path");
    if (javaLibraryPath == null) {
      System.setProperty("java.library.path", joglPath);
    } else if (!javaLibraryPath.contains(joglPath)) {
      System.setProperty("java.library.path", javaLibraryPath + File.pathSeparator + joglPath);
    }
  }

  /*
   * The below methods are how Java makes calls to the Python implementations of
   * the Processing methods.
   */

  public void buildPy5Bridge(Py5Bridge py5Bridge) {
    this.py5Bridge = py5Bridge;
    this.py5RegisteredEvents = new HashSet<String>();
    this.py5RegisteredEventParamCounts = new HashMap<String, Integer>();
    for (String f : py5Bridge.get_function_list()) {
      String[] nameParamCountPairs = f.split(":");
      this.py5RegisteredEvents.add(nameParamCountPairs[0]);
      this.py5RegisteredEventParamCounts.put(nameParamCountPairs[0], Integer.parseInt(nameParamCountPairs[1]));
    }
    this.success = true;
  }

  public boolean getSuccess() {
    return success;
  }

  public void _terminateSketch(boolean error) {
    success = !error;
    py5Bridge.terminate_sketch();
  }

  public Object callPython(String key, Object... params) {
    Object retVal = py5Bridge.call_function(key, params);
    if (retVal instanceof RuntimeException) {
      throw ((RuntimeException) retVal);
    } else {
      return retVal;
    }
  }

  public void py5Println(String text) {
    py5Bridge.py5_println(text, false);
  }

  public void py5Println(String text, boolean stderr) {
    py5Bridge.py5_println(text, stderr);
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
        success = py5Bridge.run_method("settings");
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
        success = py5Bridge.run_method("setup");
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
        success = py5Bridge.run_method("draw");
      } else {
        // super.draw();
      }
    }

    if (frameCount == 1 && platform == WINDOWS && (sketchRenderer().equals(P2D) || sketchRenderer().equals(P3D))) {
      capturePixels(false);
    }
  }

  public void preDraw() {
    if (success && py5RegisteredEvents.contains("pre_draw")) {
      success = py5Bridge.run_method("pre_draw");
    }
  }

  public void postDraw() {
    if (success && py5RegisteredEvents.contains("post_draw")) {
      success = py5Bridge.run_method("post_draw");
    }
  }

  @Override
  public void windowMoved() {
    if (success && py5RegisteredEvents.contains("window_moved")) {
      success = py5Bridge.run_method("window_moved");
    }
  }

  @Override
  public void windowResized() {
    if (success && py5RegisteredEvents.contains("window_resized")) {
      success = py5Bridge.run_method("window_resized");
    }
  }

  protected boolean handleInputEventOneParam(String eventName, Event event) {
    if (success && py5RegisteredEvents.contains(eventName) && py5RegisteredEventParamCounts.get(eventName) == 1) {
      py5Bridge.run_method(eventName, event);
      return true;
    } else {
      return false;
    }
  }

  protected void handleInputEventNoParams(String eventName) {
    if (success && py5RegisteredEvents.contains(eventName) && py5RegisteredEventParamCounts.get(eventName) == 0) {
      py5Bridge.run_method(eventName);
    }
  }

  @Override
  public void mousePressed(MouseEvent event) {
    if (!handleInputEventOneParam("mouse_pressed", event)) {
      mousePressed();
    }
  }

  @Override
  public void mousePressed() {
    handleInputEventNoParams("mouse_pressed");
  }

  @Override
  public void mouseReleased(MouseEvent event) {
    if (!handleInputEventOneParam("mouse_released", event)) {
      mouseReleased();
    }
  }

  @Override
  public void mouseReleased() {
    handleInputEventNoParams("mouse_released");
  }

  @Override
  public void mouseClicked(MouseEvent event) {
    if (!handleInputEventOneParam("mouse_clicked", event)) {
      mouseClicked();
    }
  }

  @Override
  public void mouseClicked() {
    handleInputEventNoParams("mouse_clicked");
  }

  @Override
  public void mouseDragged(MouseEvent event) {
    if (!handleInputEventOneParam("mouse_dragged", event)) {
      mouseDragged();
    }
  }

  @Override
  public void mouseDragged() {
    handleInputEventNoParams("mouse_dragged");
  }

  @Override
  public void mouseMoved(MouseEvent event) {
    if (!handleInputEventOneParam("mouse_moved", event)) {
      mouseMoved();
    }
  }

  @Override
  public void mouseMoved() {
    handleInputEventNoParams("mouse_moved");
  }

  @Override
  public void mouseEntered(MouseEvent event) {
    if (!handleInputEventOneParam("mouse_entered", event)) {
      mouseEntered();
    }
  }

  @Override
  public void mouseEntered() {
    handleInputEventNoParams("mouse_entered");
  }

  @Override
  public void mouseExited(MouseEvent event) {
    if (!handleInputEventOneParam("mouse_exited", event)) {
      mouseExited();
    }
  }

  @Override
  public void mouseExited() {
    handleInputEventNoParams("mouse_exited");
  }

  @Override
  public void mouseWheel(MouseEvent event) {
    if (!handleInputEventOneParam("mouse_wheel", event)) {
      mouseWheel();
    }
  }

  @Override
  public void mouseWheel() {
    handleInputEventNoParams("mouse_wheel");
  }

  @Override
  public void keyPressed(KeyEvent event) {
    if (!handleInputEventOneParam("key_pressed", event)) {
      keyPressed();
    }
  }

  @Override
  public void keyPressed() {
    handleInputEventNoParams("key_pressed");
  }

  @Override
  public void keyReleased(KeyEvent event) {
    if (!handleInputEventOneParam("key_released", event)) {
      keyReleased();
    }
  }

  @Override
  public void keyReleased() {
    handleInputEventNoParams("key_released");
  }

  @Override
  public void keyTyped(KeyEvent event) {
    if (!handleInputEventOneParam("key_typed", event)) {
      keyTyped();
    }
  }

  @Override
  public void keyTyped() {
    handleInputEventNoParams("key_typed");
  }

  // Support the Processing Video library. The passed movie parameter will be a
  // processing.video.Movie object but that won't compile right now because the
  // Processing Video library is not a part of py5. Nevertheless, jpype is able
  // to sort out the actual object type, so it doesn't actually matter.
  public void movieEvent(Object movie) {
    if (success && py5RegisteredEvents.contains("movie_event")
        && py5RegisteredEventParamCounts.get("movie_event") == 1) {
      success = py5Bridge.run_method("movie_event", movie);
    }
  }

  public void fakeMouseEvent(int action, int modifiers, int x, int y, int button, int count) {
    postEvent(new MouseEvent(null, System.currentTimeMillis(), action, modifiers, x, y, button, count));
  }

  public void fakeKeyEvent(int action, int modifiers, String input, boolean isAutoRepeat) {
    char key = KeyEventUtilities.getASCIIKey(input);
    int keyCode;

    if (key > 0) {
      keyCode = key;
    } else {
      key = PApplet.CODED;
      keyCode = g.isGL() ? KeyEventUtilities.getJogampKeyCode(input) : KeyEventUtilities.getAWTKeyCode(input);
      if (keyCode < 0) {
        py5Println("py5 is unable to map '" + input
            + "' to a proper key_code value. Your renderer is " + getRendererName() + " and your platform is "
            + PConstants.platformNames[PApplet.platform]
            + ". Please open an issue on github to report this bug.", true);
      }
    }

    postEvent(new KeyEvent(null, System.currentTimeMillis(), action, modifiers, key, keyCode, isAutoRepeat));
  }

  @Override
  public void postWindowMoved(int newX, int newY) {
    if (!sketchFullScreen()) {
      lastWindowX = newX;
      lastWindowY = newY;
    }
    super.postWindowMoved(newX, newY);
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
    if (py5RegisteredEvents != null && py5Bridge != null && py5RegisteredEvents.contains("exiting")) {
      py5Bridge.run_method("exiting");
      // if the exiting method was not successful we still need to run the below
      // shutdown code.
    }

    if (py5Bridge != null) {
      py5Bridge.shutdown();
    }

    final Object nativeWindow = surface.getNative();
    if (nativeWindow instanceof GLWindow) {
      GLWindow window = (GLWindow) nativeWindow;
      for (int i = 0; i < window.getGLEventListenerCount(); i++) {
        window.disposeGLEventListener(window.getGLEventListener(i), true);
      }
      if (platform == MACOS && exitActualCallCount == 1) {
        try {
          final MacOSXOnscreenCGLDrawable drawable = (MacOSXOnscreenCGLDrawable) window.getDelegatedDrawable();
          WindowDriver driver = (WindowDriver) drawable.getNativeSurface();
          driver.destroy();
        } catch (NullPointerException e) {
          // if a NullPointerException is thrown it is because the drawing surface has
          // already been destroyed
        }
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

  public void py5SelectFolder(String key, String prompt, String defaultFolder) {
    SelectCallback sc = new SelectCallback(this, key);
    File defaultSelection = (defaultFolder == null) ? null : new File(defaultFolder);
    selectFolder(prompt, "callback", defaultSelection, sc);
  }

  public void py5SelectInput(String key, String prompt, String defaultFile) {
    SelectCallback sc = new SelectCallback(this, key);
    File defaultSelection = (defaultFile == null) ? null : new File(defaultFile);
    selectInput(prompt, "callback", defaultSelection, sc);
  }

  public void py5SelectOutput(String key, String prompt, String defaultFile) {
    SelectCallback sc = new SelectCallback(this, key);
    File defaultSelection = (defaultFile == null) ? null : new File(defaultFile);
    selectOutput(prompt, "callback", defaultSelection, sc);
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
    osNoiseSeed = seed;
  }

  public float osNoise(float x, float y) {
    return OpenSimplex2S.noise2(osNoiseSeed, x, y);
  }

  public float osNoise(float x, float y, float z) {
    return OpenSimplex2S.noise3_Fallback(osNoiseSeed, x, y, z);
  }

  public float osNoise(float x, float y, float z, float w) {
    return OpenSimplex2S.noise4_Fallback(osNoiseSeed, x, y, z, w);
  }

  public float[] osNoiseArray(float[] x, float[] y) {
    float[] out = new float[x.length];
    for (int i = 0; i < x.length; ++i) {
      out[i] = OpenSimplex2S.noise2(osNoiseSeed, x[i], y[i]);
    }
    return out;
  }

  public float[] osNoiseArray(float[] x, float[] y, float[] z) {
    float[] out = new float[x.length];
    for (int i = 0; i < x.length; ++i) {
      out[i] = OpenSimplex2S.noise3_Fallback(osNoiseSeed, x[i], y[i], z[i]);
    }
    return out;
  }

  public float[] osNoiseArray(float[] x, float[] y, float[] z, float[] w) {
    float[] out = new float[x.length];
    for (int i = 0; i < x.length; ++i) {
      out[i] = OpenSimplex2S.noise4_Fallback(osNoiseSeed, x[i], y[i], z[i], w[i]);
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

  public class SelectCallback {

    protected Sketch sketch;
    protected String callback;

    public SelectCallback(Sketch sketch, String callback) {
      this.sketch = sketch;
      this.callback = callback;
    }

    public void callback(File selection) {
      try {
        sketch.callPython(callback, selection == null ? null : selection.getAbsolutePath());
      } catch (Exception e) {
        _terminateSketch(true);
      }
    }
  }
}
