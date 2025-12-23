inputs = {'exp_y': 50}

from fractions import Fraction

def solve(exp_y):
    # Right-hand sides of the system
    a = Fraction(1, 2)
    b = Fraction(1, 3)
    c = Fraction(1, 4)
    # Solve for log2(x)=lx, log2(y)=ly, log2(z)=lz
    lx = - (b + c) / 2
    ly = - (a + c) / 2
    lz = - (a + b) / 2
    # Compute |log2(x^4 y^{exp_y} z^2)|
    ey = Fraction(exp_y)
    value = abs(4 * lx + ey * ly + 2 * lz)
    return value.numerator + value.denominator

solve(3)

# 调用 solve
result = solve(inputs['exp_y'])
print(result)