inputs = {'set_count': 2016}

def solve(set_count):
    double = 2 * set_count
    binary_str = bin(double)[2:]
    reversed_binary = binary_str[::-1]
    total = 0
    for idx, bit in enumerate(reversed_binary):
        if bit == '1':
            total += idx
    return total

# 调用 solve
result = solve(inputs['set_count'])
print(result)