inputs = {'total_sets': 383}

def solve(total_sets):
    target = total_sets
    # We need sum of 2^{a_i - 1} = target
    # So sum of 2^{a_i} = 2 * target
    doubled = 2 * target
    # Now find binary representation of doubled
    bits = []
    n = doubled
    index = 0
    while n > 0:
        if n & 1:
            bits.append(index)
        n >>= 1
        index += 1
    # The set A is {b for b in bits} (no +1 here)
    A = bits
    return sum(A)

# 调用 solve
result = solve(inputs['total_sets'])
print(result)