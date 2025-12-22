inputs = {'count': 564}

def solve(count):
    S = count << 1
    return sum(i for i in range(1, S.bit_length()) if (S >> i) & 1)

# 调用 solve
result = solve(inputs['count'])
print(result)