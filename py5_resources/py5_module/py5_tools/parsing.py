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
import ast


class TransformDynamicVariablesToCalls(ast.NodeTransformer):

    def __init__(self, dynamic_variables):
        super().__init__()
        import py5
        self._dynamic_variables = dynamic_variables

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
            out.append('Cannot delete py5 reserved word')
        elif self.ctx == 'Store':
            out.append('Cannot modify py5 reserved word')
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
    import py5.reference as ref
    transformer = TransformDynamicVariablesToCalls(ref.PY5_DYNAMIC_VARIABLES)
    return ast.fix_missing_locations(transformer.visit(code_ast))
