inputs = {'K': 809}

def solve(K):
    B = 2024
    m = 5
    q, r = divmod(B, m)

    # For residues among 1..B:
    # count[0] = q; among residues 1..r count is q+1, among residues r+1..m-1 count is q.
    # If S is a set of residues with size s, I0 = 1 if 0 in S else 0,
    # and s1 = |S ∩ {1..r}|, then K = q*s + s1.
    # Feasibility constraints:
    #   s_nonzero = s - I0 must be split as s1 (picked from r residues) and
    #   s_nonzero - s1 (picked from m-1-r residues), so
    #   0 <= s1 <= r and 0 <= s_nonzero - s1 <= (m-1-r).
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