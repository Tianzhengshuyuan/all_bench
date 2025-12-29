inputs = {'bd2_greatest_lower_bound': 480}

def solve(bd2_greatest_lower_bound):
    L = bd2_greatest_lower_bound
    B = 24
    denom = L + 4 * B
    if denom == 0:
        return None
    A = L * B / denom
    r = round(A)
    return r if abs(A - r) < 1e-9 else A

bd2_greatest_lower_bound = 480
solve(bd2_greatest_lower_bound)

# 调用 solve
result = solve(inputs['bd2_greatest_lower_bound'])
print(result)