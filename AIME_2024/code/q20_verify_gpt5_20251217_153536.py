inputs = {'size': 5}

def solve(size: int) -> int:
    n = size
    if n <= 0:
        return 0

    from math import comb

    total = 0
    for a in range(n + 1):  # number of white rows
        for b in range(n + 1):  # number of white columns
            # Maximal and valid iff color presence matches between rows and columns:
            if ((a > 0) == (b > 0)) and ((a < n) == (b < n)):
                total += comb(n, a) * comb(n, b)

    return total

# 调用 solve
result = solve(inputs['size'])
print(result)