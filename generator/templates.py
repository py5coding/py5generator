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
        \"\"\"$class_{0}_{1}\"\"\"
        return self._instance.{3}
    {1}: {2} = property(fget=_get_{1})
"""

MODULE_PROPERTY_PRE_RUN_TEMPLATE = """
        global {0}
        del {0}"""


###############################################################################
# CLASS METHODS
###############################################################################

CLASS_METHOD_TYPEHINT_TEMPLATE = """
    @overload
    def {1}({2}) -> {3}:
        \"\"\"$class_{0}_{1}\"\"\"
        pass
"""

CLASS_METHOD_TEMPLATE = """
    {5}
    def {1}({2}, {6}):
        \"\"\"$class_{0}_{1}\"\"\"
        return {3}.{4}(*args)
"""

CLASS_METHOD_TEMPLATE_WITH_TYPEHINTS = """
    {5}
    def {1}({2}) -> {6}:
        \"\"\"$class_{0}_{1}\"\"\"
        return {3}.{4}({7})
"""

###############################################################################
# MODULE FUNCTIONS
###############################################################################


MODULE_FUNCTION_TYPEHINT_TEMPLATE = """
@overload
def {1}({2}) -> {3}:
    \"\"\"$module_{0}_{1}\"\"\"
    pass
"""

MODULE_FUNCTION_TEMPLATE = """
def {1}({3}):
    \"\"\"$module_{0}_{1}\"\"\"
    return {2}.{1}({4})
"""

MODULE_FUNCTION_TEMPLATE_WITH_TYPEHINTS = """
def {1}({2}) -> {4}:
    \"\"\"$module_{0}_{1}\"\"\"
    return {3}.{1}({5})
"""
