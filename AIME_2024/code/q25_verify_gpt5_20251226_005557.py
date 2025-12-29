inputs = {'all_four': 73}

def solve(all_four):
    T = 900
    rings = 195
    clubs = 367
    hearts = T
    x = 437  # exactly two
    y = 234  # exactly three
    # Total items counted by summing per-person item counts
    total_items = T + x + 2 * y + 3 * all_four
    # total_items also equals rings + clubs + spades(N) + hearts
    N = total_items - (rings + clubs + hearts)
    return N

solve(73)

# 调用 solve
result = solve(inputs['all_four'])
print(result)