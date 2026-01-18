inputs = {'two_count': 428}

def solve(two_count):
    # Given constants from the problem
    y = 234  # exactly three of the four (i.e., exactly two of the three special items)
    total_special = 195 + 367 + 562  # total counts of the three special items (excluding hearts)

    # From counting special items: total_special = two_count + 2*y + 3*z
    z_num = total_special - (two_count + 2 * y)
    return z_num // 3 if z_num % 3 == 0 else z_num / 3

# 调用 solve
result = solve(inputs['two_count'])
print(result)