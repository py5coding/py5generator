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

import processing.core.PApplet;
import processing.core.PConstants;

public class SketchBase extends PApplet {

  protected Py5Bridge py5Bridge;
  protected String py5IconPath;

  public SketchBase() {

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

}
