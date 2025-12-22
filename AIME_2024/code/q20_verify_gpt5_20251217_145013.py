inputs = {'size': 5}

def solve(size: int) -> int:
    n = size
    if n <= 0:
        return 0
    # Maximal configurations correspond to choosing white-row and white-column sets:
    # - either both are nonempty proper subsets: (2^n - 2)^2 choices
    # - or both are the full set or empty set (all-white or all-black): +2
    return (2 ** n - 2) ** 2 + 2

# 调用 solve
result = solve(inputs['size'])
print(result)