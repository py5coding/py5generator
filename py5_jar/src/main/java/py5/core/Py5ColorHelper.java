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

  protected static String formatRGB(int color, int colorModeX, int colorModeY, int colorModeZ) {
    int r = color >> 16 & 0xFF;
    int g = color >> 8 & 0xFF;
    int b = color & 0xFF;

    if (colorModeX == 255 && colorModeY == 255 && colorModeZ == 255) {
      return String.format("red=%d/%d, green=%d/%d, blue=%d/%d", r, colorModeX, g,
          colorModeY, b, colorModeZ);
    } else {
      return String.format("red=%.2f/%d, green=%.2f/%d, blue=%.2f/%d",
          r / 255f * colorModeX, colorModeX,
          g / 255f * colorModeY, colorModeY,
          b / 255f * colorModeZ, colorModeZ);
    }
  }

  protected static String formatHSB(int color, int colorModeX, int colorModeY, int colorModeZ) {
    float[] hsb = new float[3];
    Color.RGBtoHSB(color >> 16 & 0xFF, color >> 8 & 0xFF, color & 0xFF, hsb);

    return String.format("hue=%.2f/%d, saturation=%.2f/%d, brightness=%.2f/%d",
        hsb[0] * colorModeX, colorModeX,
        hsb[1] * colorModeY, colorModeY,
        hsb[2] * colorModeZ, colorModeZ);
  }

  protected static String makeStr(int colorMode, int color, float colorModeX, float colorModeY, float colorModeZ,
      float colorModeA) {
    // RGB values
    int a = color >> 24 & 0xFF;
    String alphaString;
    if (colorModeA == 255) {
      alphaString = String.format("alpha=%d/255", a);
    } else {
      alphaString = String.format("alpha=%.2f/%d", a / 255f * colorModeA, Math.round(colorModeA));
    }

    if (colorMode == PConstants.RGB) {
      String rgbString = formatRGB(color, Math.round(colorModeX), Math.round(colorModeY), Math.round(colorModeZ));
      String hsbString = formatHSB(color, 360, 100, 100);

      return String.format("Py5Color(RGB, %s, %s, %s)", rgbString, alphaString, hsbString);
    } else if (colorMode == PConstants.HSB) {
      String rgbString = formatRGB(color, 255, 255, 255);
      String hsbString = formatHSB(color, Math.round(colorModeX), Math.round(colorModeY), Math.round(colorModeZ));

      return String.format("Py5Color(HSB, %s, %s, %s)", hsbString, alphaString, rgbString);
    } else {
      throw new RuntimeException("Unrecognized colorMode value " + colorMode);
    }
  }
}
