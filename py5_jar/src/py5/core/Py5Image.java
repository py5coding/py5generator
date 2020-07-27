package py5.core;

import java.nio.ByteBuffer;

import processing.core.PImage;

public class Py5Image extends PImage {

  protected ByteBuffer pixelBuffer;

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
