inputs = {'sin_period_coeff': 2}

def solve(sin_period_coeff):
    return 8 * sin_period_coeff * 24 + 1

# 调用 solve
result = solve(inputs['sin_period_coeff'])
print(result)