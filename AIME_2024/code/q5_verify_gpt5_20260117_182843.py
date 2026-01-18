inputs = {'R_large': 34}

from fractions import Fraction

def solve(R_large):
    N_small = 2024
    N_large = 8
    R = Fraction(R_large, 1)
    two = Fraction(2, 1)

    # Solve for x using BC equality from small and large circle chains:
    # 2*x + (2*N_small - 2) = 2*R*x + (2*N_large - 2)*R
    numerator = (two * N_large - 2) * R - (two * N_small - 2)
    denominator = two * (1 - R)
    x = numerator / denominator

    # Inradius r from BC = 2*r*x and BC = 2*x + (2*N_small - 2)
    r = Fraction(1, 1) + Fraction(N_small - 1, 1) / x

    r = Fraction(r)  # ensure reduced fraction
    return r.numerator + r.denominator

solve(34)

# 调用 solve
result = solve(inputs['R_large'])
print(result)