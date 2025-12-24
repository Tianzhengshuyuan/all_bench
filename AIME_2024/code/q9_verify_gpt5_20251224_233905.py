inputs = {'xy': 25}

import math
import cmath

def solve(xy):
    # From equations: N^2 = 4 * xy, and N > 0 since bases and arguments > 1
    N_squared = 4 * xy
    try:
        N = math.sqrt(N_squared) if N_squared >= 0 else cmath.sqrt(N_squared)
    except Exception:
        N = cmath.sqrt(N_squared)
    # Prefer real positive root when applicable
    if isinstance(N, complex):
        if abs(N.imag) < 1e-12:
            r = N.real
            return int(round(r)) if abs(r - round(r)) < 1e-12 else r
        return N
    else:
        return int(round(N)) if abs(N - round(N)) < 1e-12 else N

solve(25)

# 调用 solve
result = solve(inputs['xy'])
print(result)