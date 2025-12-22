inputs = {'spade_count': 562}

def solve(spade_count):
    # Constants from the problem
    total_residents = 900
    rings = 195
    clubs = 367
    hearts = total_residents  # each resident owns one
    exactly_two = 437
    exactly_three = 234

    # Equations:
    # 1) w + x + y + z = total_residents  -> w + z = total_residents - exactly_two - exactly_three
    s1 = total_residents - exactly_two - exactly_three  # w + z

    # 2) Total items counted by ownership multiplicity:
    #    w + 2x + 3y + 4z = total_items
    total_items = rings + clubs + spade_count + hearts
    s2 = total_items - 2 * exactly_two - 3 * exactly_three  # w + 4z

    # Subtract: (w + 4z) - (w + z) = 3z
    z_num = s2 - s1
    if z_num % 3 != 0:
        raise ValueError("Inconsistent input: cannot derive integer residents count")
    return z_num // 3

# 调用 solve
result = solve(inputs['spade_count'])
print(result)