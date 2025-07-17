## `hard_coding_submission.py`

### Submission Summary

This submission defines several constants used throughout a messaging system, but the implementation of `is_valid_message` contains a hardcoded value that contradicts the constants defined above. The function is meant to validate message length based on `MIN_MESSAGE_LENGTH` and `MAX_MESSAGE_LENGTH`.

```python
def is_valid_message(text: str) -> bool:
    if 1 <= len(text) <= 30:
        return True
    else:
        return False
```

### Issues Identified

- The `is_valid_message` function uses a hardcoded value `30` instead of the provided constant `MAX_MESSAGE_LENGTH`, which is `60`.
- This causes the test to fail when the instructor or testing environment changes `MAX_MESSAGE_LENGTH` to a different value (e.g., `10`), as the function does not respond dynamically to the change.
- The test error output confirms that constants were modified but the function did not adapt, which implies the use of literals instead of the defined constants.

### Expected AI Response

- Detect that `MAX_MESSAGE_LENGTH` is not being used inside `is_valid_message`.
- Recommend replacing the literal `30` with `MAX_MESSAGE_LENGTH` and `1` with `MIN_MESSAGE_LENGTH`.
- Emphasize the importance of using constants to ensure that changes in configuration propagate throughout the codebase.
- Suggest re-running tests after fixing to confirm the code dynamically respects constant values.
