def gac_enforce(csp, arc_queue=None):
    if arc_queue is None:
        arc_queue = [(constraint, variable) for constraint in csp.constraints for variable in constraint.scope]

    pruned_values = []

    while arc_queue:
        constraint, variable = arc_queue.pop(0)

        for value in csp.get_domain(variable)[:]:
            if not constraint.has_support(variable, value):
                csp.prune_value(variable, value)
                pruned_values.append((variable, value))

                if len(csp.get_domain(variable)) == 0:
                    return False, pruned_values

                for related_constraint in csp.get_constraints_with(variable):
                    for related_variable in related_constraint.scope:
                        if related_variable != variable:
                            arc_queue.append((related_constraint, related_variable))

    return True, pruned_values
