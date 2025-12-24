inputs = {'xy': 25}

def solve(xy):
    import math
    import cmath

    # From N = x*log_x(y) = 4y*log_y(x) and log_x(y)*log_y(x)=1, we get N^2 = 4*xy
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

    if abs(r - round(r)) < 1e-12:
        return int(round(r))
    return r

solve(25)

# 调用 solve
result = solve(inputs['xy'])
print(result)