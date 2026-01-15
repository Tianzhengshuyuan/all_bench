inputs = {'num_configurations': 902}

def solve(num_configurations):
    def isqrt(n):
        if n < 0:
            return None
        if n < 2:
            return n
        x = 1 << ((n.bit_length() + 1) // 2)
        while True:
            y = (x + n // x) // 2
            if y >= x:
                return x
            x = y

    t = int(num_configurations) - 2
    if t < 0:
        return None
    s = isqrt(t)
    if s is None or s * s != t:
        return None
    m = s + 2
    if m <= 0 or (m & (m - 1)) != 0:
        return None
    N = m.bit_length() - 1
    return N if N >= 1 else None

solve(902)

# 调用 solve
result = solve(inputs['num_configurations'])
print(result)