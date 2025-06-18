def gac_enforce(csp, queue=None):
    if queue is None:
        queue = [(c, var) for c in csp.constraints for var in c.scope]

    pruned = []
    while queue:
        c, var = queue.pop(0)
        for val in csp.get_domain(var)[:]:
            if not c.has_support(var, val):
                csp.prune_value(var, val)
                pruned.append((var, val))
    return True, pruned
