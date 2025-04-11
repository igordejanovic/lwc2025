import os
from functools import partial
from textx import generator
from textx.generators import gen_file, get_output_filename
from qlweb.field import Field
from textxjinja import textx_jinja_generator

__version__ = "0.1.0.dev"


@generator('questlang', 'web')
def questlang_generate_web(metamodel, model, output_path, overwrite, debug, **custom_args):
    "Generator for generating web from questlang descriptions"

    # template directory
    template_folder = os.path.join(os.path.dirname(__file__), 'templates')

    def type_conversion(t):
        try:
            if type(t).__name__ == 'RangeType':
                return 'Decimal'
            return {
                'integer': 'Decimal',
                'money': 'Decimal',
                'date': 'Date',
            }[t]
        except KeyError:
            return t

    def fd_typed(field):
        if field.type == 'boolean':
            return f'conv_bool(fd.{field.name})'
        elif field.type == 'string':
            return f'fd.{field.name}'
        elif field.type == 'integer':
            return f'conv_integer(fd.{field.name})'
        elif field.type == 'float':
            return f'conv_float(fd.{field.name})'
        elif field.type == 'date':
            return f'dayjs(fd.{field.name}).toDate()'
        elif field.type == 'money':
            return f'conv_money(fd.{field.name})'
        else:
            raise Exception('Unhandled type {field.type}')

    def numeric(field):
        return field.type in ['money', 'integer', 'float']

    def export(field):
        if field.type == 'date':
            return f'fdt.{field.name}?.toDateString()'
        elif numeric(field):
            return f'conv_nan(fdt.{field.name})'
        else:
            return f'fdt.{field.name}'

    def tostr(field):
        prefix = 'fdt.' if not field.expression else ''
        if field.type == 'date':
            return f'str_date({prefix}{field.name})'
        elif field.type == 'boolean':
            return f'str_bool({prefix}{field.name})'
        elif field.type == 'money':
            return f'str_money({prefix}{field.name})'
        elif field.type in ['integer', 'float']:
            return f'str_number({prefix}{field.name})'
        else:
            return f'{prefix}{field.name}'


    filters = {
        'type_conversion': type_conversion,
        'fd_typed': fd_typed,
        'numeric': numeric,
        'export': export,
        'tostr': tostr,
    }

    # Emit expressions to JavaScript
    for field in model.forms[0].fields.values():
        if field.expression:
            field.emit = Field(field).emit(field.expression)
        if field.vis_condition or field.deps:
            sep = ' && ' if field.deps else ''
            # emit_vis is a JavaScript expression which is dynamically evaluated
            # to show/hide the input control. The control is visible if
            # vis_condition is satisfied and if all dependencies have value (are
            # defined).
            vis_deps = (f'v(formData.{f.name})' for f in field.deps)
            field.emit_vis = (f"{' && '.join(vis_deps)}" +
                              (f"{sep}({Field(field).emit(field.vis_condition)})"
                               if field.vis_condition else ""))

    # call the generator
    textx_jinja_generator(template_folder, output_path,
                          context={'form': model.forms[0]},
                          overwrite=overwrite, filters=filters)
