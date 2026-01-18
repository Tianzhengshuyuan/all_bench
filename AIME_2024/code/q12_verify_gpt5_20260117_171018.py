inputs = {'row_sum': 999}

def solve(row_sum):
    count = 0
    r = row_sum
    for a in range(10):
        for b in range(10):
            for c in range(10):
                s = a + b + c
                L = 99 - 10 * s
                if L < 0 or L > 27:
                    continue
                for d in range(10):
                    for e in range(10):
                        f = L - (d + e)
                        if 0 <= f <= 9:
                            if 100 * (a + d) + 10 * (b + e) + (c + f) == r:
                                count += 1
    return count

solve(row_sum)

# 调用 solve
result = solve(inputs['row_sum'])
print(result)