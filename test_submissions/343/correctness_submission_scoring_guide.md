## `correctness_submission.sql`

### Submission Summary

The query is well-structured and logically composed using multiple intermediate views, but it ultimately produces an empty result due to overly strict joins in the final step:

```sql
INSERT INTO result_q5
SELECT DISTINCT user_id, contact_email
FROM Passenger
NATURAL JOIN ViewB
NATURAL JOIN ViewC
NATURAL JOIN ViewD;
```

### Issues Identified

- Uses multiple `NATURAL JOIN`s across filtered views (`ViewB`, `ViewC`, `ViewD`) that likely **do not share overlapping passengers**.
- Applies all constraints simultaneously, which **filters out all rows**, even though individual views may be correct.
- Doesn't isolate which condition(s) eliminate rows, making debugging difficult.

### Expected AI Response

- Identify that the logic of each view (e.g., "visited 5 countries", "booked 10 in 2023", etc.) is **valid individually**.
- Explain that `NATURAL JOIN` across many restrictive views causes an **empty intersection**.
- Recommend:
  - Using `LEFT JOIN` or `INNER JOIN` with progressive `WHERE` conditions.
  - Verifying overlap in view outputs before intersecting them.
  - Possibly restructuring the logic to **relax join conditions** or **combine filters sequentially**.
