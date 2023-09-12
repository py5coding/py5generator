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
    return makeStr(g.colorMode, color, g.colorModeX, g.colorModeY, g.colorModeZ, g.colorModeA);
  }

  public static String repr(PShape s, int color) {
    return makeStr(s.colorMode, color, s.colorModeX, s.colorModeY, s.colorModeZ, s.colorModeA);
  }

  protected static String makeStr(int colorMode, int color, float colorModeX, float colorModeY, float colorModeZ,
      float colorModeA) {
    // RGB values
    int a = color >> 24 & 0xFF;
    int r = color >> 16 & 0xFF;
    int g = color >> 8 & 0xFF;
    int b = color & 0xFF;

    // HSB values
    float[] hsb = new float[3];
    Color.RGBtoHSB(color >> 16 & 0xFF, color >> 8 & 0xFF, color & 0xFF, hsb);

    if (colorMode == PConstants.RGB) {
      if (colorModeX == 255 && colorModeY == 255 && colorModeZ == 255 && colorModeA == 255) {
        return String.format("Py5Color(red=%d, green=%d, blue=%d, alpha=%d, hue=%d°, saturation=%d%%, brightness=%d%%)",
            r, g, b, a,
            (int) (hsb[0] * 360),
            (int) (hsb[1] * 100),
            (int) (hsb[2] * 100));
      } else {
        return String.format(
            "Py5Color(red=%.2f, green=%.2f, blue=%.2f, alpha=%.2f, hue=%d°, saturation=%d%%, brightness=%d%%)",
            r / 255 * colorModeX,
            g / 255 * colorModeY,
            b / 255 * colorModeZ,
            a / 255 * colorModeA,
            (int) Math.round(hsb[0] * 360),
            (int) Math.round(hsb[1] * 100),
            (int) Math.round(hsb[2] * 100));
      }
    } else if (colorMode == PConstants.HSB) {
      if (colorModeX == 360 && colorModeY == 100 && colorModeZ == 100 && colorModeA == 100) {
        return String.format("Py5Color(hue=%d°, saturation=%d%%, brightness=%d%%, alpha=%d%%, red=%d%%, green=%d%%, blue=%d%%)",
            (int) Math.round(hsb[0] * 360),
            (int) Math.round(hsb[1] * 100),
            (int) Math.round(hsb[2] * 100),
            (int) Math.round(a / 255.0 * 100),
            (int) Math.round(r / 255.0 * 100),
            (int) Math.round(g / 255.0 * 100),
            (int) Math.round(b / 255.0 * 100));
      } else {
        return String.format("Py5Color(hue=%.2f, saturation=%.2f, brightness=%.2f, alpha=%.2f, red=%d%%, green=%d%%, blue=%d%%)",
            hsb[0] * colorModeX,
            hsb[1] * colorModeY,
            hsb[2] * colorModeZ,
            a / 255 * colorModeA,
            (int) Math.round(r / 255.0 * 100),
            (int) Math.round(g / 255.0 * 100),
            (int) Math.round(b / 255.0 * 100));
      }
    } else {
      throw new RuntimeException("Unrecognized colorMode value " + colorMode);
    }
  }

  public static String toHex(int color) {
    return String.format("#%06X%02X", color & 0x00FFFFFF, color >> 24 & 0xFF);
  }
}
