inputs = {'n_sides': 6}

def solve(n_sides):
    from fractions import Fraction

    n = int(n_sides)
    if n <= 0:
        return 1  # By convention, only one coloring and it's valid

    total = 1 << n
    allmask = total - 1

    def rotate(mask, k):
        # Rotate mask left by k on n bits
        return ((mask << k) | (mask >> (n - k))) & allmask

    valid = 0
    for mask in range(total):
        ok = False
        for k in range(n):
            if (rotate(mask, k) & mask) == 0:
                ok = True
                break
        if ok:
            valid += 1

    prob = Fraction(valid, total)
    return prob.numerator + prob.denominator

# 调用 solve
result = solve(inputs['n_sides'])
print(result)