inputs = {'total_sum': 28}

def solve(total_sum):
    for n in [2, 4, 6, 8]:
        if n == 2:
            continue
        elif n == 4:
            k = 2
            rem = total_sum - k * 9
            for a in range(1, rem // 2):
                b = rem - a
                if a == b or a == 9 or b == 9:
                    continue
                if b < 9:
                    median = (b + 9) / 2
                    if median.is_integer():
                        median_val = int(median)
                        lst = [a, b, 9, 9]
                        if median_val not in lst:
                            return sum(x * x for x in lst)
    return -1

# 调用 solve
result = solve(inputs['total_sum'])
print(result)