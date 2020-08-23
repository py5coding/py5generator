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
