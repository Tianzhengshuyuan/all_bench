inputs = {'ring_count': 195}

def solve(ring_count):
    total_residents = 900
    clubs = 367
    spades = 562
    hearts = 900
    exactly_two = 437
    exactly_three = 234

    w_plus_z = total_residents - (exactly_two + exactly_three)
    total_items = ring_count + clubs + spades + hearts
    w_plus_4z = total_items - (2 * exactly_two + 3 * exactly_three)

    num = w_plus_4z - w_plus_z
    return num // 3 if num % 3 == 0 else num / 3

solve(ring_count)

# 调用 solve
result = solve(inputs['ring_count'])
print(result)