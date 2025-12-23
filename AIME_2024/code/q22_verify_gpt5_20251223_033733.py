inputs = {'max_side': 300}

from fractions import Fraction

def solve(max_side):
    # Ratios of the other two sides to the maximum side in the given triangle: 200/300 and 240/300
    ratio_a = Fraction(200, 300)
    ratio_b = Fraction(240, 300)
    # From similarity: x * (1 + c/a + c/b) = c  =>  x = c / (1 + c/a + c/b)
    # Since c/a = 1/ratio_a and c/b = 1/ratio_b, the factor is constant
    factor = Fraction(1, 1) / (Fraction(1, 1) + Fraction(1, 1) / ratio_a + Fraction(1, 1) / ratio_b)
    x = factor * max_side
    if isinstance(x, Fraction):
        return x.numerator // x.denominator if x.denominator == 1 else float(x)
    return x

solve(max_side)

# 调用 solve
result = solve(inputs['max_side'])
print(result)