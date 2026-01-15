inputs = {'row_sum': 999}

def solve(row_sum):
    count = 0
    for a in range(10):
        for b in range(10):
            for c in range(10):
                bottom_sum = 99 - 10 * (a + b + c)
                if bottom_sum < 0 or bottom_sum > 27:
                    continue
                target_bottom_value = row_sum - (100 * a + 10 * b + c)
                if target_bottom_value < 0 or target_bottom_value > 999:
                    continue
                for d in range(10):
                    for e in range(10):
                        f = bottom_sum - d - e
                        if 0 <= f <= 9 and 100 * d + 10 * e + f == target_bottom_value:
                            count += 1
    return count

solve(999)

# 调用 solve
result = solve(inputs['row_sum'])
print(result)