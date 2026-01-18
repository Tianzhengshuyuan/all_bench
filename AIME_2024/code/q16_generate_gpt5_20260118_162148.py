inputs = {'p_power': 1}

def solve(p_power):
    # Helper: extended GCD for modular inverse
    def egcd(a, b):
        if b == 0:
            return (a, 1, 0)
        g, x1, y1 = egcd(b, a % b)
        return (g, y1, x1 - (a // b) * y1)

    def inv_mod(a, m):
        a %= m
        g, x, _ = egcd(a, m)
        if g != 1:
            raise ZeroDivisionError("Inverse does not exist")
        return x % m

    # Prime check
    def is_prime(n):
        if n < 2:
            return False
        if n % 2 == 0:
            return n == 2
        if n % 3 == 0:
            return n == 3
        i = 5
        w = 2
        while i * i <= n:
            if n % i == 0:
                return False
            i += w
            w = 6 - w
        return True

    # Generate primes in increasing order
    def prime_generator():
        yield 2
        p = 3
        while True:
            if is_prime(p):
                yield p
            p += 2

    # Find all roots of x^4 + 1 ≡ 0 (mod p^k)
    def roots_mod_pk(p, k):
        if k <= 0:
            return [0]  # trivial root class mod 1 (unused in our logic)
        if p == 2:
            if k == 1:
                return [1]
            else:
                return []
        # p odd:
        # Step 1: roots modulo p
        roots_p = []
        target = (-1) % p
        for r in range(p):
            if pow(r, 4, p) == target:
                roots_p.append(r)
        if not roots_p:
            return []
        if k == 1:
            return roots_p[:]
        # Step 2: Hensel lift each root to p^k
        roots = []
        for r0 in roots_p:
            r = r0
            for t in range(1, k):
                pt = pow(p, t)
                pt1 = pt * p
                # f(r) mod p^{t+1}
                f_mod = (pow(r, 4, pt1) + 1) % pt1
                A = (f_mod // pt) % p  # coefficient in Z/pZ
                # derivative modulo p
                der = (4 * pow(r, 3, p)) % p
                inv_der = inv_mod(der, p)
                delta = (-A * inv_der) % p
                r = r + delta * pt
            roots.append(r)
        return roots

    # Main solve:
    k = int(p_power)
    if k <= 0:
        return 1  # any number works, minimal positive m is 1

    for p in prime_generator():
        roots = roots_mod_pk(p, k)
        if roots:
            mod = pow(p, k)
            # minimal positive representative among solutions
            candidates = [(r % mod) for r in roots]
            # remove 0 if ever appears (it shouldn't for x^4 + 1)
            candidates = [c for c in candidates if c != 0]
            return min(candidates) if candidates else 0  # fallback (shouldn't hit)
    # Should never reach here
    return None

# 调用 solve
result = solve(inputs['p_power'])
print(result)