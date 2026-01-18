inputs = {'divisor': 1000}

def solve(divisor):
    # Find the greatest four-digit integer N such that changing any one digit to 1 yields a multiple of 7
    N = None
    for n in range(9999, 999, -1):
        a = n // 1000
        b = (n // 100) % 10
        c = (n // 10) % 10
        d = n % 10
        n_a1 = 1000 + 100 * b + 10 * c + d
        n_b1 = 1000 * a + 100 + 10 * c + d
        n_c1 = 1000 * a + 100 * b + 10 + d
        n_d1 = 1000 * a + 100 * b + 10 * c + 1
        if n_a1 % 7 == 0 and n_b1 % 7 == 0 and n_c1 % 7 == 0 and n_d1 % 7 == 0:
            N = n
            break
    if N is None:
        raise ValueError("No four-digit integer satisfies the condition.")

    if divisor == 0:
        raise ValueError("divisor must be nonzero.")
    Q = N // divisor
    R = N % divisor
    return Q + R

# 调用 solve
result = solve(inputs['divisor'])
print(result)