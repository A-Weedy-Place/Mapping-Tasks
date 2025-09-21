import matplotlib.pyplot as plt
import numpy as np

# ------------------------------------------------------------
# Problem data (do not modify)
# ------------------------------------------------------------
lanes = {
    '65': [(-0.7071067811865475, 0.7071067811865476), (9.899494936611665, 11.31370849898476)],
    '41': [(1.414213562373095, -1.4142135623730951), (12.020815280171309, 9.192388155425116)],
    '13': [(-1.414213562373095, 1.4142135623730951), (9.192388155425117, 12.020815280171307)],
    '39': [(0.7071067811865475, -0.7071067811865476), (11.313708498984761, 9.899494936611664)],
    '87': [(0.0, 0.0), (10.606601717798213, 10.606601717798211)]
}

# For validation after you implement your solution (right→left when looking along lane direction)
# Uncomment after implementation to self-check:
# EXPECTED_SORTED_LANE_IDS = ["41", "39", "87", "65", "13"]


# ------------------------------------------------------------
# Your task is to implement this function.
# ------------------------------------------------------------
def sort_lane_ids_right_to_left(lanes_dict):
    """
    Return lane IDs ordered from RIGHT to LEFT when looking in the
    direction of travel (point0 -> point1 on each lane).

    
    """
    # TODO: implement the steps above
    raise NotImplementedError("Implement the sorting based on lateral projection.")


# ------------------------------------------------------------
# Visualization (strongly recommended before coding)
# ------------------------------------------------------------
plt.figure(figsize=(8, 8))
for lane_id, (p0, p1) in lanes.items():
    xs = [p0[0], p1[0]]
    ys = [p0[1], p1[1]]
    plt.plot(xs, ys, marker='o', label=f"Lane {lane_id}")
    # Label at midpoint
    mid_x = (p0[0] + p1[0]) / 2.0
    mid_y = (p0[1] + p1[1]) / 2.0
    plt.text(mid_x, mid_y, lane_id, fontsize=12, color="red", ha="center")

# Optional: draw a small arrow on the first lane to show "forward" direction
first_id, (s, e) = next(iter(lanes.items()))
ax_dx = e[0] - s[0]
ax_dy = e[1] - s[1]
plt.quiver(s[0], s[1], ax_dx, ax_dy, angles='xy', scale_units='xy', scale=1, width=0.007)

plt.title("Visualize the lanes & their IDs (direction is point0 → point1)")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.axis("equal")
plt.grid(True)
plt.show()


# ------------------------------------------------------------
# Driver
# ------------------------------------------------------------
try:
    sorted_lane_ids = sort_lane_ids_right_to_left(lanes)
    print("Your sorted Lane IDs (right → left):", sorted_lane_ids)

    # Uncomment to self-check after implementing:
    # print("Expected:", EXPECTED_SORTED_LANE_IDS)

except NotImplementedError as e:
    print(e)



