package processing.core;

import processing.event.MouseEvent;

public interface Py5Methods {

  public void run_method(String method_name, Object... params);

  public void mouse_wheel(MouseEvent event);

}
