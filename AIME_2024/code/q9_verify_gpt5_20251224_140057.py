inputs = {'xy': 25}

def solve(xy):
    import math
    import cmath

    # From N^2 = 4*xy, take N = 2*sqrt(xy) (principal root).
    try:
        use_real = not isinstance(xy, complex) and xy >= 0
    except TypeError:
        use_real = False

    res = 2 * (math.sqrt(xy) if use_real else cmath.sqrt(xy))

    # Normalize nearly-real results
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