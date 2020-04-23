package processing.core;

import processing.event.MouseEvent;

public interface Py5Methods {

  public void settings();

  public void setup();

  public void draw();

  public void key_pressed();

  public void key_typed();

  public void key_released();

  public void exit_actual();
  
  public void mouse_clicked();

  public void mouse_dragged();

  public void mouse_moved();

  public void mouse_entered();

  public void mouse_exited();

  public void mouse_pressed();

  public void mouse_released();

  public void mouse_wheel(MouseEvent event);
}