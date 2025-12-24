inputs = {'abs_log_denominator': 8}

def solve(abs_log_denominator):
    from fractions import Fraction
    D = Fraction(abs_log_denominator)
    A = Fraction(200, 1) / D  # 8 * (25/D)
    # s3 candidates from |20*s3 + 15| = 200/D
    candidates = [ (A - 15) / 20, (-A - 15) / 20 ]
    # Prefer form 1/N with positive N, then negative N, else fallback to 1/u (possibly non-integer)
    selected_u = None
    for u in candidates:
        if u.numerator == 1 and u.denominator > 0:
            selected_u = u
            break
    if selected_u is None:
        for u in candidates:
            if u.numerator == -1 and u.denominator > 0:
                selected_u = u
                break
    if selected_u is None:
        selected_u = candidates[0]
    if abs(selected_u.numerator) == 1:
        N = selected_u.denominator
        if selected_u.numerator == -1:
            N = -N
        return N
    inv = Fraction(1, 1) / selected_u
    if inv.denominator == 1:
        return inv.numerator
    return inv

solve(8)

# 调用 solve
result = solve(inputs['abs_log_denominator'])
print(result)