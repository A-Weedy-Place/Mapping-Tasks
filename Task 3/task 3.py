import numpy as np
import matplotlib.pyplot as plt

# Test data - curved/noisy lane
lane_a = [
    (0, 0, 0),
    (1, 0.5, 0.1),
    (2, 0.3, 0.2),
    (2, 0.3, 0.2),  # duplicate point to test
    (3, 0.8, 0.3),
    (4, 0.4, 0.4),
    (5, 0.9, 0.5),
    (6, 0.6, 0.6),
    (7, 1.0, 0.7),
    (8, 0.7, 0.8)
]

# Second lane with gap and misalignment
lane_b = [
    (8.15, 0.85, 0.82),  # gap from lane_a end
    (9, 0.5, 0.9),
    (10, 0.8, 1.0),
    (11, 0.4, 1.1),
    (12, 0.7, 1.2)
]


def remove_duplicates(polyline):
    """Remove consecutive duplicate points"""
    cleaned = [polyline[0]]
    for point in polyline[1:]:
        if not np.allclose(point, cleaned[-1]):
            cleaned.append(point)
    return cleaned



def point_to_segment_distance(point, seg_start, seg_end):
    """Calculate distance from point to line segment"""
    p = np.array(point)
    a = np.array(seg_start)
    b = np.array(seg_end)
    
    ab = b - a
    ap = p - a
    
    # Project point onto line segment
    ab_squared = np.dot(ab, ab)
    if ab_squared == 0:  # Degenerate segment (single point)
        return np.linalg.norm(ap)
    
    t = max(0, min(1, np.dot(ap, ab) / ab_squared))
    projection = a + t * ab
    
    return np.linalg.norm(p - projection)



def calculate_max_deviation(original, smoothed):
    """Calculate maximum deviation using proper distance metric"""
    max_dev = 0
    
    for point in smoothed:
        # Find minimum distance to any segment in original
        min_dist = float('inf')
        for i in range(len(original) - 1):
            dist = point_to_segment_distance(point, original[i], original[i+1])
            min_dist = min(min_dist, dist)
        max_dev = max(max_dev, min_dist)
    return max_dev



def smooth_lane(lane, max_deviation=0.3):
    """Part A: Smooth lane with fixed endpoints - keep smoothing until we hit the limit"""
    
    lane = remove_duplicates(lane)
    print(f"Removed duplicates, now have {len(lane)} points")
    
    pts = [np.array(p) for p in lane]
    original = pts.copy()
    
    # Remember the endpoints (they must stay fixed)
    first_point = pts[0].copy()
    last_point = pts[-1].copy()
    
    # Keep smoothing until we can't anymore
    iteration = 0
    max_iterations = 20  # safety limit to prevent infinite loop
    
    while iteration < max_iterations:
        iteration += 1
        new_pts = pts.copy()
        
        # Smooth interior points only
        for j in range(1, len(pts) - 1):
            # average with neighbors
            avg = (pts[j-1] + pts[j+1]) / 2
            new_pts[j] = 0.5 * pts[j] + 0.5 * avg
        
        # Make sure endpoints didn't move
        new_pts[0] = first_point
        new_pts[-1] = last_point
        
        # Check deviation using proper metric
        deviation = calculate_max_deviation(original, new_pts)
        
        if deviation <= max_deviation:
            pts = new_pts
            print(f"Iteration {iteration}: deviation = {deviation:.4f} - continuing")
        else:
            print(f"Iteration {iteration}: deviation = {deviation:.4f} - STOPPED (would exceed {max_deviation})")
            break
    
    if iteration == max_iterations:
        print(f"Stopped at maximum iterations ({max_iterations})")
    
    return [tuple(p) for p in pts]




def check_connection(lane1, lane2):
    """Part B: Check C0 and C1 continuity"""
    
    l1 = [np.array(p) for p in lane1]
    l2 = [np.array(p) for p in lane2]
    
    # C0: position check
    gap = np.linalg.norm(l1[-1] - l2[0])
    print(f"\nC0 (Position): gap = {gap:.4f}m")
    if gap < 0.1:
        print("  ✓ Continuous (gap < 0.1m)")
    else:
        print("  ✗ Discontinuous")
    
    # C1: direction check
    angle = None
    if len(l1) >= 2 and len(l2) >= 2:
        # Last direction of lane1
        dir1 = l1[-1] - l1[-2]
        len1 = np.linalg.norm(dir1)
        
        # First direction of lane2
        dir2 = l2[1] - l2[0]
        len2 = np.linalg.norm(dir2)
        
        if len1 > 0 and len2 > 0:
            dir1 = dir1 / len1
            dir2 = dir2 / len2
            
            dot = np.dot(dir1, dir2)
            angle = np.arccos(np.clip(dot, -1, 1)) * 180 / np.pi
            
            print(f"C1 (Direction): angle = {angle:.1f}°")
            if angle < 15:
                print("  ✓ Continuous (angle < 15°)")
            else:
                print("  ✗ Discontinuous")
    
    return gap, angle





