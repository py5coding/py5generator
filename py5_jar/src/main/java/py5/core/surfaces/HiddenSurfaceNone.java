/******************************************************************************

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
package py5.core.surfaces;

import processing.core.PGraphics;
import processing.core.PSurfaceNone;

public class HiddenSurfaceNone extends PSurfaceNone {

  public HiddenSurfaceNone(PGraphics graphics) {
    super(graphics);
  }

  @Override
  public void setSize(int wide, int high) {
    if (wide == sketch.width && high == sketch.height && wide == sketch.pixelWidth && high == sketch.pixelHeight) {
      return; // unchanged, don't rebuild everything
    }

    // call the proper function so pixelWidth and pixelHeight get set
    sketch.setSize(wide, high);
    // sketch.width = wide;
    // sketch.height = high;

    // set PGraphics variables for width/height/pixelWidth/pixelHeight
    graphics.setSize(wide, high);
  }

}
