package py5.core;

import java.nio.ByteBuffer;

import processing.core.PGraphics;

public class Py5Graphics extends PGraphics {

  protected ByteBuffer pixelBuffer;

  public static final char CODED = PGraphics.CODED;

  public void setPixelBuffer(ByteBuffer pixelBuffer) {
    this.pixelBuffer = pixelBuffer;
  }

  public void loadAndPutPixels() {
    loadPixels();
    pixelBuffer.asIntBuffer().put(pixels);
  }

  public void getAndUpdatePixels() {
    pixelBuffer.asIntBuffer().get(pixels);
    updatePixels();
  }

}
