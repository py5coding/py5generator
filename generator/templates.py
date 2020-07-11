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
    def _get_{0}(self) -> {1}:
        \"\"\"$class_{0}\"\"\"
        return self._py5applet.{2}
    {0}: {1} = property(fget=_get_{0})
"""

MODULE_PROPERTY_PRE_RUN_TEMPLATE = """
        global {0}
        del {0}"""


###############################################################################
# CLASS METHODS
###############################################################################

CLASS_METHOD_TYPEHINT_TEMPLATE = """
    @overload
    def {0}({1}) -> {2}:
        \"\"\"$class_{0}\"\"\"
        pass
"""

CLASS_METHOD_TEMPLATE = """
    {4}
    def {0}({1}, {5}):
        \"\"\"$class_{0}\"\"\"
        try:
            return {2}.{3}(*args)
        except Exception as e:
            raise Py5Exception(e.__class__.__name__, str(e), '{0}', args)
"""

CLASS_METHOD_TEMPLATE_WITH_TYPEHINTS = """
    {4}
    def {0}({1}) -> {5}:
        \"\"\"$class_{0}\"\"\"
        try:
            return {2}.{3}({6})
        except Exception as e:
            raise Py5Exception(e.__class__.__name__, str(e), '{0}', [{6}])
"""

###############################################################################
# MODULE FUNCTIONS
###############################################################################


MODULE_FUNCTION_TYPEHINT_TEMPLATE = """
@overload
def {0}({1}) -> {2}:
    \"\"\"$module_{0}\"\"\"
    pass
"""

MODULE_FUNCTION_TEMPLATE = """
def {0}({2}):
    \"\"\"$module_{0}\"\"\"
    return {1}.{0}({3})
"""

MODULE_FUNCTION_TEMPLATE_WITH_TYPEHINTS = """
def {0}({1}) -> {3}:
    \"\"\"$module_{0}\"\"\"
    return {2}.{0}({4})
"""
