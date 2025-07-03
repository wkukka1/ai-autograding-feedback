## Task: Proving Optimality of the Earliest Finish Time (EFT) Algorithm for Interval Scheduling

---

### Problem Summary

You are given a set of intervals $\mathcal{I} = \{I_1, I_2, \dots, I_n\}$, where each interval $I_i = [s_i, f_i)$ has a start time $s_i$ and finish time $f_i$.

The goal of the **Interval Scheduling Problem** is to select the largest possible subset of mutually non-overlapping intervals.

The proposed greedy algorithm, known as the **Earliest Finish Time (EFT)** algorithm, proceeds as follows:

> Sort the intervals in increasing order of finish time. Iteratively select the first interval that starts after the finish of the last selected one.

### Your Task

Prove that the EFT greedy algorithm always returns an optimal solution. Use a proof by contradiction, induction, or direct argument — but **do not** use an exchange argument. Your proof should be rigorous and clearly structured.

---
