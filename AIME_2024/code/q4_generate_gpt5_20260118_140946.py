inputs = {'upper_bound': 1973}

def solve(upper_bound):
    n = int(upper_bound)
    if n < 1:
        return 0
    count_mod0 = n // 5
    count_mod2 = (n - 2) // 5 + 1 if n >= 2 else 0
    return count_mod0 + count_mod2

# 调用 solve
result = solve(inputs['upper_bound'])
print(result)