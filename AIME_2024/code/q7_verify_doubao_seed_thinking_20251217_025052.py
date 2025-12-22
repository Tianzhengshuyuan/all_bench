inputs = {'vertex_count': 8}

import math

def solve(vertex_count):
    n = vertex_count
    m = n.bit_length() - 1
    sum_comb = sum(math.comb(n, k) for k in range(n // 2))
    count_k_half = 0
    for i in range(m):
        count_k_half += 2 ** (2 ** i)
    total_valid = sum_comb + count_k_half
    total_colorings = 2 ** n
    g = math.gcd(total_valid, total_colorings)
    numerator = total_valid // g
    denominator = total_colorings // g
    return numerator + denominator

# 调用 solve
result = solve(inputs['vertex_count'])
print(result)