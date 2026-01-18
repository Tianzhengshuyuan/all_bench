inputs = {'row_sum': 999}

def solve(row_sum):
    r = row_sum
    count = 0
    for x in range(19):  # x = a + d
        for y in range(19):  # y = b + e
            z = r - 100 * x - 10 * y  # z = c + f
            if not (0 <= z <= 18):
                continue
            t = 99 - (x + y + z)
            if t % 9 != 0:
                continue
            s1 = t // 9  # s1 = a + b + c
            if not (0 <= s1 <= 27):
                continue

            a_min, a_max = max(0, x - 9), min(9, x)
            b_min, b_max = max(0, y - 9), min(9, y)
            c_min, c_max = max(0, z - 9), min(9, z)
            if a_min > a_max or b_min > b_max or c_min > c_max:
                continue

            for a in range(a_min, a_max + 1):
                for b in range(b_min, b_max + 1):
                    c = s1 - a - b
                    if c_min <= c <= c_max:
                        count += 1
    return count

row_sum = 999
solve(row_sum)

# 调用 solve
result = solve(inputs['row_sum'])
print(result)