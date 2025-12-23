inputs = {'prime_power': 503}

def solve(prime_power):
    from math import isqrt

    def is_prime(n):
        if n < 2:
            return False
        if n % 2 == 0:
            return n == 2
        r = isqrt(n)
        f = 3
        while f <= r:
            if n % f == 0:
                return False
            f += 2
        return True

    def egcd(a, b):
        if b == 0:
            return (a, 1, 0)
        g, x1, y1 = egcd(b, a % b)
        return (g, y1, x1 - (a // b) * y1)

    def inv_mod(a, m):
        a %= m
        g, x, _ = egcd(a, m)
        if g != 1:
            raise ZeroDivisionError("inverse does not exist")
        return x % m

    def has_root_mod_p(p):
        # Check if x^4 ≡ -1 (mod p) has a solution
        target = (p - 1) % p
        for x in range(p):
            if pow(x, 4, p) == target:
                return True
        return False

    def hensel_lift(a, p, k):
        # Lift solution a (mod p) of x^4 + 1 ≡ 0 to mod p^k
        x = a % p
        if k == 1:
            return x
        mod = p
        for _ in range(1, k):
            # Compute c = (f(x) / mod) mod p, where f(x) = x^4 + 1
            f_mod_next = (pow(x, 4, mod * p) + 1) % (mod * p)
            c = (f_mod_next // mod) % p
            # Compute derivative f'(x) = 4x^3 mod p and its inverse
            fp = (4 * pow(x, 3, p)) % p
            inv_fp = inv_mod(fp, p)
            delta = (-c * inv_fp) % p
            x = x + delta * mod
            mod *= p
        return x % mod

    k = prime_power
    if k <= 0:
        return 1

    # For k = 1, least prime is 2 and minimal m is 1 (since 1^4 + 1 = 2)
    if k == 1:
        return 1

    # For k >= 2, search odd primes p such that x^4 ≡ -1 (mod p) has a solution
    p = None
    cand = 3
    while True:
        if is_prime(cand) and has_root_mod_p(cand):
            p = cand
            break
        cand += 2

    # Compute all roots modulo p
    roots_mod_p = set()
    target = (p - 1) % p
    for x in range(1, p):
        if pow(x, 4, p) == target:
            roots_mod_p.add(x % p)

    # Lift each root to modulo p^k and take the smallest positive representative
    m_candidates = []
    for a in roots_mod_p:
        r = hensel_lift(a, p, k)
        if r == 0:
            r = p ** k
        m_candidates.append(r)
    return min(m_candidates)

solve(2)

# 调用 solve
result = solve(inputs['prime_power'])
print(result)