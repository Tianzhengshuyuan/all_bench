inputs = {'own4': 73}

def solve(own4):
    # Given constants from the problem
    total_residents = 900
    ring = 195
    clubs = 367
    spade = 562
    hearts = 900
    exactly_three = 234

    # Total items counted across all categories
    total_items = ring + clubs + spade + hearts

    # From counting by residents: x + 2y + 3z = total_items - total_residents
    # So exactly_two = x = (total_items - total_residents) - 2*exactly_three - 3*own4
    return (total_items - total_residents) - 2 * exactly_three - 3 * own4

own4 = 73
solve(own4)

# 调用 solve
result = solve(inputs['own4'])
print(result)