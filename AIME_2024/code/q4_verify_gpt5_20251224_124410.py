inputs = {'K': 809}

def solve(K):
    B = 2024
    m = 5
    q, rem = divmod(B, m)
    candidates = set()
    for s in range(0, m + 1):
        for I0 in (0, 1):
            if I0 > s:
                continue
            s_nonzero = s - I0
            s1 = K - q * s
            # s1 must be the number of residues from {1..rem} included in S
            if 0 <= s1 <= rem and 0 <= s_nonzero - s1 <= (m - 1 - rem):
                candidates.add(10 * I0 + s)
    if candidates:
        return min(candidates)
    return None

solve(809)

# 调用 solve
result = solve(inputs['K'])
print(result)