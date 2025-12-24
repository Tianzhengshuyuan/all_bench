inputs = {'K': 809}

def solve(K):
    B = 2024
    m = 5
    q, rem = divmod(B, m)
    # For n in 1..B: residue 0 appears q times; residues 1..rem appear q+1 times; others appear q times.
    # If S is the set of winning residues for Bob, let s = |S|, I0 = 1 if 0 in S else 0,
    # and s1 = |S ∩ {1..rem}|. Then K = q*s + s1 with constraints:
    # 0 <= s1 <= rem and 0 <= (s - I0) - s1 <= (m - 1 - rem).
    for s in range(0, m + 1):
        for I0 in (0, 1):
            if I0 > s:
                continue
            s_nonzero = s - I0
            s1 = K - q * s
            if 0 <= s1 <= rem and 0 <= s_nonzero - s1 <= (m - 1 - rem):
                return 10 * I0 + s
    return None

solve(809)

# 调用 solve
result = solve(inputs['K'])
print(result)