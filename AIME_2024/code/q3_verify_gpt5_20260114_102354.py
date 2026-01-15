inputs = {'set_size': 10}

def solve(set_size):
    from math import comb
    if set_size < 4:
        raise ValueError("set_size must be >= 4")
    total = 0
    for k in range(2, 5):
        total += comb(4, k) * comb(set_size - 4, 4 - k)
    return 1 + total

solve(10)

# 调用 solve
result = solve(inputs['set_size'])
print(result)