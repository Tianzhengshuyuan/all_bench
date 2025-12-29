inputs = {'b': 211}

def solve(b):
    n = b - 1
    if n <= 1:
        return 0
    count = 0
    if n % 2 == 0:
        count += 1
        while n % 2 == 0:
            n //= 2
    p = 3
    while p * p <= n:
        if n % p == 0:
            count += 1
            while n % p == 0:
                n //= p
        p += 2
    if n > 1:
        count += 1
    return (1 << count) - 1

solve(211)

# 调用 solve
result = solve(inputs['b'])
print(result)