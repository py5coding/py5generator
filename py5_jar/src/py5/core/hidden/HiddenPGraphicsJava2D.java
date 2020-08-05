package py5.core.hidden;

import processing.awt.PGraphicsJava2D;
import processing.core.PSurface;

public class HiddenPGraphicsJava2D extends PGraphicsJava2D {

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