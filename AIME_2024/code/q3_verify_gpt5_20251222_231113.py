inputs = {'draw_count': 4}

def solve(draw_count):
    from math import comb, gcd
    N = 10
    K = 4
    d = int(draw_count)

    def C(n, k):
        if k < 0 or k > n:
            return 0
        return comb(n, k)

    # Total favorable outcomes for winning any prize (at least 2 matches)
    ways_prize = 0
    upper = min(K, d)
    for k in range(2, upper + 1):
        ways_prize += C(K, k) * C(N - K, d - k)

    if ways_prize == 0:
        return 0

    # Grand prize outcomes (all 4 match)
    ways_grand = C(N - K, d - K)  # C(K, K) = 1

    g = gcd(ways_grand, ways_prize)
    m = ways_grand // g
    n = ways_prize // g
    return m + n

draw_count = 4
solve(draw_count)

# 调用 solve
result = solve(inputs['draw_count'])
print(result)