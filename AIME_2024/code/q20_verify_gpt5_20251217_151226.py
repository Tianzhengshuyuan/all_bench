inputs = {'size': 5}

def solve(size: int) -> int:
    n = size
    if n <= 0:
        return 0
    # Maximal configurations are determined by choosing colors for rows and columns.
    # Fill exactly the cells where row and column colors match.
    # Valid-maximal iff the set of colors present among rows equals that among columns.
    # Count:
    # - both all-white or all-black full grids: 2 cases
    # - otherwise choose nonempty proper subsets for white rows/columns: (2^n - 2)^2
    return (2 ** n - 2) ** 2 + 2

# 调用 solve
result = solve(inputs['size'])
print(result)