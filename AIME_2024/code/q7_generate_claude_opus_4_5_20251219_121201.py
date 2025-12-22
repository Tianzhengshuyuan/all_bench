inputs = {'num_sides': 18}

from math import gcd
from itertools import combinations

def solve(num_sides):
    n = num_sides
    total_colorings = 2 ** n
    valid_count = 0
    
    # Iterate over all possible colorings
    for coloring in range(total_colorings):
        # Get positions of blue vertices (1 = blue, 0 = red)
        blue_positions = set()
        for i in range(n):
            if (coloring >> i) & 1:
                blue_positions.add(i)
        
        num_blues = len(blue_positions)
        red_positions = set(range(n)) - blue_positions
        
        # Check if there exists a rotation k such that all blue vertices
        # end up at positions that were originally red
        # This means: for each blue position b, (b + k) mod n must be in red_positions
        
        found_valid_rotation = False
        for k in range(n):
            # Check if this rotation works
            valid = True
            for b in blue_positions:
                new_pos = (b + k) % n
                if new_pos not in red_positions:
                    valid = False
                    break
            if valid:
                found_valid_rotation = True
                break
        
        if found_valid_rotation:
            valid_count += 1
    
    # Simplify the fraction
    m = valid_count
    n_denom = total_colorings
    common = gcd(m, n_denom)
    m //= common
    n_denom //= common
    
    return m + n_denom

result = solve(8)

# 调用 solve
result = solve(inputs['num_sides'])
print(result)