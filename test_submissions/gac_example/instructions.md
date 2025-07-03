## Task: Generalized Arc Consistency (GAC) Enforcement

---

### Problem Summary

Implement the `gac_enforce` function to enforce **Generalized Arc Consistency (GAC)** in a constraint satisfaction problem (CSP).

Each constraint has a method `has_support(var, val)` which returns `True` if the value `val` in variable `var`'s domain has support under that constraint. A CSP provides access to:

- `variables` — list of variables
- `get_domain(var)` — current domain of a variable
- `get_constraints_with(var)` — list of constraints involving `var`
- `prune_value(var, val)` — removes `val` from `var`’s domain

Your `gac_enforce` function should iteratively prune values that lack support and propagate changes through affected arcs. If any domain becomes empty, return failure.

---
