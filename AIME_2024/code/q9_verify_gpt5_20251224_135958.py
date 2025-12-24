inputs = {'xy': 25}

def solve(xy):
    import math
    import cmath

    # From log identities: N = x*log_x(y) = 4y*log_y(x) and log_x(y)*log_y(x) = 1
    # => N^2 = 4*xy => N = 2*sqrt(xy) (take principal/nonnegative root when real).
    try:
        use_real = not isinstance(xy, complex) and xy >= 0
    except TypeError:
        use_real = False

    N = 2 * (math.sqrt(xy) if use_real else cmath.sqrt(xy))

    # Normalize nearly-real results and near-integers
    if isinstance(N, complex):
        if abs(N.imag) < 1e-12:
            N = N.real
        else:
            return N

    r = round(N)
    if abs(N - r) < 1e-12:
        return int(r)
    return N

solve(25)

# 调用 solve
result = solve(inputs['xy'])
print(result)