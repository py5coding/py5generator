package py5.core;

import java.nio.ByteBuffer;
import java.nio.IntBuffer;

import processing.core.PGraphics;

public class Py5Graphics extends PGraphics {

  public static final char CODED = PGraphics.CODED;

  public byte[] loadAndGetPixels() {
    loadPixels();
    ByteBuffer byteBuffer = ByteBuffer.allocate(4 * pixels.length);
    IntBuffer intBuffer = byteBuffer.asIntBuffer();
    intBuffer.put(pixels);

    return byteBuffer.array();
  }

  public void setAndUpdatePixels(byte[] newPixels) {
    ByteBuffer byteBuffer = ByteBuffer.allocate(newPixels.length);
    byte[] byteArray = byteBuffer.array();
    System.arraycopy(newPixels, 0, byteArray, 0, newPixels.length);
    IntBuffer intBuffer = byteBuffer.asIntBuffer();

    intBuffer.get(pixels);
    updatePixels();
  }

}
