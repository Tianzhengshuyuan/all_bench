inputs = {'row_sum_target': 999}

def solve(row_sum_target):
    count = 0
    for a in range(10):
        for b in range(10):
            for c in range(10):
                sx = a + b + c
                sy = 99 - 10 * sx
                if sy < 0 or sy > 27:
                    continue
                n = row_sum_target - (100 * a + 10 * b + c)
                if n < 0 or n > 999:
                    continue
                d = n // 100
                e = (n // 10) % 10
                f = n % 10
                if d + e + f == sy:
                    count += 1
    return count

solve(999)

# 调用 solve
result = solve(inputs['row_sum_target'])
print(result)