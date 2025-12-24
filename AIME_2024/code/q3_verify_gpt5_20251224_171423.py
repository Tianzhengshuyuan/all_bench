inputs = {'m_plus_n': 116}

def solve(m_plus_n):
    from math import comb
    pick = 4
    total = 10
    rest = total - pick
    target = m_plus_n - 1
    matches = []
    for r in range(0, pick + 1):
        S = sum(comb(pick, k) * comb(rest, pick - k) for k in range(r, pick + 1))
        if S == target:
            matches.append(r)
    if len(matches) == 1:
        return matches[0]
    return None

solve(116)

# 调用 solve
result = solve(inputs['m_plus_n'])
print(result)