inputs = {'turns': 4}

def solve(turns):
    import math

    def comb(n, k):
        if k < 0 or k > n:
            return 0
        return math.comb(n, k)

    ups = rights = 8
    s = int(turns) + 1  # number of segments
    m = (s + 1) // 2    # segments of starting direction
    n = s // 2          # segments of the other direction

    return 2 * comb(ups - 1, m - 1) * comb(rights - 1, n - 1)

# 调用 solve
result = solve(inputs['turns'])
print(result)