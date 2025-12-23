inputs = {'row_sum': 999}

def solve(row_sum):
    from collections import defaultdict

    def column_map(weight):
        m = defaultdict(int)
        for top in range(10):
            for bottom in range(10):
                dR = weight * (top + bottom)
                dT = 10 * top + bottom
                m[(dR, dT)] += 1
        return m

    M100 = column_map(100)
    M10 = column_map(10)
    M1 = column_map(1)

    # Convolve first two columns (hundreds and tens)
    comb = defaultdict(int)
    for (R0, T0), c0 in M100.items():
        for (R1, T1), c1 in M10.items():
            comb[(R0 + R1, T0 + T1)] += c0 * c1

    # Add the ones column and enforce the column-sum total 99
    target_T = 99
    ans = 0
    for (R2, T2), c2 in M1.items():
        ans += comb.get((row_sum - R2, target_T - T2), 0) * c2

    return ans

solve(999)

# 调用 solve
result = solve(inputs['row_sum'])
print(result)