inputs = {'m': 110}

def solve(m):
    import random
    import math

    def is_probable_prime(n):
        if n < 2:
            return False
        small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
        for p in small_primes:
            if n % p == 0:
                return n == p
        # write n-1 = d * 2^s
        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1
        # Miller-Rabin with a few bases (good in practice)
        for a in [2, 3, 5, 7, 11, 13, 17]:
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
        # try small trial division first to stabilize
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
            if n % p == 0:
                cnt = 0
                while n % p == 0:
                    n //= p
                    cnt += 1
                res[p] = res.get(p, 0) + cnt
                factor(n, res)
                return
        d = pollard_rho(n)
        factor(d, res)
        factor(n // d, res)

    def egcd(a, b):
        if b == 0:
            return (a, 1, 0)
        g, x1, y1 = egcd(b, a % b)
        return (g, y1, x1 - (a // b) * y1)

    def inv_mod(a, p):
        a %= p
        g, x, _ = egcd(a, p)
        if g != 1:
            return None
        return x % p

    def minimal_root_mod_p2(p):
        # minimal positive x in [1, p^2-1] with x^4 ≡ -1 (mod p^2), or None if no solution
        if p == 2:
            return None
        # find roots modulo p
        roots_mod_p = [x for x in range(1, p) if pow(x, 4, p) == (p - 1)]
        if not roots_mod_p:
            return None
        roots_mod_p2 = []
        for x0 in roots_mod_p:
            # Hensel lift: f(x)=x^4+1, f'(x)=4x^3
            fx0 = x0 ** 4 + 1  # divisible by p
            s = fx0 // p       # integer, we will use s mod p
            fp = (4 * (x0 ** 3)) % p
            inv_fp = inv_mod(fp, p)
            if inv_fp is None:
                continue
            t = (-s * inv_fp) % p
            x_p2 = (x0 + t * p) % (p * p)
            if x_p2 != 0:
                roots_mod_p2.append(x_p2)
        if not roots_mod_p2:
            return None
        return min(roots_mod_p2)

    # compute N = m^4 + 1
    m2 = m * m
    N = m2 * m2 + 1

    # factor N
    fac = {}
    factor(N, fac)

    # collect candidate primes p with p^2 | N (verify directly to avoid count issues)
    candidates = []
    for p in fac.keys():
        if p == 2:
            continue
        if N % (p * p) == 0:
            r = minimal_root_mod_p2(p)
            if r is not None and r == m:
                candidates.append(p)

    if candidates:
        return min(candidates)

    # Fallback: in rare cases factorization may fail to detect squared multiplicity correctly.
    # Search primes p with p^2 > m and m^4 + 1 ≡ 0 (mod p^2) and minimal root equals m.
    # Restrict to p ≡ 1 (mod 8) since otherwise no solutions exist.
    def gen_primes_up_to(limit):
        sieve = [True] * (limit + 1)
        sieve[0] = sieve[1] = False
        for i in range(2, int(limit ** 0.5) + 1):
            if sieve[i]:
                step = i
                start = i * i
                sieve[start:limit + 1:step] = [False] * (((limit - start) // step) + 1)
        return [i for i, v in enumerate(sieve) if v]

    # We only need to check up to some reasonable bound; since p | N, p ≤ N.
    # Use a moderate bound based on m to avoid infinite work if something is inconsistent.
    bound = max(int(min(N, 10 * max(1000, int(m ** 0.5) + 1000))), 10000)
    for p in gen_primes_up_to(bound):
        if p == 2 or p % 8 != 1:
            continue
        if p * p <= m:
            continue
        if pow(m, 4, p * p) != (p * p - 1):
            continue
        r = minimal_root_mod_p2(p)
        if r is not None and r == m:
            return p

    return None

solve(110)

# 调用 solve
result = solve(inputs['m'])
print(result)