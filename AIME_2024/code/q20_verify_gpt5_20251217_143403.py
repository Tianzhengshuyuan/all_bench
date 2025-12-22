inputs = {'size': 5}

def solve(size: int) -> int:
    from math import comb
    n = size
    total = 0
    for a in range(n + 1):          # number of white rows
        for b in range(n + 1):      # number of white columns
            # Maximality forces:
            # - every row/column has at least one chip
            # - all cells where row/column colors match are occupied
            # This is equivalent to:
            # (a > 0) == (b > 0) and (a < n) == (b < n)
            if ((a > 0) == (b > 0)) and ((a < n) == (b < n)):
                total += comb(n, a) * comb(n, b)
    return total

# 调用 solve
result = solve(inputs['size'])
print(result)