inputs = {'walk_length': 9}

import math

def solve(walk_length):
    L = walk_length
    sqrt_term = math.sqrt(4 + 5 * L)
    s = (sqrt_term - 2) / 2
    t_hours = 4 - (L / s)
    new_speed = s + 0.5
    total_hours = (L / new_speed) + t_hours
    return int(total_hours * 60)

# 调用 solve
result = solve(inputs['walk_length'])
print(result)