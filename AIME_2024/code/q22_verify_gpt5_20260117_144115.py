inputs = {'c': 300}

def solve(c):
    # Constants: the other two triangle sides
    a = 200.0
    b = 240.0
    # From similarity: c = x*(c/b + 1 + c/a) => x = c / (c/b + 1 + c/a)
    denom = (c / b) + 1.0 + (c / a)
    return c / denom

solve(300)

# 调用 solve
result = solve(inputs['c'])
print(result)