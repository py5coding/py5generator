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

  public static String repr(Sketch sketch, String colorModeName, int color) {
    if (sketch == null || sketch.getGraphics() == null) {
      return makeStr(PConstants.RGB, colorModeName, color, 255, 255, 255, 255);
    } else {
      return repr(sketch.getGraphics(), colorModeName, color);
    }
  }

  public static String repr(PGraphics g, String colorModeName, int color) {
    if (g == null) {
      return makeStr(PConstants.RGB, colorModeName, color, 255, 255, 255, 255);
    } else {
      return makeStr(g.colorMode, colorModeName, color, g.colorModeX, g.colorModeY, g.colorModeZ, g.colorModeA);
    }
  }

  public static String repr(PShape s, String colorModeName, int color) {
    if (s == null) {
      return makeStr(PConstants.RGB, colorModeName, color, 255, 255, 255, 255);
    } else {
      return makeStr(s.colorMode, colorModeName, color, s.colorModeX, s.colorModeY, s.colorModeZ, s.colorModeA);
    }
  }

  protected static String formatValueRange(float value, int range) {
    int roundValue = Math.round(value);
    if (Math.abs(value - roundValue) < 0.005) {
      return String.format("%d/%d", roundValue, range);
    } else {
      return String.format("%.2f/%d", Math.round(value * 100) / 100f, range);
    }
  }

  protected static String formatRGB(int color, int colorModeX, int colorModeY, int colorModeZ) {
    int r = color >> 16 & 0xFF;
    int g = color >> 8 & 0xFF;
    int b = color & 0xFF;

    if (colorModeX == 255 && colorModeY == 255 && colorModeZ == 255) {
      return String.format("red=%d/255, green=%d/255, blue=%d/255", r, g, b);
    } else {
      return String.format("red=%s, green=%s, blue=%s",
          formatValueRange(r / 255f * colorModeX, colorModeX),
          formatValueRange(g / 255f * colorModeY, colorModeY),
          formatValueRange(b / 255f * colorModeZ, colorModeZ));
    }
  }

  protected static String formatHSB(int color, int colorModeX, int colorModeY, int colorModeZ) {
    float[] hsb = new float[3];
    Color.RGBtoHSB(color >> 16 & 0xFF, color >> 8 & 0xFF, color & 0xFF, hsb);

    return String.format("hue=%s, saturation=%s, brightness=%s",
        formatValueRange(hsb[0] * colorModeX, colorModeX),
        formatValueRange(hsb[1] * colorModeY, colorModeY),
        formatValueRange(hsb[2] * colorModeZ, colorModeZ));
  }

  protected static String makeStr(int colorMode, String colorModeName, int color, float colorModeX, float colorModeY,
      float colorModeZ,
      float colorModeA) {
    if (colorModeName == null) {
      colorModeName = (colorMode == PConstants.RGB) ? "RGB" : "HSB";
    }

    String alphaString = String.format("alpha=%s", formatValueRange(color >> 24 & 0xFF, 255));

    if (colorMode == PConstants.RGB) {
      String rgbString = formatRGB(color, Math.round(colorModeX), Math.round(colorModeY), Math.round(colorModeZ));
      String hsbString = formatHSB(color, 360, 100, 100);

      return String.format("Py5Color(%s, %s, %s, %s)", colorModeName, rgbString, alphaString, hsbString);
    } else if (colorMode == PConstants.HSB) {
      String rgbString = formatRGB(color, 255, 255, 255);
      String hsbString = formatHSB(color, Math.round(colorModeX), Math.round(colorModeY), Math.round(colorModeZ));

      return String.format("Py5Color(%s, %s, %s, %s)", colorModeName, hsbString, alphaString, rgbString);
    } else {
      throw new RuntimeException("Unrecognized colorMode value " + colorMode);
    }
  }
}
