inputs = {'volume': 23}

from fractions import Fraction

def solve(volume):
    def find_min_root(V):
        b = 1.0
        for _ in range(100):
            fb = b**3 - 27 * b + 2 * V
            dfb = 3 * b**2 - 27
            next_b = b - fb / dfb
            if abs(next_b - b) < 1e-12:
                b = next_b
                break
            b = next_b
        return b
    V = volume
    b_min = find_min_root(V)
    P_max = (3 * b_min**2 + 27) / (2 * b_min)
    a2b2c2 = P_max**2 - 54
    r_squared = a2b2c2 / 4
    frac = Fraction(r_squared).limit_denominator()
    return frac.numerator + frac.denominator

# 调用 solve
result = solve(inputs['volume'])
print(result)