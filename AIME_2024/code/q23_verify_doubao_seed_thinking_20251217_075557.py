inputs = {'a_squared': 20}

def solve(a_squared):
    b_squared = (6 / 5) * a_squared
    numerator = 4 * a_squared * b_squared
    denominator = b_squared - a_squared
    return numerator / denominator

# 调用 solve
result = solve(inputs['a_squared'])
print(result)