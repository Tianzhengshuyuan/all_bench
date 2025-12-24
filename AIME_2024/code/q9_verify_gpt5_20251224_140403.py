inputs = {'xy': 25}

def solve(xy):
    import math
    import cmath

    # From N^2 = 4*xy and x,y>1 => N>0 for real cases.
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
    return int(r) if abs(N - r) < 1e-12 else N

solve(25)

# 调用 solve
result = solve(inputs['xy'])
print(result)