package py5.core;

import java.io.File;

import processing.core.PApplet;
import processing.core.PImage;
import processing.core.PSurface;

public class Py5SurfaceDummy implements PSurface {

  @Override
  public Object getNative() {
    return null;
  }

  @Override
  public void hideCursor() {

  }

  @Override
  public void initFrame(PApplet arg0) {

  }

  @Override
  public void initOffscreen(PApplet arg0) {

  }

  @Override
  public boolean isStopped() {
    return false;
  }

  @Override
  public PImage loadImage(String arg0, Object... arg1) {
    return null;
  }

  @Override
  public boolean openLink(String arg0) {
    return false;
  }

  @Override
  public void pauseThread() {

  }

  @Override
  public void placePresent(int arg0) {

  }

  @Override
  public void placeWindow(int[] arg0, int[] arg1) {

  }

  @Override
  public void resumeThread() {

  }

  @Override
  public void selectFolder(String arg0, String arg1, File arg2, Object arg3) {

  }

  @Override
  public void selectInput(String arg0, String arg1, File arg2, Object arg3) {

  }

  @Override
  public void selectOutput(String arg0, String arg1, File arg2, Object arg3) {

  }

  @Override
  public void setAlwaysOnTop(boolean arg0) {

  }

  @Override
  public void setCursor(int arg0) {

  }

  @Override
  public void setCursor(PImage arg0, int arg1, int arg2) {

  }

  @Override
  public void setFrameRate(float arg0) {

  }

  @Override
  public void setIcon(PImage arg0) {

  }

  @Override
  public void setLocation(int arg0, int arg1) {

  }

  @Override
  public void setResizable(boolean arg0) {

  }

  @Override
  public void setSize(int arg0, int arg1) {

  }

  @Override
  public void setTitle(String arg0) {

  }

  @Override
  public void setVisible(boolean arg0) {

  }

  @Override
  public void setupExternalMessages() {

  }

  @Override
  public void showCursor() {

  }

  @Override
  public void startThread() {

  }

  @Override
  public boolean stopThread() {
    return false;
  }
  
}