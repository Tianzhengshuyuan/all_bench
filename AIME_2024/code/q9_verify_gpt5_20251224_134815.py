inputs = {'xy': 25}

def solve(xy):
    import math
    try:
        if xy >= 0:
            return 2 * math.sqrt(xy)
    except TypeError:
        pass
    import cmath
    return 2 * cmath.sqrt(xy)

solve(25)

# 调用 solve
result = solve(inputs['xy'])
print(result)