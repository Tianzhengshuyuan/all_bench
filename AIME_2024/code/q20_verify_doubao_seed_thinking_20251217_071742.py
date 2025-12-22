inputs = {'white_chip_count': 25}

import math

def solve(white_chip_count):
    grid_size = 5
    total = 0
    for a in range(grid_size + 1):
        for b in range(grid_size + 1):
            white_used = a * b
            black_used = (grid_size - a) * (grid_size - b)
            if white_used > white_chip_count or black_used > white_chip_count:
                continue
            if white_used + black_used == 0:
                continue
            total += math.comb(grid_size, a) * math.comb(grid_size, b)
    return total

# 调用 solve
result = solve(inputs['white_chip_count'])
print(result)