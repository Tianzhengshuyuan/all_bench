inputs = {'n': 10}

import math
from math import comb

def solve(n):
    # n is the number of vertices (8 for octagon)
    total = 0
    
    # Iterate over number of blue vertices k
    for k in range(0, n + 1):
        # Generate all possible blue configurations (as bitmasks or sets)
        # We'll represent a configuration as a tuple of 0s and 1s, 1 meaning blue
        # But we can do better: iterate over all combinations of k positions
        
        # For each combination of k positions, check if it satisfies the condition
        from itertools import combinations
        
        valid = 0
        # Generate all ways to choose k positions out of n to be blue
        for blues in combinations(range(n), k):
            # blues is a tuple of indices that are blue
            # We want to check: does there exist a rotation r (0 <= r < n) such that
            # every blue vertex, when rotated by r positions, lands on a red vertex?
            # That is: for every i in blues, (i + r) mod n is NOT in blues
            
            # So: for some r, the set {(i + r) % n for i in blues} is disjoint from blues
            
            # Precompute the set of blue positions for fast lookup
            blue_set = set(blues)
            
            found = False
            for r in range(n):
                # Check if rotating by r moves all blues to reds
                ok = True
                for i in blues:
                    if (i + r) % n in blue_set:
                        ok = False
                        break
                if ok:
                    found = True
                    break
            if found:
                valid += 1
        
        total += valid
    
    total_possible = 2 ** n
    from math import gcd
    g = gcd(total, total_possible)
    m = total // g
    n_reduced = total_possible // g
    return m + n_reduced

# Example: solve(8) should return 371

# 调用 solve
result = solve(inputs['n'])
print(result)