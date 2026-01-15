inputs = {'all_four': 73}

def solve(all_four):
    N = 900
    total_items = 195 + 367 + 562 + N
    y = 234
    z = all_four
    x = total_items - N - 2*y - 3*z
    return x

solve(73)

# 调用 solve
result = solve(inputs['all_four'])
print(result)