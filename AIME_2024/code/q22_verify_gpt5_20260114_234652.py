inputs = {'max_side': 300}

def solve(max_side):
    a = 200
    b = 240
    c = max_side
    numerator = c * a * b
    denominator = a * b + c * b + c * a
    if denominator == 0:
        return None
    if numerator % denominator == 0:
        return numerator // denominator
    return numerator / denominator

solve(max_side)

# 调用 solve
result = solve(inputs['max_side'])
print(result)