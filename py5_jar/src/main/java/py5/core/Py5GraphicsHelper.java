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

import processing.core.PGraphics;

public class Py5GraphicsHelper {

  public static void points(PGraphics g, float[][] coordinates) {
    g.beginShape(PGraphics.POINTS);
    if (coordinates[0].length == 2) {
      for (int i = 0; i < coordinates.length; ++i) {
        g.vertex(coordinates[i][0], coordinates[i][1]);
      }
    } else if (coordinates[0].length == 3) {
      for (int i = 0; i < coordinates.length; ++i) {
        g.vertex(coordinates[i][0], coordinates[i][1], coordinates[i][2]);
      }
    } else {
      throw new RuntimeException("the second axis of parameter coordinates must have a length equal to 2 or 3");
    }
    g.endShape();
  }

  public static void lines(PGraphics g, float[][] coordinates) {
    g.beginShape(PGraphics.LINES);
    if (coordinates[0].length == 4) {
      for (int i = 0; i < coordinates.length; ++i) {
        g.vertex(coordinates[i][0], coordinates[i][1]);
        g.vertex(coordinates[i][2], coordinates[i][3]);
      }
    } else if (coordinates[0].length == 6) {
      for (int i = 0; i < coordinates.length; ++i) {
        g.vertex(coordinates[i][0], coordinates[i][1], coordinates[i][2]);
        g.vertex(coordinates[i][3], coordinates[i][4], coordinates[i][5]);
      }
    } else {
      throw new RuntimeException("the second axis of parameter coordinates must have a length equal to 4 or 6");
    }
    g.endShape();
  }

  public static void vertices(PGraphics g, float[][] coordinates) {
    if (coordinates[0].length == 2) {
      for (int i = 0; i < coordinates.length; ++i) {
        g.vertex(coordinates[i][0], coordinates[i][1]);
      }
    } else if (coordinates[0].length == 3) {
      for (int i = 0; i < coordinates.length; ++i) {
        g.vertex(coordinates[i][0], coordinates[i][1], coordinates[i][2]);
      }
    } else if (coordinates[0].length == 4) {
      for (int i = 0; i < coordinates.length; ++i) {
        g.vertex(coordinates[i][0], coordinates[i][1], coordinates[i][2], coordinates[i][3]);
      }
    } else if (coordinates[0].length == 5) {
      for (int i = 0; i < coordinates.length; ++i) {
        g.vertex(coordinates[i][0], coordinates[i][1], coordinates[i][2], coordinates[i][3], coordinates[i][4]);
      }
    } else if (coordinates[0].length == PGraphics.VERTEX_FIELD_COUNT) {
      for (int i = 0; i < coordinates.length; ++i) {
        g.vertex(coordinates[i]);
      }
    } else {
      throw new RuntimeException("the second axis of parameter coordinates must have a length equal to 2, 3, 4, 5, or "
          + PGraphics.VERTEX_FIELD_COUNT);
    }
  }

  public static void bezierVertices(PGraphics g, float[][] coordinates) {
    if (coordinates[0].length == 6) {
      for (int i = 0; i < coordinates.length; ++i) {
        g.bezierVertex(coordinates[i][0], coordinates[i][1], coordinates[i][2], coordinates[i][3], coordinates[i][4],
            coordinates[i][5]);
      }
    } else if (coordinates[0].length == 9) {
      for (int i = 0; i < coordinates.length; ++i) {
        g.bezierVertex(coordinates[i][0], coordinates[i][1], coordinates[i][2], coordinates[i][3], coordinates[i][4],
            coordinates[i][5], coordinates[i][6], coordinates[i][7], coordinates[i][8]);
      }
    } else {
      throw new RuntimeException("the second axis of parameter coordinates must have a length equal to 6 or 9");
    }
  }

  public static void curveVertices(PGraphics g, float[][] coordinates) {
    if (coordinates[0].length == 2) {
      for (int i = 0; i < coordinates.length; ++i) {
        g.curveVertex(coordinates[i][0], coordinates[i][1]);
      }
    } else if (coordinates[0].length == 3) {
      for (int i = 0; i < coordinates.length; ++i) {
        g.curveVertex(coordinates[i][0], coordinates[i][1], coordinates[i][2]);
      }
    } else {
      throw new RuntimeException("the second axis of parameter coordinates must have a length equal to 2 or 3");
    }
  }

  public static void quadraticVertices(PGraphics g, float[][] coordinates) {
    if (coordinates[0].length == 4) {
      for (int i = 0; i < coordinates.length; ++i) {
        g.quadraticVertex(coordinates[i][0], coordinates[i][1], coordinates[i][2], coordinates[i][3]);
      }
    } else if (coordinates[0].length == 6) {
      for (int i = 0; i < coordinates.length; ++i) {
        g.quadraticVertex(coordinates[i][0], coordinates[i][1], coordinates[i][2], coordinates[i][3], coordinates[i][4],
            coordinates[i][5]);
      }
    } else {
      throw new RuntimeException("the second axis of parameter coordinates must have a length equal to 4 or 6");
    }
  }

}
