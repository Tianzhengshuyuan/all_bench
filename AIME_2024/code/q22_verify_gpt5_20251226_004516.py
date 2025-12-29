inputs = {'hexagon_side_length': 80}

from fractions import Fraction

def solve(hexagon_side_length):
    x = Fraction(hexagon_side_length).limit_denominator()
    a = Fraction(200)
    b = Fraction(240)
    sum_inv = Fraction(1, 1) / a + Fraction(1, 1) / b
    denom = Fraction(1, 1) - x * sum_inv
    if denom == 0:
        return float('inf')
    c = x / denom
    return int(c) if c.denominator == 1 else float(c)

solve(80)

# 调用 solve
result = solve(inputs['hexagon_side_length'])
print(result)