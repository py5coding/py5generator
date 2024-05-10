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

import processing.core.PShape;

public class Py5ShapeHelper {

  public static void vertices(PShape s, float[][] coordinates) {
    if (coordinates.length == 0) {
      // no vertices
      return;
    }

    if (coordinates[0].length == 2) {
      for (int i = 0; i < coordinates.length; ++i) {
        s.vertex(coordinates[i][0], coordinates[i][1]);
      }
    } else if (coordinates[0].length == 3) {
      for (int i = 0; i < coordinates.length; ++i) {
        s.vertex(coordinates[i][0], coordinates[i][1], coordinates[i][2]);
      }
    } else if (coordinates[0].length == 4) {
      for (int i = 0; i < coordinates.length; ++i) {
        s.vertex(coordinates[i][0], coordinates[i][1], coordinates[i][2], coordinates[i][3]);
      }
    } else if (coordinates[0].length == 5) {
      for (int i = 0; i < coordinates.length; ++i) {
        s.vertex(coordinates[i][0], coordinates[i][1], coordinates[i][2], coordinates[i][3], coordinates[i][4]);
      }
    } else {
      throw new RuntimeException("the second axis of parameter coordinates must have a length equal to 2, 3, 4, or 5");
    }
  }

  public static void bezierVertices(PShape s, float[][] coordinates) {
    if (coordinates.length == 0) {
      // no vertices
      return;
    }

    if (coordinates[0].length == 6) {
      for (int i = 0; i < coordinates.length; ++i) {
        s.bezierVertex(coordinates[i][0], coordinates[i][1], coordinates[i][2], coordinates[i][3], coordinates[i][4],
            coordinates[i][5]);
      }
    } else if (coordinates[0].length == 9) {
      for (int i = 0; i < coordinates.length; ++i) {
        s.bezierVertex(coordinates[i][0], coordinates[i][1], coordinates[i][2], coordinates[i][3], coordinates[i][4],
            coordinates[i][5], coordinates[i][6], coordinates[i][7], coordinates[i][8]);
      }
    } else {
      throw new RuntimeException("the second axis of parameter coordinates must have a length equal to 6 or 9");
    }
  }

  public static void curveVertices(PShape s, float[][] coordinates) {
    if (coordinates.length == 0) {
      // no vertices
      return;
    }

    if (coordinates[0].length == 2) {
      for (int i = 0; i < coordinates.length; ++i) {
        s.curveVertex(coordinates[i][0], coordinates[i][1]);
      }
    } else if (coordinates[0].length == 3) {
      for (int i = 0; i < coordinates.length; ++i) {
        s.curveVertex(coordinates[i][0], coordinates[i][1], coordinates[i][2]);
      }
    } else {
      throw new RuntimeException("the second axis of parameter coordinates must have a length equal to 2 or 3");
    }
  }

  public static void quadraticVertices(PShape s, float[][] coordinates) {
    if (coordinates.length == 0) {
      // no vertices
      return;
    }

    if (coordinates[0].length == 4) {
      for (int i = 0; i < coordinates.length; ++i) {
        s.quadraticVertex(coordinates[i][0], coordinates[i][1], coordinates[i][2], coordinates[i][3]);
      }
    } else if (coordinates[0].length == 6) {
      for (int i = 0; i < coordinates.length; ++i) {
        s.quadraticVertex(coordinates[i][0], coordinates[i][1], coordinates[i][2], coordinates[i][3], coordinates[i][4],
            coordinates[i][5]);
      }
    } else {
      throw new RuntimeException("the second axis of parameter coordinates must have a length equal to 4 or 6");
    }
  }

  public static void setFills(PShape s, int[] fills) {
    if (fills.length == 0) {
      // no fills
      return;
    }

    if (fills.length == s.getVertexCount()) {
      for (int i = 0; i < fills.length; ++i) {
        s.setFill(i, fills[i]);
      }
    } else {
      throw new RuntimeException("the length of parameter fills (" + fills.length +
          ") must equal the number of vertices in the shape (" + s.getVertexCount() + ")");
    }
  }

  public static void setStrokes(PShape s, int[] strokes) {
    if (strokes.length == 0) {
      // no strokes
      return;
    }

    if (strokes.length == s.getVertexCount()) {
      for (int i = 0; i < strokes.length; ++i) {
        s.setStroke(i, strokes[i]);
      }
    } else {
      throw new RuntimeException("the length of parameter strokes (" + strokes.length +
          ") must equal the number of vertices in the shape (" + s.getVertexCount() + ")");
    }
  }

}
