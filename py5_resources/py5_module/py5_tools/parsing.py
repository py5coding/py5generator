# *****************************************************************************
#
#   Part of the py5 library
#   Copyright (C) 2020-2021 Jim Schmitz
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
# *** FORMAT PARAMS ***
import ast


py5_dynamic_variables_str = None  # DELETE


class TransformDynamicVariablesToCalls(ast.NodeTransformer):

    def __init__(self):
        super().__init__()
        self._dynamic_variables = [{py5_dynamic_variables_str}]

    def visit_Name(self, node: ast.Name):
        if node.id in self._dynamic_variables:
            return ast.Call(func=node, args=[], keywords=[])
        else:
            return node


class ReservedWordError:

    def __init__(self, node: ast.Name):
        self.py5_name = node.id
        self.ctx = type(node.ctx).__name__
        self.lineno = node.lineno
        self.col_offset = node.col_offset

    def message(self, code):
        lines = code.splitlines()
        out = []
        out.append('Syntax Error on line ' + str(self.lineno) + ':')
        out.append(lines[self.lineno - 1])
        out.append((' ' * self.col_offset) + '^')
        if self.ctx == 'Del':
            out.append('Deleting py5 reserved words is not allowed')
        elif self.ctx == 'Store':
            out.append('Assignments to py5 reserved words are not allowed')
        return '\n'.join(out)


class ReservedWordsValidation(ast.NodeVisitor):

    def __init__(self, reserved_words):
        super().__init__()
        self._reserved_words = reserved_words
        self.problems = []

    def visit_Name(self, node: ast.Name):
        if node.id in self._reserved_words and isinstance(node.ctx, (ast.Store, ast.Del)):
            self.problems.append(ReservedWordError(node))
        self.generic_visit(node)


def check_reserved_words(code_ast: ast.Module):
    import py5.reference as ref
    validator = ReservedWordsValidation(ref.PY5_DIR_STR)
    validator.visit(code_ast)
    return validator.problems


def transform_py5_code(code_ast: ast.Module):
    transformer = TransformDynamicVariablesToCalls()
    return ast.fix_missing_locations(transformer.visit(code_ast))
