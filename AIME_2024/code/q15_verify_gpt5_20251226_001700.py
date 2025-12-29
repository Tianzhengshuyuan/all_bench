inputs = {'path_count': 294}

def solve(path_count):
    # Number of monotone paths from (0,0) to (n,n) with exactly 4 turns:
    # count(n) = 2 * C(n-1,2) * C(n-1,1) = (n-1)^2 * (n-2)
    # Let m = n - 1, then count = m^2 * (m - 1). Solve for integer m, then n = m + 1.
    def f(m):
        return m * m * (m - 1)

    if path_count < 0:
        return None

    lo, hi = 0, 1
    while f(hi) < path_count:
        hi *= 2

    while lo <= hi:
        mid = (lo + hi) // 2
        val = f(mid)
        if val == path_count:
            return mid + 1
        if val < path_count:
            lo = mid + 1
        else:
            hi = mid - 1
    return None

solve(294)

# 调用 solve
result = solve(inputs['path_count'])
print(result)