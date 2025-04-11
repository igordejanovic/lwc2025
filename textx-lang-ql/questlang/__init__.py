import os
from textx import language, metamodel_from_file
from questlang.form import form_processor, LogicalAndExpression
from questlang.types import FieldDecl

__version__ = "0.1.0.dev"


@language('questlang', '*.ql')
def questlang_language():
    "Questionnaire Language in textX - LWC 2025"
    current_dir = os.path.dirname(__file__)
    processors = {
        'Form': form_processor
    }
    custom_classes = [
        FieldDecl,
        LogicalAndExpression
    ]
    mm = metamodel_from_file(os.path.join(current_dir, 'questlang.tx'),
                             classes=custom_classes)
    mm.register_obj_processors(processors)

    # Here if necessary register object processors or scope providers
    # http://textx.github.io/textX/stable/metamodel/#object-processors
    # http://textx.github.io/textX/stable/scoping/

    return mm
