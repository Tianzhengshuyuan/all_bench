inputs = {'p_power': 3}

def solve(p_power):
    from math import gcd, isqrt

    def is_prime(n):
        if n < 2:
            return False
        if n % 2 == 0:
            return n == 2
        r = isqrt(n)
        i = 3
        while i <= r:
            if n % i == 0:
                return False
            i += 2
        return True

    def egcd(a, b):
        if b == 0:
            return (a, 1, 0)
        g, x1, y1 = egcd(b, a % b)
        return (g, y1, x1 - (a // b) * y1)

    def modinv(a, m):
        a %= m
        g, x, _ = egcd(a, m)
        if g != 1:
            return None
        return x % m

    def exists_root_for_prime(p, e):
        if p == 2:
            return e == 1
        # For odd primes, solvable mod p iff -1 is a 4th power mod p
        # Equivalent to 8 | (p-1)
        return (p - 1) % 8 == 0

    def find_least_prime_with_solution(e):
        n = 2
        while True:
            if is_prime(n) and exists_root_for_prime(n, e):
                return n
            n += 1

    def hensel_lift_roots(p, e):
        if p == 2:
            if e == 1:
                return [1]
            else:
                return []
        # find roots mod p by brute force
        roots_p = []
        target = (p - 1) % p
        for x in range(p):
            if pow(x, 4, p) == target:
                roots_p.append(x)
        # lift each root to mod p^e
        roots = []
        mod = p
        for r in roots_p:
            x = r
            mod = p
            for k in range(1, e):
                next_mod = mod * p
                f_mod = (pow(x, 4, next_mod) + 1) % next_mod
                s = (f_mod // mod) % p  # f(x) = mod * s (mod next_mod)
                df = (4 * pow(x, 3, p)) % p
                inv_df = modinv(df, p)
                t = (-s * inv_df) % p
                x = x + t * mod
                mod = next_mod
            roots.append(x % (p**e))
        return roots

    e = int(p_power)
    if e <= 0:
        return None
    p = find_least_prime_with_solution(e)
    roots = hensel_lift_roots(p, e)
    if not roots:
        return None
    # minimal positive representative
    roots_pos = [r for r in roots if r > 0]
    return min(roots_pos) if roots_pos else None

solve(2)

# 调用 solve
result = solve(inputs['p_power'])
print(result)