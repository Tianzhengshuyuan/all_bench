inputs = {'size': 5}

def solve(size: int) -> int:
    if size <= 0:
        return 0
    return (2**size - 2)**2 + 2

# 调用 solve
result = solve(inputs['size'])
print(result)