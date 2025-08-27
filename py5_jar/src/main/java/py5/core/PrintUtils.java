/* ****************************************************************************

  Part of the py5 library
  Copyright (C) 2020-2025 Jim Schmitz

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

import processing.core.PMatrix2D;
import processing.core.PMatrix3D;

public class PrintUtils {

  public static String toString(PMatrix2D matrix) {
    float[] m = matrix.get(null);
    int big = 0;
    for (int i = 0; i < m.length; ++i) {
      if (Math.abs(m[i]) > big) {
        big = (int) Math.abs(m[i]);
      }
    }

    int digits = 1;
    if (Float.isNaN(big) || Float.isInfinite(big)) { // avoid infinite loop
      digits = 5;
    } else {
      while ((big /= 10) != 0)
        digits++; // cheap log()
    }

    String out = Sketch.nfs(m[0], digits, 4) + " " + Sketch.nfs(m[1], digits, 4) + " " + Sketch.nfs(m[2], digits, 4)
        + "\n" + Sketch.nfs(m[3], digits, 4) + " " + Sketch.nfs(m[4], digits, 4) + " " + Sketch.nfs(m[5], digits, 4);

    return out;
  }

  public static String toString(PMatrix3D matrix) {
    float[] m = matrix.get(null);
    int big = 0;
    for (int i = 0; i < m.length; ++i) {
      if (Math.abs(m[i]) > big) {
        big = (int) Math.abs(m[i]);
      }
    }

    int digits = 1;
    if (Float.isNaN(big) || Float.isInfinite(big)) { // avoid infinite loop
      digits = 5;
    } else {
      while ((big /= 10) != 0)
        digits++; // cheap log()
    }

    String out = Sketch.nfs(m[0], digits, 4) + " " + Sketch.nfs(m[1], digits, 4) + " " + Sketch.nfs(m[2], digits, 4)
        + " " + Sketch.nfs(m[3], digits, 4) + "\n" + Sketch.nfs(m[4], digits, 4) + " " + Sketch.nfs(m[5], digits, 4)
        + " " + Sketch.nfs(m[6], digits, 4) + " " + Sketch.nfs(m[7], digits, 4) + "\n" + Sketch.nfs(m[8], digits, 4)
        + " " + Sketch.nfs(m[9], digits, 4) + " " + Sketch.nfs(m[10], digits, 4) + " " + Sketch.nfs(m[11], digits, 4)
        + "\n" + Sketch.nfs(m[12], digits, 4) + " " + Sketch.nfs(m[13], digits, 4) + " " + Sketch.nfs(m[14], digits, 4)
        + " " + Sketch.nfs(m[15], digits, 4);

    return out;
  }
}
