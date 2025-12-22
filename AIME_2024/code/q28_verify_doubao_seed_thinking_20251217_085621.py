inputs = {'ac_bd_squared_length': 80}

import math

def prime_factors(n):
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
    p_squared = (ac_bd_squared_length - 48) / 2
    q_squared = (130 - ac_bd_squared_length) / 2
    r_squared = (ac_bd_squared_length + 48) / 2
    
    p = math.isqrt(int(p_squared))
    q = math.isqrt(int(q_squared))
    r = math.isqrt(int(r_squared))
    
    N = p * q * r
    A = (p * q) ** 2 + (p * r) ** 2 + (q * r) ** 2
    
    factors = prime_factors(A)
    k = 1
    n = 1
    for prime, exp in factors.items():
        k *= prime ** (exp // 2)
        n *= prime ** (exp % 2)
    
    num_rational = N * k
    den_rational = 2 * A
    
    gcd_val = math.gcd(num_rational, den_rational)
    m = num_rational // gcd_val
    p_den = den_rational // gcd_val
    
    return m + n + p_den

# 调用 solve
result = solve(inputs['ac_bd_squared_length'])
print(result)