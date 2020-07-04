package py5.core;

public interface Py5Methods {

  public Object[] get_function_list();

  public void run_method(String method_name, Object... params);

  public void shutdown();

}
