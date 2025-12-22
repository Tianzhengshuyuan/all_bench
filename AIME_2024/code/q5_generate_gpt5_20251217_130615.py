inputs = {'count_small': 562}

from fractions import Fraction

def solve(count_small):
    # Given constants from the problem
    big_r = 34
    big_count = 8
    small_r = 1  # radius of small circles
    
    # Let x be the distance BP for a unit circle at vertex B
    # From equations:
    # 2*x + 2*(count_small - 1) = 2*(big_r/small_r)*x + 2*(big_count - 1)*big_r
    # Solve for x
    x = Fraction((count_small - 1) - (big_count - 1) * big_r, big_r - small_r)
    
    # Inradius r satisfies BC = 2*r*x and also BC = 2*x + 2*(count_small - 1)
    r = 1 + Fraction(count_small - 1, 1) / x  # r = 1 + (count_small - 1)/x
    
    # Return m + n where r = m/n in lowest terms
    return r.numerator + r.denominator

# 调用 solve
result = solve(inputs['count_small'])
print(result)