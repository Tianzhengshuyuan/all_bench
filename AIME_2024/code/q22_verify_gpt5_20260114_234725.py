inputs = {'max_side': 300}

def solve(max_side):
    a = 200
    b = 240
    c = max_side
    denominator = a * b + b * c + c * a
    if denominator == 0:
        return None
    numerator = a * b * c
    q, r = divmod(numerator, denominator)
    return q if r == 0 else numerator / denominator

max_side = 300
solve(max_side)

# 调用 solve
result = solve(inputs['max_side'])
print(result)