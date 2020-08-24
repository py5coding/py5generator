package py5.core;

import processing.core.PGraphics;

public class Py5GraphicsHelper {

  public static void points(PGraphics g, float[][] coordinates) {
    if (coordinates[0].length == 2) {
      for (int i = 0; i < coordinates.length; ++i) {
        g.point(coordinates[i][0], coordinates[i][1]);
      }
    } else if (coordinates[0].length == 3) {
      for (int i = 0; i < coordinates.length; ++i) {
        g.point(coordinates[i][0], coordinates[i][1], coordinates[i][2]);
      }
    } else {
      throw new RuntimeException("the second axis of parameter coordinates must have a length equal to 2 or 3");
    }
  }

  public static void lines(PGraphics g, float[][] coordinates) {
    if (coordinates[0].length == 4) {
      for (int i = 0; i < coordinates.length; ++i) {
        g.line(coordinates[i][0], coordinates[i][1], coordinates[i][2], coordinates[i][3]);
      }
    } else if (coordinates[0].length == 6) {
      for (int i = 0; i < coordinates.length; ++i) {
        g.line(coordinates[i][0], coordinates[i][1], coordinates[i][2], coordinates[i][3], coordinates[i][4],
            coordinates[i][5]);
      }
    } else {
      throw new RuntimeException("the second axis of parameter coordinates must have a length equal to 4 or 6");
    }
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
