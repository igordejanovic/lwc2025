from textx import get_location, TextXSemanticError
from dataclasses import dataclass
from typing import Any
from questlang.utils import to_snake_case


type_calculators = {}

def typed(f):
    type_calculators[f.__name__] = f
    return f


def calc_type(expr):
    '''
    Given QL expr calculate its type.
    If expr is None calculate type of this field expression.
    '''
    calculator = to_snake_case(type(expr).__name__)
    if calculator in ['integer', 'string', 'boolean', 'money', 'date']:
        # base types
        return calculator
    ret = type_calculators[calculator](expr)
    return ret

@typed
def logical_binary(expr):
    if len(expr.operands) == 1:
        return calc_type(expr.operands[0])
    optypes = (calc_type(op) for op in expr.operands)
    if any(optype != 'boolean' for optype in optypes):
        raise TextXSemanticError(
            'Cannot perform logical operation on non-bool type',
            **get_location(expr))

    return 'boolean'


@typed
def logical_or_expression(expr):
    return logical_binary(expr)


@typed
def logical_and_expression(expr):
    return logical_binary(expr)

@typed
def binary_expression(expr):
    if len(expr.operands) == 1:
        return calc_type(expr.operands[0])
    else:
        optypes = [calc_type(op) for op in expr.operands]
        for optype in optypes:
            if optype in ['date', 'boolean', 'string']:
                raise TextXSemanticError(
                    f'Cannot perform operation on {optype} type',
                    **get_location(expr))

        if any(optype == 'money' for optype in optypes):
            return 'money'
        elif any(optype == 'float' for optype in optypes):
            return 'float'
        else:
            return 'integer'

@typed
def comparison_expression(expr):
    if len(expr.operands) == 1:
        return calc_type(expr.operands[0])
    else:
        # operands must be compatible
        optypes = {calc_type(op) for op in expr.operands}
        if len(optypes) > 1 and any([x not in ['integer', 'money']
                                     for x in optypes]):
            raise TextXSemanticError(
                'Comparison of non-compatible types', **get_location(expr))
    return 'boolean'


@typed
def add_expression(expr):
    return binary_expression(expr)


@typed
def mult_expression(expr):
    return binary_expression(expr)

@typed
def unary_expression(expr):
    return calc_type(expr.operand)


@typed
def parenthesed_expression(expr):
    return calc_type(expr.expression)


@typed
def if_expression(expr):
    condition = calc_type(expr.condition)
    if condition != 'boolean':
        raise TextXSemanticError('Condition in if expression must be of boolean type',
                                 **get_location(expr))
    then_type = calc_type(expr.then_expression)
    else_type = calc_type(expr.else_expression)
    if then_type != else_type:
        raise TextXSemanticError(
            '"then" and "else" branches types differ'
            f' ("{then_type}" != "{else_type}"):',
            **get_location(expr))
    return then_type


@typed
def reference(expr):
    if expr.ref.expression:
        return calc_type(expr.ref.expression)
    return expr.ref.type


def coerce_range(py_type_from, ql_type_to) -> bool:
    valid = {
            'int': ['money', 'integer'],
            'float': ['money'],
    }
    if py_type_from in valid:
        if ql_type_to in valid[py_type_from]:
            return True

    return False


@dataclass
class FieldDecl:
    parent: Any
    description: str
    name: str
    grammar_type: str
    default_value: Any
    range_from: [int | float]
    range_to: [int | float]
    expression: Any

    def __init__(self, parent: Any, description: str, name: str,
                 grammar_type: str, default_value: Any,
                 range_from: [int | float], range_to: [int | float],
                 expression: Any):
        self.parent = parent
        self.description = description
        self.name = name
        self.grammar_type = grammar_type
        self.default_value = default_value
        self.range_from = range_from
        self.range_to = range_to
        self.expression = expression

        # Check range and default types
        if grammar_type:
            # If range is defined
            if self.range_from is not None:
                if not coerce_range(
                        self.range_from.__class__.__name__, grammar_type) \
                or not coerce_range(
                    self.range_to.__class__.__name__, grammar_type):
                    raise TextXSemanticError(
                        f"Wrong range value type for question of type '{grammar_type}'.",
                        **get_location(self))

            # If default value is defined
            if self.default_value is not None:
                if self.grammar_type.lower() != self.default_value.__class__.__name__.lower():
                    raise TextXSemanticError(
                        f"Wrong default value for question of type '{grammar_type}'.",
                        **get_location(self.default_value))

    @property
    def type(self):
        """
        Calculate and cache this field type
        """
        if self.expression is None:
            return ('integer'
                    if type(self.grammar_type).__name__ == 'RangeType'
                    else self.grammar_type)
        if not hasattr(self, '_type'):
            self._type = calc_type(self.expression)
        return self._type

