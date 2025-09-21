So, this question had 2 parts

** Part A:

- we had 2 segments of roads
- so first we calculate the widths at each point (thought the polynomila func)
- First we are checking what segment the s in lying in..... (e.g. use offset 0 or 20)
- Edge case: incase s < first offset

** Part B:

*** C0 continuity:
- means that at junction (where both segments meet), width difference should be 0 or very low
- I took a tolerance of 1cm and since the difference was 0.000m, it checked out

*** C1 continuity:
- RATE of change should be similar. So, we take slopes of both segments, get the angles
- I took tolerance of 10 degrees and got an angle diff of 8.6 degrees

then did plotting...