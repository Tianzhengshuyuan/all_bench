inputs = {'y_exp': 3}

from fractions import Fraction

def solve(y_exp):
    # Given system:
    # a - b - c = 1/2
    # -a + b - c = 1/3
    # -a - b + c = 1/4
    k1 = Fraction(1, 2)
    k2 = Fraction(1, 3)
    k3 = Fraction(1, 4)
    # Solve for a, b, c by adding pairs:
    # (1)+(3): -2b = k1 + k3  -> b = -(k1 + k3)/2
    # (1)+(2): -2c = k1 + k2  -> c = -(k1 + k2)/2
    # (2)+(3): -2a = k2 + k3  -> a = -(k2 + k3)/2
    a = - (k2 + k3) / 2
    b = - (k1 + k3) / 2
    c = - (k1 + k2) / 2
    val = abs(4 * a + Fraction(y_exp) * b + 2 * c)
    return val.numerator + val.denominator

solve(3)

# 调用 solve
result = solve(inputs['y_exp'])
print(result)