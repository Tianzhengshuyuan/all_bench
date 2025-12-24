inputs = {'xy': 25}

def solve(xy):
    import math
    import cmath

    # From N = x*log_x(y) = 4y*log_y(x) and log_x(y)*log_y(x)=1, we get N^2 = 4*xy
    # Hence N = 2*sqrt(xy). Use real sqrt for nonnegative reals; otherwise use complex principal sqrt.
    try:
        use_real = not isinstance(xy, complex) and xy >= 0
    except TypeError:
        use_real = False

    res = 2 * (math.sqrt(xy) if use_real else cmath.sqrt(xy))

    # Normalize nearly-real results and near-integers
    if isinstance(res, complex):
        if abs(res.imag) < 1e-12:
            r = res.real
        else:
            return res
    else:
        r = res

    if abs(r - round(r)) < 1e-12:
        return int(round(r))
    return r

solve(25)

# 调用 solve
result = solve(inputs['xy'])
print(result)