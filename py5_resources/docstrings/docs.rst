
# Py5Font_add_glyph

Create a new glyph, and add the character to the current font.

Parameters
----------

PARAMTEXT

Notes
-----

Create a new glyph, and add the character to the current font.


# Py5Font_ascent

Returns the ascent of this font from the baseline.

Parameters
----------

PARAMTEXT

Notes
-----

The ascent of the font. If the 'd' character is present in this Py5Font, this value is replaced with its pixel height, because the values returned by FontMetrics.getAscent() seem to be terrible.


# Py5Font_ascii

A more efficient array lookup for straight ASCII characters.

Parameters
----------

PARAMTEXT

Notes
-----

A more efficient array lookup for straight ASCII characters. For Unicode characters, a QuickSort-style search is used.


# Py5Font_charset

The default Processing character set.

Parameters
----------

PARAMTEXT

Notes
-----

The default Processing character set.

This is the union of the Mac Roman and Windows ANSI (CP1250) character sets. ISO 8859-1 Latin 1 is Unicode characters 0x80 ->0xFF, and would seem a good standard, but in practice, most P5 users would rather have characters that they expect from their platform's fonts.

This is more of an interim solution until a much better font solution can be determined. (i.e. create fonts on the fly from some sort of vector format).

Not that I expect that to happen.


# Py5Font_density

Default density set to 1 for backwards compatibility with loadFont().

Parameters
----------

PARAMTEXT

Notes
-----

Default density set to 1 for backwards compatibility with loadFont().


# Py5Font_descent

Returns how far this font descends from the baseline.

Parameters
----------

PARAMTEXT

Notes
-----

The descent of the font. If the 'p' character is present in this Py5Font, this value is replaced with its lowest pixel height, because the values returned by FontMetrics.getDescent() are gross.


# Py5Font_find_font

Starting with Java 1.5, Apple broke the ability to specify most fonts.

Parameters
----------

PARAMTEXT

Notes
-----

Starting with Java 1.5, Apple broke the ability to specify most fonts. This bug was filed years ago as #4769141 at bugreporter.apple.com. More:<a href="http://dev.processing.org/bugs/show_bug.cgi?id=407">Bug 407</a>.<br>This function displays a warning when the font is not found and Java's system font is used. See:<a href="https://github.com/processing/processing/issues/5481">issue #5481</a>


# Py5Font_find_native

Attempt to find the native version of this font.

Parameters
----------

PARAMTEXT

Notes
-----

Attempt to find the native version of this font. (Public so that it can be used by OpenGL or other renderers.)


# Py5Font_font

Native Java version of the font.

Parameters
----------

PARAMTEXT

Notes
-----

Native Java version of the font. If possible, this allows the Py5Graphics subclass to just use Java's font rendering stuff in situations where that's faster.


# Py5Font_font_searched

True if already tried to find the native AWT version of this font.

Parameters
----------

PARAMTEXT

Notes
-----

True if already tried to find the native AWT version of this font.


# Py5Font_fonts

Array of the native system fonts.

Parameters
----------

PARAMTEXT

Notes
-----

Array of the native system fonts. Used to lookup native fonts by their PostScript name. This is a workaround for a several year old Apple Java bug that they can't be bothered to fix.


# Py5Font_get_default_size

Returns the size that will be used when textFont(font) is called.

Parameters
----------

PARAMTEXT

Notes
-----

Returns the size that will be used when textFont(font) is called. When drawing with 2x pixel density, bitmap fonts in OpenGL need to be created (behind the scenes) at double the requested size. This ensures that they're shown at half on displays (so folks don't have to change their sketch code).


# Py5Font_get_font

Use the getNative() method instead, which allows library interfaces to be written in a cross-platform fashion for desktop, Android, and others.

Parameters
----------

PARAMTEXT

Notes
-----

Use the getNative() method instead, which allows library interfaces to be written in a cross-platform fashion for desktop, Android, and others.


# Py5Font_get_native

Return the native java.awt.Font associated with this Py5Font (if any).

Parameters
----------

PARAMTEXT

Notes
-----

Return the native java.awt.Font associated with this Py5Font (if any).


# Py5Font_get_size

Return size of this font.

Parameters
----------

PARAMTEXT

Notes
-----

Return size of this font.


# Py5Font_glyph

A single character, and its visage.

Parameters
----------

PARAMTEXT

Notes
-----

A single character, and its visage.


# Py5Font_glyph_count

Number of character glyphs in this font.

Parameters
----------

PARAMTEXT

Notes
-----

Number of character glyphs in this font.


# Py5Font_glyphs

Actual glyph data.

Parameters
----------

PARAMTEXT

Notes
-----

Actual glyph data. The length of this array won't necessarily be the same size as glyphCount, in cases where lazy font loading is in use.


# Py5Font_index

Get index for the character.

Parameters
----------

PARAMTEXT

Notes
-----

Get index for the character.


# Py5Font_init

Adds an additional parameter that indicates the font came from a file, not a built-in OS font.

Parameters
----------

PARAMTEXT

Notes
-----

Py5Font is the font class for Processing. To create a font to use with Processing, select "Create Font..." from the Tools menu. This will create a font in the format Processing requires and also adds it to the current sketch's data directory. Processing displays fonts using the .vlw font format, which uses images for each letter, rather than defining them through vector data. The ``load_font()`` function constructs a new font and ``text_font()`` makes a font active. The ``list()`` method creates a list of the fonts installed on the computer, which is useful information to use with the ``create_font()`` function for dynamically converting fonts into a format to use with Processing.


# Py5Font_kern

Currently un-implemented for .vlw fonts, but honored for layout in case subclasses use it.

Parameters
----------

PARAMTEXT

Notes
-----

Currently un-implemented for .vlw fonts, but honored for layout in case subclasses use it.


# Py5Font_lazy

True if this font is set to load dynamically.

Parameters
----------

PARAMTEXT

Notes
-----

True if this font is set to load dynamically. This is the default when createFont() method is called without a character set. Bitmap versions of characters are only created when prompted by an index() call.


# Py5Font_list

Gets a list of the fonts installed on the system.

Parameters
----------

PARAMTEXT

Notes
-----

Gets a list of the fonts installed on the system. The data is returned as a String array. This list provides the names of each font for input into ``create_font()`` , which allows Processing to dynamically format fonts. This function is meant as a tool for programming local applications and is not recommended for use in applets.


# Py5Font_load_fonts

Make an internal list of all installed fonts.

Parameters
----------

PARAMTEXT

Notes
-----

Make an internal list of all installed fonts. This can take a while with a lot of fonts installed, but running it on a separate thread may not help much. As of the commit that's adding this note, loadFonts() will only be called by Py5Font.list() and when loading a font by name, both of which are occasions when we'd need to block until this was finished anyway. It's also possible that running getAllFonts() on a non-EDT thread could cause graphics system issues. Further, the first fonts are usually loaded at the beginning of a sketch, meaning that sketch startup time will still be affected, even with threading in place. Where we're getting killed on font performance is due to this bug: https://bugs.openjdk.java.net/browse/JDK-8179209


# Py5Font_name

Name of the font as seen by Java when it was created.

Parameters
----------

PARAMTEXT

Notes
-----

Name of the font as seen by Java when it was created. If the font is available, the native version will be used.


# Py5Font_psname

Postscript name of the font that this bitmap was created from.

Parameters
----------

PARAMTEXT

Notes
-----

Postscript name of the font that this bitmap was created from.


# Py5Font_save

Write this Py5Font to an OutputStream.

Parameters
----------

PARAMTEXT

Notes
-----

Write this Py5Font to an OutputStream.

This is used by the Create Font tool, or whatever anyone else dreams up for messing with fonts themselves.

It is assumed that the calling class will handle closing the stream when finished.


# Py5Font_set_native

Set the native complement of this font.

Parameters
----------

PARAMTEXT

Notes
-----

Set the native complement of this font. Might be set internally via the findFont() function, or externally by a deriveFont() call if the font is resized by Py5GraphicsJava2D.


# Py5Font_size

The original size of the font when it was first created

Parameters
----------

PARAMTEXT

Notes
-----

The original size of the font when it was first created


# Py5Font_smooth

true if smoothing was enabled for this font, used for native impl

Parameters
----------

PARAMTEXT

Notes
-----

true if smoothing was enabled for this font, used for native impl


# Py5Font_stream

True if this font was loaded from an InputStream, rather than by name from the OS.

Parameters
----------

PARAMTEXT

Notes
-----

True if this font was loaded from an InputStream, rather than by name from the OS. It's best to use the native version of a font loaded from a TTF file, since that will ensure that the font is available when the sketch is exported.


# Py5Font_subsetting

True if this font should return 'null' for getFont(), so that the native font will be used to create a subset, but the native version of the font will not be used.

Parameters
----------

PARAMTEXT

Notes
-----

True if this font should return 'null' for getFont(), so that the native font will be used to create a subset, but the native version of the font will not be used.


# Py5Font_system_font_name

The name of the font that Java uses when a font isn't found.

Parameters
----------

PARAMTEXT

Notes
-----

The name of the font that Java uses when a font isn't found. See{@link #findFont(String)}and{@link #loadFonts()}for more info.


# Py5Font_width

Width of this character for a font of size 1.

Parameters
----------

PARAMTEXT

Notes
-----

Width of this character for a font of size 1.


# Py5Graphics_alpha

Extracts the alpha value from a color.

Parameters
----------

PARAMTEXT

Notes
-----

Extracts the alpha value from a color.


See Also
--------

Py5Graphics.red(int) : Extracts the red value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.green(int) : Extracts the green value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.blue(int) : Extracts the blue value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.hue(int) : Extracts the hue value from a color.

Py5Graphics.saturation(int) : Extracts the saturation value from a color.

Py5Graphics.brightness(int) : Extracts the brightness value from a color.


# Py5Graphics_ambient

Sets the ambient reflectance for shapes drawn to the screen.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the ambient reflectance for shapes drawn to the screen. This is combined with the ambient light component of environment. The color components set through the parameters define the reflectance. For example in the default color mode, setting v1=255, v2=126, v3=0, would cause all the red light to reflect and half of the green light to reflect. Used in combination with ``emissive()`` , ``specular()`` , and ``shininess()`` in setting the material properties of shapes.


See Also
--------

Py5Graphics.emissive(float, float, float) : Sets the emissive color of the material used for drawing shapes drawn to the screen.

Py5Graphics.specular(float, float, float) : Sets the specular color of the materials used for shapes drawn to the screen, which sets the color of hightlights.

Py5Graphics.shininess(float) : Sets the amount of gloss in the surface of shapes.


# Py5Graphics_ambient_light

Adds an ambient light.

Parameters
----------

PARAMTEXT

Notes
-----

Adds an ambient light. Ambient light doesn't come from a specific direction, the rays have light have bounced around so much that objects are evenly lit from all sides. Ambient lights are almost always used in combination with other types of lights. Lights need to be included in the ``draw()`` to remain persistent in a looping program. Placing them in the ``setup()`` of a looping program will cause them to only have an effect the first time through the loop. The effect of the parameters is determined by the current color mode.


See Also
--------

Py5Graphics.lights() : Sets the default ambient light, directional light, falloff, and specular values.

Py5Graphics.directionalLight(float, float, float, float, float, float)

Py5Graphics.pointLight(float, float, float, float, float, float)

Py5Graphics.spotLight(float, float, float, float, float, float, float, float, float, float, float)


# Py5Graphics_apply_matrix

Multiplies the current matrix by the one specified through the parameters.

Parameters
----------

PARAMTEXT

Notes
-----

Multiplies the current matrix by the one specified through the parameters. This is very slow because it will try to calculate the inverse of the transform, so avoid it whenever possible. The equivalent function in OpenGL is glMultMatrix().


See Also
--------

Py5Graphics.pushMatrix()

Py5Graphics.popMatrix()

Py5Graphics.resetMatrix()

Py5Graphics.printMatrix()


# Py5Graphics_arc

Draws an arc in the display window.

Parameters
----------

PARAMTEXT

Notes
-----

Draws an arc in the display window. Arcs are drawn along the outer edge of an ellipse defined by the ``x`` , ``y`` , ``width`` and ``height`` parameters. The origin or the arc's ellipse may be changed with the ``ellipse_mode()`` function. The ``start`` and ``stop`` parameters specify the angles at which to draw the arc.


See Also
--------

Sketch.ellipse(float, float, float, float) : Draws an ellipse (oval) in the display window.

Sketch.ellipseMode(int)

Sketch.radians(float) : Converts a degree measurement to its corresponding value in radians.

Sketch.degrees(float) : Converts a radian measurement to its corresponding value in degrees.


# Py5Graphics_arc_impl

Start and stop are in radians, converted by the parent function.

Parameters
----------

PARAMTEXT

Notes
-----

Start and stop are in radians, converted by the parent function. Note that the radians can be greater (or less) than TWO_PI. This is so that an arc can be drawn that crosses zero mark, and the user will still collect $200.


# Py5Graphics_await_async_save_completion

If there is running async save task for this file, blocks until it completes.

Parameters
----------

PARAMTEXT

Notes
-----

If there is running async save task for this file, blocks until it completes. Has to be called on main thread because OpenGL overrides this and calls GL.


# Py5Graphics_background

The , ``background()`` , function sets the color used for the background of the Processing window.

Parameters
----------

PARAMTEXT

Notes
-----

The ``background()`` function sets the color used for the background of the Processing window. The default background is light gray. In the ``draw()`` function, the background color is used to clear the display window at the beginning of each frame.

An image can also be used as the background for a sketch, however its width and height must be the same size as the sketch window. To resize an image 'b' to the size of the sketch window, use b.resize(width, height).

Images used as background will ignore the current ``tint()`` setting.

It is not possible to use transparency (alpha) in background colors with the main drawing surface, however they will work properly with ``create_graphics()`` .

Advanced
--------



Clear the background with a color that includes an alpha value. This can only be used with objects created by createGraphics(), because the main drawing surface cannot be set transparent.</p>

It might be tempting to use this function to partially clear the screen on each frame, however that's not how this function works. When calling background(), the pixels will be replaced with pixels that have that level of transparency. To do a semi-transparent overlay, use fill() with alpha and draw a rectangle.</p>


See Also
--------

Py5Graphics.stroke(float) : Sets the color used to draw lines and borders around shapes.

Py5Graphics.fill(float) : true if fill() is enabled, (read-only)

Py5Graphics.tint(float) : Sets the fill value for displaying images.

Py5Graphics.colorMode(int)


# Py5Graphics_background_color

Last background color that was set, zero if an image

Parameters
----------

PARAMTEXT

Notes
-----

Last background color that was set, zero if an image


# Py5Graphics_background_impl

Actual implementation of clearing the background, now that the internal variables for background color have been set.

Parameters
----------

PARAMTEXT

Notes
-----

Actual implementation of clearing the background, now that the internal variables for background color have been set. Called by the backgroundFromCalc() method, which is what all the other background() methods call once the work is done.


# Py5Graphics_begin_camera

The , ``begin_camera()`` , and , ``end_camera()`` , functions enable advanced customization of the camera space.

Parameters
----------

PARAMTEXT

Notes
-----

The ``begin_camera()`` and ``end_camera()`` functions enable advanced customization of the camera space. The functions are useful if you want to more control over camera movement, however for most users, the ``camera()`` function will be sufficient.

The camera functions will replace any transformations (such as ``rotate()`` or ``translate()`` ) that occur before them in ``draw()`` , but they will not automatically replace the camera transform itself. For this reason, camera functions should be placed at the beginning of ``draw()`` (so that transformations happen afterwards), and the ``camera()`` function can be used after ``begin_camera()`` if you want to reset the camera before applying transformations.

This function sets the matrix mode to the camera matrix so calls such as ``translate()`` , ``rotate()`` , applyMatrix() and resetMatrix() affect the camera. ``begin_camera()`` should always be used with a following ``end_camera()`` and pairs of ``begin_camera()`` and ``end_camera()`` cannot be nested.


See Also
--------

Py5Graphics.camera() : Sets the position of the camera through setting the eye position, the center of the scene, and which axis is facing upward.

Py5Graphics.endCamera()

Py5Graphics.applyMatrix(PMatrix)

Py5Graphics.resetMatrix()

Py5Graphics.translate(float, float, float) : Specifies an amount to displace objects within the display window.

Py5Graphics.scale(float, float, float) : Increases or decreases the size of a shape by expanding and contracting vertices.


# Py5Graphics_begin_contour



Parameters
----------

PARAMTEXT

Notes
-----




# Py5Graphics_begin_draw

Sets the default properties for a Py5Graphics object.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the default properties for a Py5Graphics object. It should be called before anything is drawn into the object.

Advanced
--------

When creating your own Py5Graphics, you should call this before drawing anything.


# Py5Graphics_begin_raw

Record individual lines and triangles by echoing them to another renderer.

Parameters
----------

PARAMTEXT

Notes
-----

Record individual lines and triangles by echoing them to another renderer.


# Py5Graphics_begin_shape

Using the , ``begin_shape()`` , and , ``end_shape()`` , functions allow creating more complex forms.

Parameters
----------

PARAMTEXT

Notes
-----

Using the ``begin_shape()`` and ``end_shape()`` functions allow creating more complex forms. ``begin_shape()`` begins recording vertices for a shape and ``end_shape()`` stops recording. The value of the ``mode`` parameter tells it which types of shapes to create from the provided vertices. With no mode specified, the shape can be any irregular polygon. The parameters available for beginShape() are POINTS, LINES, TRIANGLES, TRIANGLE_FAN, TRIANGLE_STRIP, QUADS, and QUAD_STRIP. After calling the ``begin_shape()`` function, a series of ``vertex()`` commands must follow. To stop drawing the shape, call ``end_shape()`` . The ``vertex()`` function with two parameters specifies a position in 2D and the ``vertex()`` function with three parameters specifies a position in 3D. Each shape will be outlined with the current stroke color and filled with the fill color.

Transformations such as ``translate()`` , ``rotate()`` , and ``scale()`` do not work within ``begin_shape()`` . It is also not possible to use other shapes, such as ``ellipse()`` or ``rect()`` within ``begin_shape()`` .

The P3D renderer settings allow ``stroke()`` and ``fill()`` settings to be altered per-vertex, however the default P2D renderer does not. Settings such as ``stroke_weight()`` , ``stroke_cap()`` , and ``stroke_join()`` cannot be changed while inside a ``begin_shape()`` / ``end_shape()`` block with any renderer.


See Also
--------

Py5Graphics.endShape()

Py5Graphics.vertex(float, float, float, float, float) : Used by renderer subclasses or Py5Shape to efficiently pass in already formatted vertex information.

Py5Graphics.curveVertex(float, float, float)

Py5Graphics.bezierVertex(float, float, float, float, float, float, float, float, float)


# Py5Graphics_bezier

Draws a Bezier curve on the screen.

Parameters
----------

PARAMTEXT

Notes
-----

Draws a Bezier curve on the screen. These curves are defined by a series of anchor and control points. The first two parameters specify the first anchor point and the last two parameters specify the other anchor point. The middle parameters specify the control points which define the shape of the curve. Bezier curves were developed by French engineer Pierre Bezier. Using the 3D version requires rendering with P3D (see the Environment reference for more information).

Advanced
--------

Draw a cubic bezier curve. The first and last points are the on-curve points. The middle two are the 'control' points, or 'handles' in an application like Illustrator.

Identical to typing:

``
begin_shape()
vertex(x1 y1)
bezier_vertex(x2 y2 x3 y3 x4 y4)
end_shape()
``

In Postscript-speak, this would be:

``
moveto(x1 y1)
curveto(x2 y2 x3 y3 x4 y4)
``

If you were to try and continue that curve like so:

``
curveto(x5 y5 x6 y6 x7 y7)
``

This would be done in processing by adding these statements:

``
bezier_vertex(x5 y5 x6 y6 x7 y7)
``

To draw a quadratic (instead of cubic) curve, use the control point twice by doubling it:

``
bezier(x1 y1 cx cy cx cy x2 y2)
``


See Also
--------

Py5Graphics.bezierVertex(float, float, float, float, float, float)

Py5Graphics.curve(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a curved line on the screen.


# Py5Graphics_bezier_detail

Sets the resolution at which Beziers display.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the resolution at which Beziers display. The default value is 20. This function is only useful when using the P3D renderer as the default P2D renderer does not use this information.


See Also
--------

Py5Graphics.curve(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a curved line on the screen.

Py5Graphics.curveVertex(float, float, float)

Py5Graphics.curveTightness(float)


# Py5Graphics_bezier_point

Evaluates the Bezier at point t for points a, b, c, d.

Parameters
----------

PARAMTEXT

Notes
-----

Evaluates the Bezier at point t for points a, b, c, d. The parameter t varies between 0 and 1, a and d are points on the curve, and b and c are the control points. This can be done once with the x coordinates and a second time with the y coordinates to get the location of a bezier curve at t.

Advanced
--------

For instance, to convert the following example:

``
stroke(255 102 0)
line(85 20 10 10)
line(90 90 15 80)
stroke(0 0 0)
bezier(85 20 10 10 90 90 15 80)
// draw it in gray using 10 steps instead of the default 20 // this is a slower way to do it but useful if you need // to do things with the coordinates at each step stroke(128)
begin_shape(line_strip)
for (int i = 0
i<= 10
i++) {   float t = i / 10.0f
float x = bezier_point(85 10 90 15 t)
float y = bezier_point(20 10 90 80 t)
vertex(x y)
} end_shape()
``


See Also
--------

Py5Graphics.bezier(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a Bezier curve on the screen.

Py5Graphics.bezierVertex(float, float, float, float, float, float)

Py5Graphics.curvePoint(float, float, float, float, float)


# Py5Graphics_bezier_tangent

Calculates the tangent of a point on a Bezier curve.

Parameters
----------

PARAMTEXT

Notes
-----

Calculates the tangent of a point on a Bezier curve. There is a good definition of<a href="http://en.wikipedia.org/wiki/Tangent"target="new"><em>tangent</em>on Wikipedia</a>.

Advanced
--------

Code submitted by Dave Bollinger (davol) for release 0136.


See Also
--------

Py5Graphics.bezier(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a Bezier curve on the screen.

Py5Graphics.bezierVertex(float, float, float, float, float, float)

Py5Graphics.curvePoint(float, float, float, float, float)


# Py5Graphics_bezier_vertex

Specifies vertex coordinates for Bezier curves.

Parameters
----------

PARAMTEXT

Notes
-----

Specifies vertex coordinates for Bezier curves. Each call to ``bezier_vertex()`` defines the position of two control points and one anchor point of a Bezier curve, adding a new segment to a line or shape. The first time ``bezier_vertex()`` is used within a ``begin_shape()`` call, it must be prefaced with a call to ``vertex()`` to set the first anchor point. This function must be used between ``begin_shape()`` and ``end_shape()`` and only when there is no MODE parameter specified to ``begin_shape()`` . Using the 3D version requires rendering with P3D (see the Environment reference for more information).


See Also
--------

Py5Graphics.curveVertex(float, float, float)

Py5Graphics.vertex(float, float, float, float, float) : Used by renderer subclasses or Py5Shape to efficiently pass in already formatted vertex information.

Py5Graphics.quadraticVertex(float, float, float, float, float, float)

Py5Graphics.bezier(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a Bezier curve on the screen.


# Py5Graphics_blend_mode

This is a new reference entry for Processing 2.0.

Parameters
----------

PARAMTEXT

Notes
-----

This is a new reference entry for Processing 2.0. It will be updated shortly.


# Py5Graphics_blue

Extracts the blue value from a color, scaled to match current , ``color_mode()`` ,.

Parameters
----------

PARAMTEXT

Notes
-----

Extracts the blue value from a color, scaled to match current ``color_mode()`` . This value is always returned as a  float so be careful not to assign it to an int value.

The ``blue()`` function is easy to use and undestand, but is slower than another technique. To achieve the same results when working in ``color_mode(rgb 255)`` , but with greater speed, use a bit mask to remove the other color components. For example, the following two lines of code are equivalent:
<pre>float r1 = blue(myColor);
float r2 = myColor&0xFF;</pre>


See Also
--------

Py5Graphics.red(int) : Extracts the red value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.green(int) : Extracts the green value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.alpha(int) : Extracts the alpha value from a color.

Py5Graphics.hue(int) : Extracts the hue value from a color.

Py5Graphics.saturation(int) : Extracts the saturation value from a color.

Py5Graphics.brightness(int) : Extracts the brightness value from a color.


# Py5Graphics_box

A box is an extruded rectangle.

Parameters
----------

PARAMTEXT

Notes
-----

A box is an extruded rectangle. A box with equal dimension on all sides is a cube.


See Also
--------

Py5Graphics.sphere(float) : A sphere is a hollow ball made from tessellated triangles.


# Py5Graphics_brightness

Extracts the brightness value from a color.

Parameters
----------

PARAMTEXT

Notes
-----

Extracts the brightness value from a color.


See Also
--------

Py5Graphics.red(int) : Extracts the red value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.green(int) : Extracts the green value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.blue(int) : Extracts the blue value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.alpha(int) : Extracts the alpha value from a color.

Py5Graphics.hue(int) : Extracts the hue value from a color.

Py5Graphics.saturation(int) : Extracts the saturation value from a color.


# Py5Graphics_cache_hsb_key

The last RGB value converted to HSB

Parameters
----------

PARAMTEXT

Notes
-----

The last RGB value converted to HSB


# Py5Graphics_cache_hsb_value

Result of the last conversion to HSB

Parameters
----------

PARAMTEXT

Notes
-----

Result of the last conversion to HSB


# Py5Graphics_cache_map

Storage for renderer-specific image data.

Parameters
----------

PARAMTEXT

Notes
-----

Storage for renderer-specific image data. In 1.x, renderers wrote cache data into the image object. In 2.x, the renderer has a weak-referenced map that points at any of the images it has worked on already. When the images go out of scope, they will be properly garbage collected.


# Py5Graphics_camera

Sets the position of the camera through setting the eye position, the center of the scene, and which axis is facing upward.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the position of the camera through setting the eye position, the center of the scene, and which axis is facing upward. Moving the eye position and the direction it is pointing (the center of the scene) allows the images to be seen from different angles. The version without any parameters sets the camera to the default position, pointing to the center of the display window with the Y axis as up. The default values are ``camera(width/2.0 height/2.0 (height/2.0) / tan(pi*30.0 / 180.0) width/2.0 height/2.0 0 0 1 0)`` . This function is similar to ``glu_look_at()`` in OpenGL, but it first clears the current camera settings.


See Also
--------

Py5Graphics.beginCamera()

Py5Graphics.endCamera()

Py5Graphics.frustum(float, float, float, float, float, float) : Sets a perspective matrix defined through the parameters.


# Py5Graphics_circle

Draws a circle to the screen.

Parameters
----------

PARAMTEXT

Notes
-----

Draws a circle to the screen. By default, the first two parameters set the location of the center, and the third sets the shape's width and height. The origin may be changed with the ``ellipse_mode()`` function.


See Also
--------

Sketch.ellipse(float, float, float, float) : Draws an ellipse (oval) in the display window.

Sketch.ellipseMode(int)


# Py5Graphics_clear



Parameters
----------

PARAMTEXT

Notes
-----




# Py5Graphics_clip

Limits the rendering to the boundaries of a rectangle defined by the parameters.

Parameters
----------

PARAMTEXT

Notes
-----

Limits the rendering to the boundaries of a rectangle defined by the parameters. The boundaries are drawn based on the state of the ``image_mode()`` fuction, either CORNER, CORNERS, or CENTER.


# Py5Graphics_color



Parameters
----------

PARAMTEXT

Notes
-----




# Py5Graphics_color_calc

Set the fill to either a grayscale value or an ARGB int.

Parameters
----------

PARAMTEXT

Notes
-----

Set the fill to either a grayscale value or an ARGB int.

The problem with this code is that it has to detect between these two situations automatically. This is done by checking to see if the high bits (the alpha for 0xAA000000) is set, and if not, whether the color value that follows is less than colorModeX (first param passed to colorMode).

This auto-detect would break in the following situation:

``
size(256 256)
for (int i = 0
i<256
i++) {   color c = color(0 0 0 i)
stroke(c)
line(i 0 i 256)
}
``

...on the first time through the loop, where (i == 0), since the color itself is zero (black) then it would appear indistinguishable from code that reads "fill(0)". The solution is to use the four parameter versions of stroke or fill to more directly specify the desired result.


# Py5Graphics_color_calc_argb

Unpacks AARRGGBB color for direct use with colorCalc.

Parameters
----------

PARAMTEXT

Notes
-----

Unpacks AARRGGBB color for direct use with colorCalc.

Handled here with its own function since this is indepenent of the color mode.

Strangely the old version of this code ignored the alpha value. not sure if that was a bug or what.

Note, no need for a bounds check for 'argb' since it's a 32 bit number. Bounds now checked on alpha, however (rev 0225).


# Py5Graphics_color_mode

Changes the way Processing interprets color data.

Parameters
----------

PARAMTEXT

Notes
-----

Changes the way Processing interprets color data. By default, the parameters for ``fill()`` , ``stroke()`` , ``background()`` , and ``color()`` are defined by values between 0 and 255 using the RGB color model. The ``color_mode()`` function is used to change the numerical range used for specifying colors and to switch color systems. For example, calling ``color_mode(rgb 1.0)`` will specify that values are specified between 0 and 1. The limits for defining colors are altered by setting the parameters range1, range2, range3, and range 4.


See Also
--------

Py5Graphics.background(float) : The , ``background()`` , function sets the color used for the background of the Processing window.

Py5Graphics.fill(float) : true if fill() is enabled, (read-only)

Py5Graphics.stroke(float) : Sets the color used to draw lines and borders around shapes.


# Py5Graphics_color_mode_a

Max value for alpha set by colorMode

Parameters
----------

PARAMTEXT

Notes
-----

Max value for alpha set by colorMode


# Py5Graphics_color_mode_default

True if colorMode(RGB, 255).

Parameters
----------

PARAMTEXT

Notes
-----

True if colorMode(RGB, 255). Defaults to true so that color() used as part of a field declaration will properly assign values.


# Py5Graphics_color_mode_scale

True if colors are not in the range 0..1

Parameters
----------

PARAMTEXT

Notes
-----

True if colors are not in the range 0..1


# Py5Graphics_color_mode_x

Max value for red (or hue) set by colorMode

Parameters
----------

PARAMTEXT

Notes
-----

Max value for red (or hue) set by colorMode


# Py5Graphics_color_mode_y

Max value for green (or saturation) set by colorMode

Parameters
----------

PARAMTEXT

Notes
-----

Max value for green (or saturation) set by colorMode


# Py5Graphics_color_mode_z

Max value for blue (or value) set by colorMode

Parameters
----------

PARAMTEXT

Notes
-----

Max value for blue (or value) set by colorMode


# Py5Graphics_create_default_font

Used by Py5Graphics to remove the requirement for loading a font.

Parameters
----------

PARAMTEXT

Notes
-----

Used by Py5Graphics to remove the requirement for loading a font.


# Py5Graphics_create_shape



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Py5Shape.endShape()

Sketch.loadShape(String)


# Py5Graphics_create_shape_family

Override this method to return an appropriate shape for your renderer

Parameters
----------

PARAMTEXT

Notes
-----

Override this method to return an appropriate shape for your renderer


# Py5Graphics_create_shape_primitive

Override this to have a custom shape object used by your renderer.

Parameters
----------

PARAMTEXT

Notes
-----

Override this to have a custom shape object used by your renderer.


# Py5Graphics_curve

Draws a curved line on the screen.

Parameters
----------

PARAMTEXT

Notes
-----

Draws a curved line on the screen. The first and second parameters specify the beginning control point and the last two parameters specify the ending control point. The middle parameters specify the start and stop of the curve. Longer curves can be created by putting a series of ``curve()`` functions together or using ``curve_vertex()`` . An additional function called ``curve_tightness()`` provides control for the visual quality of the curve. The ``curve()`` function is an implementation of Catmull-Rom splines. Using the 3D version requires rendering with P3D (see the Environment reference for more information).

Advanced
--------

As of revision 0070, this function no longer doubles the first and last points. The curves are a bit more boring, but it's more mathematically correct, and properly mirrored in curvePoint().

Identical to typing out:

``
begin_shape()
curve_vertex(x1 y1)
curve_vertex(x2 y2)
curve_vertex(x3 y3)
curve_vertex(x4 y4)
end_shape()
``


See Also
--------

Py5Graphics.curveVertex(float, float)

Py5Graphics.curveTightness(float)

Py5Graphics.bezier(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a Bezier curve on the screen.


# Py5Graphics_curve_detail

Sets the resolution at which curves display.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the resolution at which curves display. The default value is 20. This function is only useful when using the P3D renderer as the default P2D renderer does not use this information.


See Also
--------

Py5Graphics.curve(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a curved line on the screen.

Py5Graphics.curveVertex(float, float)

Py5Graphics.curveTightness(float)


# Py5Graphics_curve_init

Set the number of segments to use when drawing a Catmull-Rom curve, and setting the s parameter, which defines how tightly the curve fits to each vertex.

Parameters
----------

PARAMTEXT

Notes
-----

Set the number of segments to use when drawing a Catmull-Rom curve, and setting the s parameter, which defines how tightly the curve fits to each vertex. Catmull-Rom curves are actually a subset of this curve type where the s is set to zero.

(This function is not optimized, since it's not expected to be called all that often. there are many juicy and obvious opimizations in here, but it's probably better to keep the code more readable)


# Py5Graphics_curve_point

Evalutes the curve at point t for points a, b, c, d.

Parameters
----------

PARAMTEXT

Notes
-----

Evalutes the curve at point t for points a, b, c, d. The parameter t varies between 0 and 1, a and d are the control points, and b and c are the points on the curve. This can be done once with the x coordinates and a second time with the y coordinates to get the location of a curve at t.


See Also
--------

Py5Graphics.curve(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a curved line on the screen.

Py5Graphics.curveVertex(float, float)

Py5Graphics.bezierPoint(float, float, float, float, float)


# Py5Graphics_curve_tangent

Calculates the tangent of a point on a curve.

Parameters
----------

PARAMTEXT

Notes
-----

Calculates the tangent of a point on a curve. There's a good definition of<em><a href="http://en.wikipedia.org/wiki/Tangent"target="new">tangent</em>on Wikipedia</a>.

Advanced
--------

Code thanks to Dave Bollinger (Bug #715)


See Also
--------

Py5Graphics.curve(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a curved line on the screen.

Py5Graphics.curveVertex(float, float)

Py5Graphics.curvePoint(float, float, float, float, float)

Py5Graphics.bezierTangent(float, float, float, float, float)


# Py5Graphics_curve_tightness

Modifies the quality of forms created with , ``curve()`` , and , ``curve_vertex()`` ,.

Parameters
----------

PARAMTEXT

Notes
-----

Modifies the quality of forms created with ``curve()`` and ``curve_vertex()`` . The parameter ``squishy`` determines how the curve fits to the vertex points. The value 0.0 is the default value for ``squishy`` (this value defines the curves to be Catmull-Rom splines) and the value 1.0 connects all the points with straight lines. Values within the range -5.0 and 5.0 will deform the curves but will leave them recognizable and as values increase in magnitude, they will continue to deform.


See Also
--------

Py5Graphics.curve(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a curved line on the screen.

Py5Graphics.curveVertex(float, float)


# Py5Graphics_curve_vertex

Specifies vertex coordinates for curves.

Parameters
----------

PARAMTEXT

Notes
-----

Specifies vertex coordinates for curves. This function may only be used between ``begin_shape()`` and ``end_shape()`` and only when there is no MODE parameter specified to ``begin_shape()`` . The first and last points in a series of ``curve_vertex()`` lines will be used to guide the beginning and end of a the curve. A minimum of four points is required to draw a tiny curve between the second and third points. Adding a fifth point with ``curve_vertex()`` will draw the curve between the second, third, and fourth points. The ``curve_vertex()`` function is an implementation of Catmull-Rom splines. Using the 3D version requires rendering with P3D (see the Environment reference for more information).


See Also
--------

Py5Graphics.curve(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a curved line on the screen.

Py5Graphics.beginShape(int)

Py5Graphics.endShape(int)

Py5Graphics.vertex(float, float, float, float, float) : Used by renderer subclasses or Py5Shape to efficiently pass in already formatted vertex information.

Py5Graphics.bezier(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a Bezier curve on the screen.

Py5Graphics.quadraticVertex(float, float, float, float, float, float)


# Py5Graphics_curve_vertex_check

Perform initialization specific to curveVertex(), and handle standard error modes.

Parameters
----------

PARAMTEXT

Notes
-----

Perform initialization specific to curveVertex(), and handle standard error modes. Can be overridden by subclasses that need the flexibility.


# Py5Graphics_curve_vertex_segment

Handle emitting a specific segment of Catmull-Rom curve.

Parameters
----------

PARAMTEXT

Notes
-----

Handle emitting a specific segment of Catmull-Rom curve. This can be overridden by subclasses that need more efficient rendering options.


# Py5Graphics_default_font_or_death

First try to create a default font, but if that's not possible, throw an exception that halts the program because textFont() has not been used prior to the specified method.

Parameters
----------

PARAMTEXT

Notes
-----

First try to create a default font, but if that's not possible, throw an exception that halts the program because textFont() has not been used prior to the specified method.


# Py5Graphics_default_settings

Set engine's default values.

Parameters
----------

PARAMTEXT

Notes
-----

Set engine's default values. This has to be called by Sketch, somewhere inside setup() or draw() because it talks to the graphics buffer, meaning that for subclasses like OpenGL, there needs to be a valid graphics context to mess with otherwise you'll get some good crashing action. This is currently called by checkSettings(), during beginDraw().


# Py5Graphics_directional_light

Adds a directional light.

Parameters
----------

PARAMTEXT

Notes
-----

Adds a directional light. Directional light comes from one direction and is stronger when hitting a surface squarely and weaker if it hits at a a gentle angle. After hitting a surface, a directional lights scatters in all directions. Lights need to be included in the ``draw()`` to remain persistent in a looping program. Placing them in the ``setup()`` of a looping program will cause them to only have an effect the first time through the loop. The affect of the ``v1`` , ``v2`` , and ``v3`` parameters is determined by the current color mode. The ``nx`` , ``ny`` , and ``nz`` parameters specify the direction the light is facing. For example, setting ``ny`` to -1 will cause the geometry to be lit from below (the light is facing directly upward).


See Also
--------

Py5Graphics.lights() : Sets the default ambient light, directional light, falloff, and specular values.

Py5Graphics.ambientLight(float, float, float, float, float, float)

Py5Graphics.pointLight(float, float, float, float, float, float)

Py5Graphics.spotLight(float, float, float, float, float, float, float, float, float, float, float)


# Py5Graphics_displayable

Return true if this renderer should be drawn to the screen.

Parameters
----------

PARAMTEXT

Notes
-----

Return true if this renderer should be drawn to the screen. Defaults to returning true, since nearly all renderers are on-screen beasts. But can be overridden for subclasses like PDF so that a window doesn't open up.

A better name? showFrame, displayable, isVisible, visible, shouldDisplay, what to call this?


# Py5Graphics_dispose

Handle any takedown for this graphics context.

Parameters
----------

PARAMTEXT

Notes
-----

Handle any takedown for this graphics context.

This is called when a sketch is shut down and this renderer was specified using the size() command, or inside endRecord() and endRaw(), in order to shut things off.


# Py5Graphics_edge

Sets whether the upcoming vertex is part of an edge.

Parameters
----------

PARAMTEXT

Notes
-----

Sets whether the upcoming vertex is part of an edge. Equivalent to glEdgeFlag(), for people familiar with OpenGL.


# Py5Graphics_ellipse

Draws an ellipse (oval) in the display window.

Parameters
----------

PARAMTEXT

Notes
-----

Draws an ellipse (oval) in the display window. An ellipse with an equal ``width`` and ``height`` is a circle. The first two parameters set the location, the third sets the width, and the fourth sets the height. The origin may be changed with the ``ellipse_mode()`` function.


See Also
--------

Sketch.ellipseMode(int)

Sketch.arc(float, float, float, float, float, float) : Draws an arc in the display window.


# Py5Graphics_ellipse_mode

The origin of the ellipse is modified by the , ``ellipse_mode()`` , function.

Parameters
----------

PARAMTEXT

Notes
-----

The origin of the ellipse is modified by the ``ellipse_mode()`` function. The default configuration is ``ellipse_mode(center)`` , which specifies the location of the ellipse as the center of the shape. The ``radius`` mode is the same, but the width and height parameters to ``ellipse()`` specify the radius of the ellipse, rather than the diameter. The ``corner`` mode draws the shape from the upper-left corner of its bounding box. The ``corners`` mode uses the four parameters to ``ellipse()`` to set two opposing corners of the ellipse's bounding box. The parameter must be written in ALL CAPS because Processing is a case-sensitive language.


See Also
--------

Sketch.ellipse(float, float, float, float) : Draws an ellipse (oval) in the display window.

Sketch.arc(float, float, float, float, float, float) : Draws an arc in the display window.


# Py5Graphics_emissive

Sets the emissive color of the material used for drawing shapes drawn to the screen.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the emissive color of the material used for drawing shapes drawn to the screen. Used in combination with ``ambient()`` , ``specular()`` , and ``shininess()`` in setting the material properties of shapes.


See Also
--------

Py5Graphics.ambient(float, float, float) : Sets the ambient reflectance for shapes drawn to the screen.

Py5Graphics.specular(float, float, float) : Sets the specular color of the materials used for shapes drawn to the screen, which sets the color of hightlights.

Py5Graphics.shininess(float) : Sets the amount of gloss in the surface of shapes.


# Py5Graphics_end_camera

The , ``begin_camera()`` , and , ``end_camera()`` , functions enable advanced customization of the camera space.

Parameters
----------

PARAMTEXT

Notes
-----

The ``begin_camera()`` and ``end_camera()`` functions enable advanced customization of the camera space. Please see the reference for ``begin_camera()`` for a description of how the functions are used.


See Also
--------

Py5Graphics.beginCamera()

Py5Graphics.camera(float, float, float, float, float, float, float, float, float) : Sets the position of the camera through setting the eye position, the center of the scene, and which axis is facing upward.


# Py5Graphics_end_contour



Parameters
----------

PARAMTEXT

Notes
-----




# Py5Graphics_end_draw

Finalizes the rendering of a Py5Graphics object so that it can be shown on screen.

Parameters
----------

PARAMTEXT

Notes
-----

Finalizes the rendering of a Py5Graphics object so that it can be shown on screen.

Advanced
--------



When creating your own Py5Graphics, you should call this when you're finished drawing.


# Py5Graphics_end_shape

The , ``end_shape()`` , function is the companion to , ``begin_shape()`` , and may only be called after , ``begin_shape()`` ,.

Parameters
----------

PARAMTEXT

Notes
-----

The ``end_shape()`` function is the companion to ``begin_shape()`` and may only be called after ``begin_shape()`` . When ``endshape()`` is called, all of image data defined since the previous call to ``begin_shape()`` is written into the image buffer. The constant CLOSE as the value for the MODE parameter to close the shape (to connect the beginning and the end).


See Also
--------

Py5Graphics.beginShape(int)


# Py5Graphics_fill

true if fill() is enabled, (read-only)

Parameters
----------

PARAMTEXT

Notes
-----

Sets the color used to fill shapes. For example, if you run ``fill(204 102 0)`` , all subsequent shapes will be filled with orange. This color is either specified in terms of the RGB or HSB color depending on the current ``color_mode()`` (the default color space is RGB, with each value in the range from 0 to 255).

When using hexadecimal notation to specify a color, use "#" or "0x" before the values (e.g. #CCFFAA, 0xFFCCFFAA). The # syntax uses six digits to specify a color (the way colors are specified in HTML and CSS). When using the hexadecimal notation starting with "0x", the hexadecimal value must be specified with eight characters; the first two characters define the alpha component and the remainder the red, green, and blue components.

The value for the parameter "gray" must be less than or equal to the current maximum value as specified by ``color_mode()`` . The default maximum value is 255.

To change the color of an image (or a texture), use tint().


See Also
--------

Py5Graphics.noFill()

Py5Graphics.stroke(int, float) : Sets the color used to draw lines and borders around shapes.

Py5Graphics.noStroke()

Py5Graphics.tint(int, float) : Sets the fill value for displaying images.

Py5Graphics.background(float, float, float, float) : The , ``background()`` , function sets the color used for the background of the Processing window.

Py5Graphics.colorMode(int, float, float, float, float)


# Py5Graphics_fill_color

fill that was last set (read-only)

Parameters
----------

PARAMTEXT

Notes
-----

fill that was last set (read-only)


# Py5Graphics_filter



Parameters
----------

PARAMTEXT

Notes
-----




# Py5Graphics_frustum

Sets a perspective matrix defined through the parameters.

Parameters
----------

PARAMTEXT

Notes
-----

Sets a perspective matrix defined through the parameters. Works like glFrustum, except it wipes out the current perspective matrix rather than muliplying itself with it.


See Also
--------

Py5Graphics.camera(float, float, float, float, float, float, float, float, float) : Sets the position of the camera through setting the eye position, the center of the scene, and which axis is facing upward.

Py5Graphics.beginCamera()

Py5Graphics.endCamera()

Py5Graphics.perspective(float, float, float, float) : Sets a perspective projection applying foreshortening, making distant objects appear smaller than closer ones.


# Py5Graphics_get_cache

Get cache storage data for the specified renderer.

Parameters
----------

PARAMTEXT

Notes
-----

Get cache storage data for the specified renderer. Because each renderer will cache data in different formats, it's necessary to store cache data keyed by the renderer object. Otherwise, attempting to draw the same image to both a Py5GraphicsJava2D and a Py5GraphicsOpenGL will cause errors.


# Py5Graphics_get_matrix

Copy the current transformation matrix into the specified target.

Parameters
----------

PARAMTEXT

Notes
-----

Copy the current transformation matrix into the specified target. Pass in null to create a new matrix.


# Py5Graphics_green

Extracts the green value from a color, scaled to match current , ``color_mode()`` ,.

Parameters
----------

PARAMTEXT

Notes
-----

Extracts the green value from a color, scaled to match current ``color_mode()`` . This value is always returned as a  float so be careful not to assign it to an int value.

The ``green()`` function is easy to use and undestand, but is slower than another technique. To achieve the same results when working in ``color_mode(rgb 255)`` , but with greater speed, use the>>(right shift) operator with a bit mask. For example, the following two lines of code are equivalent:
<pre>float r1 = green(myColor);
float r2 = myColor>>8&0xFF;</pre>


See Also
--------

Py5Graphics.red(int) : Extracts the red value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.blue(int) : Extracts the blue value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.alpha(int) : Extracts the alpha value from a color.

Py5Graphics.hue(int) : Extracts the hue value from a color.

Py5Graphics.saturation(int) : Extracts the saturation value from a color.

Py5Graphics.brightness(int) : Extracts the brightness value from a color.


# Py5Graphics_handle_text_size

Sets the actual size.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the actual size. Called from textSizeImpl and from textFontImpl after setting the font.


# Py5Graphics_hint

Set various hints and hacks for the renderer.

Parameters
----------

PARAMTEXT

Notes
-----

Set various hints and hacks for the renderer. This is used to handle obscure rendering features that cannot be implemented in a consistent manner across renderers. Many options will often graduate to standard features instead of hints over time.

hint(ENABLE_OPENGL_4X_SMOOTH) - Enable 4x anti-aliasing for P3D. This can help force anti-aliasing if it has not been enabled by the user. On some graphics cards, this can also be set by the graphics driver's control panel, however not all cards make this available. This hint must be called immediately after the size() command because it resets the renderer, obliterating any settings and anything drawn (and like size(), re-running the code that came before it again).

hint(DISABLE_OPENGL_2X_SMOOTH) - In Processing 1.0, Processing always enables 2x smoothing when the P3D renderer is used. This hint disables the default 2x smoothing and returns the smoothing behavior found in earlier releases, where smooth() and noSmooth() could be used to enable and disable smoothing, though the quality was inferior.

hint(ENABLE_NATIVE_FONTS) - Use the native version fonts when they are installed, rather than the bitmapped version from a .vlw file. This is useful with the default (or JAVA2D) renderer setting, as it will improve font rendering speed. This is not enabled by default, because it can be misleading while testing because the type will look great on your machine (because you have the font installed) but lousy on others' machines if the identical font is unavailable. This option can only be set per-sketch, and must be called before any use of textFont().

hint(DISABLE_DEPTH_TEST) - Disable the zbuffer, allowing you to draw on top of everything at will. When depth testing is disabled, items will be drawn to the screen sequentially, like a painting. This hint is most often used to draw in 3D, then draw in 2D on top of it (for instance, to draw GUI controls in 2D on top of a 3D interface). Starting in release 0149, this will also clear the depth buffer. Restore the default with hint(ENABLE_DEPTH_TEST), but note that with the depth buffer cleared, any 3D drawing that happens later in draw() will ignore existing shapes on the screen.

hint(ENABLE_DEPTH_SORT) - Enable primitive z-sorting of triangles and lines in P3D and OPENGL. This can slow performance considerably, and the algorithm is not yet perfect. Restore the default with hint(DISABLE_DEPTH_SORT).

hint(DISABLE_OPENGL_ERROR_REPORT) - Speeds up the P3D renderer setting by not checking for errors while running. Undo with hint(ENABLE_OPENGL_ERROR_REPORT).

hint(ENABLE_BUFFER_READING) - Depth and stencil buffers in P2D/P3D will be downsampled to make PGL#readPixels work with multisampling. Enabling this introduces some overhead, so if you experience bad performance, disable multisampling with noSmooth() instead. This hint is not intended to be enabled and disabled repeatedely, so call this once in setup() or after creating your Py5Graphics2D/3D. You can restore the default with hint(DISABLE_BUFFER_READING) if you don't plan to read depth from this Py5Graphics anymore.

hint(ENABLE_KEY_REPEAT) - Auto-repeating key events are discarded by default (works only in P2D/P3D); use this hint to get all the key events (including auto-repeated). Call hint(DISABLE_KEY_REPEAT) to get events only when the key goes physically up or down.

hint(DISABLE_ASYNC_SAVEFRAME) - P2D/P3D only - save() and saveFrame() will not use separate threads for saving and will block until the image is written to the drive. This was the default behavior in 3.0b7 and before. To enable, call hint(ENABLE_ASYNC_SAVEFRAME).

As of release 0149, unhint() has been removed in favor of adding additional ENABLE/DISABLE constants to reset the default behavior. This prevents the double negatives, and also reinforces which hints can be enabled or disabled.


See Also
--------

Sketch.createGraphics(int, int, String, String)

Sketch.size(int, int) : Defines the dimension of the display window in units of pixels.


# Py5Graphics_hints

Array of hint[] items.

Parameters
----------

PARAMTEXT

Notes
-----

Array of hint[] items. These are hacks to get around various temporary workarounds inside the environment.

Note that this array cannot be static, as a hint() may result in a runtime change specific to a renderer. For instance, calling hint(DISABLE_DEPTH_TEST) has to call glDisable() right away on an instance of Py5GraphicsOpenGL.

The hints[] array is allocated early on because it might be used inside beginDraw(), allocate(), etc.


# Py5Graphics_hue

Extracts the hue value from a color.

Parameters
----------

PARAMTEXT

Notes
-----

Extracts the hue value from a color.


See Also
--------

Py5Graphics.red(int) : Extracts the red value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.green(int) : Extracts the green value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.blue(int) : Extracts the blue value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.alpha(int) : Extracts the alpha value from a color.

Py5Graphics.saturation(int) : Extracts the saturation value from a color.

Py5Graphics.brightness(int) : Extracts the brightness value from a color.


# Py5Graphics_image

Java AWT Image object associated with this renderer.

Parameters
----------

PARAMTEXT

Notes
-----

Displays images to the screen. The images must be in the sketch's "data" directory to load correctly. Select "Add file..." from the "Sketch" menu to add the image. Processing currently works with GIF, JPEG, and Targa images. The ``img`` parameter specifies the image to display and the ``x`` and ``y`` parameters define the location of the image from its upper-left corner. The image is displayed at its original size unless the ``width`` and ``height`` parameters specify a different size.

The ``image_mode()`` function changes the way the parameters work. For example, a call to ``image_mode(corners)`` will change the ``width`` and ``height`` parameters to define the x and y values of the opposite corner of the image.

The color of an image may be modified with the ``tint()`` function. This function will maintain transparency for GIF and PNG images.

Advanced
--------

Starting with release 0124, when using the default (JAVA2D) renderer, smooth() will also improve image quality of resized images.


See Also
--------

Sketch.loadImage(String, String)

Py5Graphics.imageMode(int)

Py5Graphics.tint(float) : Sets the fill value for displaying images.

Py5Graphics.background(float, float, float, float) : The , ``background()`` , function sets the color used for the background of the Processing window.

Py5Graphics.alpha(int) : Extracts the alpha value from a color.


# Py5Graphics_image_impl

Expects x1, y1, x2, y2 coordinates where (x2 ,>,= x1) and (y2 ,>,= y1).

Parameters
----------

PARAMTEXT

Notes
-----

Expects x1, y1, x2, y2 coordinates where (x2>= x1) and (y2>= y1). If tint() has been called, the image will be colored.

The default implementation draws an image as a textured quad. The (u, v) coordinates are in image space (they're ints, after all..)


# Py5Graphics_image_mode

Modifies the location from which images draw.

Parameters
----------

PARAMTEXT

Notes
-----

Modifies the location from which images draw. The default mode is ``image_mode(corner)`` , which specifies the location to be the upper left corner and uses the fourth and fifth parameters of ``image()`` to set the image's width and height. The syntax ``image_mode(corners)`` uses the second and third parameters of ``image()`` to set the location of one corner of the image and uses the fourth and fifth parameters to set the opposite corner. Use ``image_mode(center)`` to draw images centered at the given x and y position.

The parameter to ``image_mode()`` must be written in ALL CAPS because Processing is a case-sensitive language.


See Also
--------

Sketch.loadImage(String, String)

Py5Graphics.image(Py5Image, float, float, float, float) : Java AWT Image object associated with this renderer.

Py5Graphics.background(float, float, float, float) : The , ``background()`` , function sets the color used for the background of the Processing window.


# Py5Graphics_is2_d

Return true if this renderer supports 2D drawing.

Parameters
----------

PARAMTEXT

Notes
-----

Return true if this renderer supports 2D drawing. Defaults to true.


# Py5Graphics_is3_d

Return true if this renderer supports 3D drawing.

Parameters
----------

PARAMTEXT

Notes
-----

Return true if this renderer supports 3D drawing. Defaults to false.


# Py5Graphics_is_gl

Return true if this renderer does rendering through OpenGL.

Parameters
----------

PARAMTEXT

Notes
-----

Return true if this renderer does rendering through OpenGL. Defaults to false.


# Py5Graphics_lerp_color

Calculates a color or colors between two color at a specific increment.

Parameters
----------

PARAMTEXT

Notes
-----

Calculates a color or colors between two color at a specific increment. The ``amt`` parameter is the amount to interpolate between the two values where 0.0 equal to the first point, 0.1 is very near the first point, 0.5 is half-way in between, etc.


See Also
--------

Py5Image.blendColor(int, int, int)

Py5Graphics.color(float, float, float, float) : 

Sketch.lerp(float, float, float) : Calculates a number between two numbers at a specific increment.


# Py5Graphics_light_falloff

Sets the falloff rates for point lights, spot lights, and ambient lights.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the falloff rates for point lights, spot lights, and ambient lights. The parameters are used to determine the falloff with the following equation:

d = distance from light position to vertex position
falloff = 1 / (CONSTANT + d * LINEAR + (d*d) * QUADRATIC)

Like ``fill()`` , it affects only the elements which are created after it in the code. The default value if ``_light_falloff(1.0 0.0 0.0)`` . Thinking about an ambient light with a falloff can be tricky. It is used, for example, if you wanted a region of your scene to be lit ambiently one color and another region to be lit ambiently by another color, you would use an ambient light with location and falloff. You can think of it as a point light that doesn't care which direction a surface is facing.


See Also
--------

Py5Graphics.lights() : Sets the default ambient light, directional light, falloff, and specular values.

Py5Graphics.ambientLight(float, float, float, float, float, float)

Py5Graphics.pointLight(float, float, float, float, float, float)

Py5Graphics.spotLight(float, float, float, float, float, float, float, float, float, float, float)

Py5Graphics.lightSpecular(float, float, float)


# Py5Graphics_light_specular

Sets the specular color for lights.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the specular color for lights. Like ``fill()`` , it affects only the elements which are created after it in the code. Specular refers to light which bounces off a surface in a perferred direction (rather than bouncing in all directions like a diffuse light) and is used for creating highlights. The specular quality of a light interacts with the specular material qualities set through the ``specular()`` and ``shininess()`` functions.


See Also
--------

Py5Graphics.specular(float, float, float) : Sets the specular color of the materials used for shapes drawn to the screen, which sets the color of hightlights.

Py5Graphics.lights() : Sets the default ambient light, directional light, falloff, and specular values.

Py5Graphics.ambientLight(float, float, float, float, float, float)

Py5Graphics.pointLight(float, float, float, float, float, float)

Py5Graphics.spotLight(float, float, float, float, float, float, float, float, float, float, float)


# Py5Graphics_lights

Sets the default ambient light, directional light, falloff, and specular values.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the default ambient light, directional light, falloff, and specular values. The defaults are ambientLight(128, 128, 128) and directionalLight(128, 128, 128, 0, 0, -1), lightFalloff(1, 0, 0), and lightSpecular(0, 0, 0). Lights need to be included in the draw() to remain persistent in a looping program. Placing them in the setup() of a looping program will cause them to only have an effect the first time through the loop.


See Also
--------

Py5Graphics.ambientLight(float, float, float, float, float, float)

Py5Graphics.directionalLight(float, float, float, float, float, float)

Py5Graphics.pointLight(float, float, float, float, float, float)

Py5Graphics.spotLight(float, float, float, float, float, float, float, float, float, float, float)

Py5Graphics.noLights()


# Py5Graphics_line

Draws a line (a direct path between two points) to the screen.

Parameters
----------

PARAMTEXT

Notes
-----

Draws a line (a direct path between two points) to the screen. The version of ``line()`` with four parameters draws the line in 2D.  To color a line, use the ``stroke()`` function. A line cannot be filled, therefore the ``fill()`` function will not affect the color of a line. 2D lines are drawn with a width of one pixel by default, but this can be changed with the ``stroke_weight()`` function. The version with six parameters allows the line to be placed anywhere within XYZ space. Drawing this shape in 3D with the ``z`` parameter requires the P3D parameter in combination with ``size()`` as shown in the above example.


See Also
--------

Py5Graphics.strokeWeight(float)

Py5Graphics.strokeJoin(int)

Py5Graphics.strokeCap(int)

Py5Graphics.beginShape()


# Py5Graphics_load_shader

This is a new reference entry for Processing 2.0.

Parameters
----------

PARAMTEXT

Notes
-----

This is a new reference entry for Processing 2.0. It will be updated shortly.


# Py5Graphics_load_shape



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Sketch.createShape()


# Py5Graphics_matrix_stack_depth

Current model-view matrix transformation of the form m[row][column], which is a "column vector" (as opposed to "row vector") matrix.

Parameters
----------

PARAMTEXT

Notes
-----

Current model-view matrix transformation of the form m[row][column], which is a "column vector" (as opposed to "row vector") matrix.


# Py5Graphics_model_x

Returns the three-dimensional X, Y, Z position in model space.

Parameters
----------

PARAMTEXT

Notes
-----

Returns the three-dimensional X, Y, Z position in model space. This returns the X value for a given coordinate based on the current set of transformations (scale, rotate, translate, etc.) The X value can be used to place an object in space relative to the location of the original point once the transformations are no longer in use.

In the example, the ``model_x()`` , ``model_y()`` , and ``model_z()`` functions record the location of a box in space after being placed using a series of translate and rotate commands. After popMatrix() is called, those transformations no longer apply, but the (x, y, z) coordinate returned by the model functions is used to place another box in the same location.


See Also
--------

Py5Graphics.modelY(float, float, float)

Py5Graphics.modelZ(float, float, float)


# Py5Graphics_model_y

Returns the three-dimensional X, Y, Z position in model space.

Parameters
----------

PARAMTEXT

Notes
-----

Returns the three-dimensional X, Y, Z position in model space. This returns the Y value for a given coordinate based on the current set of transformations (scale, rotate, translate, etc.) The Y value can be used to place an object in space relative to the location of the original point once the transformations are no longer in use.

In the example, the ``model_x()`` , ``model_y()`` , and ``model_z()`` functions record the location of a box in space after being placed using a series of translate and rotate commands. After popMatrix() is called, those transformations no longer apply, but the (x, y, z) coordinate returned by the model functions is used to place another box in the same location.


See Also
--------

Py5Graphics.modelX(float, float, float)

Py5Graphics.modelZ(float, float, float)


# Py5Graphics_model_z

Returns the three-dimensional X, Y, Z position in model space.

Parameters
----------

PARAMTEXT

Notes
-----

Returns the three-dimensional X, Y, Z position in model space. This returns the Z value for a given coordinate based on the current set of transformations (scale, rotate, translate, etc.) The Z value can be used to place an object in space relative to the location of the original point once the transformations are no longer in use.

In the example, the ``model_x()`` , ``model_y()`` , and ``model_z()`` functions record the location of a box in space after being placed using a series of translate and rotate commands. After popMatrix() is called, those transformations no longer apply, but the (x, y, z) coordinate returned by the model functions is used to place another box in the same location.


See Also
--------

Py5Graphics.modelX(float, float, float)

Py5Graphics.modelY(float, float, float)


# Py5Graphics_no_clip

Disables the clipping previously started by the , ``clip()`` , function.

Parameters
----------

PARAMTEXT

Notes
-----

Disables the clipping previously started by the ``clip()`` function.


# Py5Graphics_no_fill

Disables filling geometry.

Parameters
----------

PARAMTEXT

Notes
-----

Disables filling geometry. If both ``no_stroke()`` and ``no_fill()`` are called, nothing will be drawn to the screen.


See Also
--------

Py5Graphics.fill(float, float, float, float) : true if fill() is enabled, (read-only)

Py5Graphics.stroke(int, float) : Sets the color used to draw lines and borders around shapes.

Py5Graphics.noStroke()


# Py5Graphics_no_lights

Disable all lighting.

Parameters
----------

PARAMTEXT

Notes
-----

Disable all lighting. Lighting is turned off by default and enabled with the ``lights()`` function. This function can be used to disable lighting so that 2D geometry (which does not require lighting) can be drawn after a set of lighted 3D geometry.


See Also
--------

Py5Graphics.lights() : Sets the default ambient light, directional light, falloff, and specular values.


# Py5Graphics_no_stroke

Disables drawing the stroke (outline).

Parameters
----------

PARAMTEXT

Notes
-----

Disables drawing the stroke (outline). If both ``no_stroke()`` and ``no_fill()`` are called, nothing will be drawn to the screen.


See Also
--------

Py5Graphics.stroke(int, float) : Sets the color used to draw lines and borders around shapes.

Py5Graphics.fill(float, float, float, float) : true if fill() is enabled, (read-only)

Py5Graphics.noFill()


# Py5Graphics_no_texture

Removes texture image for current shape.

Parameters
----------

PARAMTEXT

Notes
-----

Removes texture image for current shape. Needs to be called between beginShape and endShape


# Py5Graphics_no_tint

Removes the current fill value for displaying images and reverts to displaying images with their original hues.

Parameters
----------

PARAMTEXT

Notes
-----

Removes the current fill value for displaying images and reverts to displaying images with their original hues.


See Also
--------

Py5Graphics.tint(float, float, float, float) : Sets the fill value for displaying images.

Py5Graphics.image(Py5Image, float, float, float, float) : Java AWT Image object associated with this renderer.


# Py5Graphics_normal

Sets the current normal vector.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the current normal vector. This is for drawing three dimensional shapes and surfaces and specifies a vector perpendicular to the surface of the shape which determines how lighting affects it. Processing attempts to automatically assign normals to shapes, but since that's imperfect, this is a better option when you want more control. This function is identical to glNormal3f() in OpenGL.


See Also
--------

Py5Graphics.beginShape(int)

Py5Graphics.endShape(int)

Py5Graphics.lights() : Sets the default ambient light, directional light, falloff, and specular values.


# Py5Graphics_normal_x

Current normal vector.

Parameters
----------

PARAMTEXT

Notes
-----

Current normal vector.


# Py5Graphics_normal_y

Current normal vector.

Parameters
----------

PARAMTEXT

Notes
-----

Current normal vector.


# Py5Graphics_normal_z

Current normal vector.

Parameters
----------

PARAMTEXT

Notes
-----

Current normal vector.


# Py5Graphics_ortho

Sets an orthographic projection and defines a parallel clipping volume.

Parameters
----------

PARAMTEXT

Notes
-----

Sets an orthographic projection and defines a parallel clipping volume. All objects with the same dimension appear the same size, regardless of whether they are near or far from the camera. The parameters to this function specify the clipping volume where left and right are the minimum and maximum x values, top and bottom are the minimum and maximum y values, and near and far are the minimum and maximum z values. If no parameters are given, the default is used: ortho(0, width, 0, height, -10, 10).


# Py5Graphics_path

path to the file being saved for this renderer (if any)

Parameters
----------

PARAMTEXT

Notes
-----

path to the file being saved for this renderer (if any)


# Py5Graphics_perspective

Sets a perspective projection applying foreshortening, making distant objects appear smaller than closer ones.

Parameters
----------

PARAMTEXT

Notes
-----

Sets a perspective projection applying foreshortening, making distant objects appear smaller than closer ones. The parameters define a viewing volume with the shape of truncated pyramid. Objects near to the front of the volume appear their actual size, while farther objects appear smaller. This projection simulates the perspective of the world more accurately than orthographic projection. The version of perspective without parameters sets the default perspective and the version with four parameters allows the programmer to set the area precisely. The default values are: perspective(PI/3.0, width/height, cameraZ/10.0, cameraZ*10.0) where cameraZ is ((height/2.0) / tan(PI*60.0/360.0));


# Py5Graphics_point

Draws a point, a coordinate in space at the dimension of one pixel.

Parameters
----------

PARAMTEXT

Notes
-----

Draws a point, a coordinate in space at the dimension of one pixel. The first parameter is the horizontal value for the point, the second value is the vertical value for the point, and the optional third value is the depth value. Drawing this shape in 3D with the ``z`` parameter requires the P3D parameter in combination with ``size()`` as shown in the above example.


See Also
--------

Py5Graphics.stroke(int) : Sets the color used to draw lines and borders around shapes.


# Py5Graphics_point_light

Adds a point light.

Parameters
----------

PARAMTEXT

Notes
-----

Adds a point light. Lights need to be included in the ``draw()`` to remain persistent in a looping program. Placing them in the ``setup()`` of a looping program will cause them to only have an effect the first time through the loop. The affect of the ``v1`` , ``v2`` , and ``v3`` parameters is determined by the current color mode. The ``x`` , ``y`` , and ``z`` parameters set the position of the light.


See Also
--------

Py5Graphics.lights() : Sets the default ambient light, directional light, falloff, and specular values.

Py5Graphics.directionalLight(float, float, float, float, float, float)

Py5Graphics.ambientLight(float, float, float, float, float, float)

Py5Graphics.spotLight(float, float, float, float, float, float, float, float, float, float, float)


# Py5Graphics_pop

The , ``pop()`` , function restores the previous drawing style settings and transformations after , ``push()`` , has changed them.

Parameters
----------

PARAMTEXT

Notes
-----

The ``pop()`` function restores the previous drawing style settings and transformations after ``push()`` has changed them. Note that these functions are always used together. They allow you to change the style and transformation settings and later return to what you had. When a new state is started with push(), it builds on the current style and transform information.


 ``push()`` stores information related to the current transformation state and style settings controlled by the following functions: ``rotate()`` , ``translate()`` , ``scale()`` , ``fill()`` , ``stroke()`` , ``tint()`` , ``stroke_weight()`` , ``stroke_cap()`` , ``stroke_join()`` , ``image_mode()`` , ``rect_mode()`` , ``ellipse_mode()`` , ``color_mode()`` , ``text_align()`` , ``text_font()`` , ``text_mode()`` , ``text_size()`` , ``text_leading()`` .

The ``push()`` and ``pop()`` functions were added with Processing 3.5. They can be used in place of ``push_matrix()`` , ``pop_matrix()`` , ``push_styles()`` , and ``pop_styles()`` . The difference is that push() and pop() control both the transformations (rotate, scale, translate) and the drawing styles at the same time.


See Also
--------

Py5Graphics.push() : The , ``push()`` , function saves the current drawing style settings and transformations, while , ``pop()`` , restores these settings.


# Py5Graphics_pop_matrix

Pops the current transformation matrix off the matrix stack.

Parameters
----------

PARAMTEXT

Notes
-----

Pops the current transformation matrix off the matrix stack. Understanding pushing and popping requires understanding the concept of a matrix stack. The ``push_matrix()`` function saves the current coordinate system to the stack and ``pop_matrix()`` restores the prior coordinate system. ``push_matrix()`` and ``pop_matrix()`` are used in conjuction with the other transformation functions and may be embedded to control the scope of the transformations.


See Also
--------

Py5Graphics.pushMatrix()


# Py5Graphics_pop_style

The , ``push_style()`` , function saves the current style settings and , ``pop_style()`` , restores the prior settings; these functions are always used together.

Parameters
----------

PARAMTEXT

Notes
-----

The ``push_style()`` function saves the current style settings and ``pop_style()`` restores the prior settings; these functions are always used together. They allow you to change the style settings and later return to what you had. When a new style is started with ``push_style()`` , it builds on the current style information. The ``push_style()`` and ``pop_style()`` functions can be embedded to provide more control (see the second example above for a demonstration.)


See Also
--------

Py5Graphics.pushStyle()


# Py5Graphics_primary_graphics

True if this is the main graphics context for a sketch.

Parameters
----------

PARAMTEXT

Notes
-----

True if this is the main graphics context for a sketch. False for offscreen buffers retrieved via createGraphics().


# Py5Graphics_print_camera

Prints the current camera matrix to the Console (the text window at the bottom of Processing).

Parameters
----------

PARAMTEXT

Notes
-----

Prints the current camera matrix to the Console (the text window at the bottom of Processing).


See Also
--------

Py5Graphics.camera(float, float, float, float, float, float, float, float, float) : Sets the position of the camera through setting the eye position, the center of the scene, and which axis is facing upward.


# Py5Graphics_print_matrix

Prints the current matrix to the Console (the text window at the bottom of Processing).

Parameters
----------

PARAMTEXT

Notes
-----

Prints the current matrix to the Console (the text window at the bottom of Processing).


See Also
--------

Py5Graphics.pushMatrix()

Py5Graphics.popMatrix()

Py5Graphics.resetMatrix()

Py5Graphics.applyMatrix(PMatrix)


# Py5Graphics_print_projection

Prints the current projection matrix to the Console (the text window at the bottom of Processing).

Parameters
----------

PARAMTEXT

Notes
-----

Prints the current projection matrix to the Console (the text window at the bottom of Processing).


See Also
--------

Py5Graphics.camera(float, float, float, float, float, float, float, float, float) : Sets the position of the camera through setting the eye position, the center of the scene, and which axis is facing upward.


# Py5Graphics_push

The , ``push()`` , function saves the current drawing style settings and transformations, while , ``pop()`` , restores these settings.

Parameters
----------

PARAMTEXT

Notes
-----

The ``push()`` function saves the current drawing style settings and transformations, while ``pop()`` restores these settings. Note that these functions are always used together. They allow you to change the style and transformation settings and later return to what you had. When a new state is started with push(), it builds on the current style and transform information.

 ``push()`` stores information related to the current transformation state and style settings controlled by the following functions: ``rotate()`` , ``translate()`` , ``scale()`` , ``fill()`` , ``stroke()`` , ``tint()`` , ``stroke_weight()`` , ``stroke_cap()`` , ``stroke_join()`` , ``image_mode()`` , ``rect_mode()`` , ``ellipse_mode()`` , ``color_mode()`` , ``text_align()`` , ``text_font()`` , ``text_mode()`` , ``text_size()`` , ``text_leading()`` .

The ``push()`` and ``pop()`` functions were added with Processing 3.5. They can be used in place of ``push_matrix()`` , ``pop_matrix()`` , ``push_styles()`` , and ``pop_styles()`` . The difference is that push() and pop() control both the transformations (rotate, scale, translate) and the drawing styles at the same time.


See Also
--------

Py5Graphics.pop() : The , ``pop()`` , function restores the previous drawing style settings and transformations after , ``push()`` , has changed them.


# Py5Graphics_push_matrix

Pushes the current transformation matrix onto the matrix stack.

Parameters
----------

PARAMTEXT

Notes
-----

Pushes the current transformation matrix onto the matrix stack. Understanding ``push_matrix()`` and ``pop_matrix()`` requires understanding the concept of a matrix stack. The ``push_matrix()`` function saves the current coordinate system to the stack and ``pop_matrix()`` restores the prior coordinate system. ``push_matrix()`` and ``pop_matrix()`` are used in conjuction with the other transformation functions and may be embedded to control the scope of the transformations.


See Also
--------

Py5Graphics.popMatrix()

Py5Graphics.translate(float, float, float) : Specifies an amount to displace objects within the display window.

Py5Graphics.scale(float) : Increases or decreases the size of a shape by expanding and contracting vertices.

Py5Graphics.rotate(float) : Rotates a shape the amount specified by the , ``angle`` , parameter.

Py5Graphics.rotateX(float)

Py5Graphics.rotateY(float)

Py5Graphics.rotateZ(float)


# Py5Graphics_push_style

The , ``push_style()`` , function saves the current style settings and , ``pop_style()`` , restores the prior settings.

Parameters
----------

PARAMTEXT

Notes
-----

The ``push_style()`` function saves the current style settings and ``pop_style()`` restores the prior settings. Note that these functions are always used together. They allow you to change the style settings and later return to what you had. When a new style is started with ``push_style()`` , it builds on the current style information. The ``push_style()`` and ``pop_style()`` functions can be embedded to provide more control (see the second example above for a demonstration.)

The style information controlled by the following functions are included in the style: fill(), stroke(), tint(), strokeWeight(), strokeCap(), strokeJoin(), imageMode(), rectMode(), ellipseMode(), shapeMode(), colorMode(), textAlign(), textFont(), textMode(), textSize(), textLeading(), emissive(), specular(), shininess(), ambient()


See Also
--------

Py5Graphics.popStyle()


# Py5Graphics_quad

A quad is a quadrilateral, a four sided polygon.

Parameters
----------

PARAMTEXT

Notes
-----

A quad is a quadrilateral, a four sided polygon. It is similar to a rectangle, but the angles between its edges are not constrained to ninety degrees. The first pair of parameters (x1,y1) sets the first vertex and the subsequent pairs should proceed clockwise or counter-clockwise around the defined shape.


# Py5Graphics_quadratic_vertex



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Py5Graphics.curveVertex(float, float, float)

Py5Graphics.vertex(float, float, float, float, float) : Used by renderer subclasses or Py5Shape to efficiently pass in already formatted vertex information.

Py5Graphics.bezierVertex(float, float, float, float, float, float)

Py5Graphics.bezier(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a Bezier curve on the screen.


# Py5Graphics_reapply_settings

Re-apply current settings.

Parameters
----------

PARAMTEXT

Notes
-----

Re-apply current settings. Some methods, such as textFont(), require that their methods be called (rather than simply setting the textFont variable) because they affect the graphics context, or they require parameters from the context (e.g. getting native fonts for text). This will only be called from an allocate(), which is only called from size(), which is safely called from inside beginDraw(). And it cannot be called before defaultSettings(), so we should be safe.


# Py5Graphics_rect

Draws a rectangle to the screen.

Parameters
----------

PARAMTEXT

Notes
-----

Draws a rectangle to the screen. A rectangle is a four-sided shape with every angle at ninety degrees. By default, the first two parameters set the location of the upper-left corner, the third sets the width, and the fourth sets the height. These parameters may be changed with the ``rect_mode()`` function.


See Also
--------

Py5Graphics.rectMode(int)

Py5Graphics.quad(float, float, float, float, float, float, float, float) : A quad is a quadrilateral, a four sided polygon.


# Py5Graphics_rect_mode

Modifies the location from which rectangles draw.

Parameters
----------

PARAMTEXT

Notes
-----

Modifies the location from which rectangles draw. The default mode is ``rect_mode(corner)`` , which specifies the location to be the upper left corner of the shape and uses the third and fourth parameters of ``rect()`` to specify the width and height. The syntax ``rect_mode(corners)`` uses the first and second parameters of ``rect()`` to set the location of one corner and uses the third and fourth parameters to set the opposite corner. The syntax ``rect_mode(center)`` draws the image from its center point and uses the third and forth parameters of ``rect()`` to specify the image's width and height. The syntax ``rect_mode(radius)`` draws the image from its center point and uses the third and forth parameters of ``rect()`` to specify half of the image's width and height. The parameter must be written in ALL CAPS because Processing is a case sensitive language. Note: In version 125, the mode named CENTER_RADIUS was shortened to RADIUS.


See Also
--------

Py5Graphics.rect(float, float, float, float) : Draws a rectangle to the screen.


# Py5Graphics_red

Extracts the red value from a color, scaled to match current , ``color_mode()`` ,.

Parameters
----------

PARAMTEXT

Notes
-----

Extracts the red value from a color, scaled to match current ``color_mode()`` . This value is always returned as a  float so be careful not to assign it to an int value.

The red() function is easy to use and undestand, but is slower than another technique. To achieve the same results when working in ``color_mode(rgb 255)`` , but with greater speed, use the>>(right shift) operator with a bit mask. For example, the following two lines of code are equivalent:
<pre>float r1 = red(myColor);
float r2 = myColor>>16&0xFF;</pre>


See Also
--------

Py5Graphics.green(int) : Extracts the green value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.blue(int) : Extracts the blue value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.alpha(int) : Extracts the alpha value from a color.

Py5Graphics.hue(int) : Extracts the hue value from a color.

Py5Graphics.saturation(int) : Extracts the saturation value from a color.

Py5Graphics.brightness(int) : Extracts the brightness value from a color.


# Py5Graphics_remove_cache

Remove information associated with this renderer from the cache, if any.

Parameters
----------

PARAMTEXT

Notes
-----

Remove information associated with this renderer from the cache, if any.


# Py5Graphics_reset_matrix

Replaces the current matrix with the identity matrix.

Parameters
----------

PARAMTEXT

Notes
-----

Replaces the current matrix with the identity matrix. The equivalent function in OpenGL is glLoadIdentity().


See Also
--------

Py5Graphics.pushMatrix()

Py5Graphics.popMatrix()

Py5Graphics.applyMatrix(PMatrix)

Py5Graphics.printMatrix()


# Py5Graphics_reset_shader

This is a new reference entry for Processing 2.0.

Parameters
----------

PARAMTEXT

Notes
-----

This is a new reference entry for Processing 2.0. It will be updated shortly.


# Py5Graphics_rotate

Rotates a shape the amount specified by the , ``angle`` , parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Rotates a shape the amount specified by the ``angle`` parameter. Angles should be specified in radians (values from 0 to TWO_PI) or converted to radians with the ``radians()`` function.

Objects are always rotated around their relative position to the origin and positive numbers rotate objects in a clockwise direction. Transformations apply to everything that happens after and subsequent calls to the function accumulates the effect. For example, calling ``rotate(half_pi)`` and then ``rotate(half_pi)`` is the same as ``rotate(pi)`` . All tranformations are reset when ``draw()`` begins again.

Technically, ``rotate()`` multiplies the current transformation matrix by a rotation matrix. This function can be further controlled by the ``push_matrix()`` and ``pop_matrix()`` .


See Also
--------

Py5Graphics.popMatrix()

Py5Graphics.pushMatrix()

Py5Graphics.rotateX(float)

Py5Graphics.rotateY(float)

Py5Graphics.rotateZ(float)

Py5Graphics.scale(float, float, float) : Increases or decreases the size of a shape by expanding and contracting vertices.

Sketch.radians(float) : Converts a degree measurement to its corresponding value in radians.


# Py5Graphics_rotate_x

Rotates a shape around the x-axis the amount specified by the , ``angle`` , parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Rotates a shape around the x-axis the amount specified by the ``angle`` parameter. Angles should be specified in radians (values from 0 to PI*2) or converted to radians with the ``radians()`` function. Objects are always rotated around their relative position to the origin and positive numbers rotate objects in a counterclockwise direction. Transformations apply to everything that happens after and subsequent calls to the function accumulates the effect. For example, calling ``rotate_x(pi/2)`` and then ``rotate_x(pi/2)`` is the same as ``rotate_x(pi)`` . If ``rotate_x()`` is called within the ``draw()`` , the transformation is reset when the loop begins again. This function requires using P3D as a third parameter to ``size()`` as shown in the example above.


See Also
--------

Py5Graphics.popMatrix()

Py5Graphics.pushMatrix()

Py5Graphics.rotate(float) : Rotates a shape the amount specified by the , ``angle`` , parameter.

Py5Graphics.rotateY(float)

Py5Graphics.rotateZ(float)

Py5Graphics.scale(float, float, float) : Increases or decreases the size of a shape by expanding and contracting vertices.

Py5Graphics.translate(float, float, float) : Specifies an amount to displace objects within the display window.


# Py5Graphics_rotate_y

Rotates a shape around the y-axis the amount specified by the , ``angle`` , parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Rotates a shape around the y-axis the amount specified by the ``angle`` parameter. Angles should be specified in radians (values from 0 to PI*2) or converted to radians with the ``radians()`` function. Objects are always rotated around their relative position to the origin and positive numbers rotate objects in a counterclockwise direction. Transformations apply to everything that happens after and subsequent calls to the function accumulates the effect. For example, calling ``rotate_y(pi/2)`` and then ``rotate_y(pi/2)`` is the same as ``rotate_y(pi)`` . If ``rotate_y()`` is called within the ``draw()`` , the transformation is reset when the loop begins again. This function requires using P3D as a third parameter to ``size()`` as shown in the examples above.


See Also
--------

Py5Graphics.popMatrix()

Py5Graphics.pushMatrix()

Py5Graphics.rotate(float) : Rotates a shape the amount specified by the , ``angle`` , parameter.

Py5Graphics.rotateX(float)

Py5Graphics.rotateZ(float)

Py5Graphics.scale(float, float, float) : Increases or decreases the size of a shape by expanding and contracting vertices.

Py5Graphics.translate(float, float, float) : Specifies an amount to displace objects within the display window.


# Py5Graphics_rotate_z

Rotates a shape around the z-axis the amount specified by the , ``angle`` , parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Rotates a shape around the z-axis the amount specified by the ``angle`` parameter. Angles should be specified in radians (values from 0 to PI*2) or converted to radians with the ``radians()`` function. Objects are always rotated around their relative position to the origin and positive numbers rotate objects in a counterclockwise direction. Transformations apply to everything that happens after and subsequent calls to the function accumulates the effect. For example, calling ``rotate_z(pi/2)`` and then ``rotate_z(pi/2)`` is the same as ``rotate_z(pi)`` . If ``rotate_z()`` is called within the ``draw()`` , the transformation is reset when the loop begins again. This function requires using P3D as a third parameter to ``size()`` as shown in the examples above.


See Also
--------

Py5Graphics.popMatrix()

Py5Graphics.pushMatrix()

Py5Graphics.rotate(float) : Rotates a shape the amount specified by the , ``angle`` , parameter.

Py5Graphics.rotateX(float)

Py5Graphics.rotateY(float)

Py5Graphics.scale(float, float, float) : Increases or decreases the size of a shape by expanding and contracting vertices.

Py5Graphics.translate(float, float, float) : Specifies an amount to displace objects within the display window.


# Py5Graphics_saturation

Extracts the saturation value from a color.

Parameters
----------

PARAMTEXT

Notes
-----

Extracts the saturation value from a color.


See Also
--------

Py5Graphics.red(int) : Extracts the red value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.green(int) : Extracts the green value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.blue(int) : Extracts the blue value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.alpha(int) : Extracts the alpha value from a color.

Py5Graphics.hue(int) : Extracts the hue value from a color.

Py5Graphics.brightness(int) : Extracts the brightness value from a color.


# Py5Graphics_scale

Increases or decreases the size of a shape by expanding and contracting vertices.

Parameters
----------

PARAMTEXT

Notes
-----

Increases or decreases the size of a shape by expanding and contracting vertices. Objects always scale from their relative origin to the coordinate system. Scale values are specified as decimal percentages. For example, the function call ``scale(2.0)`` increases the dimension of a shape by 200%. Transformations apply to everything that happens after and subsequent calls to the function multiply the effect. For example, calling ``scale(2.0)`` and then ``scale(1.5)`` is the same as ``scale(3.0)`` . If ``scale()`` is called within ``draw()`` , the transformation is reset when the loop begins again. Using this fuction with the ``z`` parameter requires using P3D as a parameter for ``size()`` as shown in the example above. This function can be further controlled by ``push_matrix()`` and ``pop_matrix()`` .


See Also
--------

Py5Graphics.pushMatrix()

Py5Graphics.popMatrix()

Py5Graphics.translate(float, float, float) : Specifies an amount to displace objects within the display window.

Py5Graphics.rotate(float) : Rotates a shape the amount specified by the , ``angle`` , parameter.

Py5Graphics.rotateX(float)

Py5Graphics.rotateY(float)

Py5Graphics.rotateZ(float)


# Py5Graphics_screen_x

Takes a three-dimensional X, Y, Z position and returns the X value for where it will appear on a (two-dimensional) screen.

Parameters
----------

PARAMTEXT

Notes
-----

Takes a three-dimensional X, Y, Z position and returns the X value for where it will appear on a (two-dimensional) screen.


See Also
--------

Py5Graphics.screenY(float, float, float)

Py5Graphics.screenZ(float, float, float)


# Py5Graphics_screen_y

Takes a three-dimensional X, Y, Z position and returns the Y value for where it will appear on a (two-dimensional) screen.

Parameters
----------

PARAMTEXT

Notes
-----

Takes a three-dimensional X, Y, Z position and returns the Y value for where it will appear on a (two-dimensional) screen.


See Also
--------

Py5Graphics.screenX(float, float, float)

Py5Graphics.screenZ(float, float, float)


# Py5Graphics_screen_z

Takes a three-dimensional X, Y, Z position and returns the Z value for where it will appear on a (two-dimensional) screen.

Parameters
----------

PARAMTEXT

Notes
-----

Takes a three-dimensional X, Y, Z position and returns the Z value for where it will appear on a (two-dimensional) screen.


See Also
--------

Py5Graphics.screenX(float, float, float)

Py5Graphics.screenY(float, float, float)


# Py5Graphics_set_cache

Store data of some kind for the renderer that requires extra metadata of some kind.

Parameters
----------

PARAMTEXT

Notes
-----

Store data of some kind for the renderer that requires extra metadata of some kind. Usually this is a renderer-specific representation of the image data, for instance a BufferedImage with tint() settings applied for Py5GraphicsJava2D, or resized image data and OpenGL texture indices for Py5GraphicsOpenGL.


# Py5Graphics_set_matrix

Set the current transformation to the contents of the specified source.

Parameters
----------

PARAMTEXT

Notes
-----

Set the current transformation to the contents of the specified source.


# Py5Graphics_set_primary

Set (or unset) this as the main drawing surface.

Parameters
----------

PARAMTEXT

Notes
-----

Set (or unset) this as the main drawing surface. Meaning that it can safely be set to opaque (and given a default gray background), or anything else that goes along with that.


# Py5Graphics_set_size

The final step in setting up a renderer, set its size of this renderer.

Parameters
----------

PARAMTEXT

Notes
-----

The final step in setting up a renderer, set its size of this renderer. This was formerly handled by the constructor, but instead it's been broken out so that setParent/setPrimary/setPath can be handled differently. Important: this is ignored by the Methods task because otherwise it will override setSize() in Sketch/Applet/Component, which will 1) not call super.setSize(), and 2) will cause the renderer to be resized from the event thread (EDT), causing a nasty crash as it collides with the animation thread.


# Py5Graphics_shader

This is a new reference entry for Processing 2.0.

Parameters
----------

PARAMTEXT

Notes
-----

This is a new reference entry for Processing 2.0. It will be updated shortly.


# Py5Graphics_shape

Type of shape passed to beginShape(), zero if no shape is currently being drawn.

Parameters
----------

PARAMTEXT

Notes
-----

Displays shapes to the screen. The shapes must be in the sketch's "data" directory to load correctly. Select "Add file..." from the "Sketch" menu to add the shape. Processing currently works with SVG shapes only. The ``sh`` parameter specifies the shape to display and the ``x`` and ``y`` parameters define the location of the shape from its upper-left corner. The shape is displayed at its original size unless the ``width`` and ``height`` parameters specify a different size. The ``shape_mode()`` function changes the way the parameters work. A call to ``shape_mode(corners)`` , for example, will change the width and height parameters to define the x and y values of the opposite corner of the shape.

Note complex shapes may draw awkwardly with P3D. This renderer does not yet support shapes that have holes or complicated breaks.


See Also
--------

Sketch.loadShape(String)

Py5Graphics.shapeMode(int) Convenience method to draw at a particular location.


# Py5Graphics_shape_mode

Modifies the location from which shapes draw.

Parameters
----------

PARAMTEXT

Notes
-----

Modifies the location from which shapes draw. The default mode is ``shape_mode(corner)`` , which specifies the location to be the upper left corner of the shape and uses the third and fourth parameters of ``shape()`` to specify the width and height. The syntax ``shape_mode(corners)`` uses the first and second parameters of ``shape()`` to set the location of one corner and uses the third and fourth parameters to set the opposite corner. The syntax ``shape_mode(center)`` draws the shape from its center point and uses the third and forth parameters of ``shape()`` to specify the width and height. The parameter must be written in "ALL CAPS" because Processing is a case sensitive language.


See Also
--------

Py5Graphics.shape(Py5Shape) : Type of shape passed to beginShape(), zero if no shape is currently being drawn.

Py5Graphics.rectMode(int)


# Py5Graphics_shear_x

Shears a shape around the x-axis the amount specified by the , ``angle`` , parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Shears a shape around the x-axis the amount specified by the ``angle`` parameter. Angles should be specified in radians (values from 0 to PI*2) or converted to radians with the ``radians()`` function. Objects are always sheared around their relative position to the origin and positive numbers shear objects in a clockwise direction. Transformations apply to everything that happens after and subsequent calls to the function accumulates the effect. For example, calling ``shear_x(pi/2)`` and then ``shear_x(pi/2)`` is the same as ``shear_x(pi)`` . If ``shear_x()`` is called within the ``draw()`` , the transformation is reset when the loop begins again.

Technically, ``shear_x()`` multiplies the current transformation matrix by a rotation matrix. This function can be further controlled by the ``push_matrix()`` and ``pop_matrix()`` functions.


See Also
--------

Py5Graphics.popMatrix()

Py5Graphics.pushMatrix()

Py5Graphics.shearY(float)

Py5Graphics.scale(float, float, float) : Increases or decreases the size of a shape by expanding and contracting vertices.

Py5Graphics.translate(float, float, float) : Specifies an amount to displace objects within the display window.

Sketch.radians(float) : Converts a degree measurement to its corresponding value in radians.


# Py5Graphics_shear_y

Shears a shape around the y-axis the amount specified by the , ``angle`` , parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Shears a shape around the y-axis the amount specified by the ``angle`` parameter. Angles should be specified in radians (values from 0 to PI*2) or converted to radians with the ``radians()`` function. Objects are always sheared around their relative position to the origin and positive numbers shear objects in a clockwise direction. Transformations apply to everything that happens after and subsequent calls to the function accumulates the effect. For example, calling ``shear_y(pi/2)`` and then ``shear_y(pi/2)`` is the same as ``shear_y(pi)`` . If ``shear_y()`` is called within the ``draw()`` , the transformation is reset when the loop begins again.

Technically, ``shear_y()`` multiplies the current transformation matrix by a rotation matrix. This function can be further controlled by the ``push_matrix()`` and ``pop_matrix()`` functions.


See Also
--------

Py5Graphics.popMatrix()

Py5Graphics.pushMatrix()

Py5Graphics.shearX(float)

Py5Graphics.scale(float, float, float) : Increases or decreases the size of a shape by expanding and contracting vertices.

Py5Graphics.translate(float, float, float) : Specifies an amount to displace objects within the display window.

Sketch.radians(float) : Converts a degree measurement to its corresponding value in radians.


# Py5Graphics_shininess

Sets the amount of gloss in the surface of shapes.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the amount of gloss in the surface of shapes. Used in combination with ``ambient()`` , ``specular()`` , and ``emissive()`` in setting the material properties of shapes.


See Also
--------

Py5Graphics.emissive(float, float, float) : Sets the emissive color of the material used for drawing shapes drawn to the screen.

Py5Graphics.ambient(float, float, float) : Sets the ambient reflectance for shapes drawn to the screen.

Py5Graphics.specular(float, float, float) : Sets the specular color of the materials used for shapes drawn to the screen, which sets the color of hightlights.


# Py5Graphics_show_depth_warning

Display a warning that the specified method is only available with 3D.

Parameters
----------

PARAMTEXT

Notes
-----

Display a warning that the specified method is only available with 3D.


# Py5Graphics_show_depth_warning_xyz

Display a warning that the specified method that takes x, y, z parameters can only be used with x and y parameters in this renderer.

Parameters
----------

PARAMTEXT

Notes
-----

Display a warning that the specified method that takes x, y, z parameters can only be used with x and y parameters in this renderer.


# Py5Graphics_show_exception

Show an renderer-related exception that halts the program.

Parameters
----------

PARAMTEXT

Notes
-----

Show an renderer-related exception that halts the program. Currently just wraps the message as a RuntimeException and throws it, but might do something more specific might be used in the future.


# Py5Graphics_show_method_warning

Display a warning that the specified method is simply unavailable.

Parameters
----------

PARAMTEXT

Notes
-----

Display a warning that the specified method is simply unavailable.


# Py5Graphics_show_missing_warning

Display a warning that the specified method is not implemented, meaning that it could be either a completely missing function, although other variations of it may still work properly.

Parameters
----------

PARAMTEXT

Notes
-----

Display a warning that the specified method is not implemented, meaning that it could be either a completely missing function, although other variations of it may still work properly.


# Py5Graphics_show_variation_warning

Error that a particular variation of a method is unavailable (even though other variations are).

Parameters
----------

PARAMTEXT

Notes
-----

Error that a particular variation of a method is unavailable (even though other variations are). For instance, if vertex(x, y, u, v) is not available, but vertex(x, y) is just fine.


# Py5Graphics_show_warning

Show a renderer error, and keep track of it so that it's only shown once.

Parameters
----------

PARAMTEXT

Notes
-----

Show a renderer error, and keep track of it so that it's only shown once.


# Py5Graphics_specular

Sets the specular color of the materials used for shapes drawn to the screen, which sets the color of hightlights.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the specular color of the materials used for shapes drawn to the screen, which sets the color of hightlights. Specular refers to light which bounces off a surface in a perferred direction (rather than bouncing in all directions like a diffuse light). Used in combination with ``emissive()`` , ``ambient()`` , and ``shininess()`` in setting the material properties of shapes.


See Also
--------

Py5Graphics.lightSpecular(float, float, float)

Py5Graphics.ambient(float, float, float) : Sets the ambient reflectance for shapes drawn to the screen.

Py5Graphics.emissive(float, float, float) : Sets the emissive color of the material used for drawing shapes drawn to the screen.

Py5Graphics.shininess(float) : Sets the amount of gloss in the surface of shapes.


# Py5Graphics_sphere

A sphere is a hollow ball made from tessellated triangles.

Parameters
----------

PARAMTEXT

Notes
-----

A sphere is a hollow ball made from tessellated triangles.

Advanced
--------



Implementation notes:

cache all the points of the sphere in a static array top and bottom are just a bunch of triangles that land in the center point

sphere is a series of concentric circles who radii vary along the shape, based on, er.. cos or something

``
[toxi 031031] new sphere code. removed all multiplies with radius as scale() will take care of that anyway [toxi 031223] updated sphere code (removed modulos) and introduced sphere_at(xyzr) to avoid additional translate()'s on the user/sketch side [davbol 080801] now using separate sphere_detail_u/v
``


See Also
--------

Py5Graphics.sphereDetail(int)


# Py5Graphics_sphere_detail

Controls the detail used to render a sphere by adjusting the number of vertices of the sphere mesh.

Parameters
----------

PARAMTEXT

Notes
-----

Controls the detail used to render a sphere by adjusting the number of vertices of the sphere mesh. The default resolution is 30, which creates a fairly detailed sphere definition with vertices every 360/30 = 12 degrees. If you're going to render a great number of spheres per frame, it is advised to reduce the level of detail using this function. The setting stays active until ``sphere_detail()`` is called again with a new parameter and so should<i>not</i>be called prior to every ``sphere()`` statement, unless you wish to render spheres with different settings, e.g. using less detail for smaller spheres or ones further away from the camera. To control the detail of the horizontal and vertical resolution independently, use the version of the functions with two parameters.

Advanced
--------

Code for sphereDetail() submitted by toxi [031031]. Code for enhanced u/v version from davbol [080801].


See Also
--------

Py5Graphics.sphere(float) : A sphere is a hollow ball made from tessellated triangles.


# Py5Graphics_spline_forward

Setup forward-differencing matrix to be used for speedy curve rendering.

Parameters
----------

PARAMTEXT

Notes
-----

Setup forward-differencing matrix to be used for speedy curve rendering. It's based on using a specific number of curve segments and just doing incremental adds for each vertex of the segment, rather than running the mathematically expensive cubic equation.


# Py5Graphics_spot_light

Adds a spot light.

Parameters
----------

PARAMTEXT

Notes
-----

Adds a spot light. Lights need to be included in the ``draw()`` to remain persistent in a looping program. Placing them in the ``setup()`` of a looping program will cause them to only have an effect the first time through the loop. The affect of the ``v1`` , ``v2`` , and ``v3`` parameters is determined by the current color mode. The ``x`` , ``y`` , and ``z`` parameters specify the position of the light and ``nx`` , ``ny`` , ``nz`` specify the direction or light. The ``angle`` parameter affects angle of the spotlight cone.


See Also
--------

Py5Graphics.lights() : Sets the default ambient light, directional light, falloff, and specular values.

Py5Graphics.directionalLight(float, float, float, float, float, float)

Py5Graphics.pointLight(float, float, float, float, float, float)

Py5Graphics.ambientLight(float, float, float, float, float, float)


# Py5Graphics_square

Draws a square to the screen.

Parameters
----------

PARAMTEXT

Notes
-----

Draws a square to the screen. A square is a four-sided shape with every angle at ninety degrees and each side is the same length. By default, the first two parameters set the location of the upper-left corner, the third sets the width and height. The way these parameters are interpreted, however, may be changed with the ``rect_mode()`` function.


See Also
--------

Py5Graphics.rect(float, float, float, float) : Draws a rectangle to the screen.

Py5Graphics.rectMode(int)


# Py5Graphics_sr

stroke argb values

Parameters
----------

PARAMTEXT

Notes
-----

stroke argb values


# Py5Graphics_stroke

Sets the color used to draw lines and borders around shapes.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the color used to draw lines and borders around shapes. This color is either specified in terms of the RGB or HSB color depending on the current ``color_mode()`` (the default color space is RGB, with each value in the range from 0 to 255).

When using hexadecimal notation to specify a color, use "#" or "0x" before the values (e.g. #CCFFAA, 0xFFCCFFAA). The # syntax uses six digits to specify a color (the way colors are specified in HTML and CSS). When using the hexadecimal notation starting with "0x", the hexadecimal value must be specified with eight characters; the first two characters define the alpha component and the remainder the red, green, and blue components.

The value for the parameter "gray" must be less than or equal to the current maximum value as specified by ``color_mode()`` . The default maximum value is 255.


See Also
--------

Py5Graphics.noStroke()

Py5Graphics.strokeWeight(float)

Py5Graphics.strokeJoin(int)

Py5Graphics.strokeCap(int)

Py5Graphics.fill(int, float) : true if fill() is enabled, (read-only)

Py5Graphics.noFill()

Py5Graphics.tint(int, float) : Sets the fill value for displaying images.

Py5Graphics.background(float, float, float, float) : The , ``background()`` , function sets the color used for the background of the Processing window.

Py5Graphics.colorMode(int, float, float, float, float)


# Py5Graphics_stroke_cap

Sets the style for rendering line endings.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the style for rendering line endings. These ends are either squared, extended, or rounded and specified with the corresponding parameters SQUARE, PROJECT, and ROUND. The default cap is ROUND.

This function is not available with the P3D renderer (<a href="http://code.google.com/p/processing/issues/detail?id=123">see Issue 123</a>). More information about the renderers can be found in the ``size()`` reference.


See Also
--------

Py5Graphics.stroke(int, float) : Sets the color used to draw lines and borders around shapes.

Py5Graphics.strokeWeight(float)

Py5Graphics.strokeJoin(int)

Sketch.size(int, int, String, String) : Defines the dimension of the display window in units of pixels.


# Py5Graphics_stroke_color

stroke that was last set (read-only)

Parameters
----------

PARAMTEXT

Notes
-----

stroke that was last set (read-only)


# Py5Graphics_stroke_join

Sets the style of the joints which connect line segments.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the style of the joints which connect line segments. These joints are either mitered, beveled, or rounded and specified with the corresponding parameters MITER, BEVEL, and ROUND. The default joint is MITER.

This function is not available with the P3D renderer, (<a href="http://code.google.com/p/processing/issues/detail?id=123">see Issue 123</a>). More information about the renderers can be found in the ``size()`` reference.


See Also
--------

Py5Graphics.stroke(int, float) : Sets the color used to draw lines and borders around shapes.

Py5Graphics.strokeWeight(float)

Py5Graphics.strokeCap(int)


# Py5Graphics_stroke_weight

Sets the width of the stroke used for lines, points, and the border around shapes.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the width of the stroke used for lines, points, and the border around shapes. All widths are set in units of pixels.

When drawing with P3D, series of connected lines (such as the stroke around a polygon, triangle, or ellipse) produce unattractive results when a thick stroke weight is set (<a href="http://code.google.com/p/processing/issues/detail?id=123">see Issue 123</a>). With P3D, the minimum and maximum values for ``stroke_weight()`` are controlled by the graphics card and the operating system's OpenGL implementation. For instance, the thickness may not go higher than 10 pixels.


See Also
--------

Py5Graphics.stroke(int, float) : Sets the color used to draw lines and borders around shapes.

Py5Graphics.strokeJoin(int)

Py5Graphics.strokeCap(int)


# Py5Graphics_surface

Surface object that we're talking to

Parameters
----------

PARAMTEXT

Notes
-----

Surface object that we're talking to


# Py5Graphics_sw

stroke weight

Parameters
----------

PARAMTEXT

Notes
-----

stroke weight


# Py5Graphics_text

This does a basic number formatting, to avoid the generally ugly appearance of printing floats.

Parameters
----------

PARAMTEXT

Notes
-----

Draws text to the screen. Displays the information specified in the ``data`` or ``stringdata`` parameters on the screen in the position specified by the ``x`` and ``y`` parameters and the optional ``z`` parameter. A default font will be used unless a font is set with the ``text_font()`` function. Change the color of the text with the ``fill()`` function. The text displays in relation to the ``text_align()`` function, which gives the option to draw to the left, right, and center of the coordinates.

The ``x2`` and ``y2`` parameters define a rectangular area to display within and may only be used with string data. For text drawn inside a rectangle, the coordinates are interpreted based on the current ``rect_mode()`` setting.


See Also
--------

Py5Graphics.textAlign(int, int)

Py5Graphics.textFont(Py5Font)

Py5Graphics.textMode(int)

Py5Graphics.textSize(float)

Py5Graphics.textLeading(float)

Py5Graphics.textWidth(String)

Py5Graphics.textAscent()

Py5Graphics.textDescent()

Py5Graphics.rectMode(int)

Py5Graphics.fill(int, float) : true if fill() is enabled, (read-only)


# Py5Graphics_text_align

Sets the current alignment for drawing text.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the current alignment for drawing text. The parameters LEFT, CENTER, and RIGHT set the display characteristics of the letters in relation to the values for the ``x`` and ``y`` parameters of the ``text()`` function.

In Processing 0125 and later, an optional second parameter can be used to vertically align the text. BASELINE is the default, and the vertical alignment will be reset to BASELINE if the second parameter is not used. The TOP and CENTER parameters are straightforward. The BOTTOM parameter offsets the line based on the current ``text_descent()`` . For multiple lines, the final line will be aligned to the bottom, with the previous lines appearing above it.

When using ``text()`` with width and height parameters, BASELINE is ignored, and treated as TOP. (Otherwise, text would by default draw outside the box, since BASELINE is the default setting. BASELINE is not a useful drawing mode for text drawn in a rectangle.)

The vertical alignment is based on the value of ``text_ascent()`` , which many fonts do not specify correctly. It may be necessary to use a hack and offset by a few pixels by hand so that the offset looks correct. To do this as less of a hack, use some percentage of ``text_ascent()`` or ``text_descent()`` so that the hack works even if you change the size of the font.


See Also
--------

Sketch.loadFont(String)

Py5Graphics.text(String, float, float) : This does a basic number formatting, to avoid the generally ugly appearance of printing floats.

Py5Graphics.textSize(float)

Py5Graphics.textAscent()

Py5Graphics.textDescent()


# Py5Graphics_text_align_y

The current vertical text alignment (read-only)

Parameters
----------

PARAMTEXT

Notes
-----

The current vertical text alignment (read-only)


# Py5Graphics_text_ascent

Returns ascent of the current font at its current size.

Parameters
----------

PARAMTEXT

Notes
-----

Returns ascent of the current font at its current size. This information is useful for determining the height of the font above the baseline. For example, adding the ``text_ascent()`` and ``text_descent()`` values will give you the total height of the line.


See Also
--------

Py5Graphics.textDescent()


# Py5Graphics_text_buffer

Internal buffer used by the text() functions because the String object is slow

Parameters
----------

PARAMTEXT

Notes
-----

Internal buffer used by the text() functions because the String object is slow


# Py5Graphics_text_descent

Returns descent of the current font at its current size.

Parameters
----------

PARAMTEXT

Notes
-----

Returns descent of the current font at its current size. This information is useful for determining the height of the font below the baseline. For example, adding the ``text_ascent()`` and ``text_descent()`` values will give you the total height of the line.


See Also
--------

Py5Graphics.textAscent()


# Py5Graphics_text_font

Sets the current font that will be drawn with the , ``text()`` , function.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the current font that will be drawn with the ``text()`` function. Fonts must be loaded with ``load_font()`` before it can be used. This font will be used in all subsequent calls to the ``text()`` function. If no ``size`` parameter is input, the font will appear at its original size (the size it was created at with the "Create Font..." tool) until it is changed with ``text_size()`` .

Because fonts are usually bitmaped, you should create fonts at the sizes that will be used most commonly. Using ``text_font()`` without the size parameter will result in the cleanest-looking text.

With the default (JAVA2D) and PDF renderers, it's also possible to enable the use of native fonts via the command ``hint(enable_native_fonts)`` . This will produce vector text in JAVA2D sketches and PDF output in cases where the vector data is available: when the font is still installed, or the font is created via the ``create_font()`` function (rather than the Create Font tool).


See Also
--------

Sketch.createFont(String, float, boolean)

Sketch.loadFont(String)

Py5Graphics.text(String, float, float) : This does a basic number formatting, to avoid the generally ugly appearance of printing floats.

Py5Graphics.textSize(float)


# Py5Graphics_text_font_impl

Called from textFont.

Parameters
----------

PARAMTEXT

Notes
-----

Called from textFont. Check the validity of args and print possible errors to the user before calling this. Subclasses will want to override this one.


# Py5Graphics_text_leading

Sets the spacing between lines of text in units of pixels.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the spacing between lines of text in units of pixels. This setting will be used in all subsequent calls to the ``text()`` function.


See Also
--------

Sketch.loadFont(String)

Py5Font.Py5Font

Py5Graphics.text(String, float, float) : This does a basic number formatting, to avoid the generally ugly appearance of printing floats.

Py5Graphics.textFont(Py5Font)

Py5Graphics.textSize(float)


# Py5Graphics_text_line_align_impl

Handles placement of a text line, then calls textLineImpl to actually render at the specific point.

Parameters
----------

PARAMTEXT

Notes
-----

Handles placement of a text line, then calls textLineImpl to actually render at the specific point.


# Py5Graphics_text_line_impl

Implementation of actual drawing for a line of text.

Parameters
----------

PARAMTEXT

Notes
-----

Implementation of actual drawing for a line of text.


# Py5Graphics_text_mode

Sets the way text draws to the screen.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the way text draws to the screen. In the default configuration, the ``model`` mode, it's possible to rotate, scale, and place letters in two and three dimensional space.

The ``shape`` mode draws text using the the glyph outlines of individual characters rather than as textures. This mode is only supported with the ``pdf`` and ``p3_d`` renderer settings. With the ``pdf`` renderer, you must call ``text_mode(shape)`` before any other drawing occurs. If the outlines are not available, then ``text_mode(shape)`` will be ignored and ``text_mode(model)`` will be used instead.

The ``text_mode(shape)`` option in ``p3_d`` can be combined with ``begin_raw()`` to write vector-accurate text to 2D and 3D output files, for instance ``dxf`` or ``pdf`` . The ``shape`` mode is not currently optimized for ``p3_d`` , so if recording shape data, use ``text_mode(model)`` until you're ready to capture the geometry with ``begin_raw()`` .


See Also
--------

Sketch.loadFont(String)

Py5Font.Py5Font

Py5Graphics.text(String, float, float) : This does a basic number formatting, to avoid the generally ugly appearance of printing floats.

Py5Graphics.textFont(Py5Font)

Py5Graphics.beginRaw(Py5Graphics)

Sketch.createFont(String, float, boolean)


# Py5Graphics_text_sentence

Emit a sentence of text, defined as a chunk of text without any newlines.

Parameters
----------

PARAMTEXT

Notes
-----

Emit a sentence of text, defined as a chunk of text without any newlines.


# Py5Graphics_text_size

The current text size (read-only)

Parameters
----------

PARAMTEXT

Notes
-----

Sets the current font size. This size will be used in all subsequent calls to the ``text()`` function. Font size is measured in units of pixels.


See Also
--------

Sketch.loadFont(String)

Py5Font.Py5Font

Py5Graphics.text(String, float, float) : This does a basic number formatting, to avoid the generally ugly appearance of printing floats.

Py5Graphics.textFont(Py5Font)


# Py5Graphics_text_size_impl

Called from textSize() after validating size.

Parameters
----------

PARAMTEXT

Notes
-----

Called from textSize() after validating size. Subclasses will want to override this one.


# Py5Graphics_text_width

Calculates and returns the width of any character or text string.

Parameters
----------

PARAMTEXT

Notes
-----

Calculates and returns the width of any character or text string.


See Also
--------

Sketch.loadFont(String)

Py5Font.Py5Font

Py5Graphics.text(String, float, float) : This does a basic number formatting, to avoid the generally ugly appearance of printing floats.

Py5Graphics.textFont(Py5Font)

Py5Graphics.textSize(float)


# Py5Graphics_text_width_impl

Implementation of returning the text width of the chars [start, stop) in the buffer.

Parameters
----------

PARAMTEXT

Notes
-----

Implementation of returning the text width of the chars [start, stop) in the buffer. Unlike the previous version that was inside Py5Font, this will return the size not of a 1 pixel font, but the actual current size.


# Py5Graphics_texture

Sets a texture to be applied to vertex points.

Parameters
----------

PARAMTEXT

Notes
-----

Sets a texture to be applied to vertex points. The ``texture()`` function must be called between ``begin_shape()`` and ``end_shape()`` and before any calls to ``vertex()`` .

When textures are in use, the fill color is ignored. Instead, use tint() to specify the color of the texture as it is applied to the shape.


See Also
--------

Py5Graphics.textureMode(int)

Py5Graphics.textureWrap(int)

Py5Graphics.beginShape(int)

Py5Graphics.endShape(int)

Py5Graphics.vertex(float, float, float, float, float) : Used by renderer subclasses or Py5Shape to efficiently pass in already formatted vertex information.


# Py5Graphics_texture_image

Current image being used as a texture

Parameters
----------

PARAMTEXT

Notes
-----

Current image being used as a texture


# Py5Graphics_texture_mode

Sets whether texture coordinates passed to vertex() calls will be based on coordinates that are based on the IMAGE or NORMALIZED.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the coordinate space for texture mapping. There are two options, IMAGE, which refers to the actual coordinates of the image, and NORMAL, which refers to a normalized space of values ranging from 0 to 1. The default mode is IMAGE. In IMAGE, if an image is 100 x 200 pixels, mapping the image onto the entire size of a quad would require the points (0,0) (0,100) (100,200) (0,200). The same mapping in NORMAL_SPACE is (0,0) (0,1) (1,1) (0,1).


See Also
--------

Py5Graphics.texture(Py5Image) : Sets a texture to be applied to vertex points.

Py5Graphics.textureWrap(int)


# Py5Graphics_texture_u

Current horizontal coordinate for texture, will always be between 0 and 1, even if using textureMode(IMAGE).

Parameters
----------

PARAMTEXT

Notes
-----

Current horizontal coordinate for texture, will always be between 0 and 1, even if using textureMode(IMAGE).


# Py5Graphics_texture_v

Current vertical coordinate for texture, see above.

Parameters
----------

PARAMTEXT

Notes
-----

Current vertical coordinate for texture, see above.


# Py5Graphics_texture_wrap

Description to come...

Parameters
----------

PARAMTEXT

Notes
-----

Description to come... ( end auto-generated from textureWrap.xml )


See Also
--------

Py5Graphics.texture(Py5Image) : Sets a texture to be applied to vertex points.

Py5Graphics.textureMode(int)


# Py5Graphics_tint

Sets the fill value for displaying images.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the fill value for displaying images. Images can be tinted to specified colors or made transparent by setting the alpha.

To make an image transparent, but not change it's color, use white as the tint color and specify an alpha value. For instance, tint(255, 128) will make an image 50% transparent (unless ``color_mode()`` has been used).

When using hexadecimal notation to specify a color, use "#" or "0x" before the values (e.g. #CCFFAA, 0xFFCCFFAA). The # syntax uses six digits to specify a color (the way colors are specified in HTML and CSS). When using the hexadecimal notation starting with "0x", the hexadecimal value must be specified with eight characters; the first two characters define the alpha component and the remainder the red, green, and blue components.

The value for the parameter "gray" must be less than or equal to the current maximum value as specified by ``color_mode()`` . The default maximum value is 255.

The ``tint()`` function is also used to control the coloring of textures in 3D.


See Also
--------

Py5Graphics.noTint()

Py5Graphics.image(Py5Image, float, float, float, float) : Java AWT Image object associated with this renderer.


# Py5Graphics_tint_color

tint that was last set (read-only)

Parameters
----------

PARAMTEXT

Notes
-----

tint that was last set (read-only)


# Py5Graphics_translate

Specifies an amount to displace objects within the display window.

Parameters
----------

PARAMTEXT

Notes
-----

Specifies an amount to displace objects within the display window. The ``x`` parameter specifies left/right translation, the ``y`` parameter specifies up/down translation, and the ``z`` parameter specifies translations toward/away from the screen. Using this function with the ``z`` parameter requires using P3D as a parameter in combination with size as shown in the above example. Transformations apply to everything that happens after and subsequent calls to the function accumulates the effect. For example, calling ``translate(50 0)`` and then ``translate(20 0)`` is the same as ``translate(70 0)`` . If ``translate()`` is called within ``draw()`` , the transformation is reset when the loop begins again. This function can be further controlled by the ``push_matrix()`` and ``pop_matrix()`` .


See Also
--------

Py5Graphics.popMatrix()

Py5Graphics.pushMatrix()

Py5Graphics.rotate(float) : Rotates a shape the amount specified by the , ``angle`` , parameter.

Py5Graphics.rotateX(float)

Py5Graphics.rotateY(float)

Py5Graphics.rotateZ(float)

Py5Graphics.scale(float, float, float) : Increases or decreases the size of a shape by expanding and contracting vertices.


# Py5Graphics_triangle

A triangle is a plane created by connecting three points.

Parameters
----------

PARAMTEXT

Notes
-----

A triangle is a plane created by connecting three points. The first two arguments specify the first point, the middle two arguments specify the second point, and the last two arguments specify the third point.


See Also
--------

Sketch.beginShape()


# Py5Graphics_vertex

Used by renderer subclasses or Py5Shape to efficiently pass in already formatted vertex information.

Parameters
----------

PARAMTEXT

Notes
-----

All shapes are constructed by connecting a series of vertices. ``vertex()`` is used to specify the vertex coordinates for points, lines, triangles, quads, and polygons and is used exclusively within the ``begin_shape()`` and ``end_shape()`` function.

Drawing a vertex in 3D using the ``z`` parameter requires the P3D parameter in combination with size as shown in the above example.

This function is also used to map a texture onto the geometry. The ``texture()`` function declares the texture to apply to the geometry and the ``u`` and ``v`` coordinates set define the mapping of this texture to the form. By default, the coordinates used for ``u`` and ``v`` are specified in relation to the image's size in pixels, but this relation can be changed with ``texture_mode()`` .


See Also
--------

Py5Graphics.beginShape(int)

Py5Graphics.endShape(int)

Py5Graphics.bezierVertex(float, float, float, float, float, float, float, float, float)

Py5Graphics.quadraticVertex(float, float, float, float, float, float)

Py5Graphics.curveVertex(float, float, float)

Py5Graphics.texture(Py5Image) : Sets a texture to be applied to vertex points.


# Py5Graphics_vertex_texture

Set (U, V) coords for the next vertex in the current shape.

Parameters
----------

PARAMTEXT

Notes
-----

Set (U, V) coords for the next vertex in the current shape. This is ugly as its own function, and will (almost?) always be coincident with a call to vertex. As of beta, this was moved to the protected method you see here, and called from an optional param of and overloaded vertex().

The parameters depend on the current textureMode. When using textureMode(IMAGE), the coordinates will be relative to the size of the image texture, when used with textureMode(NORMAL), they'll be in the range 0..1.

Used by both Py5Graphics2D (for images) and Py5Graphics3D.


# Py5Image_blend

Blends a region of pixels into the image specified by the , ``img`` , parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Blends a region of pixels into the image specified by the ``img`` parameter. These copies utilize full alpha channel support and a choice of the following modes to blend the colors of source pixels (A) with the ones of pixels in the destination image (B):

BLEND - linear interpolation of colours: C = A*factor + B

ADD - additive blending with white clip: C = min(A*factor + B, 255)

SUBTRACT - subtractive blending with black clip: C = max(B - A*factor, 0)

DARKEST - only the darkest colour succeeds: C = min(A*factor, B)

LIGHTEST - only the lightest colour succeeds: C = max(A*factor, B)

DIFFERENCE - subtract colors from underlying image.

EXCLUSION - similar to DIFFERENCE, but less extreme.

MULTIPLY - Multiply the colors, result will always be darker.

SCREEN - Opposite multiply, uses inverse values of the colors.

OVERLAY - A mix of MULTIPLY and SCREEN. Multiplies dark values, and screens light values.

HARD_LIGHT - SCREEN when greater than 50% gray, MULTIPLY when lower.

SOFT_LIGHT - Mix of DARKEST and LIGHTEST. Works like OVERLAY, but not as harsh.

DODGE - Lightens light tones and increases contrast, ignores darks. Called "Color Dodge" in Illustrator and Photoshop.

BURN - Darker areas are applied, increasing contrast, ignores lights. Called "Color Burn" in Illustrator and Photoshop.

All modes use the alpha information (highest byte) of source image pixels as the blending factor. If the source and destination regions are different sizes, the image will be automatically resized to match the destination size. If the ``src_img`` parameter is not used, the display window is used as the source image.

As of release 0149, this function ignores ``image_mode()`` .


See Also
--------

Sketch.alpha(int) : Extracts the alpha value from a color.

Py5Image.copy(Py5Image, int, int, int, int, int, int, int, int) : Copies a region of pixels from one image into another.

Py5Image.blendColor(int,int,int)


# Py5Image_blend_add_pin

Add O = MIN(D + S, 1)

Parameters
----------

PARAMTEXT

Notes
-----

Add O = MIN(D + S, 1)


# Py5Image_blend_blend

Blend O = S

Parameters
----------

PARAMTEXT

Notes
-----

Blend O = S


# Py5Image_blend_burn

Burn O = 1 - (1 - A) / B

Parameters
----------

PARAMTEXT

Notes
-----

Burn O = 1 - (1 - A) / B


# Py5Image_blend_color

Blends two color values together based on the blending mode given as the , ``mode`` , parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Blends two color values together based on the blending mode given as the ``mode`` parameter. The possible modes are described in the reference for the ``blend()`` function.

Advanced
--------



* REPLACE - destination colour equals colour of source pixel: C = A.     Sometimes called "Normal" or "Copy" in other software.
* BLEND - linear interpolation of colours:

``
c = a*factor + b
``


* ADD - additive blending with white clip:

``
c = min(a*factor + b 255)
``

.     Clipped to 0..255, Photoshop calls this "Linear Burn",     and Director calls it "Add Pin".
* SUBTRACT - substractive blend with black clip:

``
c = max(b - a*factor 0)
``

.     Clipped to 0..255, Photoshop calls this "Linear Dodge",     and Director calls it "Subtract Pin".
* DARKEST - only the darkest colour succeeds:

``
c = min(a*factor b)
``

.     Illustrator calls this "Darken".
* LIGHTEST - only the lightest colour succeeds:

``
c = max(a*factor b)
``

.     Illustrator calls this "Lighten".
* DIFFERENCE - subtract colors from underlying image.
* EXCLUSION - similar to DIFFERENCE, but less extreme.
* MULTIPLY - Multiply the colors, result will always be darker.
* SCREEN - Opposite multiply, uses inverse values of the colors.
* OVERLAY - A mix of MULTIPLY and SCREEN. Multiplies dark values,     and screens light values.
* HARD_LIGHT - SCREEN when greater than 50% gray, MULTIPLY when lower.
* SOFT_LIGHT - Mix of DARKEST and LIGHTEST.     Works like OVERLAY, but not as harsh.
* DODGE - Lightens light tones and increases contrast, ignores darks.     Called "Color Dodge" in Illustrator and Photoshop.
* BURN - Darker areas are applied, increasing contrast, ignores lights.     Called "Color Burn" in Illustrator and Photoshop.


A useful reference for blending modes and their algorithms can be found in the<A HREF="http://www.w3.org/TR/SVG12/rendering.html">SVG</A>specification.



It is important to note that Processing uses "fast" code, not necessarily "correct" code. No biggie, most software does. A nitpicker can find numerous "off by 1 division" problems in the blend code where

``
>>8
``

or

``
>>7
``

is used when strictly speaking

``
/255.0

or

``
/127.0
``

should have been used.



for instance exclusion (not intended for real-time use) reads

``
r1 + r2 - ((2 * r1 * r2) / 255)
``

because

``
255 == 1.0
``

not

``
256 == 1.0
``

. _in other words

``
(255*255)>>8
``

is not the same as

``
(255*255)/255
``

. But for real-time use the shifts are preferrable, and the difference is insignificant for applications built with Processing.


See Also
--------

Py5Image.blend(Py5Image, int, int, int, int, int, int, int, int, int) : Blends a region of pixels into the image specified by the , ``img`` , parameter.

Sketch.color(float, float, float, float) : Creates colors for storing in variables of the , ``color`` , datatype.


# Py5Image_blend_darkest

Darkest O = MIN(D, S)

Parameters
----------

PARAMTEXT

Notes
-----

Darkest O = MIN(D, S)


# Py5Image_blend_difference

Difference O = ABS(D - S)

Parameters
----------

PARAMTEXT

Notes
-----

Difference O = ABS(D - S)


# Py5Image_blend_dodge

Dodge O = D / (1 - S)

Parameters
----------

PARAMTEXT

Notes
-----

Dodge O = D / (1 - S)


# Py5Image_blend_exclusion

Exclusion O = (1 - S)D + S(1 - D) O = D + S - 2DS

Parameters
----------

PARAMTEXT

Notes
-----

Exclusion O = (1 - S)D + S(1 - D) O = D + S - 2DS


# Py5Image_blend_hard_light

Hard Light O = OVERLAY(S, D) O = 2 * MULTIPLY(D, S) = 2DS                   for S ,<, 0.5 O = 2 * SCREEN(D, S) - 1 = 2(S + D - DS) - 1   otherwise

Parameters
----------

PARAMTEXT

Notes
-----

Hard Light O = OVERLAY(S, D) O = 2 * MULTIPLY(D, S) = 2DS                   for S<0.5 O = 2 * SCREEN(D, S) - 1 = 2(S + D - DS) - 1   otherwise


# Py5Image_blend_lightest

Lightest O = MAX(D, S)

Parameters
----------

PARAMTEXT

Notes
-----

Lightest O = MAX(D, S)


# Py5Image_blend_overlay

Overlay O = 2 * MULTIPLY(D, S) = 2DS                   for D ,<, 0.5 O = 2 * SCREEN(D, S) - 1 = 2(S + D - DS) - 1   otherwise

Parameters
----------

PARAMTEXT

Notes
-----

Overlay O = 2 * MULTIPLY(D, S) = 2DS                   for D<0.5 O = 2 * SCREEN(D, S) - 1 = 2(S + D - DS) - 1   otherwise


# Py5Image_blend_screen

Screen O = 1 - (1 - D)(1 - S) O = D + S - DS

Parameters
----------

PARAMTEXT

Notes
-----

Screen O = 1 - (1 - D)(1 - S) O = D + S - DS


# Py5Image_blend_soft_light

Soft Light (Pegtop) O = (1 - D) * MULTIPLY(D, S) + D * SCREEN(D, S) O = (1 - D) * DS + D * (1 - (1 - D)(1 - S)) O = 2DS + DD - 2DDS

Parameters
----------

PARAMTEXT

Notes
-----

Soft Light (Pegtop) O = (1 - D) * MULTIPLY(D, S) + D * SCREEN(D, S) O = (1 - D) * DS + D * (1 - (1 - D)(1 - S)) O = 2DS + DD - 2DDS


# Py5Image_blend_sub_pin

Subtract O = MAX(0, D - S)

Parameters
----------

PARAMTEXT

Notes
-----

Subtract O = MAX(0, D - S)


# Py5Image_blit_resize

Internal blitter/resizer/copier from toxi.

Parameters
----------

PARAMTEXT

Notes
-----

Internal blitter/resizer/copier from toxi. Uses bilinear filtering if smooth() has been enabled 'mode' determines the blending mode used in the process.


# Py5Image_build_blur_kernel

Optimized code for building the blur kernel.

Parameters
----------

PARAMTEXT

Notes
-----

Optimized code for building the blur kernel. further optimized blur code (approx. 15% for radius=20) bigger speed gains for larger radii (~30%) added support for various image types (ALPHA, RGB, ARGB) [toxi 050728]


# Py5Image_check_alpha

Check the alpha on an image, using a really primitive loop.

Parameters
----------

PARAMTEXT

Notes
-----

Check the alpha on an image, using a really primitive loop.


# Py5Image_clone

Duplicate an image, returns new Py5Image object.

Parameters
----------

PARAMTEXT

Notes
-----

Duplicate an image, returns new Py5Image object. The pixels[] array for the new object will be unique and recopied from the source image. This is implemented as an override of Object.clone(). We recommend using get() instead, because it prevents you from needing to catch the CloneNotSupportedException, and from doing a cast from the result.


# Py5Image_copy

Copies a region of pixels from one image into another.

Parameters
----------

PARAMTEXT

Notes
-----

Copies a region of pixels from one image into another. If the source and destination regions aren't the same size, it will automatically resize source pixels to fit the specified target region. No alpha information is used in the process, however if the source image has an alpha channel set, it will be copied as well.

As of release 0149, this function ignores ``image_mode()`` .


See Also
--------

Py5Graphics.alpha(int) : Extracts the alpha value from a color.

Py5Image.blend(Py5Image, int, int, int, int, int, int, int, int, int) : Blends a region of pixels into the image specified by the , ``img`` , parameter.


# Py5Image_dilate

Generic dilate/erode filter using luminance values as decision factor.

Parameters
----------

PARAMTEXT

Notes
-----

Generic dilate/erode filter using luminance values as decision factor. [toxi 050728]


# Py5Image_filter

Filters an image as defined by one of the following modes:,
,
,THRESHOLD - converts the image to black and white pixels depending if they are above or below the threshold defined by the level parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Filters an image as defined by one of the following modes:

THRESHOLD - converts the image to black and white pixels depending if they are above or below the threshold defined by the level parameter. The level must be between 0.0 (black) and 1.0(white). If no level is specified, 0.5 is used.

GRAY - converts any colors in the image to grayscale equivalents

INVERT - sets each pixel to its inverse value

POSTERIZE - limits each channel of the image to the number of colors specified as the level parameter

BLUR - executes a Guassian blur with the level parameter specifying the extent of the blurring. If no level parameter is used, the blur is equivalent to Guassian blur of radius 1

OPAQUE - sets the alpha channel to entirely opaque

ERODE - reduces the light areas with the amount defined by the level parameter

DILATE - increases the light areas with the amount defined by the level parameter

Advanced
--------

Method to apply a variety of basic filters to this image.



* filter(BLUR) provides a basic blur.
* filter(GRAY) converts the image to grayscale based on luminance.
* filter(INVERT) will invert the color components in the image.
* filter(OPAQUE) set all the high bits in the image to opaque
* filter(THRESHOLD) converts the image to black and white.
* filter(DILATE) grow white/light areas
* filter(ERODE) shrink white/light areas
Luminance conversion code contributed by<A HREF="http://www.toxi.co.uk">toxi</A><P/>Gaussian blur code contributed by<A HREF="http://incubator.quasimondo.com">Mario Klingemann</A>


# Py5Image_format

Format for this image, one of RGB, ARGB or ALPHA.

Parameters
----------

PARAMTEXT

Notes
-----

Format for this image, one of RGB, ARGB or ALPHA. note that RGB images still require 0xff in the high byte because of how they'll be manipulated by other functions


# Py5Image_get

Reads the color of any pixel or grabs a section of an image.

Parameters
----------

PARAMTEXT

Notes
-----

Reads the color of any pixel or grabs a section of an image. If no parameters are specified, the entire image is returned. Use the ``x`` and ``y`` parameters to get the value of one pixel. Get a section of the display window by specifying an additional ``width`` and ``height`` parameter. When getting an image, the ``x`` and ``y`` parameters define the coordinates for the upper-left corner of the image, regardless of the current ``image_mode()`` .

If the pixel requested is outside of the image window, black is returned. The numbers returned are scaled according to the current color ranges, but only RGB values are returned by this function. For example, even though you may have drawn a shape with ``color_mode(hsb)`` , the numbers returned will be in RGB format.

Getting the color of a single pixel with ``get(x y)`` is easy, but not as fast as grabbing the data directly from ``pixels[]`` . The equivalent statement to ``get(x y)`` using ``pixels[]`` is ``pixels[y*width+x]`` . See the reference for ``pixels[]`` for more information.

Advanced
--------

Returns an ARGB "color" type (a packed 32 bit int with the color. If the coordinate is outside the image, zero is returned (black, but completely transparent).

If the image is in RGB format (i.e. on a PVideo object), the value will get its high bits set, just to avoid cases where they haven't been set already.

If the image is in ALPHA format, this returns a white with its alpha value set.

This function is included primarily for beginners. It is quite slow because it has to check to see if the x, y that was provided is inside the bounds, and then has to check to see what image type it is. If you want things to be more efficient, access the pixels[] array directly.


See Also
--------

Sketch.set(int, int, int) : Changes the color of any pixel or writes an image directly into the display window.,
, ,
, The , ``x`` , and , ``y`` , parameters specify the pixel to change and the , ``color`` , parameter specifies the color value.

Sketch.pixels : Array containing the values for all the pixels in the display window.

Sketch.copy(Py5Image, int, int, int, int, int, int, int, int) : Copies a region of pixels from one image into another.


# Py5Image_get_impl

Internal function to actually handle getting a block of pixels that has already been properly cropped to a valid region.

Parameters
----------

PARAMTEXT

Notes
-----

Internal function to actually handle getting a block of pixels that has already been properly cropped to a valid region. That is, x/y/w/h are guaranteed to be inside the image space, so the implementation can use the fastest possible pixel copying method.


# Py5Image_height

The height of the image in units of pixels.

Parameters
----------

PARAMTEXT

Notes
-----

The height of the image in units of pixels.


# Py5Image_init

Function to be used by subclasses of Py5Image to init later than at the constructor, or re-init later when things changes.

Parameters
----------

PARAMTEXT

Notes
-----

Datatype for storing images. Processing can display ``.gif`` , ``.jpg`` , ``.tga`` , and ``.png`` images. Images may be displayed in 2D and 3D space. Before an image is used, it must be loaded with the ``load_image()`` function. The ``Py5Image`` object contains fields for the ``width`` and ``height`` of the image, as well as an array called ``pixels[]`` which contains the values for every pixel in the image. A group of methods, described below, allow easy access to the image's pixels and alpha channel and simplify the process of compositing.

Before using the ``pixels[]`` array, be sure to use the ``load_pixels()`` method on the image to make sure that the pixel data is properly loaded.

To create a new image, use the ``create_image()`` function (do not use ``new Py5Image()`` ).


See Also
--------

Sketch.loadImage(String, String)

Sketch.imageMode(int)

Sketch.createImage(int, int, int)


# Py5Image_intersect

Check to see if two rectangles intersect one another

Parameters
----------

PARAMTEXT

Notes
-----

Check to see if two rectangles intersect one another


# Py5Image_load_pixels

Loads the pixel data for the image into its , ``pixels[]`` , array.

Parameters
----------

PARAMTEXT

Notes
-----

Loads the pixel data for the image into its ``pixels[]`` array. This function must always be called before reading from or writing to ``pixels[]`` .

renderers may or may not seem to require ``load_pixels()`` or ``update_pixels()`` . However, the rule is that any time you want to manipulate the ``pixels[]`` array, you must first call ``load_pixels()`` , and after changes have been made, call ``update_pixels()`` . Even if the renderer may not seem to use this function in the current Processing release, this will always be subject to change.

Advanced
--------

Call this when you want to mess with the pixels[] array.

For subclasses where the pixels[] buffer isn't set by default, this should copy all data into the pixels[] array


# Py5Image_load_tga

Targa image loader for RLE-compressed TGA files.

Parameters
----------

PARAMTEXT

Notes
-----

Targa image loader for RLE-compressed TGA files.

Rewritten for 0115 to read/write RLE-encoded targa images. For 0125, non-RLE encoded images are now supported, along with images whose y-order is reversed (which is standard for TGA files).

A version of this function is in MovieMaker.java. Any fixes here should be applied over in MovieMaker as well.

Known issue with RLE encoding and odd behavior in some apps: https://github.com/processing/processing/issues/2096 Please help!


# Py5Image_loaded

Loaded pixels flag

Parameters
----------

PARAMTEXT

Notes
-----

Loaded pixels flag


# Py5Image_mask

Masks part of an image from displaying by loading another image and using it as an alpha channel.

Parameters
----------

PARAMTEXT

Notes
-----

Masks part of an image from displaying by loading another image and using it as an alpha channel. This mask image should only contain grayscale data, but only the blue color channel is used. The mask image needs to be the same size as the image to which it is applied.

In addition to using a mask image, an integer array containing the alpha channel data can be specified directly. This method is useful for creating dynamically generated alpha masks. This array must be of the same length as the target image's pixels array and should contain only grayscale data of values between 0-255.

Advanced
--------

Set alpha channel for an image. Black colors in the source image will make the destination image completely transparent, and white will make things fully opaque. Gray values will be in-between steps.

Strictly speaking the "blue" value from the source image is used as the alpha color. For a fully grayscale image, this is correct, but for a color image it's not 100% accurate. For a more accurate conversion, first use filter(GRAY) which will make the image into a "correct" grayscale by performing a proper luminance-based conversion.


# Py5Image_modified

modified portion of the image

Parameters
----------

PARAMTEXT

Notes
-----

modified portion of the image


# Py5Image_opaque

Set the high bits of all pixels to opaque.

Parameters
----------

PARAMTEXT

Notes
-----

Set the high bits of all pixels to opaque.


# Py5Image_parent

Path to parent object that will be used with save().

Parameters
----------

PARAMTEXT

Notes
-----

Path to parent object that will be used with save(). This prevents users from needing savePath() to use Py5Image.save().


# Py5Image_pixel_density

1 for most images, 2 for hi-dpi/retina

Parameters
----------

PARAMTEXT

Notes
-----

1 for most images, 2 for hi-dpi/retina


# Py5Image_pixel_width

Actual dimensions of pixels array, taking into account the 2x setting.

Parameters
----------

PARAMTEXT

Notes
-----

Actual dimensions of pixels array, taking into account the 2x setting.


# Py5Image_pixels

Array containing the values for all the pixels in the display window.

Parameters
----------

PARAMTEXT

Notes
-----

Array containing the values for all the pixels in the display window. These values are of the color datatype. This array is the size of the display window. For example, if the image is 100x100 pixels, there will be 10000 values and if the window is 200x300 pixels, there will be 60000 values. The ``index`` value defines the position of a value within the array. For example, the statement ``color b = pixels[230]`` will set the variable ``b`` to be equal to the value at that location in the array.

Before accessing this array, the data must loaded with the ``load_pixels()`` function. After the array data has been modified, the ``update_pixels()`` function must be run to update the changes. Without ``load_pixels()`` , running the code may (or will in future releases) result in a NullPointerException.


# Py5Image_resize

Resize the image to a new width and height.

Parameters
----------

PARAMTEXT

Notes
-----

Resize the image to a new width and height. To make the image scale proportionally, use 0 as the value for the ``wide`` or ``high`` parameter. For instance, to make the width of an image 150 pixels, and change the height using the same proportion, use resize(150, 0).

Even though a Py5Graphics is technically a Py5Image, it is not possible to rescale the image data found in a Py5Graphics. (It's simply not possible to do this consistently across renderers: technically infeasible with P3D, or what would it even do with PDF?) If you want to resize Py5Graphics content, first get a copy of its image data using the ``get()`` method, and call ``resize()`` on the Py5Image that is returned.


See Also
--------

Py5Image.get(int, int, int, int) : Reads the color of any pixel or grabs a section of an image.


# Py5Image_save

Saves the image into a file.

Parameters
----------

PARAMTEXT

Notes
-----

Saves the image into a file. Append a file extension to the name of the file, to indicate the file format to be used: either TIFF (.tif), TARGA (.tga), JPEG (.jpg), or PNG (.png). If no extension is included in the filename, the image will save in TIFF format and .tif will be added to the name.  These files are saved to the sketch's folder, which may be opened by selecting "Show sketch folder" from the "Sketch" menu.

To save an image created within the code, rather than through loading, it's necessary to make the image with the ``create_image()`` function so it is aware of the location of the program and can therefore save the file to the right place. See the ``create_image()`` reference for more information.

Advanced
--------

Save this image to disk.

As of revision 0100, this function requires an absolute path, in order to avoid confusion. To save inside the sketch folder, use the function savePath() from Sketch, or use saveFrame() instead. As of revision 0116, savePath() is not needed if this object has been created (as recommended) via createImage() or createGraphics() or one of its neighbors.

As of revision 0115, when using Java 1.4 and later, you can write to several formats besides tga and tiff. If Java 1.4 is installed and the extension used is supported (usually png, jpg, jpeg, bmp, and tiff), then those methods will be used to write the image. To get a list of the supported formats for writing, use:


``
println(javax.imageio._image_io.get_reader_format_names())
``



To use the original built-in image writers, use .tga or .tif as the extension, or don't include an extension. When no extension is used, the extension .tif will be added to the file name.

The ImageIO API claims to support wbmp files, however they probably require a black and white image. Basic testing produced a zero-length file with no error.


# Py5Image_save_tga

Creates a Targa32 formatted byte sequence of specified pixel buffer using RLE compression.

Parameters
----------

PARAMTEXT

Notes
-----

Creates a Targa32 formatted byte sequence of specified pixel buffer using RLE compression.</p>Also figured out how to avoid parsing the image upside-down (there's a header flag to set the image origin to top-left)</p>Starting with revision 0092, the format setting is taken into account:

* 

``
alpha
``

images written as 8bit grayscale (uses lowest byte)
* 

``
rgb
``

24 bits
* 

``
argb
``

32 bits
All versions are RLE compressed.</p>Contributed by toxi 8-10 May 2005, based on this RLE<A HREF="http://www.wotsit.org/download.asp?f=tga">specification</A>


# Py5Image_set

Changes the color of any pixel or writes an image directly into the display window.,
, ,
, The , ``x`` , and , ``y`` , parameters specify the pixel to change and the , ``color`` , parameter specifies the color value.

Parameters
----------

PARAMTEXT

Notes
-----

Changes the color of any pixel or writes an image directly into the display window.

The ``x`` and ``y`` parameters specify the pixel to change and the ``color`` parameter specifies the color value. The color parameter is affected by the current color mode (the default is RGB values from 0 to 255). When setting an image, the ``x`` and ``y`` parameters define the coordinates for the upper-left corner of the image, regardless of the current ``image_mode()`` .

Setting the color of a single pixel with ``set(x y)`` is easy, but not as fast as putting the data directly into ``pixels[]`` . The equivalent statement to ``set(x y #000000)`` using ``pixels[]`` is ``pixels[y*width+x] = #000000`` . See the reference for ``pixels[]`` for more information.


See Also
--------

Py5Image.get(int, int, int, int) : Reads the color of any pixel or grabs a section of an image.

Py5Image.pixels : Array containing the values for all the pixels in the display window.

Py5Image.copy(Py5Image, int, int, int, int, int, int, int, int) : Copies a region of pixels from one image into another.


# Py5Image_set_impl

Internal function to actually handle setting a block of pixels that has already been properly cropped from the image to a valid region.

Parameters
----------

PARAMTEXT

Notes
-----

Internal function to actually handle setting a block of pixels that has already been properly cropped from the image to a valid region.


# Py5Image_update_pixels

Updates the image with the data in its , ``pixels[]`` , array.

Parameters
----------

PARAMTEXT

Notes
-----

Updates the image with the data in its ``pixels[]`` array. Use in conjunction with ``load_pixels()`` . If you're only reading pixels from the array, there's no need to call ``update_pixels()`` .

renderers may or may not seem to require ``load_pixels()`` or ``update_pixels()`` . However, the rule is that any time you want to manipulate the ``pixels[]`` array, you must first call ``load_pixels()`` , and after changes have been made, call ``update_pixels()`` . Even if the renderer may not seem to use this function in the current Processing release, this will always be subject to change.

Currently, none of the renderers use the additional parameters to ``update_pixels()`` , however this may be implemented in the future.

Advanced
--------

Mark the pixels in this region as needing an update. This is not currently used by any of the renderers, however the api is structured this way in the hope of being able to use this to speed things up in the future.


# Py5Image_width

The width of the image in units of pixels.

Parameters
----------

PARAMTEXT

Notes
-----

The width of the image in units of pixels.


# Py5Shader_bind

Initializes (if needed) and binds the shader program.

Parameters
----------

PARAMTEXT

Notes
-----

Initializes (if needed) and binds the shader program.


# Py5Shader_bound

Returns true if the shader is bound, false otherwise.

Parameters
----------

PARAMTEXT

Notes
-----

Returns true if the shader is bound, false otherwise.


# Py5Shader_compile_fragment_shader



Parameters
----------

PARAMTEXT

Notes
-----




# Py5Shader_compile_vertex_shader



Parameters
----------

PARAMTEXT

Notes
-----




# Py5Shader_get_attribute_loc

Returns the ID location of the attribute parameter given its name.

Parameters
----------

PARAMTEXT

Notes
-----

Returns the ID location of the attribute parameter given its name.


# Py5Shader_get_uniform_loc

Returns the ID location of the uniform parameter given its name.

Parameters
----------

PARAMTEXT

Notes
-----

Returns the ID location of the uniform parameter given its name.


# Py5Shader_init

Creates a shader program using the specified vertex and fragment shaders.

Parameters
----------

PARAMTEXT

Notes
-----

Creates a shader program using the specified vertex and fragment shaders.


# Py5Shader_set



Parameters
----------

PARAMTEXT

Notes
-----




# Py5Shader_setup

Extra initialization method that can be used by subclasses, called after compiling and attaching the vertex and fragment shaders, and before linking the shader program.

Parameters
----------

PARAMTEXT

Notes
-----

Extra initialization method that can be used by subclasses, called after compiling and attaching the vertex and fragment shaders, and before linking the shader program.


# Py5Shader_unbind

Unbinds the shader program.

Parameters
----------

PARAMTEXT

Notes
-----

Unbinds the shader program.


# Py5Shape_add_child



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Py5Shape.getChild(int)


# Py5Shape_add_name

Add a shape to the name lookup table.

Parameters
----------

PARAMTEXT

Notes
-----

Add a shape to the name lookup table.


# Py5Shape_begin_contour



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Py5Shape.endContour()


# Py5Shape_begin_shape



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Sketch.endShape()


# Py5Shape_check_matrix

Make sure that the shape's matrix is 1) not null, and 2) has a matrix that can handle ,<em>,at least,</em>, the specified number of dimensions.

Parameters
----------

PARAMTEXT

Notes
-----

Make sure that the shape's matrix is 1) not null, and 2) has a matrix that can handle<em>at least</em>the specified number of dimensions.


# Py5Shape_close

True if this is a closed path.

Parameters
----------

PARAMTEXT

Notes
-----

True if this is a closed path.


# Py5Shape_color_mode

Set the pivot point for all transformations.

Parameters
----------

PARAMTEXT

Notes
-----

Set the pivot point for all transformations.


# Py5Shape_color_mode_a

Max value for alpha set by colorMode

Parameters
----------

PARAMTEXT

Notes
-----

Max value for alpha set by colorMode


# Py5Shape_color_mode_default

True if colorMode(RGB, 255)

Parameters
----------

PARAMTEXT

Notes
-----

True if colorMode(RGB, 255)


# Py5Shape_color_mode_scale

True if colors are not in the range 0..1

Parameters
----------

PARAMTEXT

Notes
-----

True if colors are not in the range 0..1


# Py5Shape_color_mode_x

Max value for red (or hue) set by colorMode

Parameters
----------

PARAMTEXT

Notes
-----

Max value for red (or hue) set by colorMode


# Py5Shape_color_mode_y

Max value for green (or saturation) set by colorMode

Parameters
----------

PARAMTEXT

Notes
-----

Max value for green (or saturation) set by colorMode


# Py5Shape_color_mode_z

Max value for blue (or value) set by colorMode

Parameters
----------

PARAMTEXT

Notes
-----

Max value for blue (or value) set by colorMode


# Py5Shape_contains

Return true if this x, y coordinate is part of this shape.

Parameters
----------

PARAMTEXT

Notes
-----

Return true if this x, y coordinate is part of this shape. Only works with PATH shapes or GROUP shapes that contain other GROUPs or PATHs.


# Py5Shape_crop

Resize the children[] array to be in line with childCount

Parameters
----------

PARAMTEXT

Notes
-----

Resize the children[] array to be in line with childCount


# Py5Shape_disable_style

Disables the shape's style data and uses Processing's current styles.

Parameters
----------

PARAMTEXT

Notes
-----

Disables the shape's style data and uses Processing's current styles. Styles include attributes such as colors, stroke weight, and stroke joints.

Advanced
--------

Overrides this shape's style information and uses Py5Graphics styles and colors. Identical to ignoreStyles(true). Also disables styles for all child shapes.


See Also
--------

Py5Shape.enableStyle()


# Py5Shape_draw

Called by the following (the shape() command adds the g) Py5Shape s = loadShape("blah.svg"); shape(s);

Parameters
----------

PARAMTEXT

Notes
-----

Called by the following (the shape() command adds the g) Py5Shape s = loadShape("blah.svg"); shape(s);


# Py5Shape_draw_impl

Draws the SVG document.

Parameters
----------

PARAMTEXT

Notes
-----

Draws the SVG document.


# Py5Shape_enable_style

Enables the shape's style data and ignores Processing's current styles.

Parameters
----------

PARAMTEXT

Notes
-----

Enables the shape's style data and ignores Processing's current styles. Styles include attributes such as colors, stroke weight, and stroke joints.


See Also
--------

Py5Shape.disableStyle()


# Py5Shape_end_contour



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Py5Shape.beginContour()


# Py5Shape_end_shape



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Sketch.beginShape()


# Py5Shape_family

The shape type, one of GROUP, PRIMITIVE, PATH, or GEOMETRY.

Parameters
----------

PARAMTEXT

Notes
-----

The shape type, one of GROUP, PRIMITIVE, PATH, or GEOMETRY.


# Py5Shape_find_child

Same as getChild(name), except that it first walks all the way up the hierarchy to the eldest grandparent, so that children can be found anywhere.

Parameters
----------

PARAMTEXT

Notes
-----

Same as getChild(name), except that it first walks all the way up the hierarchy to the eldest grandparent, so that children can be found anywhere.


# Py5Shape_geometry

Collections of vertices created with beginShape().

Parameters
----------

PARAMTEXT

Notes
-----

Collections of vertices created with beginShape().


# Py5Shape_get_child

Extracts a child shape from a parent shape.

Parameters
----------

PARAMTEXT

Notes
-----

Extracts a child shape from a parent shape. Specify the name of the shape with the ``target`` parameter. The shape is returned as a ``Py5Shape`` object, or ``null`` is returned if there is an error.


See Also
--------

Py5Shape.addChild(Py5Shape)


# Py5Shape_get_child_count



Parameters
----------

PARAMTEXT

Notes
-----




# Py5Shape_get_child_index

Returns the index of child who.

Parameters
----------

PARAMTEXT

Notes
-----

Returns the index of child who.


# Py5Shape_get_depth

Get the depth of the shape area (not necessarily the shape boundary).

Parameters
----------

PARAMTEXT

Notes
-----

Get the depth of the shape area (not necessarily the shape boundary). Only makes sense for 3D Py5Shape subclasses, such as Py5Shape3D.


# Py5Shape_get_family

The shape type, one of GROUP, PRIMITIVE, PATH, or GEOMETRY.

Parameters
----------

PARAMTEXT

Notes
-----

The shape type, one of GROUP, PRIMITIVE, PATH, or GEOMETRY.


# Py5Shape_get_height

Get the height of the drawing area (not necessarily the shape boundary).

Parameters
----------

PARAMTEXT

Notes
-----

Get the height of the drawing area (not necessarily the shape boundary).


# Py5Shape_get_vertex



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Py5Shape.setVertex(int, float, float)

Py5Shape.getVertexCount()


# Py5Shape_get_vertex_code

One of VERTEX, BEZIER_VERTEX, CURVE_VERTEX, or BREAK.

Parameters
----------

PARAMTEXT

Notes
-----

One of VERTEX, BEZIER_VERTEX, CURVE_VERTEX, or BREAK.


# Py5Shape_get_vertex_count



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Py5Shape.getVertex(int)

Py5Shape.setVertex(int, float, float)


# Py5Shape_get_width

Get the width of the drawing area (not necessarily the shape boundary).

Parameters
----------

PARAMTEXT

Notes
-----

Get the width of the drawing area (not necessarily the shape boundary).


# Py5Shape_height

The height of the Py5Shape document.

Parameters
----------

PARAMTEXT

Notes
-----

The height of the Py5Shape document.


See Also
--------

Py5Shape.width : The width of the Py5Shape document.


# Py5Shape_image

Texture or image data associated with this shape.

Parameters
----------

PARAMTEXT

Notes
-----

Texture or image data associated with this shape.


# Py5Shape_init



Parameters
----------

PARAMTEXT

Notes
-----




# Py5Shape_is2_d

Return true if this shape is 2D.

Parameters
----------

PARAMTEXT

Notes
-----

Return true if this shape is 2D. Defaults to true.


# Py5Shape_is3_d

Return true if this shape is 3D.

Parameters
----------

PARAMTEXT

Notes
-----

Return true if this shape is 3D. Defaults to false.


# Py5Shape_is_visible

Returns a boolean value "true" if the image is set to be visible, "false" if not.

Parameters
----------

PARAMTEXT

Notes
-----

Returns a boolean value "true" if the image is set to be visible, "false" if not. This is modified with the ``set_visible()`` parameter.

The visibility of a shape is usually controlled by whatever program created the SVG file. For instance, this parameter is controlled by showing or hiding the shape in the layers palette in Adobe Illustrator.


See Also
--------

Py5Shape.setVisible(boolean)


# Py5Shape_kind

ELLIPSE, LINE, QUAD; TRIANGLE_FAN, QUAD_STRIP; etc.

Parameters
----------

PARAMTEXT

Notes
-----

ELLIPSE, LINE, QUAD; TRIANGLE_FAN, QUAD_STRIP; etc.


# Py5Shape_open_shape

Retained shape being created with beginShape/endShape

Parameters
----------

PARAMTEXT

Notes
-----

Retained shape being created with beginShape/endShape


# Py5Shape_params

For primitive shapes in particular, params like x/y/w/h or x1/y1/x2/y2.

Parameters
----------

PARAMTEXT

Notes
-----

For primitive shapes in particular, params like x/y/w/h or x1/y1/x2/y2.


# Py5Shape_parse_base64_image

Parse a base 64 encoded image within an image path.

Parameters
----------

PARAMTEXT

Notes
-----

Parse a base 64 encoded image within an image path.


# Py5Shape_path

A series of vertex, curveVertex, and bezierVertex calls.

Parameters
----------

PARAMTEXT

Notes
-----

A series of vertex, curveVertex, and bezierVertex calls.


# Py5Shape_primitive

A line, ellipse, arc, image, etc.

Parameters
----------

PARAMTEXT

Notes
-----

A line, ellipse, arc, image, etc.


# Py5Shape_remove_child

Remove the child shape with index idx.

Parameters
----------

PARAMTEXT

Notes
-----

Remove the child shape with index idx.


# Py5Shape_reset_matrix

Replaces the current matrix of a shape with the identity matrix.

Parameters
----------

PARAMTEXT

Notes
-----

Replaces the current matrix of a shape with the identity matrix. The equivalent function in OpenGL is glLoadIdentity().


See Also
--------

Py5Shape.rotate(float) : Rotates a shape the amount specified by the , ``angle`` , parameter.

Py5Shape.scale(float) : Increases or decreases the size of a shape by expanding and contracting vertices.

Py5Shape.translate(float, float) : Specifies an amount to displace the shape.


# Py5Shape_rotate

Rotates a shape the amount specified by the , ``angle`` , parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Rotates a shape the amount specified by the ``angle`` parameter. Angles should be specified in radians (values from 0 to TWO_PI) or converted to radians with the ``radians()`` method.

Shapes are always rotated around the upper-left corner of their bounding box. Positive numbers rotate objects in a clockwise direction. Transformations apply to everything that happens after and subsequent calls to the method accumulates the effect. For example, calling ``rotate(half_pi)`` and then ``rotate(half_pi)`` is the same as ``rotate(pi)`` . This transformation is applied directly to the shape, it's not refreshed each time ``draw()`` is run.


See Also
--------

Py5Shape.rotateX(float)

Py5Shape.rotateY(float)

Py5Shape.rotateZ(float)

Py5Shape.scale(float) : Increases or decreases the size of a shape by expanding and contracting vertices.

Py5Shape.translate(float, float) : Specifies an amount to displace the shape.

Py5Shape.resetMatrix()


# Py5Shape_rotate_x

Rotates a shape around the x-axis the amount specified by the , ``angle`` , parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Rotates a shape around the x-axis the amount specified by the ``angle`` parameter. Angles should be specified in radians (values from 0 to TWO_PI) or converted to radians with the ``radians()`` method.

Shapes are always rotated around the upper-left corner of their bounding box. Positive numbers rotate objects in a clockwise direction. Subsequent calls to the method accumulates the effect. For example, calling ``rotate_x(half_pi)`` and then ``rotate_x(half_pi)`` is the same as ``rotate_x(pi)`` . This transformation is applied directly to the shape, it's not refreshed each time ``draw()`` is run.

This method requires a 3D renderer. You need to use P3D as a third parameter for the ``size()`` function as shown in the example above.


See Also
--------

Py5Shape.rotate(float) : Rotates a shape the amount specified by the , ``angle`` , parameter.

Py5Shape.rotateY(float)

Py5Shape.rotateZ(float)

Py5Shape.scale(float) : Increases or decreases the size of a shape by expanding and contracting vertices.

Py5Shape.translate(float, float) : Specifies an amount to displace the shape.

Py5Shape.resetMatrix()


# Py5Shape_rotate_y

Rotates a shape around the y-axis the amount specified by the , ``angle`` , parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Rotates a shape around the y-axis the amount specified by the ``angle`` parameter. Angles should be specified in radians (values from 0 to TWO_PI) or converted to radians with the ``radians()`` method.

Shapes are always rotated around the upper-left corner of their bounding box. Positive numbers rotate objects in a clockwise direction. Subsequent calls to the method accumulates the effect. For example, calling ``rotate_y(half_pi)`` and then ``rotate_y(half_pi)`` is the same as ``rotate_y(pi)`` . This transformation is applied directly to the shape, it's not refreshed each time ``draw()`` is run.

This method requires a 3D renderer. You need to use P3D as a third parameter for the ``size()`` function as shown in the example above.


See Also
--------

Py5Shape.rotate(float) : Rotates a shape the amount specified by the , ``angle`` , parameter.

Py5Shape.rotateX(float)

Py5Shape.rotateZ(float)

Py5Shape.scale(float) : Increases or decreases the size of a shape by expanding and contracting vertices.

Py5Shape.translate(float, float) : Specifies an amount to displace the shape.

Py5Shape.resetMatrix()


# Py5Shape_rotate_z

Rotates a shape around the z-axis the amount specified by the , ``angle`` , parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Rotates a shape around the z-axis the amount specified by the ``angle`` parameter. Angles should be specified in radians (values from 0 to TWO_PI) or converted to radians with the ``radians()`` method.

Shapes are always rotated around the upper-left corner of their bounding box. Positive numbers rotate objects in a clockwise direction. Subsequent calls to the method accumulates the effect. For example, calling ``rotate_z(half_pi)`` and then ``rotate_z(half_pi)`` is the same as ``rotate_z(pi)`` . This transformation is applied directly to the shape, it's not refreshed each time ``draw()`` is run.

This method requires a 3D renderer. You need to use P3D as a third parameter for the ``size()`` function as shown in the example above.


See Also
--------

Py5Shape.rotate(float) : Rotates a shape the amount specified by the , ``angle`` , parameter.

Py5Shape.rotateX(float)

Py5Shape.rotateY(float)

Py5Shape.scale(float) : Increases or decreases the size of a shape by expanding and contracting vertices.

Py5Shape.translate(float, float) : Specifies an amount to displace the shape.

Py5Shape.resetMatrix()


# Py5Shape_scale

Increases or decreases the size of a shape by expanding and contracting vertices.

Parameters
----------

PARAMTEXT

Notes
-----

Increases or decreases the size of a shape by expanding and contracting vertices. Shapes always scale from the relative origin of their bounding box. Scale values are specified as decimal percentages. For example, the method call ``scale(2.0)`` increases the dimension of a shape by 200%. Subsequent calls to the method multiply the effect. For example, calling ``scale(2.0)`` and then ``scale(1.5)`` is the same as ``scale(3.0)`` . This transformation is applied directly to the shape, it's not refreshed each time ``draw()`` is run.

Using this method with the ``z`` parameter requires using the P3D parameter in combination with size.


See Also
--------

Py5Shape.rotate(float) : Rotates a shape the amount specified by the , ``angle`` , parameter.

Py5Shape.translate(float, float) : Specifies an amount to displace the shape.

Py5Shape.resetMatrix()


# Py5Shape_set_fill

The , ``set_fill()`` , method defines the fill color of a , ``Py5Shape`` ,.

Parameters
----------

PARAMTEXT

Notes
-----

The ``set_fill()`` method defines the fill color of a ``Py5Shape`` . This method is used after shapes are created or when a shape is defined explicitly (e.g. ``create_shape(rect 20 20 80 80)`` ) as shown in the above example. When a shape is created with ``begin_shape()`` and ``end_shape()`` , its attributes may be changed with ``fill()`` and ``stroke()`` within ``begin_shape()`` and ``end_shape()`` . However, after the shape is created, only the ``set_fill()`` method can define a new fill value for the ``Py5Shape`` .


# Py5Shape_set_stroke

The , ``set_stroke()`` , method defines the outline color of a , ``Py5Shape`` ,.

Parameters
----------

PARAMTEXT

Notes
-----

The ``set_stroke()`` method defines the outline color of a ``Py5Shape`` . This method is used after shapes are created or when a shape is defined explicitly (e.g. ``create_shape(rect 20 20 80 80)`` ) as shown in the above example. When a shape is created with ``begin_shape()`` and ``end_shape()`` , its attributes may be changed with ``fill()`` and ``stroke()`` within ``begin_shape()`` and ``end_shape()`` . However, after the shape is created, only the ``set_stroke()`` method can define a new stroke value for the ``Py5Shape`` .


# Py5Shape_set_vertex



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Py5Shape.getVertex(int)

Py5Shape.getVertexCount()


# Py5Shape_set_visible

Sets the shape to be visible or invisible.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the shape to be visible or invisible. This is determined by the value of the ``visible`` parameter.

The visibility of a shape is usually controlled by whatever program created the SVG file. For instance, this parameter is controlled by showing or hiding the shape in the layers palette in Adobe Illustrator.


See Also
--------

Py5Shape.isVisible()


# Py5Shape_style

Temporary toggle for whether styles should be honored.

Parameters
----------

PARAMTEXT

Notes
-----

Temporary toggle for whether styles should be honored.


# Py5Shape_translate

Specifies an amount to displace the shape.

Parameters
----------

PARAMTEXT

Notes
-----

Specifies an amount to displace the shape. The ``x`` parameter specifies left/right translation, the ``y`` parameter specifies up/down translation, and the ``z`` parameter specifies translations toward/away from the screen. Subsequent calls to the method accumulates the effect. For example, calling ``translate(50 0)`` and then ``translate(20 0)`` is the same as ``translate(70 0)`` . This transformation is applied directly to the shape, it's not refreshed each time ``draw()`` is run.

Using this method with the ``z`` parameter requires using the P3D parameter in combination with size.


See Also
--------

Py5Shape.rotate(float) : Rotates a shape the amount specified by the , ``angle`` , parameter.

Py5Shape.scale(float) : Increases or decreases the size of a shape by expanding and contracting vertices.

Py5Shape.resetMatrix()


# Py5Shape_vertex_code_count

Array of VERTEX, BEZIER_VERTEX, and CURVE_VERTEX calls.

Parameters
----------

PARAMTEXT

Notes
-----

Array of VERTEX, BEZIER_VERTEX, and CURVE_VERTEX calls.


# Py5Shape_vertices

When drawing POLYGON shapes, the second param is an array of length VERTEX_FIELD_COUNT.

Parameters
----------

PARAMTEXT

Notes
-----

When drawing POLYGON shapes, the second param is an array of length VERTEX_FIELD_COUNT. When drawing PATH shapes, the second param has only two variables.


# Py5Shape_width

The width of the Py5Shape document.

Parameters
----------

PARAMTEXT

Notes
-----

The width of the Py5Shape document.


See Also
--------

Py5Shape.height : The height of the Py5Shape document.


# Py5Surface_get_native

Get the native window object associated with this drawing surface.

Parameters
----------

PARAMTEXT

Notes
-----

Get the native window object associated with this drawing surface. For Java2D, this will be an AWT Frame object. For OpenGL, the window. The data returned here is subject to the whims of the renderer, and using this method means you're willing to deal with underlying implementation changes and that you won't throw a fit like a toddler if your code breaks sometime in the future.


# Py5Surface_min_window_width

Minimum dimensions for the window holding an applet.

Parameters
----------

PARAMTEXT

Notes
-----

Minimum dimensions for the window holding an applet. This varies between platforms, Mac OS X 10.3 (confirmed with 10.7 and Java 6) can do any height but requires at least 128 pixels width. Windows XP has another set of limitations. And for all I know, Linux probably allows window sizes to be negative numbers.


# Py5Surface_open_link



Parameters
----------

PARAMTEXT

Notes
-----




# Py5Surface_pause_thread

On the next trip through the animation thread, things should go sleepy-bye.

Parameters
----------

PARAMTEXT

Notes
-----

On the next trip through the animation thread, things should go sleepy-bye. Does not pause the thread immediately because that needs to happen on the animation thread itself, so fires on the next trip through draw().


# Py5Surface_set_always_on_top

Dumb name, but inherited from Frame and no better ideas.

Parameters
----------

PARAMTEXT

Notes
-----

Dumb name, but inherited from Frame and no better ideas.


# Py5Surface_set_resizable

Set true if we want to resize things (default is not resizable)

Parameters
----------

PARAMTEXT

Notes
-----

Set true if we want to resize things (default is not resizable)


# Py5Surface_set_title

Set the window (and dock, or whatever necessary) title.

Parameters
----------

PARAMTEXT

Notes
-----

Set the window (and dock, or whatever necessary) title.


# Py5Surface_set_visible

Show or hide the window.

Parameters
----------

PARAMTEXT

Notes
-----

Show or hide the window.


# Py5Surface_start_thread

Start the animation thread

Parameters
----------

PARAMTEXT

Notes
-----

Start the animation thread


# Py5Surface_stop_thread

Stop the animation thread (set it null)

Parameters
----------

PARAMTEXT

Notes
-----

Stop the animation thread (set it null)


# Sketch_abs

Calculates the absolute value (magnitude) of a number.

Parameters
----------

PARAMTEXT

Notes
-----

Calculates the absolute value (magnitude) of a number. The absolute value of a number is always positive.


# Sketch_acos

The inverse of , ``cos()`` ,, returns the arc cosine of a value.

Parameters
----------

PARAMTEXT

Notes
-----

The inverse of ``cos()`` , returns the arc cosine of a value. This function expects the values in the range of -1 to 1 and values are returned in the range ``0`` to ``pi (3.1415927)`` .


See Also
--------

Sketch.cos(float) : Calculates the cosine of an angle.

Sketch.asin(float) : The inverse of , ``sin()`` ,, returns the arc sine of a value.

Sketch.atan(float) : The inverse of , ``tan()`` ,, returns the arc tangent of a value.


# Sketch_alpha

Extracts the alpha value from a color.

Parameters
----------

PARAMTEXT

Notes
-----

Extracts the alpha value from a color.


See Also
--------

Py5Graphics.red(int) : Extracts the red value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.green(int) : Extracts the green value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.blue(int) : Extracts the blue value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.hue(int) : Extracts the hue value from a color.

Py5Graphics.saturation(int) : Extracts the saturation value from a color.

Py5Graphics.brightness(int) : Extracts the brightness value from a color.


# Sketch_ambient

Sets the ambient reflectance for shapes drawn to the screen.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the ambient reflectance for shapes drawn to the screen. This is combined with the ambient light component of environment. The color components set through the parameters define the reflectance. For example in the default color mode, setting v1=255, v2=126, v3=0, would cause all the red light to reflect and half of the green light to reflect. Used in combination with ``emissive()`` , ``specular()`` , and ``shininess()`` in setting the material properties of shapes.


See Also
--------

Py5Graphics.emissive(float, float, float) : Sets the emissive color of the material used for drawing shapes drawn to the screen.

Py5Graphics.specular(float, float, float) : Sets the specular color of the materials used for shapes drawn to the screen, which sets the color of hightlights.

Py5Graphics.shininess(float) : Sets the amount of gloss in the surface of shapes.


# Sketch_ambient_light

Adds an ambient light.

Parameters
----------

PARAMTEXT

Notes
-----

Adds an ambient light. Ambient light doesn't come from a specific direction, the rays have light have bounced around so much that objects are evenly lit from all sides. Ambient lights are almost always used in combination with other types of lights. Lights need to be included in the ``draw()`` to remain persistent in a looping program. Placing them in the ``setup()`` of a looping program will cause them to only have an effect the first time through the loop. The effect of the parameters is determined by the current color mode.


See Also
--------

Py5Graphics.lights() : Sets the default ambient light, directional light, falloff, and specular values.

Py5Graphics.directionalLight(float, float, float, float, float, float)

Py5Graphics.pointLight(float, float, float, float, float, float)

Py5Graphics.spotLight(float, float, float, float, float, float, float, float, float, float, float)


# Sketch_append

Expands an array by one element and adds data to the new position.

Parameters
----------

PARAMTEXT

Notes
-----

Expands an array by one element and adds data to the new position. The datatype of the ``element`` parameter must be the same as the datatype of the array.

When using an array of objects, the data returned from the function must be cast to the object array's data type. For example:<em>SomeClass[] items = (SomeClass[]) append(originalArray, element)</em>.


See Also
--------

Sketch.shorten(boolean[]) : Decreases an array by one element and returns the shortened array.

Sketch.expand(boolean[]) : Increases the size of an array.


# Sketch_apply_matrix

Multiplies the current matrix by the one specified through the parameters.

Parameters
----------

PARAMTEXT

Notes
-----

Multiplies the current matrix by the one specified through the parameters. This is very slow because it will try to calculate the inverse of the transform, so avoid it whenever possible. The equivalent function in OpenGL is glMultMatrix().


See Also
--------

Py5Graphics.pushMatrix()

Py5Graphics.popMatrix()

Py5Graphics.resetMatrix()

Py5Graphics.printMatrix()


# Sketch_arc

Draws an arc in the display window.

Parameters
----------

PARAMTEXT

Notes
-----

Draws an arc in the display window. Arcs are drawn along the outer edge of an ellipse defined by the ``x`` , ``y`` , ``width`` and ``height`` parameters. The origin or the arc's ellipse may be changed with the ``ellipse_mode()`` function. The ``start`` and ``stop`` parameters specify the angles at which to draw the arc.


See Also
--------

Sketch.ellipse(float, float, float, float) : Draws an ellipse (oval) in the display window.

Sketch.ellipseMode(int)

Sketch.radians(float) : Converts a degree measurement to its corresponding value in radians.

Sketch.degrees(float) : Converts a radian measurement to its corresponding value in degrees.


# Sketch_args

Command line options passed in from main().

Parameters
----------

PARAMTEXT

Notes
-----

Command line options passed in from main(). This does not include the arguments passed in to Sketch itself.


See Also
--------

Sketch.main : Convenience method so that Sketch.main("YourSketch", args) launches a sketch, rather than having to wrap it into a String array, and appending the 'args' array when not null.


# Sketch_args_disable_awt

Disable AWT so that LWJGL and others can run

Parameters
----------

PARAMTEXT

Notes
-----

Disable AWT so that LWJGL and others can run


# Sketch_args_display

Used by the PDE to suggest a display (set in prefs, passed on Run)

Parameters
----------

PARAMTEXT

Notes
-----

Used by the PDE to suggest a display (set in prefs, passed on Run)


# Sketch_args_editor_location

Position of the upper-lefthand corner of the editor window that launched this applet.

Parameters
----------

PARAMTEXT

Notes
-----

Position of the upper-lefthand corner of the editor window that launched this applet.


# Sketch_args_location

Location for where to position the applet window on screen.

Parameters
----------

PARAMTEXT

Notes
-----

Location for where to position the applet window on screen.

This is used by the editor to when saving the previous applet location, or could be used by other classes to launch at a specific position on-screen.


# Sketch_args_sketch_folder

Allows the user or PdeEditor to set a specific sketch folder path.

Parameters
----------

PARAMTEXT

Notes
-----

Allows the user or PdeEditor to set a specific sketch folder path.

Used by PdeEditor to pass in the location where saveFrame() and all that stuff should write things.


# Sketch_array_copy

Shortcut to copy the entire contents of the source into the destination array.

Parameters
----------

PARAMTEXT

Notes
-----

Copies an array (or part of an array) to another array. The ``src`` array is copied to the ``dst`` array, beginning at the position specified by ``src_pos`` and into the position specified by ``dst_pos`` . The number of elements to copy is determined by ``length`` . The simplified version with two arguments copies an entire array to another of the same size. It is equivalent to "arrayCopy(src, 0, dst, 0, src.length)". This function is far more efficient for copying array data than iterating through a ``for`` and copying each element.


See Also
--------

Sketch.concat(boolean[], boolean[]) : Concatenates two arrays.


# Sketch_arraycopy

Use arrayCopy() instead.

Parameters
----------

PARAMTEXT

Notes
-----

Use arrayCopy() instead.


# Sketch_asin

The inverse of , ``sin()`` ,, returns the arc sine of a value.

Parameters
----------

PARAMTEXT

Notes
-----

The inverse of ``sin()`` , returns the arc sine of a value. This function expects the values in the range of -1 to 1 and values are returned in the range ``-pi/2`` to ``pi/2`` .


See Also
--------

Sketch.sin(float) : Calculates the sine of an angle.

Sketch.acos(float) : The inverse of , ``cos()`` ,, returns the arc cosine of a value.

Sketch.atan(float) : The inverse of , ``tan()`` ,, returns the arc tangent of a value.


# Sketch_atan

The inverse of , ``tan()`` ,, returns the arc tangent of a value.

Parameters
----------

PARAMTEXT

Notes
-----

The inverse of ``tan()`` , returns the arc tangent of a value. This function expects the values in the range of -Infinity to Infinity (exclusive) and values are returned in the range ``-pi/2`` to ``pi/2`` .


See Also
--------

Sketch.tan(float) : Calculates the ratio of the sine and cosine of an angle.

Sketch.asin(float) : The inverse of , ``sin()`` ,, returns the arc sine of a value.

Sketch.acos(float) : The inverse of , ``cos()`` ,, returns the arc cosine of a value.


# Sketch_atan2

Calculates the angle (in radians) from a specified point to the coordinate origin as measured from the positive x-axis.

Parameters
----------

PARAMTEXT

Notes
-----

Calculates the angle (in radians) from a specified point to the coordinate origin as measured from the positive x-axis. Values are returned as a ``float`` in the range from ``pi`` to ``-pi`` . The ``atan2()`` function is most often used for orienting geometry to the position of the cursor.  Note: The y-coordinate of the point is the first parameter and the x-coordinate is the second due the the structure of calculating the tangent.


See Also
--------

Sketch.tan(float) : Calculates the ratio of the sine and cosine of an angle.


# Sketch_background

The , ``background()`` , function sets the color used for the background of the Processing window.

Parameters
----------

PARAMTEXT

Notes
-----

The ``background()`` function sets the color used for the background of the Processing window. The default background is light gray. In the ``draw()`` function, the background color is used to clear the display window at the beginning of each frame.

An image can also be used as the background for a sketch, however its width and height must be the same size as the sketch window. To resize an image 'b' to the size of the sketch window, use b.resize(width, height).

Images used as background will ignore the current ``tint()`` setting.

It is not possible to use transparency (alpha) in background colors with the main drawing surface, however they will work properly with ``create_graphics()`` .

Advanced
--------



Clear the background with a color that includes an alpha value. This can only be used with objects created by createGraphics(), because the main drawing surface cannot be set transparent.</p>

It might be tempting to use this function to partially clear the screen on each frame, however that's not how this function works. When calling background(), the pixels will be replaced with pixels that have that level of transparency. To do a semi-transparent overlay, use fill() with alpha and draw a rectangle.</p>


See Also
--------

Py5Graphics.stroke(float) : Sets the color used to draw lines and borders around shapes.

Py5Graphics.fill(float) : true if fill() is enabled, (read-only)

Py5Graphics.tint(float) : Sets the fill value for displaying images.

Py5Graphics.colorMode(int)


# Sketch_begin_camera

The , ``begin_camera()`` , and , ``end_camera()`` , functions enable advanced customization of the camera space.

Parameters
----------

PARAMTEXT

Notes
-----

The ``begin_camera()`` and ``end_camera()`` functions enable advanced customization of the camera space. The functions are useful if you want to more control over camera movement, however for most users, the ``camera()`` function will be sufficient.

The camera functions will replace any transformations (such as ``rotate()`` or ``translate()`` ) that occur before them in ``draw()`` , but they will not automatically replace the camera transform itself. For this reason, camera functions should be placed at the beginning of ``draw()`` (so that transformations happen afterwards), and the ``camera()`` function can be used after ``begin_camera()`` if you want to reset the camera before applying transformations.

This function sets the matrix mode to the camera matrix so calls such as ``translate()`` , ``rotate()`` , applyMatrix() and resetMatrix() affect the camera. ``begin_camera()`` should always be used with a following ``end_camera()`` and pairs of ``begin_camera()`` and ``end_camera()`` cannot be nested.


See Also
--------

Py5Graphics.camera() : Sets the position of the camera through setting the eye position, the center of the scene, and which axis is facing upward.

Py5Graphics.endCamera()

Py5Graphics.applyMatrix(PMatrix)

Py5Graphics.resetMatrix()

Py5Graphics.translate(float, float, float) : Specifies an amount to displace objects within the display window.

Py5Graphics.scale(float, float, float) : Increases or decreases the size of a shape by expanding and contracting vertices.


# Sketch_begin_contour



Parameters
----------

PARAMTEXT

Notes
-----




# Sketch_begin_raw

To create vectors from 3D data, use the , ``begin_raw()`` , and , ``end_raw()`` , commands.

Parameters
----------

PARAMTEXT

Notes
-----

To create vectors from 3D data, use the ``begin_raw()`` and ``end_raw()`` commands. These commands will grab the shape data just before it is rendered to the screen. At this stage, your entire scene is nothing but a long list of individual lines and triangles. This means that a shape created with ``sphere()`` function will be made up of hundreds of triangles, rather than a single object. Or that a multi-segment line shape (such as a curve) will be rendered as individual segments.

When using ``begin_raw()`` and ``end_raw()`` , it's possible to write to either a 2D or 3D renderer. For instance, ``begin_raw()`` with the PDF library will write the geometry as flattened triangles and lines, even if recording from the ``p3_d`` renderer.

If you want a background to show up in your files, use ``rect(0 0 width height)`` after setting the ``fill()`` to the background color. Otherwise the background will not be rendered to the file because the background is not shape.

Using ``hint(enable_depth_sort)`` can improve the appearance of 3D geometry drawn to 2D file formats. See the ``hint()`` reference for more details.

See examples in the reference for the ``pdf`` and ``dxf`` libraries for more information.


See Also
--------

Sketch.endRaw()

Sketch.hint(int)


# Sketch_begin_record

Opens a new file and all subsequent drawing functions are echoed to this file as well as the display window.

Parameters
----------

PARAMTEXT

Notes
-----

Opens a new file and all subsequent drawing functions are echoed to this file as well as the display window. The ``begin_record()`` function requires two parameters, the first is the renderer and the second is the file name. This function is always used with ``end_record()`` to stop the recording process and close the file.

Note that beginRecord() will only pick up any settings that happen after it has been called. For instance, if you call textFont() before beginRecord(), then that font will not be set for the file that you're recording to.


See Also
--------

Sketch.endRecord()


# Sketch_begin_shape

Using the , ``begin_shape()`` , and , ``end_shape()`` , functions allow creating more complex forms.

Parameters
----------

PARAMTEXT

Notes
-----

Using the ``begin_shape()`` and ``end_shape()`` functions allow creating more complex forms. ``begin_shape()`` begins recording vertices for a shape and ``end_shape()`` stops recording. The value of the ``mode`` parameter tells it which types of shapes to create from the provided vertices. With no mode specified, the shape can be any irregular polygon. The parameters available for beginShape() are POINTS, LINES, TRIANGLES, TRIANGLE_FAN, TRIANGLE_STRIP, QUADS, and QUAD_STRIP. After calling the ``begin_shape()`` function, a series of ``vertex()`` commands must follow. To stop drawing the shape, call ``end_shape()`` . The ``vertex()`` function with two parameters specifies a position in 2D and the ``vertex()`` function with three parameters specifies a position in 3D. Each shape will be outlined with the current stroke color and filled with the fill color.

Transformations such as ``translate()`` , ``rotate()`` , and ``scale()`` do not work within ``begin_shape()`` . It is also not possible to use other shapes, such as ``ellipse()`` or ``rect()`` within ``begin_shape()`` .

The P3D renderer settings allow ``stroke()`` and ``fill()`` settings to be altered per-vertex, however the default P2D renderer does not. Settings such as ``stroke_weight()`` , ``stroke_cap()`` , and ``stroke_join()`` cannot be changed while inside a ``begin_shape()`` / ``end_shape()`` block with any renderer.


See Also
--------

Py5Graphics.endShape()

Py5Graphics.vertex(float, float, float, float, float) : Used by renderer subclasses or Py5Shape to efficiently pass in already formatted vertex information.

Py5Graphics.curveVertex(float, float, float)

Py5Graphics.bezierVertex(float, float, float, float, float, float, float, float, float)


# Sketch_bezier

Draws a Bezier curve on the screen.

Parameters
----------

PARAMTEXT

Notes
-----

Draws a Bezier curve on the screen. These curves are defined by a series of anchor and control points. The first two parameters specify the first anchor point and the last two parameters specify the other anchor point. The middle parameters specify the control points which define the shape of the curve. Bezier curves were developed by French engineer Pierre Bezier. Using the 3D version requires rendering with P3D (see the Environment reference for more information).

Advanced
--------

Draw a cubic bezier curve. The first and last points are the on-curve points. The middle two are the 'control' points, or 'handles' in an application like Illustrator.

Identical to typing:

``
begin_shape()
vertex(x1 y1)
bezier_vertex(x2 y2 x3 y3 x4 y4)
end_shape()
``

In Postscript-speak, this would be:

``
moveto(x1 y1)
curveto(x2 y2 x3 y3 x4 y4)
``

If you were to try and continue that curve like so:

``
curveto(x5 y5 x6 y6 x7 y7)
``

This would be done in processing by adding these statements:

``
bezier_vertex(x5 y5 x6 y6 x7 y7)
``

To draw a quadratic (instead of cubic) curve, use the control point twice by doubling it:

``
bezier(x1 y1 cx cy cx cy x2 y2)
``


See Also
--------

Py5Graphics.bezierVertex(float, float, float, float, float, float)

Py5Graphics.curve(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a curved line on the screen.


# Sketch_bezier_detail

Sets the resolution at which Beziers display.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the resolution at which Beziers display. The default value is 20. This function is only useful when using the P3D renderer as the default P2D renderer does not use this information.


See Also
--------

Py5Graphics.curve(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a curved line on the screen.

Py5Graphics.curveVertex(float, float, float)

Py5Graphics.curveTightness(float)


# Sketch_bezier_point

Evaluates the Bezier at point t for points a, b, c, d.

Parameters
----------

PARAMTEXT

Notes
-----

Evaluates the Bezier at point t for points a, b, c, d. The parameter t varies between 0 and 1, a and d are points on the curve, and b and c are the control points. This can be done once with the x coordinates and a second time with the y coordinates to get the location of a bezier curve at t.

Advanced
--------

For instance, to convert the following example:

``
stroke(255 102 0)
line(85 20 10 10)
line(90 90 15 80)
stroke(0 0 0)
bezier(85 20 10 10 90 90 15 80)
// draw it in gray using 10 steps instead of the default 20 // this is a slower way to do it but useful if you need // to do things with the coordinates at each step stroke(128)
begin_shape(line_strip)
for (int i = 0
i<= 10
i++) {   float t = i / 10.0f
float x = bezier_point(85 10 90 15 t)
float y = bezier_point(20 10 90 80 t)
vertex(x y)
} end_shape()
``


See Also
--------

Py5Graphics.bezier(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a Bezier curve on the screen.

Py5Graphics.bezierVertex(float, float, float, float, float, float)

Py5Graphics.curvePoint(float, float, float, float, float)


# Sketch_bezier_tangent

Calculates the tangent of a point on a Bezier curve.

Parameters
----------

PARAMTEXT

Notes
-----

Calculates the tangent of a point on a Bezier curve. There is a good definition of<a href="http://en.wikipedia.org/wiki/Tangent"target="new"><em>tangent</em>on Wikipedia</a>.

Advanced
--------

Code submitted by Dave Bollinger (davol) for release 0136.


See Also
--------

Py5Graphics.bezier(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a Bezier curve on the screen.

Py5Graphics.bezierVertex(float, float, float, float, float, float)

Py5Graphics.curvePoint(float, float, float, float, float)


# Sketch_bezier_vertex

Specifies vertex coordinates for Bezier curves.

Parameters
----------

PARAMTEXT

Notes
-----

Specifies vertex coordinates for Bezier curves. Each call to ``bezier_vertex()`` defines the position of two control points and one anchor point of a Bezier curve, adding a new segment to a line or shape. The first time ``bezier_vertex()`` is used within a ``begin_shape()`` call, it must be prefaced with a call to ``vertex()`` to set the first anchor point. This function must be used between ``begin_shape()`` and ``end_shape()`` and only when there is no MODE parameter specified to ``begin_shape()`` . Using the 3D version requires rendering with P3D (see the Environment reference for more information).


See Also
--------

Py5Graphics.curveVertex(float, float, float)

Py5Graphics.vertex(float, float, float, float, float) : Used by renderer subclasses or Py5Shape to efficiently pass in already formatted vertex information.

Py5Graphics.quadraticVertex(float, float, float, float, float, float)

Py5Graphics.bezier(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a Bezier curve on the screen.


# Sketch_binary

Converts a byte, char, int, or color to a String containing the equivalent binary notation.

Parameters
----------

PARAMTEXT

Notes
-----

Converts a byte, char, int, or color to a String containing the equivalent binary notation. For example color(0, 102, 153, 255) will convert to the String "11111111000000000110011010011001". This function can help make your geeky debugging sessions much happier.

Note that the maximum number of digits is 32, because an int value can only represent up to 32 bits. Specifying more than 32 digits will simply shorten the string to 32 anyway.


See Also
--------

Sketch.unbinary(String) : Converts a String representation of a binary number to its equivalent integer value.

Sketch.hex(int,int) : Converts a byte, char, int, or color to a String containing the equivalent hexadecimal notation.

Sketch.unhex(String) : Converts a String representation of a hexadecimal number to its equivalent integer value.


# Sketch_blend

Blends a region of pixels into the image specified by the , ``img`` , parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Blends a region of pixels into the image specified by the ``img`` parameter. These copies utilize full alpha channel support and a choice of the following modes to blend the colors of source pixels (A) with the ones of pixels in the destination image (B):

BLEND - linear interpolation of colours: C = A*factor + B

ADD - additive blending with white clip: C = min(A*factor + B, 255)

SUBTRACT - subtractive blending with black clip: C = max(B - A*factor, 0)

DARKEST - only the darkest colour succeeds: C = min(A*factor, B)

LIGHTEST - only the lightest colour succeeds: C = max(A*factor, B)

DIFFERENCE - subtract colors from underlying image.

EXCLUSION - similar to DIFFERENCE, but less extreme.

MULTIPLY - Multiply the colors, result will always be darker.

SCREEN - Opposite multiply, uses inverse values of the colors.

OVERLAY - A mix of MULTIPLY and SCREEN. Multiplies dark values, and screens light values.

HARD_LIGHT - SCREEN when greater than 50% gray, MULTIPLY when lower.

SOFT_LIGHT - Mix of DARKEST and LIGHTEST. Works like OVERLAY, but not as harsh.

DODGE - Lightens light tones and increases contrast, ignores darks. Called "Color Dodge" in Illustrator and Photoshop.

BURN - Darker areas are applied, increasing contrast, ignores lights. Called "Color Burn" in Illustrator and Photoshop.

All modes use the alpha information (highest byte) of source image pixels as the blending factor. If the source and destination regions are different sizes, the image will be automatically resized to match the destination size. If the ``src_img`` parameter is not used, the display window is used as the source image.

As of release 0149, this function ignores ``image_mode()`` .


See Also
--------

Sketch.alpha(int) : Extracts the alpha value from a color.

Py5Image.copy(Py5Image, int, int, int, int, int, int, int, int) : Copies a region of pixels from one image into another.

Py5Image.blendColor(int,int,int)


# Sketch_blend_mode

This is a new reference entry for Processing 2.0.

Parameters
----------

PARAMTEXT

Notes
-----

This is a new reference entry for Processing 2.0. It will be updated shortly.


# Sketch_blue

Extracts the blue value from a color, scaled to match current , ``color_mode()`` ,.

Parameters
----------

PARAMTEXT

Notes
-----

Extracts the blue value from a color, scaled to match current ``color_mode()`` . This value is always returned as a  float so be careful not to assign it to an int value.

The ``blue()`` function is easy to use and undestand, but is slower than another technique. To achieve the same results when working in ``color_mode(rgb 255)`` , but with greater speed, use a bit mask to remove the other color components. For example, the following two lines of code are equivalent:
<pre>float r1 = blue(myColor);
float r2 = myColor&0xFF;</pre>


See Also
--------

Py5Graphics.red(int) : Extracts the red value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.green(int) : Extracts the green value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.alpha(int) : Extracts the alpha value from a color.

Py5Graphics.hue(int) : Extracts the hue value from a color.

Py5Graphics.saturation(int) : Extracts the saturation value from a color.

Py5Graphics.brightness(int) : Extracts the brightness value from a color.


# Sketch_box

A box is an extruded rectangle.

Parameters
----------

PARAMTEXT

Notes
-----

A box is an extruded rectangle. A box with equal dimension on all sides is a cube.


See Also
--------

Py5Graphics.sphere(float) : A sphere is a hollow ball made from tessellated triangles.


# Sketch_brightness

Extracts the brightness value from a color.

Parameters
----------

PARAMTEXT

Notes
-----

Extracts the brightness value from a color.


See Also
--------

Py5Graphics.red(int) : Extracts the red value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.green(int) : Extracts the green value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.blue(int) : Extracts the blue value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.alpha(int) : Extracts the alpha value from a color.

Py5Graphics.hue(int) : Extracts the hue value from a color.

Py5Graphics.saturation(int) : Extracts the saturation value from a color.


# Sketch_camera

Sets the position of the camera through setting the eye position, the center of the scene, and which axis is facing upward.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the position of the camera through setting the eye position, the center of the scene, and which axis is facing upward. Moving the eye position and the direction it is pointing (the center of the scene) allows the images to be seen from different angles. The version without any parameters sets the camera to the default position, pointing to the center of the display window with the Y axis as up. The default values are ``camera(width/2.0 height/2.0 (height/2.0) / tan(pi*30.0 / 180.0) width/2.0 height/2.0 0 0 1 0)`` . This function is similar to ``glu_look_at()`` in OpenGL, but it first clears the current camera settings.


See Also
--------

Py5Graphics.beginCamera()

Py5Graphics.endCamera()

Py5Graphics.frustum(float, float, float, float, float, float) : Sets a perspective matrix defined through the parameters.


# Sketch_ceil

Calculates the closest int value that is greater than or equal to the value of the parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Calculates the closest int value that is greater than or equal to the value of the parameter. For example, ``ceil(9.03)`` returns the value 10.


See Also
--------

Sketch.floor(float) : Calculates the closest int value that is less than or equal to the value of the parameter.

Sketch.round(float) : Calculates the integer closest to the , ``value`` , parameter.


# Sketch_check_alpha

Check the alpha on an image, using a really primitive loop.

Parameters
----------

PARAMTEXT

Notes
-----

Check the alpha on an image, using a really primitive loop.


# Sketch_check_extension

Get the compression-free extension for this filename.

Parameters
----------

PARAMTEXT

Notes
-----

Get the compression-free extension for this filename.


# Sketch_circle

Draws a circle to the screen.

Parameters
----------

PARAMTEXT

Notes
-----

Draws a circle to the screen. By default, the first two parameters set the location of the center, and the third sets the shape's width and height. The origin may be changed with the ``ellipse_mode()`` function.


See Also
--------

Sketch.ellipse(float, float, float, float) : Draws an ellipse (oval) in the display window.

Sketch.ellipseMode(int)


# Sketch_clear



Parameters
----------

PARAMTEXT

Notes
-----




# Sketch_clip

Limits the rendering to the boundaries of a rectangle defined by the parameters.

Parameters
----------

PARAMTEXT

Notes
-----

Limits the rendering to the boundaries of a rectangle defined by the parameters. The boundaries are drawn based on the state of the ``image_mode()`` fuction, either CORNER, CORNERS, or CENTER.


# Sketch_color

Creates colors for storing in variables of the , ``color`` , datatype.

Parameters
----------

PARAMTEXT

Notes
-----

Creates colors for storing in variables of the ``color`` datatype. The parameters are interpreted as RGB or HSB values depending on the current ``color_mode()`` . The default mode is RGB values from 0 to 255 and therefore, the function call ``color(255 204 0)`` will return a bright yellow color. More about how colors are stored can be found in the reference for the<a href="color_datatype.html">color</a>datatype.


See Also
--------

Sketch.colorMode(int)


# Sketch_color_mode

Changes the way Processing interprets color data.

Parameters
----------

PARAMTEXT

Notes
-----

Changes the way Processing interprets color data. By default, the parameters for ``fill()`` , ``stroke()`` , ``background()`` , and ``color()`` are defined by values between 0 and 255 using the RGB color model. The ``color_mode()`` function is used to change the numerical range used for specifying colors and to switch color systems. For example, calling ``color_mode(rgb 1.0)`` will specify that values are specified between 0 and 1. The limits for defining colors are altered by setting the parameters range1, range2, range3, and range 4.


See Also
--------

Py5Graphics.background(float) : The , ``background()`` , function sets the color used for the background of the Processing window.

Py5Graphics.fill(float) : true if fill() is enabled, (read-only)

Py5Graphics.stroke(float) : Sets the color used to draw lines and borders around shapes.


# Sketch_concat

Concatenates two arrays.

Parameters
----------

PARAMTEXT

Notes
-----

Concatenates two arrays. For example, concatenating the array { 1, 2, 3 } and the array { 4, 5, 6 } yields { 1, 2, 3, 4, 5, 6 }. Both parameters must be arrays of the same datatype.

When using an array of objects, the data returned from the function must be cast to the object array's data type. For example:<em>SomeClass[] items = (SomeClass[]) concat(array1, array2)</em>.


See Also
--------

Sketch.splice(boolean[], boolean, int) : Inserts a value or array of values into an existing array.

Sketch.arrayCopy(Object, int, Object, int, int)


# Sketch_constrain

Constrains a value to not exceed a maximum and minimum value.

Parameters
----------

PARAMTEXT

Notes
-----

Constrains a value to not exceed a maximum and minimum value.


See Also
--------

Sketch.max(float, float, float) : Determines the largest value in a sequence of numbers.

Sketch.min(float, float, float) : Determines the smallest value in a sequence of numbers.


# Sketch_copy

Copies a region of pixels from one image into another.

Parameters
----------

PARAMTEXT

Notes
-----

Copies a region of pixels from one image into another. If the source and destination regions aren't the same size, it will automatically resize source pixels to fit the specified target region. No alpha information is used in the process, however if the source image has an alpha channel set, it will be copied as well.

As of release 0149, this function ignores ``image_mode()`` .


See Also
--------

Py5Graphics.alpha(int) : Extracts the alpha value from a color.

Py5Image.blend(Py5Image, int, int, int, int, int, int, int, int, int) : Blends a region of pixels into the image specified by the , ``img`` , parameter.


# Sketch_cos

Calculates the cosine of an angle.

Parameters
----------

PARAMTEXT

Notes
-----

Calculates the cosine of an angle. This function expects the values of the ``angle`` parameter to be provided in radians (values from 0 to PI*2). Values are returned in the range -1 to 1.


See Also
--------

Sketch.sin(float) : Calculates the sine of an angle.

Sketch.tan(float) : Calculates the ratio of the sine and cosine of an angle.

Sketch.radians(float) : Converts a degree measurement to its corresponding value in radians.


# Sketch_create_font

Dynamically converts a font to the format used by Processing from either a font name that's installed on the computer, or from a .ttf or .otf file inside the sketches "data" folder.

Parameters
----------

PARAMTEXT

Notes
-----

Dynamically converts a font to the format used by Processing from either a font name that's installed on the computer, or from a .ttf or .otf file inside the sketches "data" folder. This function is an advanced feature for precise control. On most occasions you should create fonts through selecting "Create Font..." from the Tools menu.

Use the ``Py5Font.list()`` method to first determine the names for the fonts recognized by the computer and are compatible with this function. Because of limitations in Java, not all fonts can be used and some might work with one operating system and not others. When sharing a sketch with other people or posting it on the web, you may need to include a .ttf or .otf version of your font in the data directory of the sketch because other people might not have the font installed on their computer. Only fonts that can legally be distributed should be included with a sketch.

The ``size`` parameter states the font size you want to generate. The ``smooth`` parameter specifies if the font should be antialiased or not, and the ``charset`` parameter is an array of chars that specifies the characters to generate.

This function creates a bitmapped version of a font in the same manner as the Create Font tool. It loads a font by name, and converts it to a series of images based on the size of the font. When possible, the ``text()`` function will use a native font rather than the bitmapped version created behind the scenes with ``create_font()`` . For instance, when using P2D, the actual native version of the font will be employed by the sketch, improving drawing quality and performance. With the P3D renderer, the bitmapped version will be used. While this can drastically improve speed and appearance, results are poor when exporting if the sketch does not include the .otf or .ttf file, and the requested font is not available on the machine running the sketch.


See Also
--------

Py5Graphics.textFont(Py5Font, float)

Py5Graphics.text(String, float, float, float, float) : This does a basic number formatting, to avoid the generally ugly appearance of printing floats.

Sketch.loadFont(String)


# Sketch_create_graphics

Create an offscreen graphics surface for drawing, in this case for a renderer that writes to a file (such as PDF or DXF).

Parameters
----------

PARAMTEXT

Notes
-----

Creates and returns a new ``Py5Graphics`` object of the types P2D or P3D. Use this class if you need to draw into an off-screen graphics buffer. The PDF renderer requires the filename parameter. The DXF renderer should not be used with ``create_graphics()`` , it's only built for use with ``begin_raw()`` and ``end_raw()`` .

It's important to call any drawing functions between ``begin_draw()`` and ``end_draw()`` statements. This is also true for any functions that affect drawing, such as ``smooth()`` or ``color_mode()`` .

the main drawing surface which is completely opaque, surfaces created with ``create_graphics()`` can have transparency. This makes it possible to draw into a graphics and maintain the alpha channel. By using ``save()`` to write a PNG or TGA file, the transparency of the graphics object will be honored. Note that transparency levels are binary: pixels are either complete opaque or transparent. For the time being, this means that text characters will be opaque blocks. This will be fixed in a future release (<a href="http://code.google.com/p/processing/issues/detail?id=80">Issue 80</a>).

Advanced
--------

Create an offscreen Py5Graphics object for drawing. This can be used for bitmap or vector images drawing or rendering.

* Do not use "new Py5GraphicsXxxx()", use this method. This method ensures that internal variables are set up properly that tie the new graphics context back to its parent Sketch.
* The basic way to create bitmap images is to use the<A HREF="http://processing.org/reference/saveFrame_.html">saveFrame()</A>function.
* If you want to create a really large scene and write that, first make sure that you've allocated a lot of memory in the Preferences.
* If you want to create images that are larger than the screen, you should create your own Py5Graphics object, draw to that, and use<A HREF="http://processing.org/reference/save_.html">save()</A>.

``
Py5Graphics big
void setup() {   big = create_graphics(3000 3000)
big.begin_draw()
big.background(128)
big.line(20 1800 1800 900)
// etc..   big.end_draw()
// make sure the file is written to the sketch folder   big.save("big.tif")
}
``


* It's important to always wrap drawing to createGraphics() with beginDraw() and endDraw() (beginFrame() and endFrame() prior to revision 0115). The reason is that the renderer needs to know when drawing has stopped, so that it can update itself internally. This also handles calling the defaults() method, for people familiar with that.
* With Processing 0115 and later, it's possible to write images in formats other than the default .tga and .tiff. The exact formats and background information can be found in the developer's reference for<A HREF="http://dev.processing.org/reference/core/javadoc/processing/core/Py5Image.html#save(java.lang.String)">Py5Image.save()</A>.


See Also
--------

Py5Graphics.Py5Graphics


# Sketch_create_image

Creates a new Py5Image (the datatype for storing images).

Parameters
----------

PARAMTEXT

Notes
-----

Creates a new Py5Image (the datatype for storing images). This provides a fresh buffer of pixels to play with. Set the size of the buffer with the ``width`` and ``height`` parameters. The ``format`` parameter defines how the pixels are stored. See the Py5Image reference for more information.

Be sure to include all three parameters, specifying only the width and height (but no format) will produce a strange error.

Advanced users please note that createImage() should be used instead of the syntax<tt>new Py5Image()</tt>.

Advanced
--------

Preferred method of creating new Py5Image objects, ensures that a reference to the parent Sketch is included, which makes save() work without needing an absolute path.


# Sketch_create_input

This is a function for advanced programmers to open a Java InputStream.

Parameters
----------

PARAMTEXT

Notes
-----

This is a function for advanced programmers to open a Java InputStream. It's useful if you want to use the facilities provided by Sketch to easily open files from the data folder or from a URL, but want an InputStream object so that you can use other parts of Java to take more control of how the stream is read.

The filename passed in can be:
- A URL, for instance ``open_stream("http://processing.org/")`` 
- A file in the sketch's ``data`` folder
- The full path to a file to be opened locally (when running as an application)

If the requested item doesn't exist, null is returned. If not online, this will also check to see if the user is asking for a file whose name isn't properly capitalized. If capitalization is different, an error will be printed to the console. This helps prevent issues that appear when a sketch is exported to the web, where case sensitivity matters, as opposed to running from inside the Processing Development Environment on Windows or Mac OS, where case sensitivity is preserved but ignored.

If the file ends with ``.gz`` , the stream will automatically be gzip decompressed. If you don't want the automatic decompression, use the related function ``create_input_raw()`` .
In earlier releases, this function was called ``open_stream()`` .



Advanced
--------

Simplified method to open a Java InputStream.

This method is useful if you want to use the facilities provided by Sketch to easily open things from the data folder or from a URL, but want an InputStream object so that you can use other Java methods to take more control of how the stream is read.

If the requested item doesn't exist, null is returned. (Prior to 0096, die() would be called, killing the applet)

For 0096+, the "data" folder is exported intact with subfolders, and openStream() properly handles subdirectories from the data folder

If not online, this will also check to see if the user is asking for a file whose name isn't properly capitalized. This helps prevent issues when a sketch is exported to the web, where case sensitivity matters, as opposed to Windows and the Mac OS default where case sensitivity is preserved but ignored.

It is strongly recommended that libraries use this method to open data files, so that the loading sequence is handled in the same way as functions like loadBytes(), loadImage(), etc.

The filename passed in can be:

* A URL, for instance openStream("http://processing.org/");
* A file in the sketch's data folder
* Another file to be opened locally (when running as an application)


See Also
--------

Sketch.createOutput(String)

Sketch.selectOutput(String,String)

Sketch.selectInput(String,String)


# Sketch_create_input_raw

Call openStream() without automatic gzip decompression.

Parameters
----------

PARAMTEXT

Notes
-----

Call openStream() without automatic gzip decompression.


# Sketch_create_output

Similar to , ``create_input()`` ,, this creates a Java , ``_output_stream`` , for a given filename or path.

Parameters
----------

PARAMTEXT

Notes
-----

Similar to ``create_input()`` , this creates a Java ``_output_stream`` for a given filename or path. The file will be created in the sketch folder, or in the same folder as an exported application.

If the path does not exist, intermediate folders will be created. If an exception occurs, it will be printed to the console, and ``null`` will be returned.

This function is a convenience over the Java approach that requires you to 1) create a FileOutputStream object, 2) determine the exact file location, and 3) handle exceptions. Exceptions are handled internally by the function, which is more appropriate for "sketch" projects.

If the output filename ends with ``.gz`` , the output will be automatically GZIP compressed as it is written.


See Also
--------

Sketch.createInput(String)

Sketch.selectOutput(String,String)


# Sketch_create_path

Takes a path and creates any in-between folders if they don't already exist.

Parameters
----------

PARAMTEXT

Notes
-----

Takes a path and creates any in-between folders if they don't already exist. Useful when trying to save to a subfolder that may not actually exist.


# Sketch_create_primary_graphics

Create default renderer, likely to be resized, but needed for surface init.

Parameters
----------

PARAMTEXT

Notes
-----

Create default renderer, likely to be resized, but needed for surface init.


# Sketch_create_reader

Creates a , ``_buffered_reader`` , object that can be used to read files line-by-line as individual , ``_string`` , objects.

Parameters
----------

PARAMTEXT

Notes
-----

Creates a ``_buffered_reader`` object that can be used to read files line-by-line as individual ``_string`` objects. This is the complement to the ``create_writer()`` function.

Starting with Processing release 0134, all files loaded and saved by the Processing API use UTF-8 encoding. In previous releases, the default encoding for your platform was used, which causes problems when files are moved to other platforms.


See Also
--------

Sketch.createWriter(String)


# Sketch_create_shape



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Py5Shape.endShape()

Sketch.loadShape(String)


# Sketch_create_temp_file

Creates a temporary file based on the name/extension of another file and in the same parent directory.

Parameters
----------

PARAMTEXT

Notes
-----

Creates a temporary file based on the name/extension of another file and in the same parent directory. Ensures that the same extension is used (i.e. so that .gz files are gzip compressed on output) and that it's done from the same directory so that renaming the file later won't cross file system boundaries.


# Sketch_create_writer

Creates a new file in the sketch folder, and a , ``_print_writer`` , object to write to it.

Parameters
----------

PARAMTEXT

Notes
-----

Creates a new file in the sketch folder, and a ``_print_writer`` object to write to it. For the file to be made correctly, it should be flushed and must be closed with its ``flush()`` and ``close()`` methods (see above example).

Starting with Processing release 0134, all files loaded and saved by the Processing API use UTF-8 encoding. In previous releases, the default encoding for your platform was used, which causes problems when files are moved to other platforms.


See Also
--------

Sketch.createReader


# Sketch_cursor

Sets the cursor to a predefined symbol, an image, or makes it visible if already hidden.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the cursor to a predefined symbol, an image, or makes it visible if already hidden. If you are trying to set an image as the cursor, it is recommended to make the size 16x16 or 32x32 pixels. It is not possible to load an image as the cursor if you are exporting your program for the Web and not all MODES work with all Web browsers. The values for parameters ``x`` and ``y`` must be less than the dimensions of the image.

Setting or hiding the cursor generally does not work with "Present" mode (when running full-screen).

Advanced
--------

Set a custom cursor to an image with a specific hotspot. Only works with JDK 1.2 and later. Currently seems to be broken on Java 1.4 for Mac OS X

Based on code contributed by Amit Pitaru, plus additional code to handle Java versions via reflection by Jonathan Feinberg. Reflection removed for release 0128 and later.


See Also
--------

Sketch.noCursor()


# Sketch_curve

Draws a curved line on the screen.

Parameters
----------

PARAMTEXT

Notes
-----

Draws a curved line on the screen. The first and second parameters specify the beginning control point and the last two parameters specify the ending control point. The middle parameters specify the start and stop of the curve. Longer curves can be created by putting a series of ``curve()`` functions together or using ``curve_vertex()`` . An additional function called ``curve_tightness()`` provides control for the visual quality of the curve. The ``curve()`` function is an implementation of Catmull-Rom splines. Using the 3D version requires rendering with P3D (see the Environment reference for more information).

Advanced
--------

As of revision 0070, this function no longer doubles the first and last points. The curves are a bit more boring, but it's more mathematically correct, and properly mirrored in curvePoint().

Identical to typing out:

``
begin_shape()
curve_vertex(x1 y1)
curve_vertex(x2 y2)
curve_vertex(x3 y3)
curve_vertex(x4 y4)
end_shape()
``


See Also
--------

Py5Graphics.curveVertex(float, float)

Py5Graphics.curveTightness(float)

Py5Graphics.bezier(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a Bezier curve on the screen.


# Sketch_curve_detail

Sets the resolution at which curves display.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the resolution at which curves display. The default value is 20. This function is only useful when using the P3D renderer as the default P2D renderer does not use this information.


See Also
--------

Py5Graphics.curve(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a curved line on the screen.

Py5Graphics.curveVertex(float, float)

Py5Graphics.curveTightness(float)


# Sketch_curve_point

Evalutes the curve at point t for points a, b, c, d.

Parameters
----------

PARAMTEXT

Notes
-----

Evalutes the curve at point t for points a, b, c, d. The parameter t varies between 0 and 1, a and d are the control points, and b and c are the points on the curve. This can be done once with the x coordinates and a second time with the y coordinates to get the location of a curve at t.


See Also
--------

Py5Graphics.curve(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a curved line on the screen.

Py5Graphics.curveVertex(float, float)

Py5Graphics.bezierPoint(float, float, float, float, float)


# Sketch_curve_tangent

Calculates the tangent of a point on a curve.

Parameters
----------

PARAMTEXT

Notes
-----

Calculates the tangent of a point on a curve. There's a good definition of<em><a href="http://en.wikipedia.org/wiki/Tangent"target="new">tangent</em>on Wikipedia</a>.

Advanced
--------

Code thanks to Dave Bollinger (Bug #715)


See Also
--------

Py5Graphics.curve(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a curved line on the screen.

Py5Graphics.curveVertex(float, float)

Py5Graphics.curvePoint(float, float, float, float, float)

Py5Graphics.bezierTangent(float, float, float, float, float)


# Sketch_curve_tightness

Modifies the quality of forms created with , ``curve()`` , and , ``curve_vertex()`` ,.

Parameters
----------

PARAMTEXT

Notes
-----

Modifies the quality of forms created with ``curve()`` and ``curve_vertex()`` . The parameter ``squishy`` determines how the curve fits to the vertex points. The value 0.0 is the default value for ``squishy`` (this value defines the curves to be Catmull-Rom splines) and the value 1.0 connects all the points with straight lines. Values within the range -5.0 and 5.0 will deform the curves but will leave them recognizable and as values increase in magnitude, they will continue to deform.


See Also
--------

Py5Graphics.curve(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a curved line on the screen.

Py5Graphics.curveVertex(float, float)


# Sketch_curve_vertex

Specifies vertex coordinates for curves.

Parameters
----------

PARAMTEXT

Notes
-----

Specifies vertex coordinates for curves. This function may only be used between ``begin_shape()`` and ``end_shape()`` and only when there is no MODE parameter specified to ``begin_shape()`` . The first and last points in a series of ``curve_vertex()`` lines will be used to guide the beginning and end of a the curve. A minimum of four points is required to draw a tiny curve between the second and third points. Adding a fifth point with ``curve_vertex()`` will draw the curve between the second, third, and fourth points. The ``curve_vertex()`` function is an implementation of Catmull-Rom splines. Using the 3D version requires rendering with P3D (see the Environment reference for more information).


See Also
--------

Py5Graphics.curve(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a curved line on the screen.

Py5Graphics.beginShape(int)

Py5Graphics.endShape(int)

Py5Graphics.vertex(float, float, float, float, float) : Used by renderer subclasses or Py5Shape to efficiently pass in already formatted vertex information.

Py5Graphics.bezier(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a Bezier curve on the screen.

Py5Graphics.quadraticVertex(float, float, float, float, float, float)


# Sketch_data_file

Return a full path to an item in the data folder as a File object.

Parameters
----------

PARAMTEXT

Notes
-----

Return a full path to an item in the data folder as a File object. See the dataPath() method for more information.


# Sketch_data_path

``_this function almost certainly does not do the thing you want it to.`` , The data path is handled differently on each platform, and should not be considered a location to write files.

Parameters
----------

PARAMTEXT

Notes
-----

``_this function almost certainly does not do the thing you want it to.`` The data path is handled differently on each platform, and should not be considered a location to write files. It should also not be assumed that this location can be read from or listed. This function is used internally as a possible location for reading files. It's still "public" as a holdover from earlier code.

Libraries should use createInput() to get an InputStream or createOutput() to get an OutputStream. sketchPath() can be used to get a location relative to the sketch. Again, ``do not`` use this to get relative locations of files. You'll be disappointed when your app runs on different platforms.


# Sketch_day

Processing communicates with the clock on your computer.

Parameters
----------

PARAMTEXT

Notes
-----

Processing communicates with the clock on your computer. The ``day()`` function returns the current day as a value from 1 - 31.

Advanced
--------

Get the current day of the month (1 through 31).

If you're looking for the day of the week (M-F or whatever) or day of the year (1..365) then use java's Calendar.get()


See Also
--------

Sketch.millis() : Returns the number of milliseconds (thousandths of a second) since starting an applet.

Sketch.second() : Processing communicates with the clock on your computer.

Sketch.minute() : Processing communicates with the clock on your computer.

Sketch.hour() : Processing communicates with the clock on your computer.

Sketch.month() : Processing communicates with the clock on your computer.

Sketch.year() : Processing communicates with the clock on your computer.


# Sketch_default_width

Default width and height for sketch when not specified

Parameters
----------

PARAMTEXT

Notes
-----

Default width and height for sketch when not specified


# Sketch_degrees

Converts a radian measurement to its corresponding value in degrees.

Parameters
----------

PARAMTEXT

Notes
-----

Converts a radian measurement to its corresponding value in degrees. Radians and degrees are two ways of measuring the same thing. There are 360 degrees in a circle and 2*PI radians in a circle. For example, 90°= PI/2 = 1.5707964. All trigonometric functions in Processing require their parameters to be specified in radians.


See Also
--------

Sketch.radians(float) : Converts a degree measurement to its corresponding value in radians.


# Sketch_delay

The delay() function causes the program to halt for a specified time.

Parameters
----------

PARAMTEXT

Notes
-----

The delay() function causes the program to halt for a specified time. Delay times are specified in thousandths of a second. For example, running delay(3000) will stop the program for three seconds and delay(500) will stop the program for a half-second. The screen only updates when the end of draw() is reached, so delay() cannot be used to slow down drawing. For instance, you cannot use delay() to control the timing of an animation. The delay() function should only be used for pausing scripts (i.e. a script that needs to pause a few seconds before attempting a download, or a sketch that needs to wait a few milliseconds before reading from the serial port).


See Also
--------

Sketch.frameRate

Sketch.draw() : Called directly after , ``setup()`` , and continuously executes the lines of code contained inside its block until the program is stopped or , ``no_loop()`` , is called.


# Sketch_die

Function for an applet/application to kill itself and display an error.

Parameters
----------

PARAMTEXT

Notes
-----

Function for an applet/application to kill itself and display an error. Mostly this is here to be improved later.


# Sketch_directional_light

Adds a directional light.

Parameters
----------

PARAMTEXT

Notes
-----

Adds a directional light. Directional light comes from one direction and is stronger when hitting a surface squarely and weaker if it hits at a a gentle angle. After hitting a surface, a directional lights scatters in all directions. Lights need to be included in the ``draw()`` to remain persistent in a looping program. Placing them in the ``setup()`` of a looping program will cause them to only have an effect the first time through the loop. The affect of the ``v1`` , ``v2`` , and ``v3`` parameters is determined by the current color mode. The ``nx`` , ``ny`` , and ``nz`` parameters specify the direction the light is facing. For example, setting ``ny`` to -1 will cause the geometry to be lit from below (the light is facing directly upward).


See Also
--------

Py5Graphics.lights() : Sets the default ambient light, directional light, falloff, and specular values.

Py5Graphics.ambientLight(float, float, float, float, float, float)

Py5Graphics.pointLight(float, float, float, float, float, float)

Py5Graphics.spotLight(float, float, float, float, float, float, float, float, float, float, float)


# Sketch_display_density

This function returns the number "2" if the screen is a high-density screen (called a Retina display on OS X or high-dpi on Windows and Linux) and a "1" if not.

Parameters
----------

PARAMTEXT

Notes
-----

This function returns the number "2" if the screen is a high-density screen (called a Retina display on OS X or high-dpi on Windows and Linux) and a "1" if not. This information is useful for a program to adapt to run at double the pixel density on a screen that supports it.


See Also
--------

Sketch.pixelDensity(int)

Sketch.size(int,int) : Defines the dimension of the display window in units of pixels.


# Sketch_display_height

System variable that stores the height of the computer screen.

Parameters
----------

PARAMTEXT

Notes
-----

System variable that stores the height of the computer screen. For example, if the current screen resolution is 1024x768, ``display_width`` is 1024 and ``display_height`` is 768. These dimensions are useful when exporting full-screen applications.

To ensure that the sketch takes over the entire screen, use "Present" instead of "Run". Otherwise the window will still have a frame border around it and not be placed in the upper corner of the screen. On Mac OS X, the menu bar will remain present unless "Present" mode is used.


# Sketch_display_width

System variable which stores the width of the computer screen.

Parameters
----------

PARAMTEXT

Notes
-----

System variable which stores the width of the computer screen. For example, if the current screen resolution is 1024x768, ``display_width`` is 1024 and ``display_height`` is 768. These dimensions are useful when exporting full-screen applications.

To ensure that the sketch takes over the entire screen, use "Present" instead of "Run". Otherwise the window will still have a frame border around it and not be placed in the upper corner of the screen. On Mac OS X, the menu bar will remain present unless "Present" mode is used.


# Sketch_dispose

Called to dispose of resources and shut down the sketch.

Parameters
----------

PARAMTEXT

Notes
-----

Called to dispose of resources and shut down the sketch. Destroys the thread, dispose the renderer,and notify listeners.

Not to be called or overriden by users. If called multiple times, will only notify listeners once. Register a dispose listener instead.


# Sketch_dist

Calculates the distance between two points.

Parameters
----------

PARAMTEXT

Notes
-----

Calculates the distance between two points.


# Sketch_dmouse_x

Previous mouseX/Y for the draw loop, separated out because this is separate from the pmouseX/Y when inside the mouse event handlers.

Parameters
----------

PARAMTEXT

Notes
-----

Previous mouseX/Y for the draw loop, separated out because this is separate from the pmouseX/Y when inside the mouse event handlers. See emouseX/Y for an explanation.


# Sketch_dmouse_y

Previous mouseX/Y for the draw loop, separated out because this is separate from the pmouseX/Y when inside the mouse event handlers.

Parameters
----------

PARAMTEXT

Notes
-----

Previous mouseX/Y for the draw loop, separated out because this is separate from the pmouseX/Y when inside the mouse event handlers. See emouseX/Y for an explanation.


# Sketch_draw

Called directly after , ``setup()`` , and continuously executes the lines of code contained inside its block until the program is stopped or , ``no_loop()`` , is called.

Parameters
----------

PARAMTEXT

Notes
-----

Called directly after ``setup()`` and continuously executes the lines of code contained inside its block until the program is stopped or ``no_loop()`` is called. The ``draw()`` function is called automatically and should never be called explicitly. It should always be controlled with ``no_loop()`` , ``redraw()`` and ``loop()`` . After ``no_loop()`` stops the code in ``draw()`` from executing, ``redraw()`` causes the code inside ``draw()`` to execute once and ``loop()`` will causes the code inside ``draw()`` to execute continuously again. The number of times ``draw()`` executes in each second may be controlled with ``frame_rate()`` function. There can only be one ``draw()`` function for each sketch and ``draw()`` must exist if you want the code to run continuously or to process events such as ``mouse_pressed()`` . Sometimes, you might have an empty call to ``draw()`` in your program as shown in the above example.


See Also
--------

Sketch.setup() : The , ``setup()`` , function is called once when the program starts.

Sketch.loop() : Causes Processing to continuously execute the code within , ``draw()`` ,.

Sketch.noLoop()

Sketch.redraw() : flag set to true when a redraw is asked for by the user

Sketch.frameRate(float)

Py5Graphics.background(float, float, float, float) : The , ``background()`` , function sets the color used for the background of the Processing window.


# Sketch_edge

Sets whether the upcoming vertex is part of an edge.

Parameters
----------

PARAMTEXT

Notes
-----

Sets whether the upcoming vertex is part of an edge. Equivalent to glEdgeFlag(), for people familiar with OpenGL.


# Sketch_ellipse

Draws an ellipse (oval) in the display window.

Parameters
----------

PARAMTEXT

Notes
-----

Draws an ellipse (oval) in the display window. An ellipse with an equal ``width`` and ``height`` is a circle. The first two parameters set the location, the third sets the width, and the fourth sets the height. The origin may be changed with the ``ellipse_mode()`` function.


See Also
--------

Sketch.ellipseMode(int)

Sketch.arc(float, float, float, float, float, float) : Draws an arc in the display window.


# Sketch_ellipse_mode

The origin of the ellipse is modified by the , ``ellipse_mode()`` , function.

Parameters
----------

PARAMTEXT

Notes
-----

The origin of the ellipse is modified by the ``ellipse_mode()`` function. The default configuration is ``ellipse_mode(center)`` , which specifies the location of the ellipse as the center of the shape. The ``radius`` mode is the same, but the width and height parameters to ``ellipse()`` specify the radius of the ellipse, rather than the diameter. The ``corner`` mode draws the shape from the upper-left corner of its bounding box. The ``corners`` mode uses the four parameters to ``ellipse()`` to set two opposing corners of the ellipse's bounding box. The parameter must be written in ALL CAPS because Processing is a case-sensitive language.


See Also
--------

Sketch.ellipse(float, float, float, float) : Draws an ellipse (oval) in the display window.

Sketch.arc(float, float, float, float, float, float) : Draws an arc in the display window.


# Sketch_emissive

Sets the emissive color of the material used for drawing shapes drawn to the screen.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the emissive color of the material used for drawing shapes drawn to the screen. Used in combination with ``ambient()`` , ``specular()`` , and ``shininess()`` in setting the material properties of shapes.


See Also
--------

Py5Graphics.ambient(float, float, float) : Sets the ambient reflectance for shapes drawn to the screen.

Py5Graphics.specular(float, float, float) : Sets the specular color of the materials used for shapes drawn to the screen, which sets the color of hightlights.

Py5Graphics.shininess(float) : Sets the amount of gloss in the surface of shapes.


# Sketch_emouse_x

The pmouseX/Y for the event handlers (mousePressed(), mouseDragged() etc) these are different because mouse events are queued to the end of draw, so the previous position has to be updated on each event, as opposed to the pmouseX/Y that's used inside draw, which is expected to be updated once per trip through draw().

Parameters
----------

PARAMTEXT

Notes
-----

The pmouseX/Y for the event handlers (mousePressed(), mouseDragged() etc) these are different because mouse events are queued to the end of draw, so the previous position has to be updated on each event, as opposed to the pmouseX/Y that's used inside draw, which is expected to be updated once per trip through draw().


# Sketch_emouse_y

The pmouseX/Y for the event handlers (mousePressed(), mouseDragged() etc) these are different because mouse events are queued to the end of draw, so the previous position has to be updated on each event, as opposed to the pmouseX/Y that's used inside draw, which is expected to be updated once per trip through draw().

Parameters
----------

PARAMTEXT

Notes
-----

The pmouseX/Y for the event handlers (mousePressed(), mouseDragged() etc) these are different because mouse events are queued to the end of draw, so the previous position has to be updated on each event, as opposed to the pmouseX/Y that's used inside draw, which is expected to be updated once per trip through draw().


# Sketch_end_camera

The , ``begin_camera()`` , and , ``end_camera()`` , functions enable advanced customization of the camera space.

Parameters
----------

PARAMTEXT

Notes
-----

The ``begin_camera()`` and ``end_camera()`` functions enable advanced customization of the camera space. Please see the reference for ``begin_camera()`` for a description of how the functions are used.


See Also
--------

Py5Graphics.beginCamera()

Py5Graphics.camera(float, float, float, float, float, float, float, float, float) : Sets the position of the camera through setting the eye position, the center of the scene, and which axis is facing upward.


# Sketch_end_contour



Parameters
----------

PARAMTEXT

Notes
-----




# Sketch_end_raw

Complement to , ``begin_raw()`` ,; they must always be used together.

Parameters
----------

PARAMTEXT

Notes
-----

Complement to ``begin_raw()`` ; they must always be used together. See the ``begin_raw()`` reference for details.


See Also
--------

Sketch.beginRaw(String, String)


# Sketch_end_record

Stops the recording process started by , ``begin_record()`` , and closes the file.

Parameters
----------

PARAMTEXT

Notes
-----

Stops the recording process started by ``begin_record()`` and closes the file.


See Also
--------

Sketch.beginRecord(String, String)


# Sketch_end_shape

The , ``end_shape()`` , function is the companion to , ``begin_shape()`` , and may only be called after , ``begin_shape()`` ,.

Parameters
----------

PARAMTEXT

Notes
-----

The ``end_shape()`` function is the companion to ``begin_shape()`` and may only be called after ``begin_shape()`` . When ``endshape()`` is called, all of image data defined since the previous call to ``begin_shape()`` is written into the image buffer. The constant CLOSE as the value for the MODE parameter to close the shape (to connect the beginning and the end).


See Also
--------

Py5Graphics.beginShape(int)


# Sketch_exec

Alternative version of exec() that retrieves stdout and stderr into the StringList objects provided.

Parameters
----------

PARAMTEXT

Notes
-----

Pass a set of arguments directly to the command line. Uses Java's<A HREF="https://docs.oracle.com/javase/8/docs/api/java/lang/Runtime.html#exec-java.lang.String:A-">Runtime.exec()</A>method. This is different from the<A HREF="https://processing.org/reference/launch_.html">launch()</A>method, which uses the operating system's launcher to open the files. It's always a good idea to use a full path to the executable here.<pre>exec("/usr/bin/say", "welcome to the command line");</pre>Or if you want to wait until it's completed, something like this:<pre>Process p = exec("/usr/bin/say", "waiting until done"); try {   int result = p.waitFor();   println("the process returned " + result); } catch (InterruptedException e) { }</pre>You can also get the system output and error streams from the Process object, but that's more that we'd like to cover here.


# Sketch_exit

Quits/stops/exits the program.

Parameters
----------

PARAMTEXT

Notes
-----

Quits/stops/exits the program. Programs without a ``draw()`` function exit automatically after the last line has run, but programs with ``draw()`` run continuously until the program is manually stopped or ``exit()`` is run.

Rather than terminating immediately, ``exit()`` will cause the sketch to exit after ``draw()`` has completed (or after ``setup()`` completes if called during the ``setup()`` function).

For Java programmers, this is<em>not</em>the same as System.exit(). Further, System.exit() should not be used because closing out an application while ``draw()`` is running may cause a crash (particularly with P3D).


# Sketch_exit_actual

Some subclasses (I'm looking at you, processing.py) might wish to do something other than actually terminate the JVM.

Parameters
----------

PARAMTEXT

Notes
-----

Some subclasses (I'm looking at you, processing.py) might wish to do something other than actually terminate the JVM. This gives them a chance to do whatever they have in mind when cleaning up.


# Sketch_exit_called

true if exit() has been called so that things shut down once the main thread kicks off.

Parameters
----------

PARAMTEXT

Notes
-----

true if exit() has been called so that things shut down once the main thread kicks off.


# Sketch_exp

Returns Euler's number ,<i>,e,</i>, (2.71828...) raised to the power of the , ``value`` , parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Returns Euler's number<i>e</i>(2.71828...) raised to the power of the ``value`` parameter.


# Sketch_expand

Increases the size of an array.

Parameters
----------

PARAMTEXT

Notes
-----

Increases the size of an array. By default, this function doubles the size of the array, but the optional ``new_size`` parameter provides precise control over the increase in size.

When using an array of objects, the data returned from the function must be cast to the object array's data type. For example:<em>SomeClass[] items = (SomeClass[]) expand(originalArray)</em>.


See Also
--------

Sketch.shorten(boolean[]) : Decreases an array by one element and returns the shortened array.


# Sketch_external

true if this sketch is being run by the PDE

Parameters
----------

PARAMTEXT

Notes
-----

true if this sketch is being run by the PDE


# Sketch_external_move

When run externally to a PDE Editor, this is sent by the applet whenever the window is moved.

Parameters
----------

PARAMTEXT

Notes
-----

When run externally to a PDE Editor, this is sent by the applet whenever the window is moved.

This is used so that the editor can re-open the sketch window in the same position as the user last left it.


# Sketch_external_stop

When run externally to a PdeEditor, this is sent by the sketch when it quits.

Parameters
----------

PARAMTEXT

Notes
-----

When run externally to a PdeEditor, this is sent by the sketch when it quits.


# Sketch_fill

Sets the color used to fill shapes.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the color used to fill shapes. For example, if you run ``fill(204 102 0)`` , all subsequent shapes will be filled with orange. This color is either specified in terms of the RGB or HSB color depending on the current ``color_mode()`` (the default color space is RGB, with each value in the range from 0 to 255).

When using hexadecimal notation to specify a color, use "#" or "0x" before the values (e.g. #CCFFAA, 0xFFCCFFAA). The # syntax uses six digits to specify a color (the way colors are specified in HTML and CSS). When using the hexadecimal notation starting with "0x", the hexadecimal value must be specified with eight characters; the first two characters define the alpha component and the remainder the red, green, and blue components.

The value for the parameter "gray" must be less than or equal to the current maximum value as specified by ``color_mode()`` . The default maximum value is 255.

To change the color of an image (or a texture), use tint().


See Also
--------

Py5Graphics.noFill()

Py5Graphics.stroke(int, float) : Sets the color used to draw lines and borders around shapes.

Py5Graphics.noStroke()

Py5Graphics.tint(int, float) : Sets the fill value for displaying images.

Py5Graphics.background(float, float, float, float) : The , ``background()`` , function sets the color used for the background of the Processing window.

Py5Graphics.colorMode(int, float, float, float, float)


# Sketch_filter

Filters an image as defined by one of the following modes:,
,
,THRESHOLD - converts the image to black and white pixels depending if they are above or below the threshold defined by the level parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Filters an image as defined by one of the following modes:

THRESHOLD - converts the image to black and white pixels depending if they are above or below the threshold defined by the level parameter. The level must be between 0.0 (black) and 1.0(white). If no level is specified, 0.5 is used.

GRAY - converts any colors in the image to grayscale equivalents

INVERT - sets each pixel to its inverse value

POSTERIZE - limits each channel of the image to the number of colors specified as the level parameter

BLUR - executes a Guassian blur with the level parameter specifying the extent of the blurring. If no level parameter is used, the blur is equivalent to Guassian blur of radius 1

OPAQUE - sets the alpha channel to entirely opaque

ERODE - reduces the light areas with the amount defined by the level parameter

DILATE - increases the light areas with the amount defined by the level parameter

Advanced
--------

Method to apply a variety of basic filters to this image.



* filter(BLUR) provides a basic blur.
* filter(GRAY) converts the image to grayscale based on luminance.
* filter(INVERT) will invert the color components in the image.
* filter(OPAQUE) set all the high bits in the image to opaque
* filter(THRESHOLD) converts the image to black and white.
* filter(DILATE) grow white/light areas
* filter(ERODE) shrink white/light areas
Luminance conversion code contributed by<A HREF="http://www.toxi.co.uk">toxi</A><P/>Gaussian blur code contributed by<A HREF="http://incubator.quasimondo.com">Mario Klingemann</A>


# Sketch_finished

true if the sketch has stopped permanently.

Parameters
----------

PARAMTEXT

Notes
-----

true if the sketch has stopped permanently.


# Sketch_first_mouse

Used to set pmouseX/Y to mouseX/Y the first time mouseX/Y are used, otherwise pmouseX/Y are always zero, causing a nasty jump.

Parameters
----------

PARAMTEXT

Notes
-----

Used to set pmouseX/Y to mouseX/Y the first time mouseX/Y are used, otherwise pmouseX/Y are always zero, causing a nasty jump.

Just using (frameCount == 0) won't work since mouseXxxxx() may not be called until a couple frames into things.


# Sketch_floor

Calculates the closest int value that is less than or equal to the value of the parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Calculates the closest int value that is less than or equal to the value of the parameter.


See Also
--------

Sketch.ceil(float) : Calculates the closest int value that is greater than or equal to the value of the parameter.

Sketch.round(float) : Calculates the integer closest to the , ``value`` , parameter.


# Sketch_focused

Confirms if a Processing program is "focused", meaning that it is active and will accept input from mouse or keyboard.

Parameters
----------

PARAMTEXT

Notes
-----

Confirms if a Processing program is "focused", meaning that it is active and will accept input from mouse or keyboard. This variable is "true" if it is focused and "false" if not. This variable is often used when you want to warn people they need to click on or roll over an applet before it will work.


# Sketch_frame_count

The system variable , ``frame_count`` , contains the number of frames displayed since the program started.

Parameters
----------

PARAMTEXT

Notes
-----

The system variable ``frame_count`` contains the number of frames displayed since the program started. Inside ``setup()`` the value is 0 and and after the first iteration of draw it is 1, etc.


See Also
--------

Sketch.frameRate(float)

Sketch.frameRate


# Sketch_frame_rate

The system variable , ``frame_rate`` , contains the approximate frame rate of the software as it executes.

Parameters
----------

PARAMTEXT

Notes
-----

Specifies the number of frames to be displayed every second. If the processor is not fast enough to maintain the specified rate, it will not be achieved. For example, the function call ``frame_rate(30)`` will attempt to refresh 30 times a second. It is recommended to set the frame rate within ``setup()`` . The default rate is 60 frames per second.


See Also
--------

Sketch.frameRate(float)

Sketch.frameCount

Sketch.frameRate

Sketch.frameCount

Sketch.setup() : The , ``setup()`` , function is called once when the program starts.

Sketch.draw() : Called directly after , ``setup()`` , and continuously executes the lines of code contained inside its block until the program is stopped or , ``no_loop()`` , is called.

Sketch.loop() : Causes Processing to continuously execute the code within , ``draw()`` ,.

Sketch.noLoop()

Sketch.redraw() : flag set to true when a redraw is asked for by the user


# Sketch_frame_rate_last_nanos

Last time in nanoseconds that frameRate was checked

Parameters
----------

PARAMTEXT

Notes
-----

Last time in nanoseconds that frameRate was checked


# Sketch_frustum

Sets a perspective matrix defined through the parameters.

Parameters
----------

PARAMTEXT

Notes
-----

Sets a perspective matrix defined through the parameters. Works like glFrustum, except it wipes out the current perspective matrix rather than muliplying itself with it.


See Also
--------

Py5Graphics.camera(float, float, float, float, float, float, float, float, float) : Sets the position of the camera through setting the eye position, the center of the scene, and which axis is facing upward.

Py5Graphics.beginCamera()

Py5Graphics.endCamera()

Py5Graphics.perspective(float, float, float, float) : Sets a perspective projection applying foreshortening, making distant objects appear smaller than closer ones.


# Sketch_full_screen

Create a full-screen sketch using the default renderer.

Parameters
----------

PARAMTEXT

Notes
-----

Create a full-screen sketch using the default renderer.


See Also
--------

Sketch.settings() : Description to come...

Sketch.setup() : The , ``setup()`` , function is called once when the program starts.

Sketch.size(int,int) : Defines the dimension of the display window in units of pixels.

Sketch.smooth() : 


# Sketch_g

The Py5Graphics renderer associated with this Sketch

Parameters
----------

PARAMTEXT

Notes
-----

The Py5Graphics renderer associated with this Sketch


# Sketch_get

Reads the color of any pixel or grabs a section of an image.

Parameters
----------

PARAMTEXT

Notes
-----

Reads the color of any pixel or grabs a section of an image. If no parameters are specified, the entire image is returned. Use the ``x`` and ``y`` parameters to get the value of one pixel. Get a section of the display window by specifying an additional ``width`` and ``height`` parameter. When getting an image, the ``x`` and ``y`` parameters define the coordinates for the upper-left corner of the image, regardless of the current ``image_mode()`` .

If the pixel requested is outside of the image window, black is returned. The numbers returned are scaled according to the current color ranges, but only RGB values are returned by this function. For example, even though you may have drawn a shape with ``color_mode(hsb)`` , the numbers returned will be in RGB format.

Getting the color of a single pixel with ``get(x y)`` is easy, but not as fast as grabbing the data directly from ``pixels[]`` . The equivalent statement to ``get(x y)`` using ``pixels[]`` is ``pixels[y*width+x]`` . See the reference for ``pixels[]`` for more information.

Advanced
--------

Returns an ARGB "color" type (a packed 32 bit int with the color. If the coordinate is outside the image, zero is returned (black, but completely transparent).

If the image is in RGB format (i.e. on a PVideo object), the value will get its high bits set, just to avoid cases where they haven't been set already.

If the image is in ALPHA format, this returns a white with its alpha value set.

This function is included primarily for beginners. It is quite slow because it has to check to see if the x, y that was provided is inside the bounds, and then has to check to see what image type it is. If you want things to be more efficient, access the pixels[] array directly.


See Also
--------

Sketch.set(int, int, int) : Changes the color of any pixel or writes an image directly into the display window.,
, ,
, The , ``x`` , and , ``y`` , parameters specify the pixel to change and the , ``color`` , parameter specifies the color value.

Sketch.pixels : Array containing the values for all the pixels in the display window.

Sketch.copy(Py5Image, int, int, int, int, int, int, int, int) : Copies a region of pixels from one image into another.


# Sketch_get_matrix

Copy the current transformation matrix into the specified target.

Parameters
----------

PARAMTEXT

Notes
-----

Copy the current transformation matrix into the specified target. Pass in null to create a new matrix.


# Sketch_green

Extracts the green value from a color, scaled to match current , ``color_mode()`` ,.

Parameters
----------

PARAMTEXT

Notes
-----

Extracts the green value from a color, scaled to match current ``color_mode()`` . This value is always returned as a  float so be careful not to assign it to an int value.

The ``green()`` function is easy to use and undestand, but is slower than another technique. To achieve the same results when working in ``color_mode(rgb 255)`` , but with greater speed, use the>>(right shift) operator with a bit mask. For example, the following two lines of code are equivalent:
<pre>float r1 = green(myColor);
float r2 = myColor>>8&0xFF;</pre>


See Also
--------

Py5Graphics.red(int) : Extracts the red value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.blue(int) : Extracts the blue value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.alpha(int) : Extracts the alpha value from a color.

Py5Graphics.hue(int) : Extracts the hue value from a color.

Py5Graphics.saturation(int) : Extracts the saturation value from a color.

Py5Graphics.brightness(int) : Extracts the brightness value from a color.


# Sketch_handle_mouse_event

Actually take action based on a mouse event.

Parameters
----------

PARAMTEXT

Notes
-----

Actually take action based on a mouse event. Internally updates mouseX, mouseY, mousePressed, and mouseEvent. Then it calls the event type with no params, i.e. mousePressed() or mouseReleased() that the user may have overloaded to do something more useful.


# Sketch_height

System variable which stores the height of the display window.

Parameters
----------

PARAMTEXT

Notes
-----

System variable which stores the height of the display window. This value is set by the second parameter of the ``size()`` function. For example, the function call ``size(320 240)`` sets the ``height`` variable to the value 240. The value of ``height`` is zero until ``size()`` is called.


See Also
--------

Sketch.width : System variable which stores the width of the display window.

Sketch.size(int, int) : Defines the dimension of the display window in units of pixels.


# Sketch_hex

Converts a byte, char, int, or color to a String containing the equivalent hexadecimal notation.

Parameters
----------

PARAMTEXT

Notes
-----

Converts a byte, char, int, or color to a String containing the equivalent hexadecimal notation. For example color(0, 102, 153) will convert to the String "FF006699". This function can help make your geeky debugging sessions much happier.

Note that the maximum number of digits is 8, because an int value can only represent up to 32 bits. Specifying more than eight digits will simply shorten the string to eight anyway.


See Also
--------

Sketch.unhex(String) : Converts a String representation of a hexadecimal number to its equivalent integer value.

Sketch.binary(byte) : Converts a byte, char, int, or color to a String containing the equivalent binary notation.

Sketch.unbinary(String) : Converts a String representation of a binary number to its equivalent integer value.


# Sketch_hide_menu_bar

Convenience method, should only be called by Py5Surface subclasses.

Parameters
----------

PARAMTEXT

Notes
-----

Convenience method, should only be called by Py5Surface subclasses.


# Sketch_hour

Processing communicates with the clock on your computer.

Parameters
----------

PARAMTEXT

Notes
-----

Processing communicates with the clock on your computer. The ``hour()`` function returns the current hour as a value from 0 - 23.


See Also
--------

Sketch.millis() : Returns the number of milliseconds (thousandths of a second) since starting an applet.

Sketch.second() : Processing communicates with the clock on your computer.

Sketch.minute() : Processing communicates with the clock on your computer.

Sketch.day() : Processing communicates with the clock on your computer.

Sketch.month() : Processing communicates with the clock on your computer.

Sketch.year() : Processing communicates with the clock on your computer.


# Sketch_hue

Extracts the hue value from a color.

Parameters
----------

PARAMTEXT

Notes
-----

Extracts the hue value from a color.


See Also
--------

Py5Graphics.red(int) : Extracts the red value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.green(int) : Extracts the green value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.blue(int) : Extracts the blue value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.alpha(int) : Extracts the alpha value from a color.

Py5Graphics.saturation(int) : Extracts the saturation value from a color.

Py5Graphics.brightness(int) : Extracts the brightness value from a color.


# Sketch_image

Draw an image(), also specifying u/v coordinates.

Parameters
----------

PARAMTEXT

Notes
-----

Displays images to the screen. The images must be in the sketch's "data" directory to load correctly. Select "Add file..." from the "Sketch" menu to add the image. Processing currently works with GIF, JPEG, and Targa images. The ``img`` parameter specifies the image to display and the ``x`` and ``y`` parameters define the location of the image from its upper-left corner. The image is displayed at its original size unless the ``width`` and ``height`` parameters specify a different size.

The ``image_mode()`` function changes the way the parameters work. For example, a call to ``image_mode(corners)`` will change the ``width`` and ``height`` parameters to define the x and y values of the opposite corner of the image.

The color of an image may be modified with the ``tint()`` function. This function will maintain transparency for GIF and PNG images.

Advanced
--------

Starting with release 0124, when using the default (JAVA2D) renderer, smooth() will also improve image quality of resized images.


See Also
--------

Sketch.loadImage(String, String)

Py5Graphics.imageMode(int)

Py5Graphics.tint(float) : Sets the fill value for displaying images.

Py5Graphics.background(float, float, float, float) : The , ``background()`` , function sets the color used for the background of the Processing window.

Py5Graphics.alpha(int) : Extracts the alpha value from a color.


# Sketch_image_mode

Modifies the location from which images draw.

Parameters
----------

PARAMTEXT

Notes
-----

Modifies the location from which images draw. The default mode is ``image_mode(corner)`` , which specifies the location to be the upper left corner and uses the fourth and fifth parameters of ``image()`` to set the image's width and height. The syntax ``image_mode(corners)`` uses the second and third parameters of ``image()`` to set the location of one corner of the image and uses the fourth and fifth parameters to set the opposite corner. Use ``image_mode(center)`` to draw images centered at the given x and y position.

The parameter to ``image_mode()`` must be written in ALL CAPS because Processing is a case-sensitive language.


See Also
--------

Sketch.loadImage(String, String)

Py5Graphics.image(Py5Image, float, float, float, float) : Java AWT Image object associated with this renderer.

Py5Graphics.background(float, float, float, float) : The , ``background()`` , function sets the color used for the background of the Processing window.


# Sketch_insert_frame

Check a string for #### signs to see if the frame number should be inserted.

Parameters
----------

PARAMTEXT

Notes
-----

Check a string for #### signs to see if the frame number should be inserted. Used for functions like saveFrame() and beginRecord() to replace the # marks with the frame number. If only one # is used, it will be ignored, under the assumption that it's probably not intended to be the frame number.


# Sketch_inside_settings



Parameters
----------

PARAMTEXT

Notes
-----




# Sketch_int_nf

Integer number formatter.

Parameters
----------

PARAMTEXT

Notes
-----

Integer number formatter.


# Sketch_java_version

Do not use; javaPlatform or javaVersionName are better options.

Parameters
----------

PARAMTEXT

Notes
-----

Do not use; javaPlatform or javaVersionName are better options. For instance, javaPlatform is useful when you need a number for comparison, i.e. "if (javaPlatform>= 9)".


# Sketch_java_version_name

Full name of the Java version (i.e.

Parameters
----------

PARAMTEXT

Notes
-----

Full name of the Java version (i.e. 1.5.0_11).


# Sketch_join

Combines an array of Strings into one String, each separated by the character(s) used for the , ``separator`` , parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Combines an array of Strings into one String, each separated by the character(s) used for the ``separator`` parameter. To join arrays of ints or floats, it's necessary to first convert them to strings using ``nf()`` or ``nfs()`` .


See Also
--------

Sketch.split(String, String) : The split() function breaks a string into pieces using a character or string as the divider.

Sketch.trim(String) : Removes whitespace characters from the beginning and end of a String.

Sketch.nf(float, int, int) : Utility function for formatting numbers into strings.

Sketch.nfs(float, int, int) : Utility function for formatting numbers into strings.


# Sketch_key

The system variable , ``key`` , always contains the value of the most recent key on the keyboard that was used (either pressed or released).

Parameters
----------

PARAMTEXT

Notes
-----

The system variable ``key`` always contains the value of the most recent key on the keyboard that was used (either pressed or released).

For non-ASCII keys, use the ``key_code`` variable. The keys included in the ASCII specification (BACKSPACE, TAB, ENTER, RETURN, ESC, and DELETE) do not require checking to see if they key is coded, and you should simply use the ``key`` variable instead of ``key_code`` If you're making cross-platform projects, note that the ENTER key is commonly used on PCs and Unix and the RETURN key is used instead on Macintosh. Check for both ENTER and RETURN to make sure your program will work for all platforms.

Advanced
--------

Last key pressed.

If it's a coded key, i.e. UP/DOWN/CTRL/SHIFT/ALT, this will be set to CODED (0xffff or 65535).


See Also
--------

Sketch.keyCode

Sketch.keyPressed

Sketch.keyPressed()

Sketch.keyReleased()


# Sketch_key_code

The variable , ``key_code`` , is used to detect special keys such as the UP, DOWN, LEFT, RIGHT arrow keys and ALT, CONTROL, SHIFT.

Parameters
----------

PARAMTEXT

Notes
-----

The variable ``key_code`` is used to detect special keys such as the UP, DOWN, LEFT, RIGHT arrow keys and ALT, CONTROL, SHIFT. When checking for these keys, it's first necessary to check and see if the key is coded. This is done with the conditional "if (key == CODED)" as shown in the example.

The keys included in the ASCII specification (BACKSPACE, TAB, ENTER, RETURN, ESC, and DELETE) do not require checking to see if they key is coded, and you should simply use the ``key`` variable instead of ``key_code`` If you're making cross-platform projects, note that the ENTER key is commonly used on PCs and Unix and the RETURN key is used instead on Macintosh. Check for both ENTER and RETURN to make sure your program will work for all platforms.

For users familiar with Java, the values for UP and DOWN are simply shorter versions of Java's KeyEvent.VK_UP and KeyEvent.VK_DOWN. Other keyCode values can be found in the Java<a href="http://download.oracle.com/javase/6/docs/api/java/awt/event/KeyEvent.html">KeyEvent</a>reference.

Advanced
--------

When "key" is set to CODED, this will contain a Java key code.

For the arrow keys, keyCode will be one of UP, DOWN, LEFT and RIGHT. Also available are ALT, CONTROL and SHIFT. A full set of constants can be obtained from java.awt.event.KeyEvent, from the VK_XXXX variables.


See Also
--------

Sketch.key : The system variable , ``key`` , always contains the value of the most recent key on the keyboard that was used (either pressed or released).

Sketch.keyPressed

Sketch.keyPressed()

Sketch.keyReleased()


# Sketch_key_event

The last KeyEvent object passed into a mouse function.

Parameters
----------

PARAMTEXT

Notes
-----

The last KeyEvent object passed into a mouse function.


# Sketch_key_pressed

The boolean system variable , ``key_pressed`` , is , ``true`` , if any key is pressed and , ``false`` , if no keys are pressed.

Parameters
----------

PARAMTEXT

Notes
-----

The ``key_pressed()`` function is called once every time a key is pressed. The key that was pressed is stored in the ``key`` variable.

For non-ASCII keys, use the ``key_code`` variable. The keys included in the ASCII specification (BACKSPACE, TAB, ENTER, RETURN, ESC, and DELETE) do not require checking to see if they key is coded, and you should simply use the ``key`` variable instead of ``key_code`` If you're making cross-platform projects, note that the ENTER key is commonly used on PCs and Unix and the RETURN key is used instead on Macintosh. Check for both ENTER and RETURN to make sure your program will work for all platforms.

Because of how operating systems handle key repeats, holding down a key may cause multiple calls to keyPressed() (and keyReleased() as well). The rate of repeat is set by the operating system and how each computer is configured.

Advanced
--------

Called each time a single key on the keyboard is pressed. Because of how operating systems handle key repeats, holding down a key will cause multiple calls to keyPressed(), because the OS repeat takes over.

Examples for key handling: (Tested on Windows XP, please notify if different on other platforms, I have a feeling Mac OS and Linux may do otherwise)

``
1. _pressing 'a' on the keyboard:    key_pressed  with key == 'a' and key_code == 'a'    key_typed    with key == 'a' and key_code ==  0    key_released with key == 'a' and key_code == 'a' 2. _pressing 'a' on the keyboard:    key_pressed  with key == 'a' and key_code == 'a'    key_typed    with key == 'a' and key_code ==  0    key_released with key == 'a' and key_code == 'a' 3. _pressing 'shift' then 'a' on the keyboard (caps lock is off):    key_pressed  with key == coded and key_code == shift    key_pressed  with key == 'a'   and key_code == 'a'    key_typed    with key == 'a'   and key_code == 0    key_released with key == 'a'   and key_code == 'a'    key_released with key == coded and key_code == shift 4. _holding down the 'a' key.    _the following will happen several times    depending on your machine's "key repeat rate" settings:    key_pressed  with key == 'a' and key_code == 'a'    key_typed    with key == 'a' and key_code ==  0    _when you finally let go you'll get:    key_released with key == 'a' and key_code == 'a' 5. _pressing and releasing the 'shift' key    key_pressed  with key == coded and key_code == shift    key_released with key == coded and key_code == shift    (note there is no key_typed) 6. _pressing the tab key in an applet with _java 1.4 will    normally do nothing but Sketch dynamically shuts    this behavior off if _java 1.4 is in use (tested 1.4.2_05 _windows).    _java 1.1 (_microsoft vm) passes the tab key through normally.    _not tested on other platforms or for 1.3.
``


See Also
--------

Sketch.key : The system variable , ``key`` , always contains the value of the most recent key on the keyboard that was used (either pressed or released).

Sketch.keyCode

Sketch.keyPressed()

Sketch.keyReleased()

Sketch.key : The system variable , ``key`` , always contains the value of the most recent key on the keyboard that was used (either pressed or released).

Sketch.keyCode

Sketch.keyPressed

Sketch.keyReleased()


# Sketch_key_released

The , ``key_released()`` , function is called once every time a key is released.

Parameters
----------

PARAMTEXT

Notes
-----

The ``key_released()`` function is called once every time a key is released. The key that was released will be stored in the ``key`` variable. See ``key`` and ``key_released`` for more information.


See Also
--------

Sketch.key : The system variable , ``key`` , always contains the value of the most recent key on the keyboard that was used (either pressed or released).

Sketch.keyCode

Sketch.keyPressed

Sketch.keyPressed()


# Sketch_key_repeat_enabled

Keeps track of ENABLE_KEY_REPEAT hint

Parameters
----------

PARAMTEXT

Notes
-----

Keeps track of ENABLE_KEY_REPEAT hint


# Sketch_key_typed

The , ``key_typed()`` , function is called once every time a key is pressed, but action keys such as Ctrl, Shift, and Alt are ignored.

Parameters
----------

PARAMTEXT

Notes
-----

The ``key_typed()`` function is called once every time a key is pressed, but action keys such as Ctrl, Shift, and Alt are ignored. Because of how operating systems handle key repeats, holding down a key will cause multiple calls to ``key_typed()`` , the rate is set by the operating system and how each computer is configured.


See Also
--------

Sketch.keyPressed

Sketch.key : The system variable , ``key`` , always contains the value of the most recent key on the keyboard that was used (either pressed or released).

Sketch.keyCode

Sketch.keyReleased()


# Sketch_launch

Attempts to open an application or file using your platform's launcher.

Parameters
----------

PARAMTEXT

Notes
-----

Attempts to open an application or file using your platform's launcher. The ``file`` parameter is a String specifying the file name and location. The location parameter must be a full path name, or the name of an executable in the system's PATH. In most cases, using a full path is the best option, rather than relying on the system PATH. Be sure to make the file executable before attempting to open it (chmod +x).

The ``args`` parameter is a String or String array which is passed to the command line. If you have multiple parameters, e.g. an application and a document, or a command with multiple switches, use the version that takes a String array, and place each individual item in a separate element.

If args is a String (not an array), then it can only be a single file or application with no parameters. It's not the same as executing that String using a shell. For instance, launch("javac -help") will not work properly.

This function behaves differently on each platform. On Windows, the parameters are sent to the Windows shell via "cmd /c". On Mac OS X, the "open" command is used (type "man open" in Terminal.app for documentation). On Linux, it first tries gnome-open, then kde-open, but if neither are available, it sends the command to the shell without any alterations.

For users familiar with Java, this is not quite the same as Runtime.exec(), because the launcher command is prepended. Instead, the ``exec(_string[])`` function is a shortcut for Runtime.getRuntime.exec(String[]).


# Sketch_lerp

Calculates a number between two numbers at a specific increment.

Parameters
----------

PARAMTEXT

Notes
-----

Calculates a number between two numbers at a specific increment. The ``amt`` parameter is the amount to interpolate between the two values where 0.0 equal to the first point, 0.1 is very near the first point, 0.5 is half-way in between, etc. The lerp function is convenient for creating motion along a straight path and for drawing dotted lines.


See Also
--------

Py5Graphics.curvePoint(float, float, float, float, float)

Py5Graphics.bezierPoint(float, float, float, float, float)

Sketch.lerp(PVector, float) : Calculates a number between two numbers at a specific increment.

Py5Graphics.lerpColor(int, int, float)


# Sketch_lerp_color

Calculates a color or colors between two color at a specific increment.

Parameters
----------

PARAMTEXT

Notes
-----

Calculates a color or colors between two color at a specific increment. The ``amt`` parameter is the amount to interpolate between the two values where 0.0 equal to the first point, 0.1 is very near the first point, 0.5 is half-way in between, etc.


See Also
--------

Py5Image.blendColor(int, int, int)

Py5Graphics.color(float, float, float, float) : 

Sketch.lerp(float, float, float) : Calculates a number between two numbers at a specific increment.


# Sketch_light_falloff

Sets the falloff rates for point lights, spot lights, and ambient lights.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the falloff rates for point lights, spot lights, and ambient lights. The parameters are used to determine the falloff with the following equation:

d = distance from light position to vertex position
falloff = 1 / (CONSTANT + d * LINEAR + (d*d) * QUADRATIC)

Like ``fill()`` , it affects only the elements which are created after it in the code. The default value if ``_light_falloff(1.0 0.0 0.0)`` . Thinking about an ambient light with a falloff can be tricky. It is used, for example, if you wanted a region of your scene to be lit ambiently one color and another region to be lit ambiently by another color, you would use an ambient light with location and falloff. You can think of it as a point light that doesn't care which direction a surface is facing.


See Also
--------

Py5Graphics.lights() : Sets the default ambient light, directional light, falloff, and specular values.

Py5Graphics.ambientLight(float, float, float, float, float, float)

Py5Graphics.pointLight(float, float, float, float, float, float)

Py5Graphics.spotLight(float, float, float, float, float, float, float, float, float, float, float)

Py5Graphics.lightSpecular(float, float, float)


# Sketch_light_specular

Sets the specular color for lights.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the specular color for lights. Like ``fill()`` , it affects only the elements which are created after it in the code. Specular refers to light which bounces off a surface in a perferred direction (rather than bouncing in all directions like a diffuse light) and is used for creating highlights. The specular quality of a light interacts with the specular material qualities set through the ``specular()`` and ``shininess()`` functions.


See Also
--------

Py5Graphics.specular(float, float, float) : Sets the specular color of the materials used for shapes drawn to the screen, which sets the color of hightlights.

Py5Graphics.lights() : Sets the default ambient light, directional light, falloff, and specular values.

Py5Graphics.ambientLight(float, float, float, float, float, float)

Py5Graphics.pointLight(float, float, float, float, float, float)

Py5Graphics.spotLight(float, float, float, float, float, float, float, float, float, float, float)


# Sketch_lights

Sets the default ambient light, directional light, falloff, and specular values.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the default ambient light, directional light, falloff, and specular values. The defaults are ambientLight(128, 128, 128) and directionalLight(128, 128, 128, 0, 0, -1), lightFalloff(1, 0, 0), and lightSpecular(0, 0, 0). Lights need to be included in the draw() to remain persistent in a looping program. Placing them in the setup() of a looping program will cause them to only have an effect the first time through the loop.


See Also
--------

Py5Graphics.ambientLight(float, float, float, float, float, float)

Py5Graphics.directionalLight(float, float, float, float, float, float)

Py5Graphics.pointLight(float, float, float, float, float, float)

Py5Graphics.spotLight(float, float, float, float, float, float, float, float, float, float, float)

Py5Graphics.noLights()


# Sketch_line

Draws a line (a direct path between two points) to the screen.

Parameters
----------

PARAMTEXT

Notes
-----

Draws a line (a direct path between two points) to the screen. The version of ``line()`` with four parameters draws the line in 2D.  To color a line, use the ``stroke()`` function. A line cannot be filled, therefore the ``fill()`` function will not affect the color of a line. 2D lines are drawn with a width of one pixel by default, but this can be changed with the ``stroke_weight()`` function. The version with six parameters allows the line to be placed anywhere within XYZ space. Drawing this shape in 3D with the ``z`` parameter requires the P3D parameter in combination with ``size()`` as shown in the above example.


See Also
--------

Py5Graphics.strokeWeight(float)

Py5Graphics.strokeJoin(int)

Py5Graphics.strokeCap(int)

Py5Graphics.beginShape()


# Sketch_link

Links to a webpage either in the same window or in a new window.

Parameters
----------

PARAMTEXT

Notes
-----

Links to a webpage either in the same window or in a new window. The complete URL must be specified.

Advanced
--------

Link to an external page without all the muss.

When run with an applet, uses the browser to open the url, for applications, attempts to launch a browser with the url.


# Sketch_load_bytes

Reads the contents of a file or url and places it in a byte array.

Parameters
----------

PARAMTEXT

Notes
-----

Reads the contents of a file or url and places it in a byte array. If a file is specified, it must be located in the sketch's "data" directory/folder.

The filename parameter can also be a URL to a file found online. For security reasons, a Processing sketch found online can only download files from the same server from which it came. Getting around this restriction requires a<a href="http://wiki.processing.org/w/Sign_an_Applet">signed applet</a>.


See Also
--------

Sketch.loadStrings(String)

Sketch.saveStrings(String, String[])

Sketch.saveBytes(String, byte[])


# Sketch_load_font

Loads a font into a variable of type , ``Py5Font`` ,.

Parameters
----------

PARAMTEXT

Notes
-----

Loads a font into a variable of type ``Py5Font`` . To load correctly, fonts must be located in the data directory of the current sketch. To create a font to use with Processing, select "Create Font..." from the Tools menu. This will create a font in the format Processing requires and also adds it to the current sketch's data directory.

Like ``load_image()`` and other functions that load data, the ``load_font()`` function should not be used inside ``draw()`` , because it will slow down the sketch considerably, as the font will be re-loaded from the disk (or network) on each frame.

For most renderers, Processing displays fonts using the .vlw font format, which uses images for each letter, rather than defining them through vector data. When ``hint(enable_native_fonts)`` is used with the JAVA2D renderer, the native version of a font will be used if it is installed on the user's machine.

Using ``create_font()`` (instead of loadFont) enables vector data to be used with the JAVA2D (default) renderer setting. This can be helpful when many font sizes are needed, or when using any renderer based on JAVA2D, such as the PDF library.


See Also
--------

Py5Graphics.textFont(Py5Font, float)

Sketch.createFont(String, float, boolean, char[])


# Sketch_load_image

Loads an image into a variable of type , ``Py5Image`` ,.

Parameters
----------

PARAMTEXT

Notes
-----

Loads an image into a variable of type ``Py5Image`` . Four types of images ( ``.gif`` , ``.jpg`` , ``.tga`` , ``.png`` ) images may be loaded. To load correctly, images must be located in the data directory of the current sketch. In most cases, load all images in ``setup()`` to preload them at the start of the program. Loading images inside ``draw()`` will reduce the speed of a program.

 ``filename`` parameter can also be a URL to a file found online. For security reasons, a Processing sketch found online can only download files from the same server from which it came. Getting around this restriction requires a<a href="http://wiki.processing.org/w/Sign_an_Applet">signed applet</a>.

 ``extension`` parameter is used to determine the image type in cases where the image filename does not end with a proper extension. Specify the extension as the second parameter to ``load_image()`` , as shown in the third example on this page.

an image is not loaded successfully, the ``null`` value is returned and an error message will be printed to the console. The error message does not halt the program, however the null value may cause a NullPointerException if your code does not check whether the value returned from ``load_image()`` is null.

on the type of error, a ``Py5Image`` object may still be returned, but the width and height of the image will be set to -1. This happens if bad image data is returned or cannot be decoded properly. Sometimes this happens with image URLs that produce a 403 error or that redirect to a password prompt, because ``load_image()`` will attempt to interpret the HTML as image data.


See Also
--------

Py5Graphics.image(Py5Image, float, float, float, float) : Java AWT Image object associated with this renderer.

Py5Graphics.imageMode(int)

Py5Graphics.background(float, float, float, float) : The , ``background()`` , function sets the color used for the background of the Processing window.


# Sketch_load_json_array



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Sketch.loadJSONObject(String)

Sketch.saveJSONObject(JSONObject, String)

Sketch.saveJSONArray(JSONArray, String)


# Sketch_load_json_object



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Sketch.loadJSONArray(String)

Sketch.saveJSONObject(JSONObject, String)

Sketch.saveJSONArray(JSONArray, String)


# Sketch_load_pixels

Loads the pixel data for the display window into the , ``pixels[]`` , array.

Parameters
----------

PARAMTEXT

Notes
-----

Loads the pixel data for the display window into the ``pixels[]`` array. This function must always be called before reading from or writing to ``pixels[]`` .

renderers may or may not seem to require ``load_pixels()`` or ``update_pixels()`` . However, the rule is that any time you want to manipulate the ``pixels[]`` array, you must first call ``load_pixels()`` , and after changes have been made, call ``update_pixels()`` . Even if the renderer may not seem to use this function in the current Processing release, this will always be subject to change.

Advanced
--------

Override the g.pixels[] function to set the pixels[] array that's part of the Sketch object. Allows the use of pixels[] in the code, rather than g.pixels[].


See Also
--------

Sketch.pixels : Array containing the values for all the pixels in the display window.

Sketch.updatePixels()


# Sketch_load_shader

This is a new reference entry for Processing 2.0.

Parameters
----------

PARAMTEXT

Notes
-----

This is a new reference entry for Processing 2.0. It will be updated shortly.


# Sketch_load_shape



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Sketch.createShape()


# Sketch_load_strings

Reads the contents of a file or url and creates a String array of its individual lines.

Parameters
----------

PARAMTEXT

Notes
-----

Reads the contents of a file or url and creates a String array of its individual lines. If a file is specified, it must be located in the sketch's "data" directory/folder.

The filename parameter can also be a URL to a file found online. For security reasons, a Processing sketch found online can only download files from the same server from which it came. Getting around this restriction requires a<a href="http://wiki.processing.org/w/Sign_an_Applet">signed applet</a>.
If the file is not available or an error occurs, ``null`` will be returned and an error message will be printed to the console. The error message does not halt the program, however the null value may cause a NullPointerException if your code does not check whether the value returned is null.

Starting with Processing release 0134, all files loaded and saved by the Processing API use UTF-8 encoding. In previous releases, the default encoding for your platform was used, which causes problems when files are moved to other platforms.

Advanced
--------

Load data from a file and shove it into a String array.

Exceptions are handled internally, when an error, occurs, an exception is printed to the console and 'null' is returned, but the program continues running. This is a tradeoff between 1) showing the user that there was a problem but 2) not requiring that all i/o code is contained in try/catch blocks, for the sake of new users (or people who are just trying to get things done in a "scripting" fashion. If you want to handle exceptions, use Java methods for I/O.


See Also
--------

Sketch.loadBytes(String)

Sketch.saveStrings(String, String[])

Sketch.saveBytes(String, byte[])


# Sketch_load_table

Options may contain "header", "tsv", "csv", or "bin" separated by commas.

Parameters
----------

PARAMTEXT

Notes
-----

Options may contain "header", "tsv", "csv", or "bin" separated by commas. Another option is "dictionary=filename.tsv", which allows users to specify a "dictionary" file that contains a mapping of the column titles and the data types used in the table file. This can be far more efficient (in terms of speed and memory usage) for loading and parsing tables. The dictionary file can only be tab separated values (.tsv) and its extension will be ignored. This option was added in Processing 2.0.2.


See Also
--------

Sketch.saveTable(Table, String)

Sketch.loadBytes(String)

Sketch.loadStrings(String)

Sketch.loadXML(String)


# Sketch_load_xml



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Sketch.parseXML(String)

Sketch.saveXML(XML, String)

Sketch.loadBytes(String)

Sketch.loadStrings(String)

Sketch.loadTable(String)


# Sketch_log

Calculates the natural logarithm (the base-,<i>,e,</i>, logarithm) of a number.

Parameters
----------

PARAMTEXT

Notes
-----

Calculates the natural logarithm (the base-<i>e</i>logarithm) of a number. This function expects the values greater than 0.0.


# Sketch_loop

Causes Processing to continuously execute the code within , ``draw()`` ,.

Parameters
----------

PARAMTEXT

Notes
-----

Causes Processing to continuously execute the code within ``draw()`` . If ``no_loop()`` is called, the code in ``draw()`` stops executing.


See Also
--------

Sketch.noLoop()

Sketch.redraw() : flag set to true when a redraw is asked for by the user

Sketch.draw() : Called directly after , ``setup()`` , and continuously executes the lines of code contained inside its block until the program is stopped or , ``no_loop()`` , is called.


# Sketch_mag

Calculates the magnitude (or length) of a vector.

Parameters
----------

PARAMTEXT

Notes
-----

Calculates the magnitude (or length) of a vector. A vector is a direction in space commonly used in computer graphics and linear algebra. Because it has no "start" position, the magnitude of a vector can be thought of as the distance from coordinate (0,0) to its (x,y) value. Therefore, mag() is a shortcut for writing "dist(0, 0, x, y)".


See Also
--------

Sketch.dist(float, float, float, float) : Calculates the distance between two points.


# Sketch_main

Convenience method so that Sketch.main("YourSketch", args) launches a sketch, rather than having to wrap it into a String array, and appending the 'args' array when not null.

Parameters
----------

PARAMTEXT

Notes
-----

main() method for running this class from the command line.

Usage: Sketch [options]<class name>[sketch args]<ul><li>The [options] are one or several of the parameters seen below.<li>The class name is required. If you're running outside the PDE and your class is in a package, this should include the full name. That means that if the class is called Sketchy and the package is com.sketchycompany then com.sketchycompany.Sketchy should be used as the class name.<li>The [sketch args] are any command line parameters you want to send to the sketch itself. These will be passed into the args[] array in Sketch.

The simplest way to turn and sketch into an application is to add the following code to your program:

``
static public void main(_string args[]) {   Sketch.main("_your_sketch_name")
}
``

That will properly launch your code from a double-clickable .jar or from the command line.

``
Parameters useful for launching or also used by the PDE: --location=x,y         Upper-lefthand corner of where the applet                        should appear on screen. If not used,                        the default is to center on the main screen. --present              Presentation mode: blanks the entire screen and                        shows the sketch by itself. If the sketch is                        smaller than the screen, the background around it                        will use the --window-color setting. --hide-stop            Use to hide the stop button in situations where                        you don't want to allow users to exit. also                        see the FAQ on information for capturing the ESC                        key when running in presentation mode. --stop-color=#xxxxxx   Color of the 'stop' text used to quit an                        sketch when it's in present mode. --window-color=#xxxxxx Background color of the window. The color used                        around the sketch when it's smaller than the                        minimum window size for the OS, and the matte                        color when using 'present' mode. --sketch-path          Location of where to save files from functions                        like saveStrings() or saveFrame(). defaults to                        the folder that the java application was                        launched from, which means if this isn't set by                        the pde, everything goes into the same folder                        as processing.exe. --display=n            Set what display should be used by this sketch.                        Displays are numbered starting from 1. This will                        be overridden by fullScreen() calls that specify                        a display. Omitting this option will cause the                        default display to be used. Parameters used by Processing when running via the PDE --external             set when the applet is being used by the PDE --editor-location=x,y  position of the upper-lefthand corner of the                        editor window, for placement of applet window All parameters *after* the sketch class name are passed to the sketch itself and available from its 'args' array while the sketch is running.


See Also
--------

Sketch.args 
``


# Sketch_make_graphics

Version of createGraphics() used internally.

Parameters
----------

PARAMTEXT

Notes
-----

Version of createGraphics() used internally.


# Sketch_map

Re-maps a number from one range to another.

Parameters
----------

PARAMTEXT

Notes
-----

Re-maps a number from one range to another. In the example above, the number '25' is converted from a value in the range 0..100 into a value that ranges from the left edge (0) to the right edge (width) of the screen.

Numbers outside the range are not clamped to 0 and 1, because out-of-range values are often intentional and useful.


See Also
--------

Sketch.norm(float, float, float) : Normalizes a number from another range into a value between 0 and 1.

Sketch.lerp(float, float, float) : Calculates a number between two numbers at a specific increment.


# Sketch_mask

Masks part of an image from displaying by loading another image and using it as an alpha channel.

Parameters
----------

PARAMTEXT

Notes
-----

Masks part of an image from displaying by loading another image and using it as an alpha channel. This mask image should only contain grayscale data, but only the blue color channel is used. The mask image needs to be the same size as the image to which it is applied.

In addition to using a mask image, an integer array containing the alpha channel data can be specified directly. This method is useful for creating dynamically generated alpha masks. This array must be of the same length as the target image's pixels array and should contain only grayscale data of values between 0-255.

Advanced
--------

Set alpha channel for an image. Black colors in the source image will make the destination image completely transparent, and white will make things fully opaque. Gray values will be in-between steps.

Strictly speaking the "blue" value from the source image is used as the alpha color. For a fully grayscale image, this is correct, but for a color image it's not 100% accurate. For a more accurate conversion, first use filter(GRAY) which will make the image into a "correct" grayscale by performing a proper luminance-based conversion.


# Sketch_match

The match() function is used to apply a regular expression to a piece of text, and return matching groups (elements found inside parentheses) as a String array.

Parameters
----------

PARAMTEXT

Notes
-----

The match() function is used to apply a regular expression to a piece of text, and return matching groups (elements found inside parentheses) as a String array. No match will return null. If no groups are specified in the regexp, but the sequence matches, an array of length one (with the matched text as the first element of the array) will be returned.

To use the function, first check to see if the result is null. If the result is null, then the sequence did not match. If the sequence did match, an array is returned. If there are groups (specified by sets of parentheses) in the regexp, then the contents of each will be returned in the array. Element [0] of a regexp match returns the entire matching string, and the match groups start at element [1] (the first group is [1], the second [2], and so on).

The syntax can be found in the reference for Java's<a href="http://download.oracle.com/javase/6/docs/api/">Pattern</a>class. For regular expression syntax, read the<a href="http://download.oracle.com/javase/tutorial/essential/regex/">Java Tutorial</a>on the topic.


See Also
--------

Sketch.matchAll(String, String)

Sketch.split(String, String) : The split() function breaks a string into pieces using a character or string as the divider.

Sketch.splitTokens(String, String)

Sketch.join(String[], String) : Combines an array of Strings into one String, each separated by the character(s) used for the , ``separator`` , parameter.

Sketch.trim(String) : Removes whitespace characters from the beginning and end of a String.


# Sketch_match_all

This function is used to apply a regular expression to a piece of text, and return a list of matching groups (elements found inside parentheses) as a two-dimensional String array.

Parameters
----------

PARAMTEXT

Notes
-----

This function is used to apply a regular expression to a piece of text, and return a list of matching groups (elements found inside parentheses) as a two-dimensional String array. No matches will return null. If no groups are specified in the regexp, but the sequence matches, a two dimensional array is still returned, but the second dimension is only of length one.

To use the function, first check to see if the result is null. If the result is null, then the sequence did not match at all. If the sequence did match, a 2D array is returned. If there are groups (specified by sets of parentheses) in the regexp, then the contents of each will be returned in the array. Assuming, a loop with counter variable i, element [i][0] of a regexp match returns the entire matching string, and the match groups start at element [i][1] (the first group is [i][1], the second [i][2], and so on).

The syntax can be found in the reference for Java's<a href="http://download.oracle.com/javase/6/docs/api/">Pattern</a>class. For regular expression syntax, read the<a href="http://download.oracle.com/javase/tutorial/essential/regex/">Java Tutorial</a>on the topic.


See Also
--------

Sketch.match(String, String) : The match() function is used to apply a regular expression to a piece of text, and return matching groups (elements found inside parentheses) as a String array.

Sketch.split(String, String) : The split() function breaks a string into pieces using a character or string as the divider.

Sketch.splitTokens(String, String)

Sketch.join(String[], String) : Combines an array of Strings into one String, each separated by the character(s) used for the , ``separator`` , parameter.

Sketch.trim(String) : Removes whitespace characters from the beginning and end of a String.


# Sketch_max

Determines the largest value in a sequence of numbers.

Parameters
----------

PARAMTEXT

Notes
-----

Determines the largest value in a sequence of numbers.


See Also
--------

Sketch.min(float, float, float) : Determines the smallest value in a sequence of numbers.


# Sketch_method

Call a method in the current class based on its name.

Parameters
----------

PARAMTEXT

Notes
-----

Call a method in the current class based on its name.

Note that the function being called must be public. Inside the PDE, 'public' is automatically added, but when used without the preprocessor, (like from Eclipse) you'll have to do it yourself.


# Sketch_millis

Returns the number of milliseconds (thousandths of a second) since starting an applet.

Parameters
----------

PARAMTEXT

Notes
-----

Returns the number of milliseconds (thousandths of a second) since starting an applet. This information is often used for timing animation sequences.

Advanced
--------



This is a function, rather than a variable, because it may change multiple times per frame.


See Also
--------

Sketch.second() : Processing communicates with the clock on your computer.

Sketch.minute() : Processing communicates with the clock on your computer.

Sketch.hour() : Processing communicates with the clock on your computer.

Sketch.day() : Processing communicates with the clock on your computer.

Sketch.month() : Processing communicates with the clock on your computer.

Sketch.year() : Processing communicates with the clock on your computer.


# Sketch_millis_offset

Time in milliseconds when the applet was started.

Parameters
----------

PARAMTEXT

Notes
-----

Time in milliseconds when the applet was started.

Used by the millis() function.


# Sketch_min

Determines the smallest value in a sequence of numbers.

Parameters
----------

PARAMTEXT

Notes
-----

Determines the smallest value in a sequence of numbers.


See Also
--------

Sketch.max(float, float, float) : Determines the largest value in a sequence of numbers.


# Sketch_minute

Processing communicates with the clock on your computer.

Parameters
----------

PARAMTEXT

Notes
-----

Processing communicates with the clock on your computer. The ``minute()`` function returns the current minute as a value from 0 - 59.


See Also
--------

Sketch.millis() : Returns the number of milliseconds (thousandths of a second) since starting an applet.

Sketch.second() : Processing communicates with the clock on your computer.

Sketch.hour() : Processing communicates with the clock on your computer.

Sketch.day() : Processing communicates with the clock on your computer.

Sketch.month() : Processing communicates with the clock on your computer.

Sketch.year() : Processing communicates with the clock on your computer.


# Sketch_model_x

Returns the three-dimensional X, Y, Z position in model space.

Parameters
----------

PARAMTEXT

Notes
-----

Returns the three-dimensional X, Y, Z position in model space. This returns the X value for a given coordinate based on the current set of transformations (scale, rotate, translate, etc.) The X value can be used to place an object in space relative to the location of the original point once the transformations are no longer in use.

In the example, the ``model_x()`` , ``model_y()`` , and ``model_z()`` functions record the location of a box in space after being placed using a series of translate and rotate commands. After popMatrix() is called, those transformations no longer apply, but the (x, y, z) coordinate returned by the model functions is used to place another box in the same location.


See Also
--------

Py5Graphics.modelY(float, float, float)

Py5Graphics.modelZ(float, float, float)


# Sketch_model_y

Returns the three-dimensional X, Y, Z position in model space.

Parameters
----------

PARAMTEXT

Notes
-----

Returns the three-dimensional X, Y, Z position in model space. This returns the Y value for a given coordinate based on the current set of transformations (scale, rotate, translate, etc.) The Y value can be used to place an object in space relative to the location of the original point once the transformations are no longer in use.

In the example, the ``model_x()`` , ``model_y()`` , and ``model_z()`` functions record the location of a box in space after being placed using a series of translate and rotate commands. After popMatrix() is called, those transformations no longer apply, but the (x, y, z) coordinate returned by the model functions is used to place another box in the same location.


See Also
--------

Py5Graphics.modelX(float, float, float)

Py5Graphics.modelZ(float, float, float)


# Sketch_model_z

Returns the three-dimensional X, Y, Z position in model space.

Parameters
----------

PARAMTEXT

Notes
-----

Returns the three-dimensional X, Y, Z position in model space. This returns the Z value for a given coordinate based on the current set of transformations (scale, rotate, translate, etc.) The Z value can be used to place an object in space relative to the location of the original point once the transformations are no longer in use.

In the example, the ``model_x()`` , ``model_y()`` , and ``model_z()`` functions record the location of a box in space after being placed using a series of translate and rotate commands. After popMatrix() is called, those transformations no longer apply, but the (x, y, z) coordinate returned by the model functions is used to place another box in the same location.


See Also
--------

Py5Graphics.modelX(float, float, float)

Py5Graphics.modelY(float, float, float)


# Sketch_month

Processing communicates with the clock on your computer.

Parameters
----------

PARAMTEXT

Notes
-----

Processing communicates with the clock on your computer. The ``month()`` function returns the current month as a value from 1 - 12.


See Also
--------

Sketch.millis() : Returns the number of milliseconds (thousandths of a second) since starting an applet.

Sketch.second() : Processing communicates with the clock on your computer.

Sketch.minute() : Processing communicates with the clock on your computer.

Sketch.hour() : Processing communicates with the clock on your computer.

Sketch.day() : Processing communicates with the clock on your computer.

Sketch.year() : Processing communicates with the clock on your computer.


# Sketch_mouse_button

Processing automatically tracks if the mouse button is pressed and which button is pressed.

Parameters
----------

PARAMTEXT

Notes
-----

Processing automatically tracks if the mouse button is pressed and which button is pressed. The value of the system variable ``mouse_button`` is either ``left`` , ``right`` , or ``center`` depending on which button is pressed.

Advanced:
--------

If running on Mac OS, a ctrl-click will be interpreted as the right-hand mouse button (unlike Java, which reports it as the left mouse).


See Also
--------

Sketch.mouseX

Sketch.mouseY

Sketch.pmouseX

Sketch.pmouseY

Sketch.mousePressed

Sketch.mousePressed()

Sketch.mouseReleased()

Sketch.mouseClicked()

Sketch.mouseMoved()

Sketch.mouseDragged()

Sketch.mouseWheel(MouseEvent)


# Sketch_mouse_clicked

The , ``mouse_clicked()`` , function is called once after a mouse button has been pressed and then released.

Parameters
----------

PARAMTEXT

Notes
-----

The ``mouse_clicked()`` function is called once after a mouse button has been pressed and then released.

Advanced
--------

When the mouse is clicked, mousePressed() will be called, then mouseReleased(), then mouseClicked(). Note that mousePressed is already false inside of mouseClicked().


See Also
--------

Sketch.mouseX

Sketch.mouseY

Sketch.pmouseX

Sketch.pmouseY

Sketch.mousePressed

Sketch.mousePressed()

Sketch.mouseReleased()

Sketch.mouseMoved()

Sketch.mouseDragged()

Sketch.mouseButton

Sketch.mouseWheel(MouseEvent)


# Sketch_mouse_dragged

The , ``mouse_dragged()`` , function is called once every time the mouse moves and a mouse button is pressed.

Parameters
----------

PARAMTEXT

Notes
-----

The ``mouse_dragged()`` function is called once every time the mouse moves and a mouse button is pressed.


See Also
--------

Sketch.mouseX

Sketch.mouseY

Sketch.pmouseX

Sketch.pmouseY

Sketch.mousePressed

Sketch.mousePressed()

Sketch.mouseReleased()

Sketch.mouseClicked()

Sketch.mouseMoved()

Sketch.mouseButton

Sketch.mouseWheel(MouseEvent)


# Sketch_mouse_event



Parameters
----------

PARAMTEXT

Notes
-----




# Sketch_mouse_moved

The , ``mouse_moved()`` , function is called every time the mouse moves and a mouse button is not pressed.

Parameters
----------

PARAMTEXT

Notes
-----

The ``mouse_moved()`` function is called every time the mouse moves and a mouse button is not pressed.


See Also
--------

Sketch.mouseX

Sketch.mouseY

Sketch.pmouseX

Sketch.pmouseY

Sketch.mousePressed

Sketch.mousePressed()

Sketch.mouseReleased()

Sketch.mouseClicked()

Sketch.mouseDragged()

Sketch.mouseButton

Sketch.mouseWheel(MouseEvent)


# Sketch_mouse_pressed

The , ``mouse_pressed()`` , function is called once after every time a mouse button is pressed.

Parameters
----------

PARAMTEXT

Notes
-----

The ``mouse_pressed()`` function is called once after every time a mouse button is pressed. The ``mouse_button`` variable (see the related reference entry) can be used to determine which button has been pressed.

Advanced
--------

If you must, use int button = mouseEvent.getButton(); to figure out which button was clicked. It will be one of: MouseEvent.BUTTON1, MouseEvent.BUTTON2, MouseEvent.BUTTON3 Note, however, that this is completely inconsistent across platforms.


See Also
--------

Sketch.mouseX

Sketch.mouseY

Sketch.pmouseX

Sketch.pmouseY

Sketch.mousePressed()

Sketch.mouseReleased()

Sketch.mouseClicked()

Sketch.mouseMoved()

Sketch.mouseDragged()

Sketch.mouseButton

Sketch.mouseWheel(MouseEvent)

Sketch.mouseX

Sketch.mouseY

Sketch.pmouseX

Sketch.pmouseY

Sketch.mousePressed

Sketch.mouseReleased()

Sketch.mouseClicked()

Sketch.mouseMoved()

Sketch.mouseDragged()

Sketch.mouseButton

Sketch.mouseWheel(MouseEvent)


# Sketch_mouse_released

The , ``mouse_released()`` , function is called every time a mouse button is released.

Parameters
----------

PARAMTEXT

Notes
-----

The ``mouse_released()`` function is called every time a mouse button is released.


See Also
--------

Sketch.mouseX

Sketch.mouseY

Sketch.pmouseX

Sketch.pmouseY

Sketch.mousePressed

Sketch.mousePressed()

Sketch.mouseClicked()

Sketch.mouseMoved()

Sketch.mouseDragged()

Sketch.mouseButton

Sketch.mouseWheel(MouseEvent)


# Sketch_mouse_wheel

The event.getAmount() method returns negative values if the mouse wheel if rotated up or away from the user and positive in the other direction.

Parameters
----------

PARAMTEXT

Notes
-----

The event.getAmount() method returns negative values if the mouse wheel if rotated up or away from the user and positive in the other direction. On OS X with "natural" scrolling enabled, the values are opposite.


See Also
--------

Sketch.mouseX

Sketch.mouseY

Sketch.pmouseX

Sketch.pmouseY

Sketch.mousePressed

Sketch.mousePressed()

Sketch.mouseReleased()

Sketch.mouseClicked()

Sketch.mouseMoved()

Sketch.mouseDragged()

Sketch.mouseButton


# Sketch_mouse_x

The system variable , ``mouse_x`` , always contains the current horizontal coordinate of the mouse.

Parameters
----------

PARAMTEXT

Notes
-----

The system variable ``mouse_x`` always contains the current horizontal coordinate of the mouse.


See Also
--------

Sketch.mouseY

Sketch.pmouseX

Sketch.pmouseY

Sketch.mousePressed

Sketch.mousePressed()

Sketch.mouseReleased()

Sketch.mouseClicked()

Sketch.mouseMoved()

Sketch.mouseDragged()

Sketch.mouseButton

Sketch.mouseWheel(MouseEvent)


# Sketch_mouse_y

The system variable , ``mouse_y`` , always contains the current vertical coordinate of the mouse.

Parameters
----------

PARAMTEXT

Notes
-----

The system variable ``mouse_y`` always contains the current vertical coordinate of the mouse.


See Also
--------

Sketch.mouseX

Sketch.pmouseX

Sketch.pmouseY

Sketch.mousePressed

Sketch.mousePressed()

Sketch.mouseReleased()

Sketch.mouseClicked()

Sketch.mouseMoved()

Sketch.mouseDragged()

Sketch.mouseButton

Sketch.mouseWheel(MouseEvent)


# Sketch_nf

Utility function for formatting numbers into strings.

Parameters
----------

PARAMTEXT

Notes
-----

Utility function for formatting numbers into strings. There are two versions, one for formatting floats and one for formatting ints. The values for the ``digits`` , ``left`` , and ``right`` parameters should always be positive integers.

As shown in the above example, ``nf()`` is used to add zeros to the left and/or right of a number. This is typically for aligning a list of numbers. To<em>remove</em>digits from a floating-point number, use the ``int()`` , ``ceil()`` , ``floor()`` , or ``round()`` functions.


See Also
--------

Sketch.nfs(float, int, int) : Utility function for formatting numbers into strings.

Sketch.nfp(float, int, int) : Utility function for formatting numbers into strings.

Sketch.nfc(float, int) : Utility function for formatting numbers into strings and placing appropriate commas to mark units of 1000.


# Sketch_nfc

Utility function for formatting numbers into strings and placing appropriate commas to mark units of 1000.

Parameters
----------

PARAMTEXT

Notes
-----

Utility function for formatting numbers into strings and placing appropriate commas to mark units of 1000. There are two versions, one for formatting ints and one for formatting an array of ints. The value for the ``digits`` parameter should always be a positive integer.

For a non-US locale, this will insert periods instead of commas, or whatever is apprioriate for that region.


See Also
--------

Sketch.nf(float, int, int) : Utility function for formatting numbers into strings.

Sketch.nfp(float, int, int) : Utility function for formatting numbers into strings.

Sketch.nfs(float, int, int) : Utility function for formatting numbers into strings.


# Sketch_nfp

Utility function for formatting numbers into strings.

Parameters
----------

PARAMTEXT

Notes
-----

Utility function for formatting numbers into strings. Similar to ``nf()`` but puts a "+" in front of positive numbers and a "-" in front of negative numbers. There are two versions, one for formatting floats and one for formatting ints. The values for the ``digits`` , ``left`` , and ``right`` parameters should always be positive integers.


See Also
--------

Sketch.nf(float, int, int) : Utility function for formatting numbers into strings.

Sketch.nfs(float, int, int) : Utility function for formatting numbers into strings.

Sketch.nfc(float, int) : Utility function for formatting numbers into strings and placing appropriate commas to mark units of 1000.


# Sketch_nfs

Utility function for formatting numbers into strings.

Parameters
----------

PARAMTEXT

Notes
-----

Utility function for formatting numbers into strings. Similar to ``nf()`` but leaves a blank space in front of positive numbers so they align with negative numbers in spite of the minus symbol. There are two versions, one for formatting floats and one for formatting ints. The values for the ``digits`` , ``left`` , and ``right`` parameters should always be positive integers.


See Also
--------

Sketch.nf(float, int, int) : Utility function for formatting numbers into strings.

Sketch.nfp(float, int, int) : Utility function for formatting numbers into strings.

Sketch.nfc(float, int) : Utility function for formatting numbers into strings and placing appropriate commas to mark units of 1000.


# Sketch_no_clip

Disables the clipping previously started by the , ``clip()`` , function.

Parameters
----------

PARAMTEXT

Notes
-----

Disables the clipping previously started by the ``clip()`` function.


# Sketch_no_cursor

Hides the cursor from view.

Parameters
----------

PARAMTEXT

Notes
-----

Hides the cursor from view. Will not work when running the program in a web browser or when running in full screen (Present) mode.

Advanced
--------

Hide the cursor by creating a transparent image and using it as a custom cursor.


See Also
--------

Sketch.cursor() : Sets the cursor to a predefined symbol, an image, or makes it visible if already hidden.


# Sketch_no_fill

Disables filling geometry.

Parameters
----------

PARAMTEXT

Notes
-----

Disables filling geometry. If both ``no_stroke()`` and ``no_fill()`` are called, nothing will be drawn to the screen.


See Also
--------

Py5Graphics.fill(float, float, float, float) : true if fill() is enabled, (read-only)

Py5Graphics.stroke(int, float) : Sets the color used to draw lines and borders around shapes.

Py5Graphics.noStroke()


# Sketch_no_lights

Disable all lighting.

Parameters
----------

PARAMTEXT

Notes
-----

Disable all lighting. Lighting is turned off by default and enabled with the ``lights()`` function. This function can be used to disable lighting so that 2D geometry (which does not require lighting) can be drawn after a set of lighted 3D geometry.


See Also
--------

Py5Graphics.lights() : Sets the default ambient light, directional light, falloff, and specular values.


# Sketch_no_loop

Stops Processing from continuously executing the code within , ``draw()`` ,.

Parameters
----------

PARAMTEXT

Notes
-----

Stops Processing from continuously executing the code within ``draw()`` . If ``loop()`` is called, the code in ``draw()`` begin to run continuously again. If using ``no_loop()`` in ``setup()`` , it should be the last line inside the block.

When ``no_loop()`` is used, it's not possible to manipulate or access the screen inside event handling functions such as ``mouse_pressed()`` or ``key_pressed()`` . Instead, use those functions to call ``redraw()`` or ``loop()`` , which will run ``draw()`` , which can update the screen properly. This means that when noLoop() has been called, no drawing can happen, and functions like saveFrame() or loadPixels() may not be used.

Note that if the sketch is resized, ``redraw()`` will be called to update the sketch, even after ``no_loop()`` has been specified. Otherwise, the sketch would enter an odd state until ``loop()`` was called.


See Also
--------

Sketch.loop() : Causes Processing to continuously execute the code within , ``draw()`` ,.

Sketch.redraw() : flag set to true when a redraw is asked for by the user

Sketch.draw() : Called directly after , ``setup()`` , and continuously executes the lines of code contained inside its block until the program is stopped or , ``no_loop()`` , is called.


# Sketch_no_smooth



Parameters
----------

PARAMTEXT

Notes
-----




# Sketch_no_stroke

Disables drawing the stroke (outline).

Parameters
----------

PARAMTEXT

Notes
-----

Disables drawing the stroke (outline). If both ``no_stroke()`` and ``no_fill()`` are called, nothing will be drawn to the screen.


See Also
--------

Py5Graphics.stroke(int, float) : Sets the color used to draw lines and borders around shapes.

Py5Graphics.fill(float, float, float, float) : true if fill() is enabled, (read-only)

Py5Graphics.noFill()


# Sketch_no_texture

Removes texture image for current shape.

Parameters
----------

PARAMTEXT

Notes
-----

Removes texture image for current shape. Needs to be called between beginShape and endShape


# Sketch_no_tint

Removes the current fill value for displaying images and reverts to displaying images with their original hues.

Parameters
----------

PARAMTEXT

Notes
-----

Removes the current fill value for displaying images and reverts to displaying images with their original hues.


See Also
--------

Py5Graphics.tint(float, float, float, float) : Sets the fill value for displaying images.

Py5Graphics.image(Py5Image, float, float, float, float) : Java AWT Image object associated with this renderer.


# Sketch_noise

Returns the Perlin noise value at specified coordinates.

Parameters
----------

PARAMTEXT

Notes
-----

Returns the Perlin noise value at specified coordinates. Perlin noise is a random sequence generator producing a more natural ordered, harmonic succession of numbers compared to the standard ``random()`` function. It was invented by Ken Perlin in the 1980s and been used since in graphical applications to produce procedural textures, natural motion, shapes, terrains etc.

The main difference to the ``random()`` function is that Perlin noise is defined in an infinite n-dimensional space where each pair of coordinates corresponds to a fixed semi-random value (fixed only for the lifespan of the program). The resulting value will always be between 0.0 and 1.0. Processing can compute 1D, 2D and 3D noise, depending on the number of coordinates given. The noise value can be animated by moving through the noise space as demonstrated in the example above. The 2nd and 3rd dimension can also be interpreted as time.

The actual noise is structured similar to an audio signal, in respect to the function's use of frequencies. Similar to the concept of harmonics in physics, perlin noise is computed over several octaves which are added together for the final result.

Another way to adjust the character of the resulting sequence is the scale of the input coordinates. As the function works within an infinite space the value of the coordinates doesn't matter as such, only the distance between successive coordinates does (eg. when using ``noise()`` within a loop). As a general rule the smaller the difference between coordinates, the smoother the resulting noise sequence will be. Steps of 0.005-0.03 work best for most applications, but this will differ depending on use.


See Also
--------

Sketch.noiseSeed(long)

Sketch.noiseDetail(int, float)

Sketch.random(float,float) : Generates random numbers.


# Sketch_noise_detail

Adjusts the character and level of detail produced by the Perlin noise function.

Parameters
----------

PARAMTEXT

Notes
-----

Adjusts the character and level of detail produced by the Perlin noise function. Similar to harmonics in physics, noise is computed over several octaves. Lower octaves contribute more to the output signal and as such define the overal intensity of the noise, whereas higher octaves create finer grained details in the noise sequence. By default, noise is computed over 4 octaves with each octave contributing exactly half than its predecessor, starting at 50% strength for the 1st octave. This falloff amount can be changed by adding an additional function parameter. Eg. a falloff factor of 0.75 means each octave will now have 75% impact (25% less) of the previous lower octave. Any value between 0.0 and 1.0 is valid, however note that values greater than 0.5 might result in greater than 1.0 values returned by ``noise()`` .

By changing these parameters, the signal created by the ``noise()`` function can be adapted to fit very specific needs and characteristics.


See Also
--------

Sketch.noise(float, float, float) : Returns the Perlin noise value at specified coordinates.

Sketch.noiseDetail(int)


# Sketch_noise_seed

Sets the seed value for , ``noise()`` ,.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the seed value for ``noise()`` . By default, ``noise()`` produces different results each time the program is run. Set the ``value`` parameter to a constant to return the same pseudo-random numbers each time the software is run.


See Also
--------

Sketch.noise(float, float, float) : Returns the Perlin noise value at specified coordinates.

Sketch.noiseDetail(int, float)

Sketch.random(float,float) : Generates random numbers.

Sketch.randomSeed(long)


# Sketch_norm

Normalizes a number from another range into a value between 0 and 1.

Parameters
----------

PARAMTEXT

Notes
-----

Normalizes a number from another range into a value between 0 and 1.

Identical to map(value, low, high, 0, 1);

Numbers outside the range are not clamped to 0 and 1, because out-of-range values are often intentional and useful.


See Also
--------

Sketch.map(float, float, float, float, float) : Re-maps a number from one range to another.

Sketch.lerp(float, float, float) : Calculates a number between two numbers at a specific increment.


# Sketch_normal

Sets the current normal vector.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the current normal vector. This is for drawing three dimensional shapes and surfaces and specifies a vector perpendicular to the surface of the shape which determines how lighting affects it. Processing attempts to automatically assign normals to shapes, but since that's imperfect, this is a better option when you want more control. This function is identical to glNormal3f() in OpenGL.


See Also
--------

Py5Graphics.beginShape(int)

Py5Graphics.endShape(int)

Py5Graphics.lights() : Sets the default ambient light, directional light, falloff, and specular values.


# Sketch_ortho

Sets an orthographic projection and defines a parallel clipping volume.

Parameters
----------

PARAMTEXT

Notes
-----

Sets an orthographic projection and defines a parallel clipping volume. All objects with the same dimension appear the same size, regardless of whether they are near or far from the camera. The parameters to this function specify the clipping volume where left and right are the minimum and maximum x values, top and bottom are the minimum and maximum y values, and near and far are the minimum and maximum z values. If no parameters are given, the default is used: ortho(0, width, 0, height, -10, 10).


# Sketch_parse_boolean

Convert the string "true" or "false" to a boolean.

Parameters
----------

PARAMTEXT

Notes
-----

Convert an integer to a boolean. Because of how Java handles upgrading numbers, this will also cover byte and char (as they will upgrade to an int without any sort of explicit cast).</p>

The preprocessor will convert boolean(what) to parseBoolean(what).</p>


# Sketch_parse_float

Convert an int to a float value.

Parameters
----------

PARAMTEXT

Notes
-----

Convert an int to a float value. Also handles bytes because of Java's rules for upgrading values.


# Sketch_parse_int

Parse a String to an int, and provide an alternate value that should be used when the number is invalid.

Parameters
----------

PARAMTEXT

Notes
-----

Make an array of int elements from an array of String objects. If the String can't be parsed as a number, its entry in the array will be set to the value of the "missing" parameter. String s[] = { "1", "300", "apple", "44" }; int numbers[] = parseInt(s, 9999); numbers will contain { 1, 300, 9999, 44 }


# Sketch_parse_json_array



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Sketch.loadJSONObject(String)

Sketch.saveJSONObject(JSONObject, String)


# Sketch_parse_json_object



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Sketch.loadJSONObject(String)

Sketch.saveJSONObject(JSONObject, String)


# Sketch_parse_xml



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Sketch.loadXML(String)

Sketch.saveXML(XML, String)


# Sketch_pause

Sketch has been paused.

Parameters
----------

PARAMTEXT

Notes
-----

Sketch has been paused. Called when switching tabs in a browser or swapping to a different application on Android. Also called just before quitting. Use to safely disable things like serial, sound, or sensors.


# Sketch_perspective

Sets a perspective projection applying foreshortening, making distant objects appear smaller than closer ones.

Parameters
----------

PARAMTEXT

Notes
-----

Sets a perspective projection applying foreshortening, making distant objects appear smaller than closer ones. The parameters define a viewing volume with the shape of truncated pyramid. Objects near to the front of the volume appear their actual size, while farther objects appear smaller. This projection simulates the perspective of the world more accurately than orthographic projection. The version of perspective without parameters sets the default perspective and the version with four parameters allows the programmer to set the area precisely. The default values are: perspective(PI/3.0, width/height, cameraZ/10.0, cameraZ*10.0) where cameraZ is ((height/2.0) / tan(PI*60.0/360.0));


# Sketch_pixel_density



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Sketch.pixelWidth

Sketch.pixelHeight


# Sketch_pixel_height

When , ``,pixelDensity(2),</d>, is used to make use of a high resolution display (called a Retina display on OS X or high-dpi on Windows and Linux), the width and height of the sketch do not change, but the number of pixels is doubled.

Parameters
----------

PARAMTEXT

Notes
-----

When ``pixel_density(2)</d>is used to make use of a high resolution display (called a _retina display on os x or high-dpi on _windows and _linux) the width and height of the sketch do not change but the number of pixels is doubled. _as a result all operations that use pixels (like ``loadPixels()``  ``get()``  ``set()``  etc.) happen in this doubled space. _as a convenience the variables ``pixelWidth`` and ``pixelHeight ``hold the actual width and height of the sketch in pixels. _this is useful for any sketch that uses the ``pixels[]`` array for instance because the number of elements in the array will be ``pixelWidth*pixelHeight``  not ``width*height`` .


See Also
--------

Sketch.pixelWidth

Sketch.pixelDensity(int)

Sketch.displayDensity()


# Sketch_pixel_width

When , ``,pixelDensity(2),</d>, is used to make use of a high resolution display (called a Retina display on OS X or high-dpi on Windows and Linux), the width and height of the sketch do not change, but the number of pixels is doubled.

Parameters
----------

PARAMTEXT

Notes
-----

When ``pixel_density(2)</d>is used to make use of a high resolution display (called a _retina display on os x or high-dpi on _windows and _linux) the width and height of the sketch do not change but the number of pixels is doubled. _as a result all operations that use pixels (like ``loadPixels()``  ``get()``  ``set()``  etc.) happen in this doubled space. _as a convenience the variables ``pixelWidth`` and ``pixelHeight ``hold the actual width and height of the sketch in pixels. _this is useful for any sketch that uses the ``pixels[]`` array for instance because the number of elements in the array will be ``pixelWidth*pixelHeight``  not ``width*height`` .


See Also
--------

Sketch.pixelHeight

Sketch.pixelDensity(int)

Sketch.displayDensity()


# Sketch_pixels

Array containing the values for all the pixels in the display window.

Parameters
----------

PARAMTEXT

Notes
-----

Array containing the values for all the pixels in the display window. These values are of the color datatype. This array is the size of the display window. For example, if the image is 100x100 pixels, there will be 10000 values and if the window is 200x300 pixels, there will be 60000 values. The ``index`` value defines the position of a value within the array. For example, the statement ``color b = pixels[230]`` will set the variable ``b`` to be equal to the value at that location in the array.

Before accessing this array, the data must loaded with the ``load_pixels()`` function. After the array data has been modified, the ``update_pixels()`` function must be run to update the changes. Without ``load_pixels()`` , running the code may (or will in future releases) result in a NullPointerException.


See Also
--------

Sketch.loadPixels()

Sketch.updatePixels()

Sketch.get(int, int, int, int) : Reads the color of any pixel or grabs a section of an image.

Sketch.set(int, int, int) : Changes the color of any pixel or writes an image directly into the display window.,
, ,
, The , ``x`` , and , ``y`` , parameters specify the pixel to change and the , ``color`` , parameter specifies the color value.

Sketch.pixelDensity(int)

Sketch.pixelWidth

Sketch.pixelHeight


# Sketch_platform

Current platform in use, one of the PConstants WINDOWS, MACOS, LINUX or OTHER.

Parameters
----------

PARAMTEXT

Notes
-----

Current platform in use, one of the PConstants WINDOWS, MACOS, LINUX or OTHER.


# Sketch_pmouse_x

The system variable , ``pmouse_x`` , always contains the horizontal position of the mouse in the frame previous to the current frame.,
, ,
, You may find that , ``pmouse_x`` , and , ``pmouse_y`` , have different values inside , ``draw()`` , and inside events like , ``mouse_pressed()`` , and , ``mouse_moved()`` ,.

Parameters
----------

PARAMTEXT

Notes
-----

The system variable ``pmouse_x`` always contains the horizontal position of the mouse in the frame previous to the current frame.

You may find that ``pmouse_x`` and ``pmouse_y`` have different values inside ``draw()`` and inside events like ``mouse_pressed()`` and ``mouse_moved()`` . This is because they're used for different roles, so don't mix them. Inside ``draw()`` , ``pmouse_x`` and ``pmouse_y`` update only once per frame (once per trip through your ``draw()`` ). But, inside mouse events, they update each time the event is called. If they weren't separated, then the mouse would be read only once per frame, making response choppy. If the mouse variables were always updated multiple times per frame, using ``line(pmouse_x pmouse_y mouse_x mouse_y)`` inside ``draw()`` would have lots of gaps, because ``pmouse_x`` may have changed several times in between the calls to ``line()`` . Use ``pmouse_x`` and ``pmouse_y`` inside ``draw()`` if you want values relative to the previous frame. Use ``pmouse_x`` and ``pmouse_y`` inside the mouse functions if you want continuous response.


See Also
--------

Sketch.mouseX

Sketch.mouseY

Sketch.pmouseY

Sketch.mousePressed

Sketch.mousePressed()

Sketch.mouseReleased()

Sketch.mouseClicked()

Sketch.mouseMoved()

Sketch.mouseDragged()

Sketch.mouseButton

Sketch.mouseWheel(MouseEvent)


# Sketch_pmouse_y

The system variable , ``pmouse_y`` , always contains the vertical position of the mouse in the frame previous to the current frame.

Parameters
----------

PARAMTEXT

Notes
-----

The system variable ``pmouse_y`` always contains the vertical position of the mouse in the frame previous to the current frame. More detailed information about how ``pmouse_y`` is updated inside of ``draw()`` and mouse events is explained in the reference for ``pmouse_x`` .


See Also
--------

Sketch.mouseX

Sketch.mouseY

Sketch.pmouseX

Sketch.mousePressed

Sketch.mousePressed()

Sketch.mouseReleased()

Sketch.mouseClicked()

Sketch.mouseMoved()

Sketch.mouseDragged()

Sketch.mouseButton

Sketch.mouseWheel(MouseEvent)


# Sketch_point

Draws a point, a coordinate in space at the dimension of one pixel.

Parameters
----------

PARAMTEXT

Notes
-----

Draws a point, a coordinate in space at the dimension of one pixel. The first parameter is the horizontal value for the point, the second value is the vertical value for the point, and the optional third value is the depth value. Drawing this shape in 3D with the ``z`` parameter requires the P3D parameter in combination with ``size()`` as shown in the above example.


See Also
--------

Py5Graphics.stroke(int) : Sets the color used to draw lines and borders around shapes.


# Sketch_point_light

Adds a point light.

Parameters
----------

PARAMTEXT

Notes
-----

Adds a point light. Lights need to be included in the ``draw()`` to remain persistent in a looping program. Placing them in the ``setup()`` of a looping program will cause them to only have an effect the first time through the loop. The affect of the ``v1`` , ``v2`` , and ``v3`` parameters is determined by the current color mode. The ``x`` , ``y`` , and ``z`` parameters set the position of the light.


See Also
--------

Py5Graphics.lights() : Sets the default ambient light, directional light, falloff, and specular values.

Py5Graphics.directionalLight(float, float, float, float, float, float)

Py5Graphics.ambientLight(float, float, float, float, float, float)

Py5Graphics.spotLight(float, float, float, float, float, float, float, float, float, float, float)


# Sketch_pop

The , ``pop()`` , function restores the previous drawing style settings and transformations after , ``push()`` , has changed them.

Parameters
----------

PARAMTEXT

Notes
-----

The ``pop()`` function restores the previous drawing style settings and transformations after ``push()`` has changed them. Note that these functions are always used together. They allow you to change the style and transformation settings and later return to what you had. When a new state is started with push(), it builds on the current style and transform information.


 ``push()`` stores information related to the current transformation state and style settings controlled by the following functions: ``rotate()`` , ``translate()`` , ``scale()`` , ``fill()`` , ``stroke()`` , ``tint()`` , ``stroke_weight()`` , ``stroke_cap()`` , ``stroke_join()`` , ``image_mode()`` , ``rect_mode()`` , ``ellipse_mode()`` , ``color_mode()`` , ``text_align()`` , ``text_font()`` , ``text_mode()`` , ``text_size()`` , ``text_leading()`` .

The ``push()`` and ``pop()`` functions were added with Processing 3.5. They can be used in place of ``push_matrix()`` , ``pop_matrix()`` , ``push_styles()`` , and ``pop_styles()`` . The difference is that push() and pop() control both the transformations (rotate, scale, translate) and the drawing styles at the same time.


See Also
--------

Py5Graphics.push() : The , ``push()`` , function saves the current drawing style settings and transformations, while , ``pop()`` , restores these settings.


# Sketch_pop_matrix

Pops the current transformation matrix off the matrix stack.

Parameters
----------

PARAMTEXT

Notes
-----

Pops the current transformation matrix off the matrix stack. Understanding pushing and popping requires understanding the concept of a matrix stack. The ``push_matrix()`` function saves the current coordinate system to the stack and ``pop_matrix()`` restores the prior coordinate system. ``push_matrix()`` and ``pop_matrix()`` are used in conjuction with the other transformation functions and may be embedded to control the scope of the transformations.


See Also
--------

Py5Graphics.pushMatrix()


# Sketch_pop_style

The , ``push_style()`` , function saves the current style settings and , ``pop_style()`` , restores the prior settings; these functions are always used together.

Parameters
----------

PARAMTEXT

Notes
-----

The ``push_style()`` function saves the current style settings and ``pop_style()`` restores the prior settings; these functions are always used together. They allow you to change the style settings and later return to what you had. When a new style is started with ``push_style()`` , it builds on the current style information. The ``push_style()`` and ``pop_style()`` functions can be embedded to provide more control (see the second example above for a demonstration.)


See Also
--------

Py5Graphics.pushStyle()


# Sketch_post_event

Add an event to the internal event queue, or process it immediately if the sketch is not currently looping.

Parameters
----------

PARAMTEXT

Notes
-----

Add an event to the internal event queue, or process it immediately if the sketch is not currently looping.


# Sketch_pow

Facilitates exponential expressions.

Parameters
----------

PARAMTEXT

Notes
-----

Facilitates exponential expressions. The ``pow()`` function is an efficient way of multiplying numbers by themselves (or their reciprocal) in large quantities. For example, ``pow(3 5)`` is equivalent to the expression 3*3*3*3*3 and ``pow(3 -5)`` is equivalent to 1 / 3*3*3*3*3.


See Also
--------

Sketch.sqrt(float) : Calculates the square root of a number.


# Sketch_print

Writes to the console area of the Processing environment.

Parameters
----------

PARAMTEXT

Notes
-----

Writes to the console area of the Processing environment. This is often helpful for looking at the data a program is producing. The companion function ``println()`` works like ``print()`` , but creates a new line of text for each call to the function. Individual elements can be separated with quotes ("") and joined with the addition operator (+).

Beginning with release 0125, to print the contents of an array, use println(). There's no sensible way to do a ``print()`` of an array, because there are too many possibilities for how to separate the data (spaces, commas, etc). If you want to print an array as a single line, use ``join()`` . With ``join()`` , you can choose any delimiter you like and ``print()`` the result.

Using ``print()`` on an object will output ``null`` , a memory location that may look like "@10be08," or the result of the ``to_string()`` method from the object that's being printed. Advanced users who want more useful output when calling ``print()`` on their own classes can add a ``to_string()`` method to the class that returns a String.


See Also
--------

Sketch.println() : Writes to the text area of the Processing environment's console.

Sketch.printArray(Object)

Sketch.join(String[], char) : Combines an array of Strings into one String, each separated by the character(s) used for the , ``separator`` , parameter.


# Sketch_print_array

To come...

Parameters
----------

PARAMTEXT

Notes
-----

To come...


See Also
--------

Sketch.print(byte) : Writes to the console area of the Processing environment.

Sketch.println() : Writes to the text area of the Processing environment's console.


# Sketch_print_camera

Prints the current camera matrix to the Console (the text window at the bottom of Processing).

Parameters
----------

PARAMTEXT

Notes
-----

Prints the current camera matrix to the Console (the text window at the bottom of Processing).


See Also
--------

Py5Graphics.camera(float, float, float, float, float, float, float, float, float) : Sets the position of the camera through setting the eye position, the center of the scene, and which axis is facing upward.


# Sketch_print_matrix

Prints the current matrix to the Console (the text window at the bottom of Processing).

Parameters
----------

PARAMTEXT

Notes
-----

Prints the current matrix to the Console (the text window at the bottom of Processing).


See Also
--------

Py5Graphics.pushMatrix()

Py5Graphics.popMatrix()

Py5Graphics.resetMatrix()

Py5Graphics.applyMatrix(PMatrix)


# Sketch_print_projection

Prints the current projection matrix to the Console (the text window at the bottom of Processing).

Parameters
----------

PARAMTEXT

Notes
-----

Prints the current projection matrix to the Console (the text window at the bottom of Processing).


See Also
--------

Py5Graphics.camera(float, float, float, float, float, float, float, float, float) : Sets the position of the camera through setting the eye position, the center of the scene, and which axis is facing upward.


# Sketch_print_stack_trace

Better way of handling e.printStackTrace() calls so that they can be handled by subclasses as necessary.

Parameters
----------

PARAMTEXT

Notes
-----

Better way of handling e.printStackTrace() calls so that they can be handled by subclasses as necessary.


# Sketch_println

Writes to the text area of the Processing environment's console.

Parameters
----------

PARAMTEXT

Notes
-----

Writes to the text area of the Processing environment's console. This is often helpful for looking at the data a program is producing. Each call to this function creates a new line of output. Individual elements can be separated with quotes ("") and joined with the string concatenation operator (+). See ``print()`` for more about what to expect in the output.

 ``println()`` on an array (by itself) will write the contents of the array to the console. This is often helpful for looking at the data a program is producing. A new line is put between each element of the array. This function can only print one dimensional arrays. For arrays with higher dimensions, the result will be closer to that of ``print()`` .


See Also
--------

Sketch.print(byte) : Writes to the console area of the Processing environment.

Sketch.printArray(Object)


# Sketch_push

The , ``push()`` , function saves the current drawing style settings and transformations, while , ``pop()`` , restores these settings.

Parameters
----------

PARAMTEXT

Notes
-----

The ``push()`` function saves the current drawing style settings and transformations, while ``pop()`` restores these settings. Note that these functions are always used together. They allow you to change the style and transformation settings and later return to what you had. When a new state is started with push(), it builds on the current style and transform information.

 ``push()`` stores information related to the current transformation state and style settings controlled by the following functions: ``rotate()`` , ``translate()`` , ``scale()`` , ``fill()`` , ``stroke()`` , ``tint()`` , ``stroke_weight()`` , ``stroke_cap()`` , ``stroke_join()`` , ``image_mode()`` , ``rect_mode()`` , ``ellipse_mode()`` , ``color_mode()`` , ``text_align()`` , ``text_font()`` , ``text_mode()`` , ``text_size()`` , ``text_leading()`` .

The ``push()`` and ``pop()`` functions were added with Processing 3.5. They can be used in place of ``push_matrix()`` , ``pop_matrix()`` , ``push_styles()`` , and ``pop_styles()`` . The difference is that push() and pop() control both the transformations (rotate, scale, translate) and the drawing styles at the same time.


See Also
--------

Py5Graphics.pop() : The , ``pop()`` , function restores the previous drawing style settings and transformations after , ``push()`` , has changed them.


# Sketch_push_matrix

Pushes the current transformation matrix onto the matrix stack.

Parameters
----------

PARAMTEXT

Notes
-----

Pushes the current transformation matrix onto the matrix stack. Understanding ``push_matrix()`` and ``pop_matrix()`` requires understanding the concept of a matrix stack. The ``push_matrix()`` function saves the current coordinate system to the stack and ``pop_matrix()`` restores the prior coordinate system. ``push_matrix()`` and ``pop_matrix()`` are used in conjuction with the other transformation functions and may be embedded to control the scope of the transformations.


See Also
--------

Py5Graphics.popMatrix()

Py5Graphics.translate(float, float, float) : Specifies an amount to displace objects within the display window.

Py5Graphics.scale(float) : Increases or decreases the size of a shape by expanding and contracting vertices.

Py5Graphics.rotate(float) : Rotates a shape the amount specified by the , ``angle`` , parameter.

Py5Graphics.rotateX(float)

Py5Graphics.rotateY(float)

Py5Graphics.rotateZ(float)


# Sketch_push_style

The , ``push_style()`` , function saves the current style settings and , ``pop_style()`` , restores the prior settings.

Parameters
----------

PARAMTEXT

Notes
-----

The ``push_style()`` function saves the current style settings and ``pop_style()`` restores the prior settings. Note that these functions are always used together. They allow you to change the style settings and later return to what you had. When a new style is started with ``push_style()`` , it builds on the current style information. The ``push_style()`` and ``pop_style()`` functions can be embedded to provide more control (see the second example above for a demonstration.)

The style information controlled by the following functions are included in the style: fill(), stroke(), tint(), strokeWeight(), strokeCap(), strokeJoin(), imageMode(), rectMode(), ellipseMode(), shapeMode(), colorMode(), textAlign(), textFont(), textMode(), textSize(), textLeading(), emissive(), specular(), shininess(), ambient()


See Also
--------

Py5Graphics.popStyle()


# Sketch_quad

A quad is a quadrilateral, a four sided polygon.

Parameters
----------

PARAMTEXT

Notes
-----

A quad is a quadrilateral, a four sided polygon. It is similar to a rectangle, but the angles between its edges are not constrained to ninety degrees. The first pair of parameters (x1,y1) sets the first vertex and the subsequent pairs should proceed clockwise or counter-clockwise around the defined shape.


# Sketch_quadratic_vertex



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Py5Graphics.curveVertex(float, float, float)

Py5Graphics.vertex(float, float, float, float, float) : Used by renderer subclasses or Py5Shape to efficiently pass in already formatted vertex information.

Py5Graphics.bezierVertex(float, float, float, float, float, float)

Py5Graphics.bezier(float, float, float, float, float, float, float, float, float, float, float, float) : Draws a Bezier curve on the screen.


# Sketch_radians

Converts a degree measurement to its corresponding value in radians.

Parameters
----------

PARAMTEXT

Notes
-----

Converts a degree measurement to its corresponding value in radians. Radians and degrees are two ways of measuring the same thing. There are 360 degrees in a circle and 2*PI radians in a circle. For example, 90°= PI/2 = 1.5707964. All trigonometric functions in Processing require their parameters to be specified in radians.


See Also
--------

Sketch.degrees(float) : Converts a radian measurement to its corresponding value in degrees.


# Sketch_random

Generates random numbers.

Parameters
----------

PARAMTEXT

Notes
-----

Generates random numbers. Each time the ``random()`` function is called, it returns an unexpected value within the specified range. If one parameter is passed to the function it will return a ``float`` between zero and the value of the ``high`` parameter. The function call ``random(5)`` returns values between 0 and 5 (starting at zero, up to but not including 5). If two parameters are passed, it will return a ``float`` with a value between the the parameters. The function call ``random(-5 10.2)`` returns values starting at -5 up to (but not including) 10.2. To convert a floating-point random number to an integer, use the ``int()`` function.


See Also
--------

Sketch.randomSeed(long)

Sketch.noise(float, float, float) : Returns the Perlin noise value at specified coordinates.


# Sketch_random_gaussian

Returns a float from a random series of numbers having a mean of 0 and standard deviation of 1.

Parameters
----------

PARAMTEXT

Notes
-----

Returns a float from a random series of numbers having a mean of 0 and standard deviation of 1. Each time the ``random_gaussian()`` function is called, it returns a number fitting a Gaussian, or normal, distribution. There is theoretically no minimum or maximum value that ``random_gaussian()`` might return. Rather, there is just a very low probability that values far from the mean will be returned; and a higher probability that numbers near the mean will be returned.


See Also
--------

Sketch.random(float,float) : Generates random numbers.

Sketch.noise(float, float, float) : Returns the Perlin noise value at specified coordinates.


# Sketch_random_seed

Sets the seed value for , ``random()`` ,.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the seed value for ``random()`` . By default, ``random()`` produces different results each time the program is run. Set the ``value`` parameter to a constant to return the same pseudo-random numbers each time the software is run.


See Also
--------

Sketch.random(float,float) : Generates random numbers.

Sketch.noise(float, float, float) : Returns the Perlin noise value at specified coordinates.

Sketch.noiseSeed(long)


# Sketch_recorder

A leech graphics object that is echoing all events.

Parameters
----------

PARAMTEXT

Notes
-----

A leech graphics object that is echoing all events.


# Sketch_rect

Draws a rectangle to the screen.

Parameters
----------

PARAMTEXT

Notes
-----

Draws a rectangle to the screen. A rectangle is a four-sided shape with every angle at ninety degrees. By default, the first two parameters set the location of the upper-left corner, the third sets the width, and the fourth sets the height. These parameters may be changed with the ``rect_mode()`` function.


See Also
--------

Py5Graphics.rectMode(int)

Py5Graphics.quad(float, float, float, float, float, float, float, float) : A quad is a quadrilateral, a four sided polygon.


# Sketch_rect_mode

Modifies the location from which rectangles draw.

Parameters
----------

PARAMTEXT

Notes
-----

Modifies the location from which rectangles draw. The default mode is ``rect_mode(corner)`` , which specifies the location to be the upper left corner of the shape and uses the third and fourth parameters of ``rect()`` to specify the width and height. The syntax ``rect_mode(corners)`` uses the first and second parameters of ``rect()`` to set the location of one corner and uses the third and fourth parameters to set the opposite corner. The syntax ``rect_mode(center)`` draws the image from its center point and uses the third and forth parameters of ``rect()`` to specify the image's width and height. The syntax ``rect_mode(radius)`` draws the image from its center point and uses the third and forth parameters of ``rect()`` to specify half of the image's width and height. The parameter must be written in ALL CAPS because Processing is a case sensitive language. Note: In version 125, the mode named CENTER_RADIUS was shortened to RADIUS.


See Also
--------

Py5Graphics.rect(float, float, float, float) : Draws a rectangle to the screen.


# Sketch_red

Extracts the red value from a color, scaled to match current , ``color_mode()`` ,.

Parameters
----------

PARAMTEXT

Notes
-----

Extracts the red value from a color, scaled to match current ``color_mode()`` . This value is always returned as a  float so be careful not to assign it to an int value.

The red() function is easy to use and undestand, but is slower than another technique. To achieve the same results when working in ``color_mode(rgb 255)`` , but with greater speed, use the>>(right shift) operator with a bit mask. For example, the following two lines of code are equivalent:
<pre>float r1 = red(myColor);
float r2 = myColor>>16&0xFF;</pre>


See Also
--------

Py5Graphics.green(int) : Extracts the green value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.blue(int) : Extracts the blue value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.alpha(int) : Extracts the alpha value from a color.

Py5Graphics.hue(int) : Extracts the hue value from a color.

Py5Graphics.saturation(int) : Extracts the saturation value from a color.

Py5Graphics.brightness(int) : Extracts the brightness value from a color.


# Sketch_redraw

flag set to true when a redraw is asked for by the user

Parameters
----------

PARAMTEXT

Notes
-----

Executes the code within ``draw()`` one time. This functions allows the program to update the display window only when necessary, for example when an event registered by ``mouse_pressed()`` or ``key_pressed()`` occurs.

structuring a program, it only makes sense to call redraw() within events such as ``mouse_pressed()`` . This is because ``redraw()`` does not run ``draw()`` immediately (it only sets a flag that indicates an update is needed).

 ``redraw()`` within ``draw()`` has no effect because ``draw()`` is continuously called anyway.


See Also
--------

Sketch.draw() : Called directly after , ``setup()`` , and continuously executes the lines of code contained inside its block until the program is stopped or , ``no_loop()`` , is called.

Sketch.loop() : Causes Processing to continuously execute the code within , ``draw()`` ,.

Sketch.noLoop()

Sketch.frameRate(float)


# Sketch_register_lock

Lock when un/registering from multiple threads

Parameters
----------

PARAMTEXT

Notes
-----

Lock when un/registering from multiple threads


# Sketch_register_map

Map of registered methods, stored by name.

Parameters
----------

PARAMTEXT

Notes
-----

Map of registered methods, stored by name.


# Sketch_register_method

Register a built-in event so that it can be fired for libraries, etc.

Parameters
----------

PARAMTEXT

Notes
-----

Register a built-in event so that it can be fired for libraries, etc. Supported events include:<ul><li>pre \u2013 at the very top of the draw() method (safe to draw)<li>draw \u2013 at the end of the draw() method (safe to draw)<li>post \u2013 after draw() has exited (not safe to draw)<li>pause \u2013 called when the sketch is paused<li>resume \u2013 called when the sketch is resumed<li>dispose \u2013 when the sketch is shutting down (definitely not safe to draw)<ul>In addition, the new (for 2.0) processing.event classes are passed to the following event types:<ul><li>mouseEvent<li>keyEvent<li>touchEvent</ul>The older java.awt events are no longer supported. See the Library Wiki page for more details.


# Sketch_request_image

This function load images on a separate thread so that your sketch does not freeze while images load during , ``setup()`` ,.

Parameters
----------

PARAMTEXT

Notes
-----

This function load images on a separate thread so that your sketch does not freeze while images load during ``setup()`` . While the image is loading, its width and height will be 0. If an error occurs while loading the image, its width and height will be set to -1. You'll know when the image has loaded properly because its width and height will be greater than 0. Asynchronous image loading (particularly when downloading from a server) can dramatically improve performance.

 ``extension`` parameter is used to determine the image type in cases where the image filename does not end with a proper extension. Specify the extension as the second parameter to ``request_image()`` .


See Also
--------

Sketch.loadImage(String, String)


# Sketch_reset_matrix

Replaces the current matrix with the identity matrix.

Parameters
----------

PARAMTEXT

Notes
-----

Replaces the current matrix with the identity matrix. The equivalent function in OpenGL is glLoadIdentity().


See Also
--------

Py5Graphics.pushMatrix()

Py5Graphics.popMatrix()

Py5Graphics.applyMatrix(PMatrix)

Py5Graphics.printMatrix()


# Sketch_reset_shader

This is a new reference entry for Processing 2.0.

Parameters
----------

PARAMTEXT

Notes
-----

This is a new reference entry for Processing 2.0. It will be updated shortly.


# Sketch_resume

Sketch has resumed.

Parameters
----------

PARAMTEXT

Notes
-----

Sketch has resumed. Called when switching tabs in a browser or swapping to this application on Android. Also called on startup. Use this to safely disable things like serial, sound, or sensors.


# Sketch_reverse

Reverses the order of an array.

Parameters
----------

PARAMTEXT

Notes
-----

Reverses the order of an array.


See Also
--------

Sketch.sort(String[], int) : Sorts an array of numbers from smallest to largest and puts an array of words in alphabetical order.


# Sketch_rotate

Rotates a shape the amount specified by the , ``angle`` , parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Rotates a shape the amount specified by the ``angle`` parameter. Angles should be specified in radians (values from 0 to TWO_PI) or converted to radians with the ``radians()`` function.

Objects are always rotated around their relative position to the origin and positive numbers rotate objects in a clockwise direction. Transformations apply to everything that happens after and subsequent calls to the function accumulates the effect. For example, calling ``rotate(half_pi)`` and then ``rotate(half_pi)`` is the same as ``rotate(pi)`` . All tranformations are reset when ``draw()`` begins again.

Technically, ``rotate()`` multiplies the current transformation matrix by a rotation matrix. This function can be further controlled by the ``push_matrix()`` and ``pop_matrix()`` .


See Also
--------

Py5Graphics.popMatrix()

Py5Graphics.pushMatrix()

Py5Graphics.rotateX(float)

Py5Graphics.rotateY(float)

Py5Graphics.rotateZ(float)

Py5Graphics.scale(float, float, float) : Increases or decreases the size of a shape by expanding and contracting vertices.

Sketch.radians(float) : Converts a degree measurement to its corresponding value in radians.


# Sketch_rotate_x

Rotates a shape around the x-axis the amount specified by the , ``angle`` , parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Rotates a shape around the x-axis the amount specified by the ``angle`` parameter. Angles should be specified in radians (values from 0 to PI*2) or converted to radians with the ``radians()`` function. Objects are always rotated around their relative position to the origin and positive numbers rotate objects in a counterclockwise direction. Transformations apply to everything that happens after and subsequent calls to the function accumulates the effect. For example, calling ``rotate_x(pi/2)`` and then ``rotate_x(pi/2)`` is the same as ``rotate_x(pi)`` . If ``rotate_x()`` is called within the ``draw()`` , the transformation is reset when the loop begins again. This function requires using P3D as a third parameter to ``size()`` as shown in the example above.


See Also
--------

Py5Graphics.popMatrix()

Py5Graphics.pushMatrix()

Py5Graphics.rotate(float) : Rotates a shape the amount specified by the , ``angle`` , parameter.

Py5Graphics.rotateY(float)

Py5Graphics.rotateZ(float)

Py5Graphics.scale(float, float, float) : Increases or decreases the size of a shape by expanding and contracting vertices.

Py5Graphics.translate(float, float, float) : Specifies an amount to displace objects within the display window.


# Sketch_rotate_y

Rotates a shape around the y-axis the amount specified by the , ``angle`` , parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Rotates a shape around the y-axis the amount specified by the ``angle`` parameter. Angles should be specified in radians (values from 0 to PI*2) or converted to radians with the ``radians()`` function. Objects are always rotated around their relative position to the origin and positive numbers rotate objects in a counterclockwise direction. Transformations apply to everything that happens after and subsequent calls to the function accumulates the effect. For example, calling ``rotate_y(pi/2)`` and then ``rotate_y(pi/2)`` is the same as ``rotate_y(pi)`` . If ``rotate_y()`` is called within the ``draw()`` , the transformation is reset when the loop begins again. This function requires using P3D as a third parameter to ``size()`` as shown in the examples above.


See Also
--------

Py5Graphics.popMatrix()

Py5Graphics.pushMatrix()

Py5Graphics.rotate(float) : Rotates a shape the amount specified by the , ``angle`` , parameter.

Py5Graphics.rotateX(float)

Py5Graphics.rotateZ(float)

Py5Graphics.scale(float, float, float) : Increases or decreases the size of a shape by expanding and contracting vertices.

Py5Graphics.translate(float, float, float) : Specifies an amount to displace objects within the display window.


# Sketch_rotate_z

Rotates a shape around the z-axis the amount specified by the , ``angle`` , parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Rotates a shape around the z-axis the amount specified by the ``angle`` parameter. Angles should be specified in radians (values from 0 to PI*2) or converted to radians with the ``radians()`` function. Objects are always rotated around their relative position to the origin and positive numbers rotate objects in a counterclockwise direction. Transformations apply to everything that happens after and subsequent calls to the function accumulates the effect. For example, calling ``rotate_z(pi/2)`` and then ``rotate_z(pi/2)`` is the same as ``rotate_z(pi)`` . If ``rotate_z()`` is called within the ``draw()`` , the transformation is reset when the loop begins again. This function requires using P3D as a third parameter to ``size()`` as shown in the examples above.


See Also
--------

Py5Graphics.popMatrix()

Py5Graphics.pushMatrix()

Py5Graphics.rotate(float) : Rotates a shape the amount specified by the , ``angle`` , parameter.

Py5Graphics.rotateX(float)

Py5Graphics.rotateY(float)

Py5Graphics.scale(float, float, float) : Increases or decreases the size of a shape by expanding and contracting vertices.

Py5Graphics.translate(float, float, float) : Specifies an amount to displace objects within the display window.


# Sketch_round

Calculates the integer closest to the , ``value`` , parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Calculates the integer closest to the ``value`` parameter. For example, ``round(9.2)`` returns the value 9.


See Also
--------

Sketch.floor(float) : Calculates the closest int value that is less than or equal to the value of the parameter.

Sketch.ceil(float) : Calculates the closest int value that is greater than or equal to the value of the parameter.


# Sketch_run_sketch

Convenience method for Python Mode to run an already-constructed sketch.

Parameters
----------

PARAMTEXT

Notes
-----

Convenience method for Python Mode to run an already-constructed sketch. This makes it makes it easy to launch a sketch in Jython:<pre>class MySketch(Sketch):     passMySketch().runSketch();</pre>


# Sketch_saturation

Extracts the saturation value from a color.

Parameters
----------

PARAMTEXT

Notes
-----

Extracts the saturation value from a color.


See Also
--------

Py5Graphics.red(int) : Extracts the red value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.green(int) : Extracts the green value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.blue(int) : Extracts the blue value from a color, scaled to match current , ``color_mode()`` ,.

Py5Graphics.alpha(int) : Extracts the alpha value from a color.

Py5Graphics.hue(int) : Extracts the hue value from a color.

Py5Graphics.brightness(int) : Extracts the brightness value from a color.


# Sketch_save

Saves an image from the display window.

Parameters
----------

PARAMTEXT

Notes
-----

Saves an image from the display window. Images are saved in TIFF, TARGA, JPEG, and PNG format depending on the extension within the ``filename`` parameter. For example, "image.tif" will have a TIFF image and "image.png" will save a PNG image. If no extension is included in the filename, the image will save in TIFF format and ``.tif`` will be added to the name. These files are saved to the sketch's folder, which may be opened by selecting "Show sketch folder" from the "Sketch" menu. It is not possible to use ``save()`` while running the program in a web browser.
images saved from the main drawing window will be opaque. To save images without a background, use ``create_graphics()`` .


See Also
--------

Sketch.saveFrame()

Sketch.createGraphics(int, int, String)


# Sketch_save_bytes

Opposite of , ``load_bytes()`` ,, will write an entire array of bytes to a file.

Parameters
----------

PARAMTEXT

Notes
-----

Opposite of ``load_bytes()`` , will write an entire array of bytes to a file. The data is saved in binary format. This file is saved to the sketch's folder, which is opened by selecting "Show sketch folder" from the "Sketch" menu.

It is not possible to use saveXxxxx() functions inside a web browser unless the sketch is<a href="http://wiki.processing.org/w/Sign_an_Applet">signed applet</A>. To save a file back to a server, see the<a href="http://wiki.processing.org/w/Saving_files_to_a_web-server">save to web</A>code snippet on the Processing Wiki.


See Also
--------

Sketch.loadStrings(String)

Sketch.loadBytes(String)

Sketch.saveStrings(String, String[])


# Sketch_save_file

Identical to savePath(), but returns a File object.

Parameters
----------

PARAMTEXT

Notes
-----

Identical to savePath(), but returns a File object.


# Sketch_save_frame

Saves a numbered sequence of images, one image each time the function is run.

Parameters
----------

PARAMTEXT

Notes
-----

Saves a numbered sequence of images, one image each time the function is run. To save an image that is identical to the display window, run the function at the end of ``draw()`` or within mouse and key events such as ``mouse_pressed()`` and ``key_pressed()`` . If ``save_frame()`` is called without parameters, it will save the files as screen-0000.tif, screen-0001.tif, etc. It is possible to specify the name of the sequence with the ``filename`` parameter and make the choice of saving TIFF, TARGA, PNG, or JPEG files with the ``ext`` parameter. These image sequences can be loaded into programs such as Apple's QuickTime software and made into movies. These files are saved to the sketch's folder, which may be opened by selecting "Show sketch folder" from the "Sketch" menu.

It is not possible to use saveXxxxx() functions inside a web browser unless the sketch is<a href="http://wiki.processing.org/w/Sign_an_Applet">signed applet</A>. To save a file back to a server, see the<a href="http://wiki.processing.org/w/Saving_files_to_a_web-server">save to web</A>code snippet on the Processing Wiki.
<br/>All images saved from the main drawing window will be opaque. To save images without a background, use ``create_graphics()`` .


See Also
--------

Sketch.save(String) : Saves an image from the display window.

Sketch.createGraphics(int, int, String, String)

Sketch.frameCount


# Sketch_save_json_array



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Sketch.loadJSONObject(String)

Sketch.loadJSONArray(String)

Sketch.saveJSONObject(JSONObject, String)


# Sketch_save_json_object



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Sketch.loadJSONObject(String)

Sketch.loadJSONArray(String)

Sketch.saveJSONArray(JSONArray, String)


# Sketch_save_path

Returns a path inside the applet folder to save to.

Parameters
----------

PARAMTEXT

Notes
-----

Returns a path inside the applet folder to save to. Like sketchPath(), but creates any in-between folders so that things save properly.

All saveXxxx() functions use the path to the sketch folder, rather than its data folder. Once exported, the data folder will be found inside the jar file of the exported application or applet. In this case, it's not possible to save data into the jar file, because it will often be running from a server, or marked in-use if running from a local file system. With this in mind, saving to the data path doesn't make sense anyway. If you know you're running locally, and want to save to the data folder, use

``
save_xxxx("data/blah.dat")
``

.


# Sketch_save_stream

Identical to the other saveStream(), but writes to a File object, for greater control over the file location.

Parameters
----------

PARAMTEXT

Notes
-----

Save the contents of a stream to a file in the sketch folder. This is basically ``save_bytes(blah load_bytes())`` , but done more efficiently (and with less confusing syntax).

When using the ``target_file`` parameter, it writes to a ``_file`` object for greater control over the file location. (Note that unlike some other functions, this will not automatically compress or uncompress gzip files.)


See Also
--------

Sketch.createOutput(String)


# Sketch_save_strings

Writes an array of strings to a file, one line per string.

Parameters
----------

PARAMTEXT

Notes
-----

Writes an array of strings to a file, one line per string. This file is saved to the sketch's folder, which is opened by selecting "Show sketch folder" from the "Sketch" menu.

It is not possible to use saveXxxxx() functions inside a web browser unless the sketch is<a href="http://wiki.processing.org/w/Sign_an_Applet">signed applet</A>. To save a file back to a server, see the<a href="http://wiki.processing.org/w/Saving_files_to_a_web-server">save to web</A>code snippet on the Processing Wiki.
<br/>Starting with Processing 1.0, all files loaded and saved by the Processing API use UTF-8 encoding. In previous releases, the default encoding for your platform was used, which causes problems when files are moved to other platforms.


See Also
--------

Sketch.loadStrings(String)

Sketch.loadBytes(String)

Sketch.saveBytes(String, byte[])


# Sketch_save_table



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Sketch.loadTable(String)


# Sketch_save_xml



Parameters
----------

PARAMTEXT

Notes
-----




See Also
--------

Sketch.loadXML(String)

Sketch.parseXML(String)


# Sketch_scale

Increases or decreases the size of a shape by expanding and contracting vertices.

Parameters
----------

PARAMTEXT

Notes
-----

Increases or decreases the size of a shape by expanding and contracting vertices. Objects always scale from their relative origin to the coordinate system. Scale values are specified as decimal percentages. For example, the function call ``scale(2.0)`` increases the dimension of a shape by 200%. Transformations apply to everything that happens after and subsequent calls to the function multiply the effect. For example, calling ``scale(2.0)`` and then ``scale(1.5)`` is the same as ``scale(3.0)`` . If ``scale()`` is called within ``draw()`` , the transformation is reset when the loop begins again. Using this fuction with the ``z`` parameter requires using P3D as a parameter for ``size()`` as shown in the example above. This function can be further controlled by ``push_matrix()`` and ``pop_matrix()`` .


See Also
--------

Py5Graphics.pushMatrix()

Py5Graphics.popMatrix()

Py5Graphics.translate(float, float, float) : Specifies an amount to displace objects within the display window.

Py5Graphics.rotate(float) : Rotates a shape the amount specified by the , ``angle`` , parameter.

Py5Graphics.rotateX(float)

Py5Graphics.rotateY(float)

Py5Graphics.rotateZ(float)


# Sketch_screen_x

Takes a three-dimensional X, Y, Z position and returns the X value for where it will appear on a (two-dimensional) screen.

Parameters
----------

PARAMTEXT

Notes
-----

Takes a three-dimensional X, Y, Z position and returns the X value for where it will appear on a (two-dimensional) screen.


See Also
--------

Py5Graphics.screenY(float, float, float)

Py5Graphics.screenZ(float, float, float)


# Sketch_screen_y

Takes a three-dimensional X, Y, Z position and returns the Y value for where it will appear on a (two-dimensional) screen.

Parameters
----------

PARAMTEXT

Notes
-----

Takes a three-dimensional X, Y, Z position and returns the Y value for where it will appear on a (two-dimensional) screen.


See Also
--------

Py5Graphics.screenX(float, float, float)

Py5Graphics.screenZ(float, float, float)


# Sketch_screen_z

Takes a three-dimensional X, Y, Z position and returns the Z value for where it will appear on a (two-dimensional) screen.

Parameters
----------

PARAMTEXT

Notes
-----

Takes a three-dimensional X, Y, Z position and returns the Z value for where it will appear on a (two-dimensional) screen.


See Also
--------

Py5Graphics.screenX(float, float, float)

Py5Graphics.screenY(float, float, float)


# Sketch_second

Processing communicates with the clock on your computer.

Parameters
----------

PARAMTEXT

Notes
-----

Processing communicates with the clock on your computer. The ``second()`` function returns the current second as a value from 0 - 59.


See Also
--------

Sketch.millis() : Returns the number of milliseconds (thousandths of a second) since starting an applet.

Sketch.minute() : Processing communicates with the clock on your computer.

Sketch.hour() : Processing communicates with the clock on your computer.

Sketch.day() : Processing communicates with the clock on your computer.

Sketch.month() : Processing communicates with the clock on your computer.

Sketch.year() : Processing communicates with the clock on your computer.


# Sketch_select_folder

See selectInput() for details.

Parameters
----------

PARAMTEXT

Notes
-----

See selectInput() for details.


# Sketch_select_input

Open a platform-specific file chooser dialog to select a file for input.

Parameters
----------

PARAMTEXT

Notes
-----

Open a platform-specific file chooser dialog to select a file for input. After the selection is made, the selected File will be passed to the 'callback' function. If the dialog is closed or canceled, null will be sent to the function, so that the program is not waiting for additional input. The callback is necessary because of how threading works.<pre>void setup() {   selectInput("Select a file to process:", "fileSelected"); } void fileSelected(File selection) {   if (selection == null) {     println("Window was closed or the user hit cancel.");   } else {     println("User selected " + fileSeleted.getAbsolutePath());   } }</pre>For advanced users, the method must be 'public', which is true for all methods inside a sketch when run from the PDE, but must explicitly be set when using Eclipse or other development environments.


# Sketch_select_output

See selectInput() for details.

Parameters
----------

PARAMTEXT

Notes
-----

See selectInput() for details.


# Sketch_set

Changes the color of any pixel or writes an image directly into the display window.,
, ,
, The , ``x`` , and , ``y`` , parameters specify the pixel to change and the , ``color`` , parameter specifies the color value.

Parameters
----------

PARAMTEXT

Notes
-----

Changes the color of any pixel or writes an image directly into the display window.

The ``x`` and ``y`` parameters specify the pixel to change and the ``color`` parameter specifies the color value. The color parameter is affected by the current color mode (the default is RGB values from 0 to 255). When setting an image, the ``x`` and ``y`` parameters define the coordinates for the upper-left corner of the image, regardless of the current ``image_mode()`` .

Setting the color of a single pixel with ``set(x y)`` is easy, but not as fast as putting the data directly into ``pixels[]`` . The equivalent statement to ``set(x y #000000)`` using ``pixels[]`` is ``pixels[y*width+x] = #000000`` . See the reference for ``pixels[]`` for more information.


See Also
--------

Py5Image.get(int, int, int, int) : Reads the color of any pixel or grabs a section of an image.

Py5Image.pixels : Array containing the values for all the pixels in the display window.

Py5Image.copy(Py5Image, int, int, int, int, int, int, int, int) : Copies a region of pixels from one image into another.


# Sketch_set_matrix

Set the current transformation to the contents of the specified source.

Parameters
----------

PARAMTEXT

Notes
-----

Set the current transformation to the contents of the specified source.


# Sketch_set_size

Called by Py5Surface objects to set the width and height variables, and update the pixelWidth and pixelHeight variables.

Parameters
----------

PARAMTEXT

Notes
-----

Called by Py5Surface objects to set the width and height variables, and update the pixelWidth and pixelHeight variables.


# Sketch_settings

Description to come...

Parameters
----------

PARAMTEXT

Notes
-----

Description to come...  Override this method to call size() when not using the PDE.


See Also
--------

Sketch.fullScreen()

Sketch.setup() : The , ``setup()`` , function is called once when the program starts.

Sketch.size(int,int) : Defines the dimension of the display window in units of pixels.

Sketch.smooth() : 


# Sketch_setup

The , ``setup()`` , function is called once when the program starts.

Parameters
----------

PARAMTEXT

Notes
-----

The ``setup()`` function is called once when the program starts. It's used to define initial enviroment properties such as screen size and background color and to load media such as images and fonts as the program starts. There can only be one ``setup()`` function for each program and it shouldn't be called again after its initial execution. Note: Variables declared within ``setup()`` are not accessible within other functions, including ``draw()`` .


See Also
--------

Sketch.size(int, int) : Defines the dimension of the display window in units of pixels.

Sketch.loop() : Causes Processing to continuously execute the code within , ``draw()`` ,.

Sketch.noLoop()

Sketch.draw() : Called directly after , ``setup()`` , and continuously executes the lines of code contained inside its block until the program is stopped or , ``no_loop()`` , is called.


# Sketch_shader

This is a new reference entry for Processing 2.0.

Parameters
----------

PARAMTEXT

Notes
-----

This is a new reference entry for Processing 2.0. It will be updated shortly.


# Sketch_shape

Displays shapes to the screen.

Parameters
----------

PARAMTEXT

Notes
-----

Displays shapes to the screen. The shapes must be in the sketch's "data" directory to load correctly. Select "Add file..." from the "Sketch" menu to add the shape. Processing currently works with SVG shapes only. The ``sh`` parameter specifies the shape to display and the ``x`` and ``y`` parameters define the location of the shape from its upper-left corner. The shape is displayed at its original size unless the ``width`` and ``height`` parameters specify a different size. The ``shape_mode()`` function changes the way the parameters work. A call to ``shape_mode(corners)`` , for example, will change the width and height parameters to define the x and y values of the opposite corner of the shape.

Note complex shapes may draw awkwardly with P3D. This renderer does not yet support shapes that have holes or complicated breaks.


See Also
--------

Sketch.loadShape(String)

Py5Graphics.shapeMode(int) Convenience method to draw at a particular location.


# Sketch_shape_mode

Modifies the location from which shapes draw.

Parameters
----------

PARAMTEXT

Notes
-----

Modifies the location from which shapes draw. The default mode is ``shape_mode(corner)`` , which specifies the location to be the upper left corner of the shape and uses the third and fourth parameters of ``shape()`` to specify the width and height. The syntax ``shape_mode(corners)`` uses the first and second parameters of ``shape()`` to set the location of one corner and uses the third and fourth parameters to set the opposite corner. The syntax ``shape_mode(center)`` draws the shape from its center point and uses the third and forth parameters of ``shape()`` to specify the width and height. The parameter must be written in "ALL CAPS" because Processing is a case sensitive language.


See Also
--------

Py5Graphics.shape(Py5Shape) : Type of shape passed to beginShape(), zero if no shape is currently being drawn.

Py5Graphics.rectMode(int)


# Sketch_shear_x

Shears a shape around the x-axis the amount specified by the , ``angle`` , parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Shears a shape around the x-axis the amount specified by the ``angle`` parameter. Angles should be specified in radians (values from 0 to PI*2) or converted to radians with the ``radians()`` function. Objects are always sheared around their relative position to the origin and positive numbers shear objects in a clockwise direction. Transformations apply to everything that happens after and subsequent calls to the function accumulates the effect. For example, calling ``shear_x(pi/2)`` and then ``shear_x(pi/2)`` is the same as ``shear_x(pi)`` . If ``shear_x()`` is called within the ``draw()`` , the transformation is reset when the loop begins again.

Technically, ``shear_x()`` multiplies the current transformation matrix by a rotation matrix. This function can be further controlled by the ``push_matrix()`` and ``pop_matrix()`` functions.


See Also
--------

Py5Graphics.popMatrix()

Py5Graphics.pushMatrix()

Py5Graphics.shearY(float)

Py5Graphics.scale(float, float, float) : Increases or decreases the size of a shape by expanding and contracting vertices.

Py5Graphics.translate(float, float, float) : Specifies an amount to displace objects within the display window.

Sketch.radians(float) : Converts a degree measurement to its corresponding value in radians.


# Sketch_shear_y

Shears a shape around the y-axis the amount specified by the , ``angle`` , parameter.

Parameters
----------

PARAMTEXT

Notes
-----

Shears a shape around the y-axis the amount specified by the ``angle`` parameter. Angles should be specified in radians (values from 0 to PI*2) or converted to radians with the ``radians()`` function. Objects are always sheared around their relative position to the origin and positive numbers shear objects in a clockwise direction. Transformations apply to everything that happens after and subsequent calls to the function accumulates the effect. For example, calling ``shear_y(pi/2)`` and then ``shear_y(pi/2)`` is the same as ``shear_y(pi)`` . If ``shear_y()`` is called within the ``draw()`` , the transformation is reset when the loop begins again.

Technically, ``shear_y()`` multiplies the current transformation matrix by a rotation matrix. This function can be further controlled by the ``push_matrix()`` and ``pop_matrix()`` functions.


See Also
--------

Py5Graphics.popMatrix()

Py5Graphics.pushMatrix()

Py5Graphics.shearX(float)

Py5Graphics.scale(float, float, float) : Increases or decreases the size of a shape by expanding and contracting vertices.

Py5Graphics.translate(float, float, float) : Specifies an amount to displace objects within the display window.

Sketch.radians(float) : Converts a degree measurement to its corresponding value in radians.


# Sketch_shell

Same as exec() above, but prefixes the call with a shell.

Parameters
----------

PARAMTEXT

Notes
-----

Same as exec() above, but prefixes the call with a shell.


# Sketch_shininess

Sets the amount of gloss in the surface of shapes.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the amount of gloss in the surface of shapes. Used in combination with ``ambient()`` , ``specular()`` , and ``emissive()`` in setting the material properties of shapes.


See Also
--------

Py5Graphics.emissive(float, float, float) : Sets the emissive color of the material used for drawing shapes drawn to the screen.

Py5Graphics.ambient(float, float, float) : Sets the ambient reflectance for shapes drawn to the screen.

Py5Graphics.specular(float, float, float) : Sets the specular color of the materials used for shapes drawn to the screen, which sets the color of hightlights.


# Sketch_shorten

Decreases an array by one element and returns the shortened array.

Parameters
----------

PARAMTEXT

Notes
-----

Decreases an array by one element and returns the shortened array.

When using an array of objects, the data returned from the function must be cast to the object array's data type. For example:<em>SomeClass[] items = (SomeClass[]) shorten(originalArray)</em>.


See Also
--------

Sketch.append(byte[], byte) : Expands an array by one element and adds data to the new position.

Sketch.expand(boolean[]) : Increases the size of an array.


# Sketch_show_depth_warning

Display a warning that the specified method is only available with 3D.

Parameters
----------

PARAMTEXT

Notes
-----

Display a warning that the specified method is only available with 3D.


# Sketch_show_depth_warning_xyz

Display a warning that the specified method that takes x, y, z parameters can only be used with x and y parameters in this renderer.

Parameters
----------

PARAMTEXT

Notes
-----

Display a warning that the specified method that takes x, y, z parameters can only be used with x and y parameters in this renderer.


# Sketch_show_method_warning

Display a warning that the specified method is simply unavailable.

Parameters
----------

PARAMTEXT

Notes
-----

Display a warning that the specified method is simply unavailable.


# Sketch_show_missing_warning

Display a warning that the specified method is not implemented, meaning that it could be either a completely missing function, although other variations of it may still work properly.

Parameters
----------

PARAMTEXT

Notes
-----

Display a warning that the specified method is not implemented, meaning that it could be either a completely missing function, although other variations of it may still work properly.


# Sketch_show_surface

Danger: available for advanced subclassing, but here be dragons.

Parameters
----------

PARAMTEXT

Notes
-----

Danger: available for advanced subclassing, but here be dragons.


# Sketch_show_variation_warning

Error that a particular variation of a method is unavailable (even though other variations are).

Parameters
----------

PARAMTEXT

Notes
-----

Error that a particular variation of a method is unavailable (even though other variations are). For instance, if vertex(x, y, u, v) is not available, but vertex(x, y) is just fine.


# Sketch_sin

Calculates the sine of an angle.

Parameters
----------

PARAMTEXT

Notes
-----

Calculates the sine of an angle. This function expects the values of the ``angle`` parameter to be provided in radians (values from 0 to 6.28). Values are returned in the range -1 to 1.


See Also
--------

Sketch.cos(float) : Calculates the cosine of an angle.

Sketch.tan(float) : Calculates the ratio of the sine and cosine of an angle.

Sketch.radians(float) : Converts a degree measurement to its corresponding value in radians.


# Sketch_size

Defines the dimension of the display window in units of pixels.

Parameters
----------

PARAMTEXT

Notes
-----

Defines the dimension of the display window in units of pixels. The ``size()`` function must be the first line in ``setup()`` . If ``size()`` is not used, the default size of the window is 100x100 pixels. The system variables ``width`` and ``height`` are set by the parameters passed to this function.

Do not use variables as the parameters to ``size()`` function, because it will cause problems when exporting your sketch. When variables are used, the dimensions of your sketch cannot be determined during export. Instead, employ numeric values in the ``size()`` statement, and then use the built-in ``width`` and ``height`` variables inside your program when the dimensions of the display window are needed.

The ``size()`` function can only be used once inside a sketch, and cannot be used for resizing.

 ``renderer`` parameter selects which rendering engine to use. For example, if you will be drawing 3D shapes, use ``p3_d`` , if you want to export images from a program as a PDF file use ``pdf`` . A brief description of the three primary renderers follows:

 ``p2_d`` (Processing 2D) - The default renderer that supports two dimensional drawing.

 ``p3_d`` (Processing 3D) - 3D graphics renderer that makes use of OpenGL-compatible graphics hardware.

 ``pdf`` - The PDF renderer draws 2D graphics directly to an Acrobat PDF file. This produces excellent results when you need vector shapes for high resolution output or printing. You must first use Import LibraryPDF to make use of the library. More information can be found in the PDF library reference.

The P3D renderer doesn't support ``stroke_cap()`` or ``stroke_join()`` , which can lead to ugly results when using ``stroke_weight()`` . (<a href="http://code.google.com/p/processing/issues/detail?id=123">Issue 123</a>)

The maximum width and height is limited by your operating system, and is usually the width and height of your actual screen. On some machines it may simply be the number of pixels on your current screen, meaning that a screen of 800x600 could support ``size(1600 300)`` , since it's the same number of pixels. This varies widely so you'll have to try different rendering modes and sizes until you get what you're looking for. If you need something larger, use ``create_graphics`` to create a non-visible drawing surface.

Again, the ``size()`` function must be the first line of the code (or first item inside setup). Any code that appears before the ``size()`` command may run more than once, which can lead to confusing results.

Advanced
--------

If using Java 1.3 or later, this will default to using Py5Graphics2, the Java2D-based renderer. If using Java 1.1, or if Py5Graphics2 is not available, then Py5Graphics will be used. To set your own renderer, use the other version of the size() method that takes a renderer as its last parameter.

If called once a renderer has already been set, this will use the previous renderer and simply resize it.


See Also
--------

Sketch.width : System variable which stores the width of the display window.

Sketch.height : System variable which stores the height of the display window.

Sketch.setup() : The , ``setup()`` , function is called once when the program starts.

Sketch.settings() : Description to come...

Sketch.fullScreen()


# Sketch_sketch_path

Prepend the sketch folder path to the filename (or path) that is passed in.

Parameters
----------

PARAMTEXT

Notes
-----

Prepend the sketch folder path to the filename (or path) that is passed in. External libraries should use this function to save to the sketch folder.

Note that when running as an applet inside a web browser, the sketchPath will be set to null, because security restrictions prevent applets from accessing that information.

This will also cause an error if the sketch is not inited properly, meaning that init() was never called on the Sketch when hosted my some other main() or by other code. For proper use of init(), see the examples in the main description text for Sketch.


# Sketch_smooth



Parameters
----------

PARAMTEXT

Notes
-----




# Sketch_sort

Sorts an array of numbers from smallest to largest and puts an array of words in alphabetical order.

Parameters
----------

PARAMTEXT

Notes
-----

Sorts an array of numbers from smallest to largest and puts an array of words in alphabetical order. The original array is not modified, a re-ordered array is returned. The ``count`` parameter states the number of elements to sort. For example if there are 12 elements in an array and if count is the value 5, only the first five elements on the array will be sorted.<!--As of release 0126, the alphabetical ordering is case insensitive.-->


See Also
--------

Sketch.reverse(boolean[]) : Reverses the order of an array.


# Sketch_specular

Sets the specular color of the materials used for shapes drawn to the screen, which sets the color of hightlights.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the specular color of the materials used for shapes drawn to the screen, which sets the color of hightlights. Specular refers to light which bounces off a surface in a perferred direction (rather than bouncing in all directions like a diffuse light). Used in combination with ``emissive()`` , ``ambient()`` , and ``shininess()`` in setting the material properties of shapes.


See Also
--------

Py5Graphics.lightSpecular(float, float, float)

Py5Graphics.ambient(float, float, float) : Sets the ambient reflectance for shapes drawn to the screen.

Py5Graphics.emissive(float, float, float) : Sets the emissive color of the material used for drawing shapes drawn to the screen.

Py5Graphics.shininess(float) : Sets the amount of gloss in the surface of shapes.


# Sketch_sphere

A sphere is a hollow ball made from tessellated triangles.

Parameters
----------

PARAMTEXT

Notes
-----

A sphere is a hollow ball made from tessellated triangles.

Advanced
--------



Implementation notes:

cache all the points of the sphere in a static array top and bottom are just a bunch of triangles that land in the center point

sphere is a series of concentric circles who radii vary along the shape, based on, er.. cos or something

``
[toxi 031031] new sphere code. removed all multiplies with radius as scale() will take care of that anyway [toxi 031223] updated sphere code (removed modulos) and introduced sphere_at(xyzr) to avoid additional translate()'s on the user/sketch side [davbol 080801] now using separate sphere_detail_u/v
``


See Also
--------

Py5Graphics.sphereDetail(int)


# Sketch_sphere_detail

Controls the detail used to render a sphere by adjusting the number of vertices of the sphere mesh.

Parameters
----------

PARAMTEXT

Notes
-----

Controls the detail used to render a sphere by adjusting the number of vertices of the sphere mesh. The default resolution is 30, which creates a fairly detailed sphere definition with vertices every 360/30 = 12 degrees. If you're going to render a great number of spheres per frame, it is advised to reduce the level of detail using this function. The setting stays active until ``sphere_detail()`` is called again with a new parameter and so should<i>not</i>be called prior to every ``sphere()`` statement, unless you wish to render spheres with different settings, e.g. using less detail for smaller spheres or ones further away from the camera. To control the detail of the horizontal and vertical resolution independently, use the version of the functions with two parameters.

Advanced
--------

Code for sphereDetail() submitted by toxi [031031]. Code for enhanced u/v version from davbol [080801].


See Also
--------

Py5Graphics.sphere(float) : A sphere is a hollow ball made from tessellated triangles.


# Sketch_splice

Inserts a value or array of values into an existing array.

Parameters
----------

PARAMTEXT

Notes
-----

Inserts a value or array of values into an existing array. The first two parameters must be of the same datatype. The ``array`` parameter defines the array which will be modified and the second parameter defines the data which will be inserted.

When using an array of objects, the data returned from the function must be cast to the object array's data type. For example:<em>SomeClass[] items = (SomeClass[]) splice(array1, array2, index)</em>.


See Also
--------

Sketch.concat(boolean[], boolean[]) : Concatenates two arrays.

Sketch.subset(boolean[], int, int) : Extracts an array of elements from an existing array.


# Sketch_split

The split() function breaks a string into pieces using a character or string as the divider.

Parameters
----------

PARAMTEXT

Notes
-----

The split() function breaks a string into pieces using a character or string as the divider. The ``delim`` parameter specifies the character or characters that mark the boundaries between each piece. A String[] array is returned that contains each of the pieces.

If the result is a set of numbers, you can convert the String[] array to to a float[] or int[] array using the datatype conversion functions ``int()`` and ``float()`` (see example above).

The ``split_tokens()`` function works in a similar fashion, except that it splits using a range of characters instead of a specific character or sequence.<!-- /><br /> This function uses regular expressions to determine how the  ``delim``  parameter divides the  ``str``  parameter. Therefore, if you use characters such parentheses and brackets that are used with regular expressions as a part of the  ``delim``  parameter, you'll need to put two blackslashes (\\\\) in front of the character (see example above). You can read more about <a href="http://en.wikipedia.org/wiki/Regular_expression">regular expressions</a> and <a href="http://en.wikipedia.org/wiki/Escape_character">escape characters</a> on Wikipedia. -->


# Sketch_split_tokens

The splitTokens() function splits a String at one or many character "tokens." The , ``tokens`` , parameter specifies the character or characters to be used as a boundary.

Parameters
----------

PARAMTEXT

Notes
-----

The splitTokens() function splits a String at one or many character "tokens." The ``tokens`` parameter specifies the character or characters to be used as a boundary.

If no ``tokens`` character is specified, any whitespace character is used to split. Whitespace characters include tab (\\t), line feed (\\n), carriage return (\\r), form feed (\\f), and space. To convert a String to an array of integers or floats, use the datatype conversion functions ``int()`` and ``float()`` to convert the array of Strings.


See Also
--------

Sketch.split(String, String) : The split() function breaks a string into pieces using a character or string as the divider.

Sketch.join(String[], String) : Combines an array of Strings into one String, each separated by the character(s) used for the , ``separator`` , parameter.

Sketch.trim(String) : Removes whitespace characters from the beginning and end of a String.


# Sketch_spot_light

Adds a spot light.

Parameters
----------

PARAMTEXT

Notes
-----

Adds a spot light. Lights need to be included in the ``draw()`` to remain persistent in a looping program. Placing them in the ``setup()`` of a looping program will cause them to only have an effect the first time through the loop. The affect of the ``v1`` , ``v2`` , and ``v3`` parameters is determined by the current color mode. The ``x`` , ``y`` , and ``z`` parameters specify the position of the light and ``nx`` , ``ny`` , ``nz`` specify the direction or light. The ``angle`` parameter affects angle of the spotlight cone.


See Also
--------

Py5Graphics.lights() : Sets the default ambient light, directional light, falloff, and specular values.

Py5Graphics.directionalLight(float, float, float, float, float, float)

Py5Graphics.pointLight(float, float, float, float, float, float)

Py5Graphics.ambientLight(float, float, float, float, float, float)


# Sketch_sq

Squares a number (multiplies a number by itself).

Parameters
----------

PARAMTEXT

Notes
-----

Squares a number (multiplies a number by itself). The result is always a positive number, as multiplying two negative numbers always yields a positive result. For example, -1 * -1 = 1.


See Also
--------

Sketch.sqrt(float) : Calculates the square root of a number.


# Sketch_sqrt

Calculates the square root of a number.

Parameters
----------

PARAMTEXT

Notes
-----

Calculates the square root of a number. The square root of a number is always positive, even though there may be a valid negative root. The square root ``s`` of number ``a`` is such that ``s*s = a`` . It is the opposite of squaring.


See Also
--------

Sketch.pow(float, float) : Facilitates exponential expressions.

Sketch.sq(float) : Squares a number (multiplies a number by itself).


# Sketch_square

Draws a square to the screen.

Parameters
----------

PARAMTEXT

Notes
-----

Draws a square to the screen. A square is a four-sided shape with every angle at ninety degrees and each side is the same length. By default, the first two parameters set the location of the upper-left corner, the third sets the width and height. The way these parameters are interpreted, however, may be changed with the ``rect_mode()`` function.


See Also
--------

Py5Graphics.rect(float, float, float, float) : Draws a rectangle to the screen.

Py5Graphics.rectMode(int)


# Sketch_start

Called by the browser or applet viewer to inform this applet that it should start its execution.

Parameters
----------

PARAMTEXT

Notes
-----

Called by the browser or applet viewer to inform this applet that it should start its execution. It is called after the init method and each time the applet is revisited in a Web page.

Called explicitly via the first call to Sketch.paint(), because SketchGL needs to have a usable screen before getting things rolling.


# Sketch_start_surface

See warning in showSurface()

Parameters
----------

PARAMTEXT

Notes
-----

See warning in showSurface()


# Sketch_stop

Called by the browser or applet viewer to inform this applet that it should stop its execution.

Parameters
----------

PARAMTEXT

Notes
-----

Called by the browser or applet viewer to inform this applet that it should stop its execution.

Unfortunately, there are no guarantees from the Java spec when or if stop() will be called (i.e. on browser quit, or when moving between web pages), and it's not always called.


# Sketch_stroke

Sets the color used to draw lines and borders around shapes.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the color used to draw lines and borders around shapes. This color is either specified in terms of the RGB or HSB color depending on the current ``color_mode()`` (the default color space is RGB, with each value in the range from 0 to 255).

When using hexadecimal notation to specify a color, use "#" or "0x" before the values (e.g. #CCFFAA, 0xFFCCFFAA). The # syntax uses six digits to specify a color (the way colors are specified in HTML and CSS). When using the hexadecimal notation starting with "0x", the hexadecimal value must be specified with eight characters; the first two characters define the alpha component and the remainder the red, green, and blue components.

The value for the parameter "gray" must be less than or equal to the current maximum value as specified by ``color_mode()`` . The default maximum value is 255.


See Also
--------

Py5Graphics.noStroke()

Py5Graphics.strokeWeight(float)

Py5Graphics.strokeJoin(int)

Py5Graphics.strokeCap(int)

Py5Graphics.fill(int, float) : true if fill() is enabled, (read-only)

Py5Graphics.noFill()

Py5Graphics.tint(int, float) : Sets the fill value for displaying images.

Py5Graphics.background(float, float, float, float) : The , ``background()`` , function sets the color used for the background of the Processing window.

Py5Graphics.colorMode(int, float, float, float, float)


# Sketch_stroke_cap

Sets the style for rendering line endings.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the style for rendering line endings. These ends are either squared, extended, or rounded and specified with the corresponding parameters SQUARE, PROJECT, and ROUND. The default cap is ROUND.

This function is not available with the P3D renderer (<a href="http://code.google.com/p/processing/issues/detail?id=123">see Issue 123</a>). More information about the renderers can be found in the ``size()`` reference.


See Also
--------

Py5Graphics.stroke(int, float) : Sets the color used to draw lines and borders around shapes.

Py5Graphics.strokeWeight(float)

Py5Graphics.strokeJoin(int)

Sketch.size(int, int, String, String) : Defines the dimension of the display window in units of pixels.


# Sketch_stroke_join

Sets the style of the joints which connect line segments.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the style of the joints which connect line segments. These joints are either mitered, beveled, or rounded and specified with the corresponding parameters MITER, BEVEL, and ROUND. The default joint is MITER.

This function is not available with the P3D renderer, (<a href="http://code.google.com/p/processing/issues/detail?id=123">see Issue 123</a>). More information about the renderers can be found in the ``size()`` reference.


See Also
--------

Py5Graphics.stroke(int, float) : Sets the color used to draw lines and borders around shapes.

Py5Graphics.strokeWeight(float)

Py5Graphics.strokeCap(int)


# Sketch_stroke_weight

Sets the width of the stroke used for lines, points, and the border around shapes.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the width of the stroke used for lines, points, and the border around shapes. All widths are set in units of pixels.

When drawing with P3D, series of connected lines (such as the stroke around a polygon, triangle, or ellipse) produce unattractive results when a thick stroke weight is set (<a href="http://code.google.com/p/processing/issues/detail?id=123">see Issue 123</a>). With P3D, the minimum and maximum values for ``stroke_weight()`` are controlled by the graphics card and the operating system's OpenGL implementation. For instance, the thickness may not go higher than 10 pixels.


See Also
--------

Py5Graphics.stroke(int, float) : Sets the color used to draw lines and borders around shapes.

Py5Graphics.strokeJoin(int)

Py5Graphics.strokeCap(int)


# Sketch_subset

Extracts an array of elements from an existing array.

Parameters
----------

PARAMTEXT

Notes
-----

Extracts an array of elements from an existing array. The ``array`` parameter defines the array from which the elements will be copied and the ``offset`` and ``length`` parameters determine which elements to extract. If no ``length`` is given, elements will be extracted from the ``offset`` to the end of the array. When specifying the ``offset`` remember the first array element is 0. This function does not change the source array.

When using an array of objects, the data returned from the function must be cast to the object array's data type. For example:<em>SomeClass[] items = (SomeClass[]) subset(originalArray, 0, 4)</em>.


See Also
--------

Sketch.splice(boolean[], boolean, int) : Inserts a value or array of values into an existing array.


# Sketch_tan

Calculates the ratio of the sine and cosine of an angle.

Parameters
----------

PARAMTEXT

Notes
-----

Calculates the ratio of the sine and cosine of an angle. This function expects the values of the ``angle`` parameter to be provided in radians (values from 0 to PI*2). Values are returned in the range ``infinity`` to ``-infinity`` .


See Also
--------

Sketch.cos(float) : Calculates the cosine of an angle.

Sketch.sin(float) : Calculates the sine of an angle.

Sketch.radians(float) : Converts a degree measurement to its corresponding value in radians.


# Sketch_text

This does a basic number formatting, to avoid the generally ugly appearance of printing floats.

Parameters
----------

PARAMTEXT

Notes
-----

Draws text to the screen. Displays the information specified in the ``data`` or ``stringdata`` parameters on the screen in the position specified by the ``x`` and ``y`` parameters and the optional ``z`` parameter. A default font will be used unless a font is set with the ``text_font()`` function. Change the color of the text with the ``fill()`` function. The text displays in relation to the ``text_align()`` function, which gives the option to draw to the left, right, and center of the coordinates.

The ``x2`` and ``y2`` parameters define a rectangular area to display within and may only be used with string data. For text drawn inside a rectangle, the coordinates are interpreted based on the current ``rect_mode()`` setting.


See Also
--------

Py5Graphics.textAlign(int, int)

Py5Graphics.textFont(Py5Font)

Py5Graphics.textMode(int)

Py5Graphics.textSize(float)

Py5Graphics.textLeading(float)

Py5Graphics.textWidth(String)

Py5Graphics.textAscent()

Py5Graphics.textDescent()

Py5Graphics.rectMode(int)

Py5Graphics.fill(int, float) : true if fill() is enabled, (read-only)


# Sketch_text_align

Sets the current alignment for drawing text.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the current alignment for drawing text. The parameters LEFT, CENTER, and RIGHT set the display characteristics of the letters in relation to the values for the ``x`` and ``y`` parameters of the ``text()`` function.

In Processing 0125 and later, an optional second parameter can be used to vertically align the text. BASELINE is the default, and the vertical alignment will be reset to BASELINE if the second parameter is not used. The TOP and CENTER parameters are straightforward. The BOTTOM parameter offsets the line based on the current ``text_descent()`` . For multiple lines, the final line will be aligned to the bottom, with the previous lines appearing above it.

When using ``text()`` with width and height parameters, BASELINE is ignored, and treated as TOP. (Otherwise, text would by default draw outside the box, since BASELINE is the default setting. BASELINE is not a useful drawing mode for text drawn in a rectangle.)

The vertical alignment is based on the value of ``text_ascent()`` , which many fonts do not specify correctly. It may be necessary to use a hack and offset by a few pixels by hand so that the offset looks correct. To do this as less of a hack, use some percentage of ``text_ascent()`` or ``text_descent()`` so that the hack works even if you change the size of the font.


See Also
--------

Sketch.loadFont(String)

Py5Graphics.text(String, float, float) : This does a basic number formatting, to avoid the generally ugly appearance of printing floats.

Py5Graphics.textSize(float)

Py5Graphics.textAscent()

Py5Graphics.textDescent()


# Sketch_text_ascent

Returns ascent of the current font at its current size.

Parameters
----------

PARAMTEXT

Notes
-----

Returns ascent of the current font at its current size. This information is useful for determining the height of the font above the baseline. For example, adding the ``text_ascent()`` and ``text_descent()`` values will give you the total height of the line.


See Also
--------

Py5Graphics.textDescent()


# Sketch_text_descent

Returns descent of the current font at its current size.

Parameters
----------

PARAMTEXT

Notes
-----

Returns descent of the current font at its current size. This information is useful for determining the height of the font below the baseline. For example, adding the ``text_ascent()`` and ``text_descent()`` values will give you the total height of the line.


See Also
--------

Py5Graphics.textAscent()


# Sketch_text_font

Sets the current font that will be drawn with the , ``text()`` , function.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the current font that will be drawn with the ``text()`` function. Fonts must be loaded with ``load_font()`` before it can be used. This font will be used in all subsequent calls to the ``text()`` function. If no ``size`` parameter is input, the font will appear at its original size (the size it was created at with the "Create Font..." tool) until it is changed with ``text_size()`` .

Because fonts are usually bitmaped, you should create fonts at the sizes that will be used most commonly. Using ``text_font()`` without the size parameter will result in the cleanest-looking text.

With the default (JAVA2D) and PDF renderers, it's also possible to enable the use of native fonts via the command ``hint(enable_native_fonts)`` . This will produce vector text in JAVA2D sketches and PDF output in cases where the vector data is available: when the font is still installed, or the font is created via the ``create_font()`` function (rather than the Create Font tool).


See Also
--------

Sketch.createFont(String, float, boolean)

Sketch.loadFont(String)

Py5Graphics.text(String, float, float) : This does a basic number formatting, to avoid the generally ugly appearance of printing floats.

Py5Graphics.textSize(float)


# Sketch_text_leading

Sets the spacing between lines of text in units of pixels.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the spacing between lines of text in units of pixels. This setting will be used in all subsequent calls to the ``text()`` function.


See Also
--------

Sketch.loadFont(String)

Py5Font.Py5Font

Py5Graphics.text(String, float, float) : This does a basic number formatting, to avoid the generally ugly appearance of printing floats.

Py5Graphics.textFont(Py5Font)

Py5Graphics.textSize(float)


# Sketch_text_mode

Sets the way text draws to the screen.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the way text draws to the screen. In the default configuration, the ``model`` mode, it's possible to rotate, scale, and place letters in two and three dimensional space.

The ``shape`` mode draws text using the the glyph outlines of individual characters rather than as textures. This mode is only supported with the ``pdf`` and ``p3_d`` renderer settings. With the ``pdf`` renderer, you must call ``text_mode(shape)`` before any other drawing occurs. If the outlines are not available, then ``text_mode(shape)`` will be ignored and ``text_mode(model)`` will be used instead.

The ``text_mode(shape)`` option in ``p3_d`` can be combined with ``begin_raw()`` to write vector-accurate text to 2D and 3D output files, for instance ``dxf`` or ``pdf`` . The ``shape`` mode is not currently optimized for ``p3_d`` , so if recording shape data, use ``text_mode(model)`` until you're ready to capture the geometry with ``begin_raw()`` .


See Also
--------

Sketch.loadFont(String)

Py5Font.Py5Font

Py5Graphics.text(String, float, float) : This does a basic number formatting, to avoid the generally ugly appearance of printing floats.

Py5Graphics.textFont(Py5Font)

Py5Graphics.beginRaw(Py5Graphics)

Sketch.createFont(String, float, boolean)


# Sketch_text_size

Sets the current font size.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the current font size. This size will be used in all subsequent calls to the ``text()`` function. Font size is measured in units of pixels.


See Also
--------

Sketch.loadFont(String)

Py5Font.Py5Font

Py5Graphics.text(String, float, float) : This does a basic number formatting, to avoid the generally ugly appearance of printing floats.

Py5Graphics.textFont(Py5Font)


# Sketch_text_width

Calculates and returns the width of any character or text string.

Parameters
----------

PARAMTEXT

Notes
-----

Calculates and returns the width of any character or text string.


See Also
--------

Sketch.loadFont(String)

Py5Font.Py5Font

Py5Graphics.text(String, float, float) : This does a basic number formatting, to avoid the generally ugly appearance of printing floats.

Py5Graphics.textFont(Py5Font)

Py5Graphics.textSize(float)


# Sketch_texture

Sets a texture to be applied to vertex points.

Parameters
----------

PARAMTEXT

Notes
-----

Sets a texture to be applied to vertex points. The ``texture()`` function must be called between ``begin_shape()`` and ``end_shape()`` and before any calls to ``vertex()`` .

When textures are in use, the fill color is ignored. Instead, use tint() to specify the color of the texture as it is applied to the shape.


See Also
--------

Py5Graphics.textureMode(int)

Py5Graphics.textureWrap(int)

Py5Graphics.beginShape(int)

Py5Graphics.endShape(int)

Py5Graphics.vertex(float, float, float, float, float) : Used by renderer subclasses or Py5Shape to efficiently pass in already formatted vertex information.


# Sketch_texture_mode

Sets the coordinate space for texture mapping.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the coordinate space for texture mapping. There are two options, IMAGE, which refers to the actual coordinates of the image, and NORMAL, which refers to a normalized space of values ranging from 0 to 1. The default mode is IMAGE. In IMAGE, if an image is 100 x 200 pixels, mapping the image onto the entire size of a quad would require the points (0,0) (0,100) (100,200) (0,200). The same mapping in NORMAL_SPACE is (0,0) (0,1) (1,1) (0,1).


See Also
--------

Py5Graphics.texture(Py5Image) : Sets a texture to be applied to vertex points.

Py5Graphics.textureWrap(int)


# Sketch_texture_wrap

Description to come...

Parameters
----------

PARAMTEXT

Notes
-----

Description to come... ( end auto-generated from textureWrap.xml )


See Also
--------

Py5Graphics.texture(Py5Image) : Sets a texture to be applied to vertex points.

Py5Graphics.textureMode(int)


# Sketch_thread

Launch a new thread and call the specified function from that new thread.

Parameters
----------

PARAMTEXT

Notes
-----

Launch a new thread and call the specified function from that new thread. This is a very simple way to do a thread without needing to get into classes, runnables, etc.

Note that the function being called must be public. Inside the PDE, 'public' is automatically added, but when used without the preprocessor, (like from Eclipse) you'll have to do it yourself.


See Also
--------

Sketch.setup() : The , ``setup()`` , function is called once when the program starts.

Sketch.draw() : Called directly after , ``setup()`` , and continuously executes the lines of code contained inside its block until the program is stopped or , ``no_loop()`` , is called.

Sketch.loop() : Causes Processing to continuously execute the code within , ``draw()`` ,.

Sketch.noLoop()


# Sketch_tint

Sets the fill value for displaying images.

Parameters
----------

PARAMTEXT

Notes
-----

Sets the fill value for displaying images. Images can be tinted to specified colors or made transparent by setting the alpha.

To make an image transparent, but not change it's color, use white as the tint color and specify an alpha value. For instance, tint(255, 128) will make an image 50% transparent (unless ``color_mode()`` has been used).

When using hexadecimal notation to specify a color, use "#" or "0x" before the values (e.g. #CCFFAA, 0xFFCCFFAA). The # syntax uses six digits to specify a color (the way colors are specified in HTML and CSS). When using the hexadecimal notation starting with "0x", the hexadecimal value must be specified with eight characters; the first two characters define the alpha component and the remainder the red, green, and blue components.

The value for the parameter "gray" must be less than or equal to the current maximum value as specified by ``color_mode()`` . The default maximum value is 255.

The ``tint()`` function is also used to control the coloring of textures in 3D.


See Also
--------

Py5Graphics.noTint()

Py5Graphics.image(Py5Image, float, float, float, float) : Java AWT Image object associated with this renderer.


# Sketch_translate

Specifies an amount to displace objects within the display window.

Parameters
----------

PARAMTEXT

Notes
-----

Specifies an amount to displace objects within the display window. The ``x`` parameter specifies left/right translation, the ``y`` parameter specifies up/down translation, and the ``z`` parameter specifies translations toward/away from the screen. Using this function with the ``z`` parameter requires using P3D as a parameter in combination with size as shown in the above example. Transformations apply to everything that happens after and subsequent calls to the function accumulates the effect. For example, calling ``translate(50 0)`` and then ``translate(20 0)`` is the same as ``translate(70 0)`` . If ``translate()`` is called within ``draw()`` , the transformation is reset when the loop begins again. This function can be further controlled by the ``push_matrix()`` and ``pop_matrix()`` .


See Also
--------

Py5Graphics.popMatrix()

Py5Graphics.pushMatrix()

Py5Graphics.rotate(float) : Rotates a shape the amount specified by the , ``angle`` , parameter.

Py5Graphics.rotateX(float)

Py5Graphics.rotateY(float)

Py5Graphics.rotateZ(float)

Py5Graphics.scale(float, float, float) : Increases or decreases the size of a shape by expanding and contracting vertices.


# Sketch_triangle

A triangle is a plane created by connecting three points.

Parameters
----------

PARAMTEXT

Notes
-----

A triangle is a plane created by connecting three points. The first two arguments specify the first point, the middle two arguments specify the second point, and the last two arguments specify the third point.


See Also
--------

Sketch.beginShape()


# Sketch_trim

Removes whitespace characters from the beginning and end of a String.

Parameters
----------

PARAMTEXT

Notes
-----

Removes whitespace characters from the beginning and end of a String. In addition to standard whitespace characters such as space, carriage return, and tab, this function also removes the Unicode "nbsp" character.


See Also
--------

Sketch.split(String, String) : The split() function breaks a string into pieces using a character or string as the divider.

Sketch.join(String[], char) : Combines an array of Strings into one String, each separated by the character(s) used for the , ``separator`` , parameter.


# Sketch_unbinary

Converts a String representation of a binary number to its equivalent integer value.

Parameters
----------

PARAMTEXT

Notes
-----

Converts a String representation of a binary number to its equivalent integer value. For example, unbinary("00001000") will return 8.


See Also
--------

Sketch.binary(byte) : Converts a byte, char, int, or color to a String containing the equivalent binary notation.

Sketch.hex(int,int) : Converts a byte, char, int, or color to a String containing the equivalent hexadecimal notation.

Sketch.unhex(String) : Converts a String representation of a hexadecimal number to its equivalent integer value.


# Sketch_uncaught_throwable

used by the UncaughtExceptionHandler, so has to be static

Parameters
----------

PARAMTEXT

Notes
-----

used by the UncaughtExceptionHandler, so has to be static


# Sketch_unhex

Converts a String representation of a hexadecimal number to its equivalent integer value.

Parameters
----------

PARAMTEXT

Notes
-----

Converts a String representation of a hexadecimal number to its equivalent integer value.


See Also
--------

Sketch.hex(int, int) : Converts a byte, char, int, or color to a String containing the equivalent hexadecimal notation.

Sketch.binary(byte) : Converts a byte, char, int, or color to a String containing the equivalent binary notation.

Sketch.unbinary(String) : Converts a String representation of a binary number to its equivalent integer value.


# Sketch_update_pixels

Updates the display window with the data in the , ``pixels[]`` , array.

Parameters
----------

PARAMTEXT

Notes
-----

Updates the display window with the data in the ``pixels[]`` array. Use in conjunction with ``load_pixels()`` . If you're only reading pixels from the array, there's no need to call ``update_pixels()`` unless there are changes.

renderers may or may not seem to require ``load_pixels()`` or ``update_pixels()`` . However, the rule is that any time you want to manipulate the ``pixels[]`` array, you must first call ``load_pixels()`` , and after changes have been made, call ``update_pixels()`` . Even if the renderer may not seem to use this function in the current Processing release, this will always be subject to change.

Currently, none of the renderers use the additional parameters to ``update_pixels()`` , however this may be implemented in the future.


See Also
--------

Sketch.loadPixels()

Sketch.pixels : Array containing the values for all the pixels in the display window.


# Sketch_use_native_select

Whether to use native (AWT) dialogs for selectInput and selectOutput.

Parameters
----------

PARAMTEXT

Notes
-----

Whether to use native (AWT) dialogs for selectInput and selectOutput. The native dialogs on some platforms can be ugly, buggy, or missing features. For 3.3.5, this defaults to true on all platforms.


# Sketch_vertex

Used by renderer subclasses or Py5Shape to efficiently pass in already formatted vertex information.

Parameters
----------

PARAMTEXT

Notes
-----

All shapes are constructed by connecting a series of vertices. ``vertex()`` is used to specify the vertex coordinates for points, lines, triangles, quads, and polygons and is used exclusively within the ``begin_shape()`` and ``end_shape()`` function.

Drawing a vertex in 3D using the ``z`` parameter requires the P3D parameter in combination with size as shown in the above example.

This function is also used to map a texture onto the geometry. The ``texture()`` function declares the texture to apply to the geometry and the ``u`` and ``v`` coordinates set define the mapping of this texture to the form. By default, the coordinates used for ``u`` and ``v`` are specified in relation to the image's size in pixels, but this relation can be changed with ``texture_mode()`` .


See Also
--------

Py5Graphics.beginShape(int)

Py5Graphics.endShape(int)

Py5Graphics.bezierVertex(float, float, float, float, float, float, float, float, float)

Py5Graphics.quadraticVertex(float, float, float, float, float, float)

Py5Graphics.curveVertex(float, float, float)

Py5Graphics.texture(Py5Image) : Sets a texture to be applied to vertex points.


# Sketch_width

System variable which stores the width of the display window.

Parameters
----------

PARAMTEXT

Notes
-----

System variable which stores the width of the display window. This value is set by the first parameter of the ``size()`` function. For example, the function call ``size(320 240)`` sets the ``width`` variable to the value 320. The value of ``width`` is zero until ``size()`` is called.


See Also
--------

Sketch.height : System variable which stores the height of the display window.

Sketch.size(int, int) : Defines the dimension of the display window in units of pixels.


# Sketch_year

Processing communicates with the clock on your computer.

Parameters
----------

PARAMTEXT

Notes
-----

Processing communicates with the clock on your computer. The ``year()`` function returns the current year as an integer (2003, 2004, 2005, etc).  The ``year()`` function returns the current year as an integer (2003, 2004, 2005, etc).


See Also
--------

Sketch.millis() : Returns the number of milliseconds (thousandths of a second) since starting an applet.

Sketch.second() : Processing communicates with the clock on your computer.

Sketch.minute() : Processing communicates with the clock on your computer.

Sketch.hour() : Processing communicates with the clock on your computer.

Sketch.day() : Processing communicates with the clock on your computer.

Sketch.month() : Processing communicates with the clock on your computer.

