from textx import metamodel_for_language
from qlweb.expressions import emit


def test_generaotr_1():
    questionnaire_mm = metamodel_for_language('questlang')

    # Parse a form definition
    model = questionnaire_mm.model_from_str('''
    form TaxForm {
        "Are you married?"
            isMarried: boolean

        if (isMarried) {
            "Spouse's income:"
                spouseIncome: money

            "Joint deduction:"
                jointDeduction = (spouseIncome * 0.2) + 2 * (3 + 4.8)
        }
    }
    ''')

    assert emit(model.forms[0].questions[1].condition) \
        == 'n(formData.isMarried)'
    assert emit(model.forms[0].questions[1].questions[1].field.expression) \
        == '(n(formData.spouseIncome) * 0.2) + 2 * (3 + 4.8)'
