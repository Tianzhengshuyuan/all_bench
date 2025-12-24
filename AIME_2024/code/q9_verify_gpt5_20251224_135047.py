inputs = {'xy': 25}

def solve(xy):
    import math
    import cmath

    # From the relations: N = x*log_x(y) = 4y*log_y(x) and log_x(y)*log_y(x)=1,
    # we get N^2 = 4*xy => N = 2*sqrt(xy) (take principal/nonnegative root when real).
    try:
        if isinstance(xy, complex) or xy < 0:
            res = 2 * cmath.sqrt(xy)
        else:
            res = 2 * math.sqrt(xy)
    except TypeError:
        res = 2 * cmath.sqrt(xy)

    # Normalize near-real results and near-integers
    if isinstance(res, complex):
        if abs(res.imag) < 1e-12:
            val = res.real
            if abs(val - round(val)) < 1e-12:
                return int(round(val))
            return val
        return res
    else:
        if abs(res - round(res)) < 1e-12:
            return int(round(res))
        return res

solve(25)

# 调用 solve
result = solve(inputs['xy'])
print(result)