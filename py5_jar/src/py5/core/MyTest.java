package py5.core;

import java.nio.ByteBuffer;
import java.nio.IntBuffer;

public class MyTest {

  public ByteBuffer buffer;
  public int[] pixels;

  public MyTest(ByteBuffer buffer) {
    this.buffer = buffer;
    this.pixels = new int[buffer.capacity() / 4];
  }

  public void resetPixels() {
    for (int i = 0; i < pixels.length; ++i) {
      pixels[i] = 0xFF801001;
    }
  }

  public static int[] test1(int[] array) {
    System.out.println("length " + array.length);
    System.out.println(array[0]);
    array[0] = 42;
    return array;
  }

  public static void test2(ByteBuffer buffer) {
    // passing data to Java
    int[] pixels = new int[buffer.capacity() / 4];
    // copy from buffer to pixels array
    buffer.asIntBuffer().get(pixels);

    System.out.println(pixels[0]);
  }

  public static void test3(ByteBuffer buffer) {
    // passing data to Python
    int[] pixels = new int[buffer.capacity() / 4];
    for (int i = 0; i < pixels.length; ++i) {
      pixels[i] = 42;
    }

    IntBuffer intBuffer = buffer.asIntBuffer();
    // copy from pixels array to buffer
    intBuffer.put(pixels);
  }

  public void setPixels() {
    // passing data to Java

    // copy from buffer to pixels
    buffer.asIntBuffer().get(pixels);
  }

  public void getPixels() {
    // passing data to Python

    // copy from pixels array to buffer
    buffer.asIntBuffer().put(pixels);
  }
}
