def gac_enforce(csp, queue=None):
    for var in csp.variables:
        for val in csp.get_domain(var)[:]:
            for c in csp.get_constraints_with(var):
                if not c.has_support(var, val):
                    csp.prune_value(var, val)
    return True, []
