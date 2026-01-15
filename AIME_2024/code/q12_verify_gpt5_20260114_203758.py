inputs = {'vertical_sum': 99}

def solve(vertical_sum):
    from math import comb
    t = vertical_sum - 27
    if t % 9 != 0:
        return 0
    S = t // 9
    if S < 0 or S > 27:
        return 0
    res = 0
    for k in range(4):
        n = S - 10 * k
        term = comb(n + 2, 2) if n >= 0 else 0
        res += (-1) ** k * comb(3, k) * term
    return res

try:
    vertical_sum
except NameError:
    vertical_sum = 99

solve(vertical_sum)

# 调用 solve
result = solve(inputs['vertical_sum'])
print(result)