def make_plots(original, smoothed, lane2):
    """Make the two required plots as separate files"""
    
    orig = np.array(original)
    smooth = np.array(smoothed)
    l2 = np.array(lane2)
    
    # PLOT 1: Smoothing comparison - save as smoothing.png
    plt.figure(figsize=(6, 5))
    plt.plot(orig[:,0], orig[:,1], 'bo-', alpha=0.5, markersize=5, label='Original')
    plt.plot(smooth[:,0], smooth[:,1], 'r-', linewidth=2, label='Smoothed')
    # Highlight fixed endpoints
    plt.plot(orig[0,0], orig[0,1], 'gs', markersize=10, label='Fixed endpoints')
    plt.plot(orig[-1,0], orig[-1,1], 'gs', markersize=10)
    plt.title('Smoothing Comparison')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('smoothing.png', dpi=100)
    plt.close()  # Close this figure
    
    # PLOT 2: Continuity visualization - save as continuity.png
    plt.figure(figsize=(6, 5))
    
    # Plot both polylines near junction
    plt.plot(smooth[:,0], smooth[:,1], 'b-', linewidth=2, label='Polyline A')
    plt.plot(l2[:,0], l2[:,1], 'r-', linewidth=2, label='Polyline B')
    
    # Draw direction arrows
    if len(smooth) >= 2 and len(l2) >= 2:
        # Arrow for A's last segment
        dir1 = smooth[-1] - smooth[-2]
        dir1 = dir1 / np.linalg.norm(dir1) * 0.5
        plt.arrow(smooth[-2,0], smooth[-2,1], dir1[0], dir1[1], 
                 head_width=0.1, fc='blue', alpha=0.5)
        
        # Arrow for B's first segment
        dir2 = l2[1] - l2[0]
        dir2 = dir2 / np.linalg.norm(dir2) * 0.5
        plt.arrow(l2[0,0], l2[0,1], dir2[0], dir2[1],
                 head_width=0.1, fc='red', alpha=0.5)
    
    # Annotate gap (ε) and angle (θ)
    gap = np.linalg.norm(smooth[-1] - l2[0])
    plt.text(l2[0,0] + 0.2, l2[0,1], f'ε={gap:.3f}m', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
    
    if len(smooth) >= 2 and len(l2) >= 2:
        d1 = (smooth[-1] - smooth[-2]) / np.linalg.norm(smooth[-1] - smooth[-2])
        d2 = (l2[1] - l2[0]) / np.linalg.norm(l2[1] - l2[0])
        angle = np.arccos(np.clip(np.dot(d1, d2), -1, 1)) * 180 / np.pi
        plt.text(l2[0,0] + 0.2, l2[0,1] - 0.3, f'θ={angle:.1f}°', fontsize=10,
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    
    # Zoom to junction area
    margin = 1.5
    x_center = (smooth[-1,0] + l2[0,0]) / 2
    y_center = (smooth[-1,1] + l2[0,1]) / 2
    plt.xlim(x_center - margin, x_center + margin)
    plt.ylim(y_center - margin, y_center + margin)
    
    plt.title('Continuity Visualization')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('continuity.png', dpi=100)
    plt.close()
    
    print("✓ Created smoothing.png - shows original vs smoothed with fixed endpoints")
    print("✓ Created continuity.png - shows junction with gap (ε) and angle (θ)")
    
    # Show both plots together for viewing
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Recreate plot 1 in subplot
    ax1.plot(orig[:,0], orig[:,1], 'bo-', alpha=0.5, markersize=5, label='Original')
    ax1.plot(smooth[:,0], smooth[:,1], 'r-', linewidth=2, label='Smoothed')
    ax1.plot(orig[0,0], orig[0,1], 'gs', markersize=10, label='Fixed endpoints')
    ax1.plot(orig[-1,0], orig[-1,1], 'gs', markersize=10)
    ax1.set_title('smoothing.png')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.axis('equal')
    
    # Recreate plot 2 in subplot
    ax2.plot(smooth[:,0], smooth[:,1], 'b-', linewidth=2, label='Polyline A')
    ax2.plot(l2[:,0], l2[:,1], 'r-', linewidth=2, label='Polyline B')
    ax2.set_xlim(x_center - margin, x_center + margin)
    ax2.set_ylim(y_center - margin, y_center + margin)
    ax2.text(l2[0,0] + 0.2, l2[0,1], f'ε={gap:.3f}m', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
    if 'angle' in locals():
        ax2.text(l2[0,0] + 0.2, l2[0,1] - 0.3, f'θ={angle:.1f}°', fontsize=9,
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    ax2.set_title('continuity.png')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()





# Main
print("-"*50)
print("TASK 3: LANE SMOOTHING AND CONTINUITY")
print("-"*50)

print("\nOriginal lane A has", len(lane_a), "points")

print("\nPART A: Smoothing")
print("-"*30)
smoothed = smooth_lane(lane_a, max_deviation=0.3)

print("\nPART B: Continuity Check")
print("-"*30)
gap, angle = check_connection(smoothed, lane_b)

print("\nGenerating plots...")
make_plots(lane_a, smoothed, lane_b)

print("\nResults saved to smoothing.png")
print(f"\nSummary:")
print(f"- Max deviation allowed: 0.3m")
print(f"- Final gap at junction: {gap:.4f}m")
if angle:
    print(f"- Angle between segments: {angle:.1f}°")