inputs = {'size': 5}

def solve(size: int) -> int:
    n = size
    if n <= 0:
        return 0
    return (2 ** n - 2) ** 2 + 2

# 调用 solve
result = solve(inputs['size'])
print(result)