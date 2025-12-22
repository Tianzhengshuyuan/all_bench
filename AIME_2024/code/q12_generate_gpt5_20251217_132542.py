inputs = {'cols': 2}

def solve(cols):
    # Number of columns (cols) is the number of digits per horizontal number.
    # Conditions:
    # 1) Per column j, top digit a_j and bottom digit b_j must satisfy a_j + b_j = 9 (to sum to all-9s horizontally without carry).
    # 2) Sum over columns of vertical two-digit numbers 10*a_j + b_j equals 99.
    #    Using b_j = 9 - a_j, we get 9*sum(a_j) + 9*cols = 99 -> sum(a_j) = 11 - cols.
    # Count the number of C-tuples (a_j) with 0 <= a_j <= 9 and sum(a_j) = S where S = 11 - cols.
    # This is a bounded stars-and-bars problem with upper bound 9.
    S = 11 - cols
    if S < 0:
        return 0

    U = 9  # upper bound per digit

    def nCr(n, k):
        if k < 0 or k > n:
            return 0
        k = min(k, n - k)
        res = 1
        for i in range(1, k + 1):
            res = res * (n - k + i) // i
        return res

    # Inclusion-exclusion for bounded compositions
    max_j = min(cols, S // (U + 1))
    res = 0
    for j in range(max_j + 1):
        t = S - j * (U + 1)
        res += (-1) ** j * nCr(cols, j) * nCr(t + cols - 1, cols - 1)
    return res

# 调用 solve
result = solve(inputs['cols'])
print(result)