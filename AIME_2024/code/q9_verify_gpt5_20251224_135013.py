inputs = {'xy': 25}

def solve(xy):
    import math
    import cmath

    val = 4 * xy
    # Prefer real nonnegative root when applicable; otherwise use complex principal root
    if not isinstance(xy, complex) and val >= 0:
        res = math.sqrt(val)
        if abs(res - round(res)) < 1e-12:
            return int(round(res))
        return res
    res = cmath.sqrt(val)
    if abs(res.imag) < 1e-12:
        r = res.real
        if abs(r - round(r)) < 1e-12:
            return int(round(r))
        return r
    return res

solve(25)

# 调用 solve
result = solve(inputs['xy'])
print(result)