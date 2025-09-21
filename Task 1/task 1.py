import numpy as np
import matplotlib.pyplot as plt

# Given: 2 segments
width_segments = [
    {"sOffset": 0.0, "a": 3.0, "b": 0.1, "c": 0.0, "d": 0.0},
    {"sOffset": 20.0, "a": 5.0, "b": -0.05, "c": 0.001, "d": 0.0}
]



def getLaneWidth(s):
    """
    PART A: Calculate lane width at position s.
    """
    
    # Find the right segment to use
    segment_to_use = None
    
    for segment in width_segments:
        # Check if starts before or at pos s
        if segment["sOffset"] <= s:
            segment_to_use = segment
        # If exceed pos s, stop.
        else:
            break
    
    # If  s in before all segmenst (edge case). Use  1st segment
    if segment_to_use is None:
        segment_to_use = width_segments[0]
    
    # Calculate width using polynomial formula
    # w(s) = a + b*(s-sOffset) + c*(s-sOffset)^2 + d*(s-sOffset)^3
    
    sOffset = segment_to_use["sOffset"]
    a = segment_to_use["a"]
    b = segment_to_use["b"]
    c = segment_to_use["c"]
    d = segment_to_use["d"]
    
    delta_s = s - sOffset
    
    width = a + b*delta_s + c*(delta_s**2) + d*(delta_s**3)
    
    return width



def check_continuity():
    """
    PART B: Check if the width functions connect smoothly.
    
    We check two things:
    1. C0: Do the widths match at the junction?
    2. C1: Do the slopes match at the junction?
    """
    
    print("\nCONTINUITY CHECK AT JUNCTION")
    
    seg1 = width_segments[0]
    seg2 = width_segments[1]
    
    # Junction is where 2nd segment starts
    junction_s = seg2["sOffset"]  # s = 20.0
    
    # C0 CHECK: widths at junction
    print(f"\nC0 (Positional) Continuity at s={junction_s}:")
    
    # Width from segment 1 at junction
    delta_s1 = junction_s - seg1["sOffset"]
    width_from_seg1 = seg1["a"] + seg1["b"]*delta_s1 + seg1["c"]*(delta_s1**2) + seg1["d"]*(delta_s1**3)
    
    # Width from segment 2 at junction (delta_s = 0 at start)
    width_from_seg2 = seg2["a"]  # All are 0 when delta_s = 0
    
    gap = abs(width_from_seg1 - width_from_seg2)
    
    print(f"  Width from Segment 1: {width_from_seg1:.3f}m")
    print(f"  Width from Segment 2: {width_from_seg2:.3f}m")
    print(f"  Gap: {gap:.3f}m")
    
    if gap < 0.01:  # Within 1cm tolerance
        print("  ✓ Continuous (no gap)")
    else:
        print("  ✗ Discontinuous (there's a gap)")
    
    # C1 CHECK: Compare slopes (derivatives) at junction
    print(f"\n~C1 (Directional) Continuity:")
    
    # Derivative formula: dw/ds = b + 2*c*(s-sOffset) + 3*d*(s-sOffset)^2
    
    # Slope from segment 1 at junction
    delta_s1 = junction_s - seg1["sOffset"]
    slope_from_seg1 = seg1["b"] + 2*seg1["c"]*delta_s1 + 3*seg1["d"]*(delta_s1**2)
    
    # Slope from segment 2 at junction (delta_s = 0)
    slope_from_seg2 = seg2["b"]
    
    # Convert slope difference to angle difference
    angle1 = np.arctan(slope_from_seg1) * 180 / np.pi  # Convert to degrees
    angle2 = np.arctan(slope_from_seg2) * 180 / np.pi
    angle_diff = abs(angle1 - angle2)
    
    print(f"  Slope from Segment 1: {slope_from_seg1:.3f}")
    print(f"  Slope from Segment 2: {slope_from_seg2:.3f}")
    print(f"  Angle difference: {angle_diff:.1f}°")
    
    if angle_diff < 10:  # Within 10 degrees tolerance
        print("  ✓ Approximately continuous")
    else:
        print("  ✗ Discontinuous (sharp change)")



