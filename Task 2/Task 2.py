import matplotlib.pyplot as plt
import numpy as np

lanes = {
    '65': [(-0.7071067811865475, 0.7071067811865476), (9.899494936611665, 11.31370849898476)],
    '41': [(1.414213562373095, -1.4142135623730951), (12.020815280171309, 9.192388155425116)],
    '13': [(-1.414213562373095, 1.4142135623730951), (9.192388155425117, 12.020815280171307)],
    '39': [(0.7071067811865475, -0.7071067811865476), (11.313708498984761, 9.899494936611664)],
    '87': [(0.0, 0.0), (10.606601717798213, 10.606601717798211)]
}

# Expected answer (given)
EXPECTED_SORTED_LANE_IDS = ["41", "39", "87", "65", "13"]

def sort_lane_ids_right_to_left(lanes_dict):
    """
    Sort lanes from right to left when looking forward.
    
    Algorithm:
    1. Find average forward direction of all lanes
    2. Calculate right direction (perpendicular to forward)
    3. Project each lane onto the right axis
    4. Sort by projection (high to low = right to left)
    """
    print("\nSORTING PROCESS:")
    print("="*40)
    
    # STEP 1: Calculate forward direction for each lane
    print("\nStep 1: Calculate lane directions")
    forward_vectors = []
    
    for lane_id, (start_point, end_point) in lanes_dict.items():
        direction_x = end_point[0] - start_point[0]
        direction_y = end_point[1] - start_point[1]
        
        length = np.sqrt(direction_x**2 + direction_y**2)
        
        # Normalize (make length = 1)
        if length > 0:
            normalized_x = direction_x / length
            normalized_y = direction_y / length
            forward_vectors.append((normalized_x, normalized_y))
            print(f"  Lane {lane_id}: direction = ({normalized_x:.3f}, {normalized_y:.3f})")
    
    # STEP 2: Average all directions to get road direction
    print("\nStep 2: Calculate average forward direction")
    avg_x = sum(vec[0] for vec in forward_vectors) / len(forward_vectors)
    avg_y = sum(vec[1] for vec in forward_vectors) / len(forward_vectors)
    
    # Normalize the average
    avg_length = np.sqrt(avg_x**2 + avg_y**2)
    forward_x = avg_x / avg_length
    forward_y = avg_y / avg_length
    
    print(f"  Average forward: ({forward_x:.3f}, {forward_y:.3f})")
    
    # STEP 3: Calculate right direction (90° clockwise)
    print("\nStep 3: Calculate right direction")
    # If forward is (x, y), right is (y, -x)
    right_x = forward_y
    right_y = -forward_x
    
    print(f"  Right direction: ({right_x:.3f}, {right_y:.3f})")
    
    # Verify perpendicular (dot product should be 0)
    dot_product = forward_x * right_x + forward_y * right_y
    print(f"  Verification (should be ~0): {dot_product:.6f}")
    
    # STEP 4: Project each lane onto right axis
    print("\nStep 4: Project lanes onto right axis")
    lane_projections = []
    
    for lane_id, (start_point, end_point) in lanes_dict.items():
        # Use lane center as representative point
        center_x = (start_point[0] + end_point[0]) / 2
        center_y = (start_point[1] + end_point[1]) / 2
        
        # Project onto right direction (dot product)
        projection = center_x * right_x + center_y * right_y
        
        lane_projections.append((lane_id, projection))
        print(f"  Lane {lane_id}: center=({center_x:.2f}, {center_y:.2f}), projection={projection:.2f}")
    
    # STEP 5: Sort by projection (high to low = right to left)
    print("\nStep 5: Sort by projection (right to left)")
    lane_projections.sort(key=lambda x: x[1], reverse=True)
    
    sorted_ids = []
    for i, (lane_id, projection) in enumerate(lane_projections):
        sorted_ids.append(lane_id)
        position = "lane 1) rightmost" if i == 0 else "lane 5) leftmost" if i == len(lane_projections)-1 else f"lane {i+1}"
        print(f"  {i+1}. Lane {lane_id} ({position})")
    
    return sorted_ids

def visualize_lanes(lanes_dict, sorted_ids):    

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    lane_colors = {
        '65': 'blue',
        '41': 'red', 
        '13': 'green',
        '39': 'orange',
        '87': 'purple'
    }
    
    # LEFT PLOT: Original lanes
    ax1.set_title("Before Sorting")
    
    for lane_id, (start, end) in lanes_dict.items():
        x_coords = [start[0], end[0]]
        y_coords = [start[1], end[1]]
        
        # Plot lane with consistent color
        ax1.plot(x_coords, y_coords, '-', 
                color=lane_colors[lane_id], linewidth=2, label=f'Lane {lane_id}')
        
        # Simple text label at midpoint
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        ax1.text(mid_x, mid_y, lane_id, fontsize=10, fontweight='bold')
    
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y") 
    ax1.grid(True, alpha=0.3)
    ax1.axis('equal')
    ax1.legend(fontsize=8)
    
    # RIGHT PLOT: Sorted lanes with position numbers
    ax2.set_title(f"After Sorting: {' → '.join(sorted_ids)}")
    
    for idx, lane_id in enumerate(sorted_ids):
        start, end = lanes_dict[lane_id]
        x_coords = [start[0], end[0]]
        y_coords = [start[1], end[1]]
        
        # Same color as before
        ax2.plot(x_coords, y_coords, '-',
                color=lane_colors[lane_id], linewidth=2, 
                label=f'#{idx+1}: {lane_id}')
        
        # Show position number
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        ax2.text(mid_x, mid_y, str(idx+1), fontsize=12, fontweight='bold',
                bbox=dict(boxstyle="circle", facecolor="white", edgecolor=lane_colors[lane_id]))
    
    ax2.set_xlabel("X")
    ax2.set_ylabel("Y")
    ax2.grid(True, alpha=0.3)
    ax2.axis('equal')
    ax2.legend(fontsize=8)
    
    plt.tight_layout()
    plt.savefig('lane_sorting.png', dpi=100)
    plt.show()



# MAIN PROGRAM
if __name__ == "__main__":
        
    # Sort the lanes
    sorted_lane_ids = sort_lane_ids_right_to_left(lanes)
    
    # Print results
    print("\n" + "-"*50)
    print("RESULTS:")
    print(f"Your sorted order:     {sorted_lane_ids}")
    print(f"Expected sorted order: {EXPECTED_SORTED_LANE_IDS}")
    
    # Check if correct
    if sorted_lane_ids == EXPECTED_SORTED_LANE_IDS:
        print("\n✓ SUCCESS! The sorting is correct!")
    else:
        print("\n✗ The sorting doesn't match expected result")
    
    # Create visualization
    print("\nGenerating visualization...")
    visualize_lanes(lanes, sorted_lane_ids)
    
    print("\nDone! Check lane_sorting.png")