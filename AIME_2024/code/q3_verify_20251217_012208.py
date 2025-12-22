inputs = {'pick_count': 4}

def solve(pick_count):
    from math import comb

    n = 10  # size of S = {1,2,...,10}
    k = int(pick_count)

    if k < 2 or k > n:
        raise ValueError("pick_count must satisfy 2 <= pick_count <= 10")

    denom = 0
    for r in range(2, k + 1):
        if 0 <= k - r <= n - k:
            denom += comb(k, r) * comb(n - k, k - r)

    if denom == 0:
        raise ValueError("No winning outcomes for the given pick_count.")

    # Probability of grand prize given a prize is 1 / denom, so m=1, n=denom -> answer m+n = 1 + denom
    return 1 + denom

# 调用 solve
result = solve(inputs['pick_count'])
print(result)