inputs = {'AB_AC': 468}

def solve(AB_AC):
    R = 13
    denom = 6 * R
    if isinstance(AB_AC, int) and AB_AC % denom == 0:
        return AB_AC // denom
    return AB_AC / denom

solve(468)

# 调用 solve
result = solve(inputs['AB_AC'])
print(result)