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
package py5.core.graphics;

import processing.awt.PGraphicsJava2D;
import processing.core.PSurface;
import py5.core.surfaces.HiddenSurfaceNone;

public class HiddenPy5GraphicsJava2D extends PGraphicsJava2D {

  @Override
  public PSurface createSurface() {
    return surface = new HiddenSurfaceNone(this);
  }

  @Override
  public void dispose() {

  }

  @Override
  public boolean displayable() {
    return false;
  }

}
