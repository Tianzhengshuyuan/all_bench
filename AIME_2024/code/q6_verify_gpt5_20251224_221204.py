inputs = {'intersection_count': 385}

def solve(intersection_count):
    num = intersection_count - 1
    q, r = divmod(num, 128)
    if r == 0:
        return q
    return num / 128

result = solve(intersection_count)

# 调用 solve
result = solve(inputs['intersection_count'])
print(result)