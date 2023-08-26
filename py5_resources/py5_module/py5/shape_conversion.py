# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2023 Jim Schmitz
#
#   This library is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 2.1 of the License, or (at
#   your option) any later version.
#
#   This library is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
#   General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this library. If not, see <https://www.gnu.org/licenses/>.
#
# *****************************************************************************
from typing import Callable

import numpy as np

pshape_functions = []


def _convertable(obj):
    return any(pre(obj) for pre, _ in pshape_functions)


def _convert(sketch, obj):
    for precondition, convert_function in pshape_functions:
        if precondition(obj):
            obj = convert_function(sketch, obj)
            break
    else:
        raise RuntimeError(f"Py5 Converter is not able to convert {str(obj)}")

    return obj


def register_shape_conversion(
    precondition: Callable, convert_function: Callable
) -> None:
    # TODO: add docstring
    pshape_functions.append((precondition, convert_function))


###############################################################################
# BUILT-IN CONVERSTION FUNCTIONS
###############################################################################


try:
    import shapely
    from shapely import (
        GeometryCollection,
        LineString,
        MultiLineString,
        MultiPolygon,
        Point,
        Polygon,
        affinity,
    )

    def shapely_to_py5shape_precondition(obj):
        return isinstance(
            obj,
            (
                GeometryCollection,
                LineString,
                MultiLineString,
                MultiPolygon,
                Point,
                Polygon,
            ),
        )

    def shapely_to_py5shape_converter(sketch, obj, first_call=True):
        if first_call:
            obj = affinity.scale(obj, yfact=-1, origin="center")

        if isinstance(obj, Polygon):
            shape = sketch.create_shape()
            with shape.begin_closed_shape():
                if obj.exterior.coords:
                    coords = (
                        np.array(obj.exterior.coords)
                        if obj.exterior.is_ccw
                        else np.array(obj.exterior.coords[::-1])
                    )
                    shape.vertices(coords[:-1])
                for hole in obj.interiors:
                    with shape.begin_contour():
                        coords = (
                            np.array(hole.coords[::-1])
                            if hole.is_ccw
                            else np.array(hole.coords)
                        )
                        shape.vertices(coords[:-1])
            return shape
        elif isinstance(obj, MultiPolygon):
            shape = sketch.create_shape(sketch.GROUP)
            for p in obj.geoms:
                shape.add_child(
                    shapely_to_py5shape_converter(sketch, p, first_call=False)
                )
            return shape
        else:
            raise RuntimeError(f"Py5 Converter is not able to convert {str(obj)}")

    register_shape_conversion(
        shapely_to_py5shape_precondition, shapely_to_py5shape_converter
    )

except Exception:
    pass
