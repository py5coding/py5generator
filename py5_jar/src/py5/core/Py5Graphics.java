package py5.core;

import processing.core.PGraphics;

/**
 * This class is never instantiated by Py5. Observe that this class extends
 * PGraphics, as does PGraphicsJava2D, PGraphics2D, PGraphics3D, etc. Therefore
 * I cannot do anything to this class and have it impact those other classes in
 * any way. This is only useful for generate_py5.py when it inspects classes and
 * picks up on the replaced CODED constant.
 * 
 * If I replaced the "JAVA2D", "P2D", "P3D", etc constants and possibly also
 * overloaded the makeGraphics method I could force Processing to create my own
 * versions of those classes (perhaps named Py5GraphicsJava2D, Py5Graphics2D,
 * etc) to get the same result as modifying Processing's PGraphics class, but
 * that would end up being a lot of work and hard to maintain. A better approach
 * is to add functions to Py5GraphicsHelper.
 */

public class Py5Graphics extends PGraphics {

  public static final char CODED = PGraphics.CODED;

}
