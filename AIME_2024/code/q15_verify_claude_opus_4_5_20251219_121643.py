inputs = {'direction_changes': 4}

from math import comb

def solve(direction_changes):
    """
    Calculate the number of paths on an 8x8 grid that change direction exactly 
    direction_changes times.
    
    A path from lower left to upper right on an 8x8 grid has 8 R moves and 8 U moves.
    If we change direction k times, we have k+1 segments alternating between R and U.
    
    For direction_changes = 4, we have 5 segments.
    Two cases: RURUR or URURU
    
    For RURUR: 3 R-segments and 2 U-segments
    For URURU: 3 U-segments and 2 R-segments
    
    These are symmetric, so we calculate one and multiply by 2.
    """
    
    # Number of segments = direction_changes + 1
    num_segments = direction_changes + 1
    
    # Grid size is 8x8, so we need 8 R moves and 8 U moves
    grid_size = 8
    
    # For a path with num_segments alternating segments:
    # If starting with R: ceil(num_segments/2) R-segments, floor(num_segments/2) U-segments
    # If starting with U: ceil(num_segments/2) U-segments, floor(num_segments/2) R-segments
    
    # Number of segments for each direction when starting with R
    r_segments = (num_segments + 1) // 2  # ceiling division
    u_segments = num_segments // 2  # floor division
    
    # We need to distribute 8 R moves into r_segments parts (each part >= 1)
    # This is equivalent to distributing 8 - r_segments into r_segments parts (each part >= 0)
    # Using stars and bars: C(8 - r_segments + r_segments - 1, r_segments - 1) = C(7, r_segments - 1)
    
    # Similarly for U moves into u_segments parts
    
    # Ways to split 8 R moves into r_segments positive parts
    ways_r = comb(grid_size - 1, r_segments - 1)
    
    # Ways to split 8 U moves into u_segments positive parts
    ways_u = comb(grid_size - 1, u_segments - 1)
    
    # Total for starting with R
    count_start_r = ways_r * ways_u
    
    # By symmetry, starting with U gives the same count (since grid is square)
    # So total = 2 * count_start_r
    total = 2 * count_start_r
    
    return total

result = solve(4)

# 调用 solve
result = solve(inputs['direction_changes'])
print(result)