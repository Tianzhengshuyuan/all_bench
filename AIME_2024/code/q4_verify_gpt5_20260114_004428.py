inputs = {'upper_bound': 2024}

def solve(upper_bound):
    if upper_bound < 1:
        return 0
    count_mult_5 = upper_bound // 5
    count_mod2 = ((upper_bound - 2) // 5 + 1) if upper_bound >= 2 else 0
    return count_mult_5 + count_mod2

solve(2024)

# 调用 solve
result = solve(inputs['upper_bound'])
print(result)