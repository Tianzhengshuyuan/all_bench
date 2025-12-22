inputs = {'size': 5}

def solve(size: int) -> int:
    n = size
    if n <= 0:
        return 0
    # Maximal configurations correspond to choosing colors for rows and columns such that:
    # - either all rows and all columns are the same color (2 cases), filling the whole grid, or
    # - both colors appear among rows and columns; then all equal-color intersections are filled.
    # The count is (2^n - 2)^2 + 2.
    return (2 ** n - 2) ** 2 + 2

# 调用 solve
result = solve(inputs['size'])
print(result)