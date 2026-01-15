inputs = {'diamond_count': 195}

def solve(diamond_count):
    N = 900
    clubs = 367
    spades = 562
    hearts = N
    x = 437  # exactly two items
    y = 234  # exactly three items
    total_items = diamond_count + clubs + spades + hearts
    numerator = total_items - N - x - 2 * y
    return numerator // 3 if numerator % 3 == 0 else numerator / 3

solve(195)

# 调用 solve
result = solve(inputs['diamond_count'])
print(result)