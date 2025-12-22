inputs = {'volume': 23}

from fractions import Fraction

def solve(volume):
    V = volume
    def get_divisors(n):
        divisors = set()
        for i in range(1, int(n**0.5) + 1):
            if n % i == 0:
                divisors.add(i)
                divisors.add(n // i)
        return sorted(divisors)
    divisors = get_divisors(2 * V)
    roots = []
    for d in divisors:
        if d ** 3 - 27 * d + 2 * V == 0:
            roots.append(d)
    max_r_sq = Fraction(0, 1)
    for d in roots:
        if d <= 0:
            continue
        a = Fraction(V, d * d)
        a_sq = a * a
        two_b_sq = Fraction(2 * d * d, 1)
        sum_sq = a_sq + two_b_sq
        current_r_sq = sum_sq / 4
        if current_r_sq > max_r_sq:
            max_r_sq = current_r_sq
    return max_r_sq.numerator + max_r_sq.denominator

# 调用 solve
result = solve(inputs['volume'])
print(result)