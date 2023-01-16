/******************************************************************************

  Part of the py5 library
  Copyright (C) 2020-2023 Jim Schmitz

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

public class SketchBase extends PApplet {

  protected Py5Bridge py5Bridge;
  protected Set<String> py5RegisteredEvents;
  protected Map<String, Integer> py5RegisteredEventParamCounts;
  protected int exitActualCallCount;

  public SketchBase() {
    py5Bridge = null;
    this.py5RegisteredEvents = new HashSet<String>();
    this.py5RegisteredEventParamCounts = new HashMap<String, Integer>();
    this.exitActualCallCount = 0;
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

  public void buildPy5Bridge(Py5Bridge py5Bridge) {
    this.py5Bridge = py5Bridge;
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

}
