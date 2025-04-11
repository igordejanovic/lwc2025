from textx import metamodel_for_language, get_children


def test_simple_expression_evaluation():
    mm = metamodel_for_language('questlang')
    model = mm.model_from_str('''
    form TestExpression {
        "First value"
            first_value:  integer

        "Second value"
            second_value: integer

        "difference"
            difference = first_value - second_value

    }
    ''')

    difference = get_children(lambda x: hasattr(x, 'name') and x.name == 'difference', model)[0]

    import pudb; pudb.set_trace()
