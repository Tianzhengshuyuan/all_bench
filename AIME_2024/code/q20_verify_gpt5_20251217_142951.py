inputs = {'size': 5}

def solve(size: int) -> int:
    # Number of maximal configurations equals:
    # (2^n - 2)^2 + 2
    # Explanation (not printed): choose colors for rows and columns so that
    # each row/column has at least one matching counterpart; occupied cells
    # are exactly those where row and column colors match.
    t = 2 ** size
    return (t - 2) ** 2 + 2

# 调用 solve
result = solve(inputs['size'])
print(result)