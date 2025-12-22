inputs = {'size': 5}

def solve(size: int) -> int:
    # Number of maximal configurations equals:
    # - choose a nontrivial coloring for rows: 2^n - 2 options (exclude all-white and all-black)
    # - choose a nontrivial coloring for columns: 2^n - 2 options
    # Each such pair yields a unique maximal configuration by filling exactly the cells
    # where row and column colors match.
    # Additionally, there are 2 monochromatic full-grid configurations (all white or all black).
    return (2 ** size - 2) ** 2 + 2

# 调用 solve
result = solve(inputs['size'])
print(result)