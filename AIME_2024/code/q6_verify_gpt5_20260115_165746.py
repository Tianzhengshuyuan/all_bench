inputs = {'intersection_count': 385}

def solve(intersection_count):
    return (intersection_count - 1) // 128

solve(intersection_count)

# 调用 solve
result = solve(inputs['intersection_count'])
print(result)