inputs = {'qr_sum': 699}

from math import gcd, isqrt

def solve(qr_sum):
    maxN_for_M = {}
    for N in range(9999, 999, -1):
        a = N // 1000
        rest = N % 1000
        b = rest // 100
        rest2 = rest % 100
        c = rest2 // 10
        d = rest2 % 10

        t1 = N - 1000 * (a - 1)
        t2 = N - 100 * (b - 1)
        t3 = N - 10 * (c - 1)
        t4 = N - (d - 1)

        G = gcd(gcd(t1, t2), gcd(t3, t4))
        if G <= 1:
            continue

        divs = set()
        r = isqrt(G)
        for i in range(1, r + 1):
            if G % i == 0:
                if i > 1:
                    divs.add(i)
                if G // i > 1:
                    divs.add(G // i)
        if not divs:
            continue

        for m in divs:
            if m not in maxN_for_M:
                maxN_for_M[m] = N

    candidates = []
    for m, N in maxN_for_M.items():
        a = N // 1000
        if a + (N % 1000) == qr_sum:
            candidates.append(m)

    if not candidates:
        return -1
    return min(candidates)

solve(699)

# 调用 solve
result = solve(inputs['qr_sum'])
print(result)