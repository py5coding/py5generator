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
package py5.util;

import java.awt.GraphicsDevice;
import java.awt.GraphicsEnvironment;

public class CheckHeadless {

  public static boolean test() {
    if (GraphicsEnvironment.isHeadless()) {
      return true;
    }

    try {
      GraphicsDevice[] devices = GraphicsEnvironment.getLocalGraphicsEnvironment().getScreenDevices();
      return devices == null || devices.length == 0;
    } catch (Exception e) {
      return true;
    }
  }

}
