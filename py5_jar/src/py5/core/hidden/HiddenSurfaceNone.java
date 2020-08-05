package py5.core.hidden;

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
