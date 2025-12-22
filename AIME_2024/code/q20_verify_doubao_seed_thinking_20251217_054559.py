inputs = {'white_chip_count': 25}

def solve(white_chip_count):
    n = int(white_chip_count ** 0.5)
    return 4 ** n

# 调用 solve
result = solve(inputs['white_chip_count'])
print(result)