inputs = {'sum_abc': 27}

def solve(sum_abc):
    k = sum_abc // 3
    per_case = (sum_abc - k) + 1
    total = 3 * per_case - 2
    return total

# 调用 solve
result = solve(inputs['sum_abc'])
print(result)