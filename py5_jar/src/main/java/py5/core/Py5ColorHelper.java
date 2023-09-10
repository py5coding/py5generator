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

import java.awt.Color;

import processing.core.PConstants;
import processing.core.PGraphics;
import processing.core.PShape;

public class Py5ColorHelper {

  public static String repr(Sketch g, int color) {
    return repr(g.getGraphics(), color);
  }

  public static String repr(PGraphics g, int color) {
    if (g.colorMode == PConstants.RGB) {
      return intToRGB(color, g.colorModeX, g.colorModeY, g.colorModeZ, g.colorModeA);
    } else if (g.colorMode == PConstants.HSB) {
      return intToHSB(color, g.colorModeX, g.colorModeY, g.colorModeZ, g.colorModeA);
    } else {
      throw new RuntimeException("Unrecognized colorMode value " + g.colorMode);
    }
  }

  public static String repr(PShape s, int color) {
    if (s.colorMode == PConstants.RGB) {
      return intToRGB(color, s.colorModeX, s.colorModeY, s.colorModeZ, s.colorModeA);
    } else if (s.colorMode == PConstants.HSB) {
      return intToHSB(color, s.colorModeX, s.colorModeY, s.colorModeZ, s.colorModeA);
    } else {
      throw new RuntimeException("Unrecognized colorMode value " + s.colorMode);
    }
  }

  public static String intToRGB(int color, float colorModeX, float colorModeY, float colorModeZ, float colorModeA) {
    int a = color >> 24 & 0xFF;
    int r = color >> 16 & 0xFF;
    int g = color >> 8 & 0xFF;
    int b = color & 0xFF;

    if (colorModeX == 255 && colorModeY == 255 && colorModeZ == 255 && colorModeA == 255) {
      return String.format("(red=%d, green=%d, blue=%d, alpha=%d)", r, g, b, a);
    } else {
      return String.format("(red=%f, green=%f, blue=%f, alpha=%f)", r / 255 * colorModeX, g / 255 * colorModeY, b / 255 * colorModeZ,
          a / 255 * colorModeA);
    }
  }

  public static String intToHSB(int color, float colorModeX, float colorModeY, float colorModeZ, float colorModeA) {
    int a = color >> 24 & 0xFF;
    float[] hsb = new float[3];
    Color.RGBtoHSB(color >> 16 & 0xFF, color >> 8 & 0xFF, color & 0xFF, hsb);

    return String.format("(hue=%f, saturation=%f, brightness=%f, alpha=%f)", hsb[0] * colorModeX, hsb[1] * colorModeY, hsb[2] * colorModeZ,
        a / 255 * colorModeA);
  }

  public static String toHex(int color) {
    return String.format("#%08X", color);
  }
}
