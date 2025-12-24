inputs = {'xy': 25}

def solve(xy):
    import math
    import cmath

    # From the relations, N^2 = 4*xy => N = 2*sqrt(xy)
    try:
        use_real = not isinstance(xy, complex) and xy >= 0
    except TypeError:
        use_real = False

    N = 2 * (math.sqrt(xy) if use_real else cmath.sqrt(xy))

    # Normalize nearly-real results and near-integers
    if isinstance(N, complex):
        if abs(N.imag) < 1e-12:
            r = N.real
        else:
            return N
    else:
        r = N

    ir = round(r)
    return int(ir) if abs(r - ir) < 1e-12 else r

solve(25)

# 调用 solve
result = solve(inputs['xy'])
print(result)