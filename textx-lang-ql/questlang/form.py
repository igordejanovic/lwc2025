from textx import (get_children_of_type, get_parent_of_type,
                   get_model, TextXSemanticError, get_location)
from dataclasses import dataclass
from typing import Any
from questlang.kahn import kahn
from questlang.utils import remove_dupes
from questlang.types import calc_type


@dataclass
class LogicalAndExpression:
    parent: Any
    operands: list


def form_processor(form):
    """
    Calculates question references
    """

    graph = {}
    fields = {}
    # Prepare dependency graph for Khan topological sort algorithm
    for field in get_children_of_type('FieldDecl', form):
        deps = [ref.ref for ref in get_children_of_type('Reference', field)]
        remove_dupes(deps)
        graph[field.name] = [f.name for f in deps]
        fields[field.name] = field
        field.deps = deps

    topo_order, cycle = kahn(graph)

    if cycle:
        raise TextXSemanticError(f'Cycle detected: {cycle}',
                                 **get_location(fields[cycle[0]].expression))

    for field in get_children_of_type('FieldDecl', form):
        # Force type calculation
        field.type

    # Calculate visibility conditions
    def find_parent_ifs(field_or_if):
        """
        Get all parent if conditions going up the parent chain.
        """
        parent_if = get_parent_of_type('IfConditionalBlock', field_or_if)
        if parent_if is not None:
            return [parent_if] + find_parent_ifs(parent_if)
        return []

    for field in fields.values():
        parent_ifs = find_parent_ifs(field)
        vis_expr = None
        if parent_ifs:
            # join all ifs with LogicalAndExpression
            vis_expr = LogicalAndExpression(None,
                                            operands=[p.condition
                                                      for p in parent_ifs])

        # vis_condition is a boolean expression which controls a visibility of
        # this field.
        field.vis_condition = vis_expr

    form.fields = fields
    form.field_order = topo_order
    form.field_order.reverse()

    # Check conditions in If statements
    for ifblock in get_children_of_type('IfConditionalBlock', form):
        iftype = calc_type(ifblock.condition)
        if iftype != 'boolean':
            raise TextXSemanticError(
                f'If block condition type cannot be "{iftype}"',
                **get_location(ifblock.condition))
