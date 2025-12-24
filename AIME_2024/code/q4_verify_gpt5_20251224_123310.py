inputs = {'K': 809}

def solve(K):
    total = 2024
    m = 5
    base = total // m  # 404
    # For n in 1..2024: count of residue 0 is base, others are base+1
    for s in range(0, m + 1):
        i0 = (base + 1) * s - K
        if i0 in (0, 1) and s >= i0:
            return 10 * i0 + s
    return None

solve(809)

# 调用 solve
result = solve(inputs['K'])
print(result)