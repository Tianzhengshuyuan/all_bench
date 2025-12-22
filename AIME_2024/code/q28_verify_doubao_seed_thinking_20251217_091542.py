inputs = {'ac_bd_squared_length': 80}

import math

def prime_factorization(n):
    factors = {}
    while n % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        n = n // 2
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors[i] = factors.get(i, 0) + 1
            n = n // i
        i += 2
    if n > 1:
        factors[n] = 1
    return factors

def solve(ac_bd_squared_length):
    sum_squares = (41 + ac_bd_squared_length + 89) // 2
    a_squared = sum_squares - 89
    b_squared = sum_squares - ac_bd_squared_length
    c_squared = sum_squares - 41
    a = math.isqrt(a_squared)
    b = math.isqrt(b_squared)
    c = math.isqrt(c_squared)
    abc = a * b * c
    term = a_squared * b_squared + a_squared * c_squared + b_squared * c_squared
    factors = prime_factorization(term)
    k = 1
    n_val = 1
    for p, exp in factors.items():
        k *= p ** (exp // 2)
        if exp % 2 != 0:
            n_val *= p
    num = abc * k
    den = 2 * term
    gcd_val = math.gcd(num, den)
    m = num // gcd_val
    p_val = den // gcd_val
    return m + n_val + p_val

# 调用 solve
result = solve(inputs['ac_bd_squared_length'])
print(result)