inputs = {'size': 5}

def solve(size: int) -> int:
    n = size
    if n <= 0:
        return 0

    # Count all configurations where both colors appear in rows and columns:
    # choose a nonempty proper subset of rows and columns for white;
    # all matching intersections are filled; others are empty.
    # Number of such choices: (2^n - 2)^2
    mixed = (2 ** n - 2) ** 2

    # Add the two extreme configurations: all white or all black
    return mixed + 2

# 调用 solve
result = solve(inputs['size'])
print(result)