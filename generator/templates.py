# *****************************************************************************
#
#   Part of the py5generator project; generator of the py5 library
#   Copyright (C) 2020-2022 Jim Schmitz
#
#   This project is free software: you can redistribute it and/or modify it
#   under the terms of the GNU General Public License as published by the
#   Free Software Foundation, either version 3 of the License, or (at your
#   option) any later version.
#
#   This project is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
#   Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program. If not, see <https://www.gnu.org/licenses/>.
#
# *****************************************************************************
"""
Templates
"""


###############################################################################
# STATIC FIELDS
###############################################################################


CLASS_STATIC_FIELD_TEMPLATE = """
    {0} = {1}"""

MODULE_STATIC_FIELD_TEMPLATE = """
{0} = {1}"""


###############################################################################
# DYNAMIC FIELDS
###############################################################################


MODULE_PROPERTY_TEMPLATE = """
{0}: {1} = None"""

CLASS_PROPERTY_TEMPLATE = """
    {4}
    def _get_{1}(self) -> {2}:
        \"\"\"$class_{0}_{1}
        \"\"\"
        return self._instance.{3}
    {1}: {2} = property(fget=_get_{1}, doc=\"\"\"$class_{0}_{1}\"\"\")
"""


###############################################################################
# CLASS METHODS
###############################################################################

CLASS_METHOD_TYPEHINT_TEMPLATE = """
    @overload
    def {1}({2}) -> {3}:
        \"\"\"$class_{0}_{1}
        \"\"\"
        pass
"""

CLASS_METHOD_TEMPLATE = """
    {5}
    def {1}({2}, {6}):
        \"\"\"$class_{0}_{1}
        \"\"\"
        return {3}.{4}(*args)
"""

CLASS_METHOD_TEMPLATE_WITH_TYPEHINTS = """
    {5}
    def {1}({2}) -> {6}:
        \"\"\"$class_{0}_{1}
        \"\"\"
        return {3}.{4}({7})
"""

CLASS_OPTIONAL_METHOD_TEMPLATE = """
    {5}
    def {1}({2}, {6}, renderer_name=None):
        \"\"\"$class_{0}_{1}
        \"\"\"
        try:
            _JClass = JClass(clsname)
        except:
            _JClass = None

        if _JClass and isinstance({3}, _JClass):
            return {3}.{4}(*args)
        else:
            raise AttributeError("The '{1}()' method is only available when using the " + renderer_name + " renderer. Read this method's documentation for more information.")
"""

CLASS_OPTIONAL_METHOD_TEMPLATE_WITH_TYPEHINTS = """
    {5}
    def {1}({2}, renderer_name=None, clsname=None) -> {6}:
        \"\"\"$class_{0}_{1}
        \"\"\"
        try:
            _JClass = JClass(clsname)
        except:
            _JClass = None

        if _JClass and isinstance({3}, _JClass):
            return {3}.{4}({7})
        else:
            raise AttributeError("The '{1}()' method is only available when using the " + renderer_name + " renderer. Read this method's documentation for more information.")
"""

###############################################################################
# MODULE FUNCTIONS
###############################################################################


MODULE_FUNCTION_TYPEHINT_TEMPLATE = """
@overload
def {1}({2}) -> {3}:
    \"\"\"$module_{0}_{1}
    \"\"\"
    pass
"""

MODULE_FUNCTION_TEMPLATE = """
def {1}({3}):
    \"\"\"$module_{0}_{1}
    \"\"\"
    return {2}.{1}({4})
"""

MODULE_FUNCTION_TEMPLATE_WITH_TYPEHINTS = """
def {1}({2}) -> {4}:
    \"\"\"$module_{0}_{1}
    \"\"\"
    return {3}.{1}({5})
"""
