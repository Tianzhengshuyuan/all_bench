inputs = {'size': 5}

def solve(size):
    if size == 0:
        return 1
    return (2**size - 2)**2 + 2

# 调用 solve
result = solve(inputs['size'])
print(result)