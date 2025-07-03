def gac_enforce(csp, queue=None):
    if queue is None:
        queue = [(c, var) for c in csp.constraints for var in c.scope]

    pruned = []

    while queue:
        constraint, var = queue.pop(0)
        for val in csp.get_domain(var)[:]:
            if not constraint.has_support(var, val):
                csp.prune_value(var, val)
                pruned.append((var, val))
                if len(csp.get_domain(var)) == 0:
                    return False, pruned
                for other_constraint in csp.get_constraints_with(var):
                    for v in other_constraint.scope:
                        if v != var:
                            queue.append((other_constraint, v))
    return True, pruned
