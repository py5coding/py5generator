package py5.core;

public class MyTest {

  public static int[] test1(int[] array) {
    System.out.println("length " + array.length);
    System.out.println(array[0]);
    array[0] = 42;
    return array;
  }

  public static char[] test2(char[] array) {
    System.out.println("length " + array.length);
    System.out.println(array[0]);
    array[0] = 'x';
    return array;
  }

  public static boolean[] test3(boolean[] array) {
    System.out.println("length " + array.length);
    System.out.println(array[0]);
    array[0] = true;
    return array;
  }

  public static Object[] test4() {
    Object[] array = new Object[10];
    for (int i = 0; i < array.length; i++) {
      array[i] = new Object();
    }
    return array;
  }
}
