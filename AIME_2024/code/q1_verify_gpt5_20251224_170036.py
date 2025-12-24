inputs = {'abs_log_denominator': 8}

def solve(abs_log_denominator):
    from fractions import Fraction
    D = Fraction(abs_log_denominator)
    # Given:
    # b - a - c = 1/3
    # c - a - b = 1/4
    # |4a + 3b + 2c| = 25/D
    # Solve a from the first two: a = -7/24, and b = c + 1/24
    a = Fraction(-7, 24)
    T = Fraction(25, 1) / D  # absolute value target

    candidates = []
    for sgn in (1, -1):
        # From 4a + 3b + 2c = ± 25/D and b = c + 1/24:
        # t = 4a + 3(c + 1/24) + 2c = 5c - 25/24
        # => 5c - 25/24 = ± 25/D
        c = (Fraction(25, 24) + sgn * T) / 5
        b = c + Fraction(1, 24)
        s = a - b - c  # s = log2(x/(yz))
        candidates.append(s)

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