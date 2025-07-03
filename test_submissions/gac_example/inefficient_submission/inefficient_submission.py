def gac_enforce(csp, queue=None):
    if queue is None:
        queue = [(c, var) for c in csp.constraints for var in c.scope]

    pruned = []
    seen = set()

    while queue:
        c, var = queue.pop(0)
        if (c.name, var) in seen:
            continue
        seen.add((c.name, var))
        for val in csp.get_domain(var)[:]:
            if not c.has_support(var, val):
                csp.prune_value(var, val)
                pruned.append((var, val))
                if not csp.get_domain(var):
                    return False, pruned
                for c2 in csp.get_constraints_with(var):
                    for v in c2.scope:
                        if v != var:
                            queue.append((c2, v))
    return True, pruned
