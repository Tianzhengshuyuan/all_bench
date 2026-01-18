inputs = {'pick_count': 4}

def solve(pick_count):
    from math import comb
    from fractions import Fraction

    N = 10  # size of S
    D = 4   # numbers randomly chosen from S
    k = pick_count

    if k < 0 or k > N:
        return 0

    ways_prize = 0
    max_m = min(k, D)
    for m in range(2, max_m + 1):
        if D - m <= N - k:
            ways_prize += comb(k, m) * comb(N - k, D - m)

    ways_grand = comb(N - k, D - k) if k <= D else 0

    if ways_prize == 0:
        return 0

    prob = Fraction(ways_grand, ways_prize)
    return prob.numerator + prob.denominator

solve(4)

# 调用 solve
result = solve(inputs['pick_count'])
print(result)