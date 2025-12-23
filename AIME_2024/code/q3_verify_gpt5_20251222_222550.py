inputs = {'draw_count': 4}

def solve(draw_count):
    from math import gcd

    def comb(n, k):
        if n < 0 or k < 0 or k > n:
            return 0
        k = min(k, n - k)
        res = 1
        for i in range(1, k + 1):
            res = res * (n - k + i) // i
        return res

    k = draw_count
    total_numbers = 10
    chosen_by_jen = 4
    others = total_numbers - chosen_by_jen

    num = comb(others, k - chosen_by_jen) if k >= chosen_by_jen else 0

    denom = 0
    for r in range(2, chosen_by_jen + 1):
        if r <= k:
            denom += comb(chosen_by_jen, r) * comb(others, k - r)

    if denom == 0:
        return 0

    g = gcd(num, denom)
    num //= g
    denom //= g
    return num + denom

solve(4)

# 调用 solve
result = solve(inputs['draw_count'])
print(result)