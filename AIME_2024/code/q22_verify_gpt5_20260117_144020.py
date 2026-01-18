inputs = {'c': 300}

def solve(c):
    # Ratios from the given triangle: KL/KM=200/300=2/3, LM/KM=240/300=4/5
    r_KL_KM = 2/3
    r_LM_KM = 4/5
    # From similarity: KA = x/(LM/KM), AF = x, FM = x/(KL/KM)
    coef = 1 / r_LM_KM + 1 + 1 / r_KL_KM
    return c / coef

solve(300)

# 调用 solve
result = solve(inputs['c'])
print(result)