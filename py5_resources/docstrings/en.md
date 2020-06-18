
# background

the background function sets the background

Params
----

pass a 'color'

this function is awesome.

# text_align

Sets the current alignment for drawing text.

Parameters
----------

align_x: int
    horizontal alignment, either LEFT, CENTER, or RIGHT

align_y: int
    vertical alignment, either TOP, BOTTOM, CENTER, or BASELINE

Notes
-----

Sets the current alignment for drawing text. The parameters LEFT, CENTER, and RIGHT set the display characteristics of the letters in relation to the values for the `x` and `y` parameters of the `text()` function.

In Processing 0125 and later, an optional second parameter can be used to vertically align the text. BASELINE is the default, and the vertical alignment will be reset to BASELINE if the second parameter is not used. The TOP and CENTER parameters are straightforward. The BOTTOM parameter offsets the line based on the current `text_descent()` . For multiple lines, the final line will be aligned to the bottom, with the previous lines appearing above it.

When using `text()` with width and height parameters, BASELINE is ignored, and treated as TOP. (Otherwise, text would by default draw outside the box, since BASELINE is the default setting. BASELINE is not a useful drawing mode for text drawn in a rectangle.)

The vertical alignment is based on the value of `text_ascent()` , which many fonts do not specify correctly. It may be necessary to use a hack and offset by a few pixels by hand so that the offset looks correct. To do this as less of a hack, use some percentage of `text_ascent()` or `text_descent()` so that the hack works even if you change the size of the font.

See Also
--------

PApplet.loadFont(String) : brief statement on what this does

PFont : brief statement on what this does

PGraphics.text(String, float, float) : brief statement on what this does

PGraphics.textSize(float) : brief statement on what this does

PGraphics.textAscent() : brief statement on what this does

PGraphics.textDescent() : brief statement on what this does

# bezier_detail

Sets the resolution at which Beziers display.

Parameters
----------

detail: int
    resolution of the curves

Notes
-----

Sets the resolution at which Beziers display. The default value is 20. This function is only useful when using the P3D renderer as the default P2D renderer does not use this information.

See Also
--------

PGraphics.curve(float, float, float, float, float, float, float, float, float, float, float, float) : brief statement on what this does

PGraphics.curveVertex(float, float, float) : brief statement on what this does

PGraphics.curveTightness(float) : brief statement on what this does
