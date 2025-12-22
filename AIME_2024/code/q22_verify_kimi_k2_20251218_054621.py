inputs = {'side_length': 200}

def solve(side_length):
    # side_length is not used directly; we use the given triangle side lengths 200, 240, 300
    # Let the side length of the hexagon be x
    # From the similar triangles setup:
    # KA = (5/4)*x, AF = x, FM = (3/2)*x
    # KA + AF + FM = 300
    # (5/4)*x + x + (3/2)*x = 300
    # Convert to common denominator: (5x + 4x + 6x)/4 = 300
    # 15x/4 = 300
    # x = 300 * 4 / 15
    x = 300 * 4 // 15
    return x

# 调用 solve
result = solve(inputs['side_length'])
print(result)