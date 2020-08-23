package py5.core;

import processing.core.PGraphics;

public class Py5GraphicsHelper {

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
      System.out.println("error in lines");
    }
  }

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
      System.out.println("error in points");
    }
  }

}