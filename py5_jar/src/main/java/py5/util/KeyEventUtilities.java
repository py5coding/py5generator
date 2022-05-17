package py5.util;

import java.awt.Component;

import com.jogamp.newt.event.KeyEvent;

import processing.core.PApplet;

public class KeyEventUtilities {

  public static char getASCIIKey(String input) {
    if (input.length() == 1) {
      return input.charAt(0);
    }

    switch (input) {
      case "Backspace":
        return PApplet.BACKSPACE;
      case "Tab":
        return PApplet.TAB;
      case "Enter":
        return PApplet.ENTER;
      case "Return":
        return PApplet.RETURN;
      case "Escape":
        return PApplet.ESC;
      case "Delete":
        return PApplet.DELETE;
      default:
        return 0;
    }
  }

  private static class AWTKeyEvent extends java.awt.event.KeyEvent {
    private static final long serialVersionUID = 1L;

    public AWTKeyEvent(Component source, int id, long when, int modifiers, int keyCode, char keyChar, int keyLocation) {
      super(source, id, when, modifiers, keyCode, keyChar, keyLocation);
    }
  }

  public static int getAWTKeyCode(String input) {
    switch (input) {
      case "F1":
        return AWTKeyEvent.VK_F1;
      case "F2":
        return AWTKeyEvent.VK_F2;
      case "F3":
        return AWTKeyEvent.VK_F3;
      case "F4":
        return AWTKeyEvent.VK_F4;
      case "F5":
        return AWTKeyEvent.VK_F5;
      case "F6":
        return AWTKeyEvent.VK_F6;
      case "F7":
        return AWTKeyEvent.VK_F7;
      case "F8":
        return AWTKeyEvent.VK_F8;
      case "F9":
        return AWTKeyEvent.VK_F9;
      case "F10":
        return AWTKeyEvent.VK_F10;
      case "F11":
        return AWTKeyEvent.VK_F11;
      case "F12":
        return AWTKeyEvent.VK_F12;
      case "ArrowUp":
        return AWTKeyEvent.VK_UP;
      case "ArrowLeft":
        return AWTKeyEvent.VK_LEFT;
      case "ArrowDown":
        return AWTKeyEvent.VK_DOWN;
      case "ArrowRight":
        return AWTKeyEvent.VK_RIGHT;
      case "PageUp":
        return AWTKeyEvent.VK_PAGE_UP;
      case "PageDown":
        return AWTKeyEvent.VK_PAGE_DOWN;
      case "Control":
        return AWTKeyEvent.VK_CONTROL;
      case "Shift":
        return AWTKeyEvent.VK_SHIFT;
      case "Alt":
        return AWTKeyEvent.VK_ALT;
      case "OS":
        return AWTKeyEvent.VK_WINDOWS;
      case "Meta":
        return AWTKeyEvent.VK_META;
      case "CapsLock":
        return AWTKeyEvent.VK_CAPS_LOCK;
      case "NumLock":
        return AWTKeyEvent.VK_NUM_LOCK;
      case "ScrollLock":
        return AWTKeyEvent.VK_SCROLL_LOCK;
      case "Home":
        return AWTKeyEvent.VK_HOME;
      case "End":
        return AWTKeyEvent.VK_END;
      case "Insert":
        return AWTKeyEvent.VK_INSERT;
      case "Pause":
        return AWTKeyEvent.VK_PAUSE;
      case "ContextMenu":
        return AWTKeyEvent.VK_CONTEXT_MENU;
      default:
        return -1;
    }
  }

  public static int getJogampKeyCode(String input) {
    switch (input) {
      case "F1":
        return KeyEvent.VK_F1;
      case "F2":
        return KeyEvent.VK_F2;
      case "F3":
        return KeyEvent.VK_F3;
      case "F4":
        return KeyEvent.VK_F4;
      case "F5":
        return KeyEvent.VK_F5;
      case "F6":
        return KeyEvent.VK_F6;
      case "F7":
        return KeyEvent.VK_F7;
      case "F8":
        return KeyEvent.VK_F8;
      case "F9":
        return KeyEvent.VK_F9;
      case "F10":
        return KeyEvent.VK_F10;
      case "F11":
        return KeyEvent.VK_F11;
      case "F12":
        return KeyEvent.VK_F12;
      case "ArrowUp":
        return KeyEvent.VK_UP;
      case "ArrowLeft":
        return KeyEvent.VK_LEFT;
      case "ArrowDown":
        return KeyEvent.VK_DOWN;
      case "ArrowRight":
        return KeyEvent.VK_RIGHT;
      case "PageUp":
        return KeyEvent.VK_PAGE_UP;
      case "PageDown":
        return KeyEvent.VK_PAGE_DOWN;
      case "Control":
        return KeyEvent.VK_CONTROL;
      case "Shift":
        return KeyEvent.VK_SHIFT;
      case "Alt":
        return KeyEvent.VK_ALT;
      case "OS":
        return KeyEvent.VK_COMPOSE;  // note the difference from AWT
      case "Meta":
        return KeyEvent.VK_META;
      case "CapsLock":
        return KeyEvent.VK_CAPS_LOCK;
      case "NumLock":
        return KeyEvent.VK_NUM_LOCK;
      case "ScrollLock":
        return KeyEvent.VK_SCROLL_LOCK;
      case "Home":
        return KeyEvent.VK_HOME;
      case "End":
        return KeyEvent.VK_END;
      case "Insert":
        return KeyEvent.VK_INSERT;
      case "Pause":
        return KeyEvent.VK_PAUSE;
      case "ContextMenu":
        return KeyEvent.VK_CONTEXT_MENU;
      default:
        return -1;
    }
  }
}
