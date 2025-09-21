So we have noisy lane boundaries and need to clean them.

---

## Part A - Smoothing
The lanes are randomized from sensor noise. Need to smooth them 

BUT:
- Can't move the endpoints (they connect to other road segments)
- Can't smooth too much (max 0.3m tolerance/deviation)

So:
- Remove any duplicate points.
- Keep smoothing until we hit the limit: (lapplacian smoothing)

        (Each point moves halfway toward average of its neighbors
        First and last points stay locked in place
        Check how far we've moved from original
        Stop when next smoothing would go over 0.3m limit)


- Used proper distance calculation (point to line segment) instead of just point-to-point because that's more accurate for checking deviation.

---

## Part B - Continuity Check
Two lanes should connect at a junction. Check if they actually do:

C0 (position): Just measure the gap between end of lane A and start of lane B. Should be < 0.1m.
C1 (direction): Check if they point the same way:

Get direction of last segment of A
Get direction of first segment of B
Find angle between them
Should be < 15 degrees (tolerance)
