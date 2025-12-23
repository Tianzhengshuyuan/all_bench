inputs = {'upper_bound': 501}

def solve(upper_bound):
    if upper_bound <= 0:
        return 0
    count0 = upper_bound // 5
    count2 = ((upper_bound - 2) // 5 + 1) if upper_bound >= 2 else 0
    return count0 + count2

solve(upper_bound=2024)

# 调用 solve
result = solve(inputs['upper_bound'])
print(result)