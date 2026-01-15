from fractions import Fraction
inputs = {'r': Fraction(192, 5)}

from fractions import Fraction

def solve(r):
    if not isinstance(r, Fraction):
        r = Fraction(r)
    R2 = Fraction(34, 1)
    M2 = 8
    two = Fraction(2, 1)
    # From equality of BC for three arrangements:
    # 2*r*x = 2*R2*x + 2*R2*(M2-1) -> x = [2*R2*(M2-1)] / [2*(r - R2)]
    denom = two * (r - R2)
    x = (two * R2 * Fraction(M2 - 1, 1)) / denom
    # For unit circles: 2*r*x = 2*x + 2*(n-1) -> n = (r - 1)*x + 1
    n = (r - Fraction(1, 1)) * x + Fraction(1, 1)
    return n.numerator if n.denominator == 1 else n

result = solve(Fraction(192, 5))

# 调用 solve
result = solve(inputs['r'])
print(result)