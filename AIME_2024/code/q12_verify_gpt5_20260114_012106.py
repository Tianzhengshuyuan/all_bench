inputs = {'column_sum': 99}

def solve(column_sum):
    from math import comb

    def C(n, k):
        if n < 0 or k < 0 or k > n:
            return 0
        return comb(n, k)

    # From the row-sum condition (999), we get a+d=9, b+e=9, c+f=9.
    # Column-sum is: 10(a+b+c) + (d+e+f) = column_sum
    # Substitute d=9-a, e=9-b, f=9-c -> 10(a+b+c) + (27 - (a+b+c)) = column_sum
    # So 9(a+b+c) + 27 = column_sum -> s = a+b+c = (column_sum - 27) / 9
    s_num = column_sum - 27
    if s_num % 9 != 0:
        return 0
    s = s_num // 9
    if s < 0 or s > 27:
        return 0

    # Count solutions to a+b+c = s with 0 <= a,b,c <= 9 via inclusion-exclusion
    res = 0
    for j in range(0, 4):
        res += (-1) ** j * C(3, j) * C(s - 10 * j + 2, 2)
    return res

solve(column_sum)

# 调用 solve
result = solve(inputs['column_sum'])
print(result)