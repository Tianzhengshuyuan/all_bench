inputs = {'m': 110}

def solve(m):
    import random
    import math

    def is_probable_prime(n):
        if n < 2:
            return False
        small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        for p in small_primes:
            if n % p == 0:
                return n == p
        # write n-1 = d * 2^s
        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1
        # Deterministic bases for 64-bit; probabilistic beyond
        for a in [2, 3, 5, 7, 11, 13]:
            if a % n == 0:
                continue
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            skip = False
            for _ in range(s - 1):
                x = (x * x) % n
                if x == n - 1:
                    skip = True
                    break
            if not skip:
                return False
        return True

    def pollard_rho(n):
        if n % 2 == 0:
            return 2
        if n % 3 == 0:
            return 3
        while True:
            c = random.randrange(1, n - 1)
            f = lambda x: (x * x + c) % n
            x = random.randrange(0, n - 1)
            y = x
            d = 1
            while d == 1:
                x = f(x)
                y = f(f(y))
                d = math.gcd(abs(x - y), n)
            if d != n:
                return d

    def factor(n, res):
        if n == 1:
            return
        if is_probable_prime(n):
            res[n] = res.get(n, 0) + 1
            return
        d = pollard_rho(n)
        factor(d, res)
        factor(n // d, res)

    def egcd(a, b):
        if b == 0:
            return (a, 0, 1)
        g, x1, y1 = egcd(b, a % b)
        return (g, y1, x1 - (a // b) * y1)

    def inv_mod(a, p):
        a %= p
        g, x, y = egcd(a, p)
        if g != 1:
            return None
        return x % p

    def minimal_root_mod_p2_for_eq(x4_eq_neg1, p):
        # find all solutions to x^4 ≡ -1 (mod p^2) and return minimal positive residue
        if p == 2:
            return None
        roots_mod_p = []
        for x in range(p):
            if pow(x, 4, p) == (p - 1) % p:
                roots_mod_p.append(x)
        if not roots_mod_p:
            return None
        roots_mod_p2 = set()
        for x0 in roots_mod_p:
            f_x0 = x0 * x0
            f_x0 = f_x0 * f_x0 + 1  # x0^4 + 1 (small int)
            # f_x0 is divisible by p
            s = f_x0 // p
            fp = (4 * (x0 ** 3)) % p
            inv_fp = inv_mod(fp, p)
            if inv_fp is None:
                continue
            t = (-s * inv_fp) % p
            x_p2 = (x0 + t * p) % (p * p)
            if x_p2 != 0:
                roots_mod_p2.add(x_p2)
        if not roots_mod_p2:
            return None
        return min(roots_mod_p2)

    N = m ** 4 + 1
    fac = {}
    factor(N, fac)

    candidates = []
    for p, e in fac.items():
        if e >= 2 and p != 2:
            min_root = minimal_root_mod_p2_for_eq(lambda x: (x * x * x * x + 1), p)
            if min_root is not None and min_root == m:
                candidates.append(p)
    if not candidates:
        return None
    return min(candidates)

solve(110)

# 调用 solve
result = solve(inputs['m'])
print(result)