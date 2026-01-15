inputs = {'exp_z': 2}

from fractions import Fraction

def solve(exp_z):
    a = Fraction(-7, 24)   # log2(x)
    b = Fraction(-3, 8)    # log2(y)
    c = Fraction(-5, 12)   # log2(z)
    e = Fraction(exp_z)
    val = abs(4*a + 3*b + e*c)
    return val.numerator + val.denominator

solve(2)

# 调用 solve
result = solve(inputs['exp_z'])
print(result)