inputs = {'log_x4y3z2_denominator': 8}

from fractions import Fraction

def solve(log_x4y3z2_denominator):
    D = Fraction(log_x4y3z2_denominator, 1)
    # Using -(4a+3b+2c)=25/D and relations among a,b,c to get:
    # A = log2(x/(yz)) = (2/5) * (25/D - 15/8)
    A = Fraction(2, 5) * (Fraction(25, 1) / D - Fraction(15, 8))
    if A == 0:
        return None
    N = Fraction(1, A)
    return N.numerator if N.denominator == 1 else N

solve(8)

# 调用 solve
result = solve(inputs['log_x4y3z2_denominator'])
print(result)