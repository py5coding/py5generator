/******************************************************************************

  Part of the py5 library
  Copyright (C) 2020-2024 Jim Schmitz

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

import com.jogamp.newt.opengl.GLWindow;

import java.awt.Canvas;

import processing.core.PApplet;
import processing.core.PConstants;
import processing.core.PMatrix2D;
import processing.core.PShape;
import processing.core.PStyle;
import processing.core.PSurface;
import processing.core.ThinkDifferent;
import processing.event.Event;
import processing.event.KeyEvent;
import processing.event.MouseEvent;
import processing.opengl.PGraphicsOpenGL;
import processing.opengl.PJOGL;
import py5.util.KeyEventUtilities;
import py5.util.OpenSimplex2S;

public class Sketch extends SketchBase {

  protected boolean success;
  protected String py5IconPath;
  protected int[] pixelCapture;
  protected long osNoiseSeed;
  public Integer lastWindowX;
  public Integer lastWindowY;
  protected PreDrawUpdateRunner preDrawUpdateRunner;
  protected PStyle savedStyle;

  public static final char CODED = PApplet.CODED;

  public static final String HIDDEN = "py5.core.graphics.HiddenPy5GraphicsJava2D";

  long millisOffset = System.currentTimeMillis();

  public Sketch() {
    this.success = false;
    this.py5IconPath = null;
    this.pixelCapture = null;
    this.osNoiseSeed = (long) (Math.random() * Long.MAX_VALUE);
    this.lastWindowX = null;
    this.lastWindowY = null;

    Sketch.useNativeSelect = platform == MACOS;
  }

  public void setPy5IconPath(String py5IconPath) {
    this.py5IconPath = py5IconPath;
  }

  /*
   * The below methods are how Java makes calls to the Python implementations of
   * the Processing methods.
   */

  @Override
  public void buildPy5Bridge(Py5Bridge py5Bridge, boolean inIPythonSession, boolean inJupyterZMQShell) {
    super.buildPy5Bridge(py5Bridge, inIPythonSession, inJupyterZMQShell);
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

  public String getRendererName() {
    switch (sketchRenderer()) {
      case HIDDEN:
        return "HIDDEN";
      default:
        return super.getRendererName();
    }
  }

  @Override
  public int millis() {
    return (int) (System.currentTimeMillis() - millisOffset);
  }

  public void _resetSyncSketch() {
    millisOffset = System.currentTimeMillis();
    frameCount = 1;
    if (savedStyle != null) {
      style(savedStyle);
    }

    // reset window settings
    frameRate(60);
    cursor(ARROW);
    noClip();

    // reset 3D settings
    if (g.is3D()) {
      camera();
      perspective();
    }

    // reset shaders and other opengl only stuff
    if (g instanceof PGraphicsOpenGL) {
      resetShader(POINTS);
      resetShader(LINES);
      resetShader(TRIANGLES);
      textureMode(IMAGE);
      textureWrap(CLAMP);
    }

    // reset hints
    hint(ENABLE_DEPTH_TEST);
    hint(DISABLE_DEPTH_SORT);
    hint(ENABLE_OPENGL_ERRORS);
    hint(ENABLE_DEPTH_MASK);
    hint(ENABLE_OPTIMIZED_STROKE);
    hint(DISABLE_STROKE_PERSPECTIVE);
    hint(ENABLE_TEXTURE_MIPMAPS);
    hint(DISABLE_STROKE_PURE);
    hint(DISABLE_BUFFER_READING);
    hint(DISABLE_KEY_REPEAT);
    hint(ENABLE_ASYNC_SAVEFRAME);

    // in case user doesn't call background in setup
    background(204);

    // reset random methods
    osNoiseSeed = (long) (Math.random() * Long.MAX_VALUE);
    noiseSeed((long) (Math.random() * Long.MAX_VALUE));
    noiseDetail(4, 0.5f);

    // reset detail settings
    sphereDetail(30);
    bezierDetail(20);
    curveDetail(20);
    curveTightness(0f);
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

      // request focus for Java2D renderer on Windows and MacOS
      if (platform == WINDOWS && sketchRenderer().equals(JAVA2D)) {
        Canvas canvas = (Canvas) surface.getNative();
        canvas.setFocusable(true);
        canvas.requestFocus();
      } else if (platform == MACOS && (sketchRenderer().equals(JAVA2D) || g.isGL())) {
        ThinkDifferent.activateIgnoringOtherApps();
      }

      if (py5IconPath != null && !(g instanceof PGraphicsOpenGL)) {
        try {
          surface.setIcon(loadImage(py5IconPath));
        } catch (Exception e) {
        }
      }

      // save for safe keeping
      savedStyle = getGraphics().getStyle();

      if (py5RegisteredEvents.contains("setup")) {
        success = py5Bridge.run_method("setup");
      } else {
        // parent method doesn't do anything but that might change
        super.setup();
      }

      if (success && py5RegisteredEvents.contains("predraw_update")) {
        preDrawUpdateRunner = new PreDrawUpdateRunner();
        preDrawUpdateRunner.start();
      }

      // Weirdness with Windows and OpenGL, need to capture pixels and restore
      // them before the first draw() call
      if (platform == WINDOWS && g.isGL()) {
        capturePixels();
        GLWindow window = (GLWindow) surface.getNative();
        long windowHandle = window.getWindowHandle();
        // the bridge will make a Windows API call to request focus
        py5Bridge.focus_window(windowHandle);
      }
    }
  }

  @Override
  public void draw() {
    if (pixelCapture != null) {
      restorePixels();
    }

    if (preDrawUpdateRunner != null) {
      while (preDrawUpdateRunner.runningPreDrawUpdate) {
        try {
          Thread.sleep(0, 10000);
        } catch (InterruptedException e) {
        }
      }
    }

    if (success) {
      if (py5RegisteredEvents.contains("draw")) {
        success = py5Bridge.run_method("draw");
      } else {
        // super.draw();
      }
    }

    if (success && preDrawUpdateRunner != null && !py5RegisteredEvents.contains("post_draw")) {
      preDrawUpdateRunner.interrupt();
    }
  }

  protected void preDrawUpdate() {
    if (success) {
      success = py5Bridge.run_method("predraw_update");
    }
  }

  public void preDraw() {
    if (preDrawUpdateRunner != null) {
      while (preDrawUpdateRunner.runningPreDrawUpdate) {
        try {
          Thread.sleep(0, 10000);
        } catch (InterruptedException e) {
        }
      }
    }

    if (success && py5RegisteredEvents.contains("pre_draw")) {
      success = py5Bridge.run_method("pre_draw");
    }
  }

  public void postDraw() {
    if (success && py5RegisteredEvents.contains("post_draw")) {
      success = py5Bridge.run_method("post_draw");
    }

    if (success && preDrawUpdateRunner != null) {
      preDrawUpdateRunner.interrupt();
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

  public void interceptEscape() {
    if (key == ESC) {
      interceptEscape = true;
    }
  }

  @Override
  protected void handleKeyEvent(KeyEvent event) {
    super.handleKeyEvent(event);
    interceptEscape = false;
  }

  @Override
  public void postWindowMoved(int newX, int newY) {
    if (!sketchFullScreen()) {
      lastWindowX = newX;
      lastWindowY = newY;
    }
    super.postWindowMoved(newX, newY);
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
   * This is to get around an issue with JPype method dispatching. It would always
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
   * shortcoming.
   */

  protected void capturePixels() {
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

  /*
   * Class for running user predraw_update() function
   */

  protected class PreDrawUpdateRunner extends Thread {

    public boolean runningPreDrawUpdate;

    public PreDrawUpdateRunner() {
      runningPreDrawUpdate = false;
    }

    public void run() {
      runningPreDrawUpdate = true;
      callPreDrawUpdate();

      while (!disposeCalled) {
        try {
          Thread.sleep(100);
        } catch (InterruptedException e) {
          callPreDrawUpdate();
        }
      }
    }

    public void interrupt() {
      runningPreDrawUpdate = true;
      super.interrupt();
    }

    protected void callPreDrawUpdate() {
      preDrawUpdate();
      runningPreDrawUpdate = false;
    }
  }

}
