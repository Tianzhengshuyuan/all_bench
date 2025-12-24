inputs = {'xy': 25}

def solve(xy):
    import math
    import cmath

    val = 4 * xy
    try:
        use_real = not isinstance(val, complex) and val >= 0
    except TypeError:
        use_real = False

    res = math.sqrt(val) if use_real else cmath.sqrt(val)

    if isinstance(res, complex):
        if abs(res.imag) < 1e-12:
            r = res.real
        else:
            return res
    else:
        r = res

    ir = round(r)
    if abs(r - ir) < 1e-12:
        return int(ir)
    return r

solve(25)

# 调用 solve
result = solve(inputs['xy'])
print(result)