def plot_width_profile():
    """
    PLOT 1: Show how lane width changes along the road.
    """
    
    # Create points from s=0 to s=40
    s_values = np.linspace(0, 40, 400)
    
    # Calculate width at each point
    width_values = [getLaneWidth(s) for s in s_values]
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    
    # Plot the width curve
    plt.plot(s_values, width_values, 'b-', linewidth=2, label='Lane Width')
    
    # Mark segment boundaries with vertical lines
    for segment in width_segments:
        plt.axvline(x=segment["sOffset"], color='red', linestyle='--', alpha=0.7)
        
        # Add width value at boundary
        width_at_boundary = getLaneWidth(segment["sOffset"])
        plt.plot(segment["sOffset"], width_at_boundary, 'ro', markersize=8)
        plt.text(segment["sOffset"], width_at_boundary + 0.1, 
                f'{width_at_boundary:.2f}m', ha='center')
    
    plt.xlabel('Position along road (s) [meters]')
    plt.ylabel('Lane Width [meters]')
    plt.title('Lane Width Profile Along Road')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Save the plot
    plt.savefig('width_profile.png')
    plt.show()

def plot_continuity():
    """
    PLOT 2: Zoom in on the junction to show continuity.
    """
    
    junction_s = width_segments[1]["sOffset"]  # s = 20
    
    # Create points around the junction
    s_values = np.linspace(junction_s - 5, junction_s + 5, 200)
    
    # Calculate widths using both segments
    widths_seg1 = []
    widths_seg2 = []
    
    for s in s_values:
        # Segment 1 formula (even beyond its range)
        delta_s1 = s - width_segments[0]["sOffset"]
        w1 = width_segments[0]["a"] + width_segments[0]["b"]*delta_s1 + \
             width_segments[0]["c"]*(delta_s1**2) + width_segments[0]["d"]*(delta_s1**3)
        widths_seg1.append(w1)
        
        # Segment 2 formula
        if s >= junction_s:
            delta_s2 = s - width_segments[1]["sOffset"]
            w2 = width_segments[1]["a"] + width_segments[1]["b"]*delta_s2 + \
                 width_segments[1]["c"]*(delta_s2**2) + width_segments[1]["d"]*(delta_s2**3)
            widths_seg2.append(w2)
        else:
            widths_seg2.append(np.nan)  # Not valid before junction
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    
    # Plot both curves
    plt.plot(s_values, widths_seg1, 'b--', linewidth=2, alpha=0.7, label='Segment 1 (extended)')
    plt.plot(s_values, widths_seg2, 'r-', linewidth=2, label='Segment 2')
    
    # Mark the junction
    plt.axvline(x=junction_s, color='green', linestyle='--', linewidth=2, alpha=0.7)
    
    # Mark junction points
    w1_at_junction = getLaneWidth(junction_s - 0.001)  # Just before
    w2_at_junction = getLaneWidth(junction_s)  # At junction
    
    plt.plot(junction_s, w1_at_junction, 'bo', markersize=10)
    plt.plot(junction_s, w2_at_junction, 'ro', markersize=10)
    
    # Calculate gap for title
    gap = abs(w1_at_junction - w2_at_junction)
    
    plt.xlabel('Position along road (s) [meters]')
    plt.ylabel('Lane Width [meters]')
    plt.title(f'Continuity at Junction (s={junction_s}m)\nGap: {gap:.3f}m')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Save the plot
    plt.savefig('continuity.png')
    plt.show()

def run_tests():
    """
    Test the getLaneWidth function with expected values.
    """
    print("TESTING getLaneWidth() function:")
    print("-"*50)
    
    test_cases = [
        (0.0, 3.0),    # At start
        (10.0, 4.0),   # Middle of first segment
        (20.0, 5.0),   # At junction
        (25.0, 4.76)   # In second segment
    ]
    
    for s, expected in test_cases:
        actual = getLaneWidth(s)
        print(f"s={s:5.1f}: width={actual:.3f}m (expected ~{expected:.2f}m)")

# MAIN PROGRAM
if __name__ == "__main__":
    print("TASK 1: LANE WIDTH EVALUATION")
    print("-"*50)
    
    run_tests()
    
    check_continuity()
    
    print("\nGenerating plots...")
    plot_width_profile()
    plot_continuity()