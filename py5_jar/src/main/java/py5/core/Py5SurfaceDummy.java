/* ****************************************************************************

  Part of the py5 library
  Copyright (C) 2020-2025 Jim Schmitz

  This library is free software: you can redistribute it and/or modify it
  under the terms of the GNU Lesser General Public License as published by
  the Free Software Foundation, either version 2.1 of the License, or (at
  your option) any later version.

  This library is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
  General Public License for more details.

  You should have received a copy of the GNU Lesser General Public License
  along with this library. If not, see <https://www.gnu.org/licenses/>.

******************************************************************************/
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
  public void initFrame(PApplet sketch) {

  }

  @Override
  public void initOffscreen(PApplet sketch) {

  }

  @Override
  public boolean isStopped() {
    return false;
  }

  @Override
  public PImage loadImage(String path, Object... args) {
    return null;
  }

  @Override
  public boolean openLink(String url) {
    return false;
  }

  @Override
  public void pauseThread() {

  }

  @Override
  public void placePresent(int stopColor) {

  }

  @Override
  public void placeWindow(int[] location, int[] editorLocation) {

  }

  @Override
  public void resumeThread() {

  }

  @Override
  public void selectFolder(String prompt, String callback, File file, Object callbackObject) {

  }

  @Override
  public void selectInput(String prompt, String callback, File file, Object callbackObject) {

  }

  @Override
  public void selectOutput(String prompt, String callback, File file, Object callbackObject) {

  }

  @Override
  public void setAlwaysOnTop(boolean always) {

  }

  @Override
  public void setCursor(int kind) {

  }

  @Override
  public void setCursor(PImage image, int hotspotX, int hotspotY) {

  }

  @Override
  public void setFrameRate(float fps) {

  }

  @Override
  public void setIcon(PImage icon) {

  }

  @Override
  public void setLocation(int x, int y) {

  }

  @Override
  public void setResizable(boolean resizable) {

  }

  @Override
  public void setSize(int width, int height) {

  }

  @Override
  public void setTitle(String title) {

  }

  @Override
  public void setVisible(boolean visible) {

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