## `correctness_submission.py`

### Submission Summary

This implementation of the `Society` class includes two key methods for retrieving citizens: `get_all_citizens` and `get_citizens_with_job`. While structurally sound, the logic in `get_all_citizens` assumes that the society is non-empty, leading to a runtime error when called on an empty instance.

```python
def get_all_citizens(self) -> list[Citizen]:
    everyone = self._head.get_all_subordinates()
    return everyone
```

```python
def get_citizens_with_job(self, job: str) -> list[Citizen]:
    employed = []
    everyone = self.get_all_citizens()
    for ctz in everyone:
        employed = employed.append([ctz])
    return employed
```

### Issues Identified

- `get_all_citizens()` assumes `self._head` is not `None`. If the society is empty, this causes:
  ```python
  AttributeError: 'NoneType' object has no attribute 'get_all_subordinates'
  ```
- In `get_citizens_with_job()`, the line `employed = employed.append([ctz])` is incorrect:
  - `list.append()` returns `None`, so `employed` becomes `None` after the first iteration.
  - The intended behavior was likely `employed.append(ctz)`.

### Expected AI Response

- Clearly identify the crash in `get_all_citizens()` due to an empty `_head`.
- Recommend adding a check like:
  ```python
  if self._head is None:
      return []
  ```
- Point out the misuse of `.append()` and suggest fixing it to avoid `NoneType` errors.
- Confirm that these changes would allow the test case for an empty society to pass.

