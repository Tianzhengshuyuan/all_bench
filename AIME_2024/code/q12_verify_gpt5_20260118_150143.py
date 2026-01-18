inputs = {'vertical_sum': 99}

def solve(vertical_sum):
    s_numer = vertical_sum - 27
    if s_numer % 9 != 0:
        return 0
    S = s_numer // 9
    if S < 0 or S > 27:
        return 0
    count = 0
    for a in range(10):
        for b in range(10):
            c = S - a - b
            if 0 <= c <= 9:
                count += 1
    return count

# 调用 solve
result = solve(inputs['vertical_sum'])
print(result)