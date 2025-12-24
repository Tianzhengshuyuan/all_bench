inputs = {'K': 809}

def solve(K):
    B = 2024
    m = 5
    q, r = divmod(B, m)
    for s in range(0, m + 1):
        for I0 in (0, 1):
            if I0 > s:
                continue
            s_nonzero = s - I0
            s1 = K - q * s
            if 0 <= s1 <= r and 0 <= s_nonzero - s1 <= (m - 1 - r):
                return 10 * I0 + s
    return None

solve(809)

# 调用 solve
result = solve(inputs['K'])
print(result)