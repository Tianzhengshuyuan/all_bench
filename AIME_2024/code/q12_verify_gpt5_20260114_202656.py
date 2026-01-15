inputs = {'row_sum_target': 999}

def solve(row_sum_target):
    col_target = 99  # sum of vertical 2-digit numbers
    # Precompute all 3-digit (with leading zeros) values grouped by digit sum
    triples_by_sum = [[] for _ in range(28)]  # sums 0..27
    for x in range(10):
        for y in range(10):
            for z in range(10):
                s = x + y + z
                triples_by_sum[s].append(100 * x + 10 * y + z)
    # For quick membership checks for bottom row candidates by sum
    bottom_values_sets = [set(vals) for vals in triples_by_sum]
    res = 0
    for S in range(28):
        T = col_target - 10 * S
        if 0 <= T <= 27:
            bottom_set = bottom_values_sets[T]
            for top_val in triples_by_sum[S]:
                need = row_sum_target - top_val
                if 0 <= need <= 999 and need in bottom_set:
                    res += 1
    return res

solve(999)

# 调用 solve
result = solve(inputs['row_sum_target'])
print(result)