inputs = {'ax_num': 1}

from fractions import Fraction

def solve(ax_num):
    a = Fraction(ax_num, 2)
    t = a * a
    s = Fraction(1, 1) - 3 * t + 3 * t * t
    return s.numerator + s.denominator

ax_num = 1
solve(ax_num)

# 调用 solve
result = solve(inputs['ax_num'])
print(result)