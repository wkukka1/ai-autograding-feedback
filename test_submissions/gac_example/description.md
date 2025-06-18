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

## Submissions

---

### `fail_submission.py`

#### Submission Summary

This version performs pruning but does not propagate effects or revisit related arcs:

```python
def gac_enforce(csp, queue=None):
    for var in csp.variables:
        for val in csp.get_domain(var)[:]:
            for c in csp.get_constraints_with(var):
                if not c.has_support(var, val):
                    csp.prune_value(var, val)
    return True, []
```

- There is no queue or arc processing logic.
- No handling of downstream effects when pruning changes domains.
- No check for domain wipeout (i.e., empty domains).

#### Expected AI Response

- Identify that there is no propagation mechanism.
- Suggest using a queue to track and revisit arcs when pruning affects constraints.
- Point out missing early return on empty domains.

---

### `partial_correct_submission.py`

#### Submission Summary

Includes a queue-based structure but does not re-add arcs after pruning:

```python
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
```

- Performs pruning, but pruned values don’t trigger updates to related arcs.
- No failure handling for empty domains.

#### Expected AI Response

- Acknowledge use of queue but highlight lack of propagation.
- Recommend re-adding related arcs when pruning happens.
- Mention that empty domains should return failure.

---

### `inefficent_submission.py`

#### Submission Summary

Implements GAC with propagation, but inefficiently:

```python
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
```

- Uses a `seen` set that may prevent necessary revisits.
- Slightly non-standard queue logic could cause missed pruning.

#### Expected AI Response

- Confirm that the function is logically correct and enforces GAC.
- Point out inefficiencies in arc tracking and redundancy.
- Recommend improvements for duplicate avoidance and performance.

---
