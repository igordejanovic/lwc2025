from questlang.utils import to_snake_case


class Field:
    """
    Wrapper for FieldDecl to provide emit methods for JavaScript
    """

    def __init__(self, field):
        # Model field
        self.field = field

    def emit(self, obj):
        '''
        Calls appropriate emiter method based on obj type.
        Given model object emit it to JavaScript.
        Return JavaScript code.
        '''
        method = to_snake_case(type(obj).__name__)
        try:
            return getattr(self, method)(obj)
        except AttributeError:
            return obj

    def logical_or_expression(self, obj):
        return f"{' || '.join(self.emit(o) for o in obj.operands)}"

    def logical_and_expression(self, obj):
        return f"{' && '.join(self.emit(o) for o in obj.operands)}"

    def binary_expression(self, obj):
        result = []
        # Mapping operations to Decimal methods
        operations = {
            '==': 'equals',
            '!=': '!=', # needs special handling
            '>': 'greaterThan',
            '>=': 'greaterThan',
            '<': 'lessThan',
            '<=': 'lessThan',
            '+': 'plus',
            '-': 'minus',
            '*': 'times',
            '/': 'dividedBy',
        }
        if obj.operations and obj.operations[0] == '!=':
            return f'!{obj.operands[0]}.equals({obj.operands[1]})'

        operands = (o for o in obj.operands)
        result.append(self.emit(next(operands)))
        result.extend(f'.{operations[o]}({self.emit(b)})'
                      for o, b in zip(obj.operations, operands))
        return f"{''.join(result)}"

    def comparison_expression(self, obj):
        return self.binary_expression(obj)

    def add_expression(self, obj):
        return self.binary_expression(obj)

    def mult_expression(self, obj):
        return self.binary_expression(obj)

    def unary_expression(self, obj):
        if obj.operation:
            if obj.operation == '!':
                return f'not({self.emit(obj.operand)})'
            return f'{obj.operation}({self.emit(obj.operand)})'
        else:
            return f'{self.emit(obj.operand)}'

    def parenthesed_expression(self, obj):
        return f'({self.emit(obj.expression)})'

    def if_expression(self, obj):
        return (f'{self.emit(obj.condition)} ? {self.emit(obj.then_expression)}'
                f' : {self.emit(obj.else_expression)}')

    def integer(self, obj):
        return f"Decimal('{obj.value}')"

    def string(self, obj):
        return f"'{obj.value}'"

    def boolean(self, obj):
        return 'true' if obj.value else 'false'

    def money(self, obj):
        return f"Decimal('{obj.value}')"

    def date(self, obj):
        return f"dayjs('{obj}')"

    def reference(self, obj):
        """Returns a reference to either state variable or local JS variable.
        We cannot use state variable if current field expression depends on the
        current state and not the previous one. State in react is updated async
        so we refer to locals variable if the dependency is calculated field
        also.

        """
        if obj.ref.expression:
            return f'{obj.ref.name}'
        return f'fdt.{obj.ref.name}'
