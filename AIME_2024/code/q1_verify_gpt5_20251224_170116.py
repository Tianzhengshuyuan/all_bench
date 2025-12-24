inputs = {'abs_log_denominator': 8}

def solve(abs_log_denominator):
    from fractions import Fraction
    D = Fraction(abs_log_denominator)
    # From the system:
    # a = log2(x), b = log2(y), c = log2(z)
    # b - a - c = 1/3
    # c - a - b = 1/4
    # => a = -7/24 and b - c = 1/24
    # Also, |4a + 3b + 2c| = 25/D
    # This leads to two candidates for s = a - b - c:
    # s = -3/4 ± 10/D
    candidates = [Fraction(-3, 4) + Fraction(10, 1) / D,
                  Fraction(-3, 4) - Fraction(10, 1) / D]
    # Prefer positive unit fraction 1/N
    for s in candidates:
        if s > 0 and s.numerator == 1:
            return s.denominator
    # If not, allow negative unit fraction -1/N (return N positive)
    for s in candidates:
        if s.numerator == -1:
            return s.denominator
    return None

solve(8)

# 调用 solve
result = solve(inputs['abs_log_denominator'])
print(result)