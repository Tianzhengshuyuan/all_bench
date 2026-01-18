inputs = {'power': 4}

def solve(power):
    from math import gcd

    def v2(n):
        c = 0
        while n % 2 == 0:
            n //= 2
            c += 1
        return c

    def mr_pow(a, d, n):
        r = 1
        while d:
            if d & 1:
                r = (r * a) % n
            a = (a * a) % n
            d >>= 1
        return r

    def is_prime(n):
        if n < 2:
            return False
        small_primes = [2, 3, 5, 7, 11, 13, 17]
        for p in small_primes:
            if n % p == 0:
                return n == p
        # write n-1 = d * 2^s
        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1
        for a in small_primes:
            if a % n == 0:
                continue
            x = mr_pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            skip = False
            for _ in range(s - 1):
                x = (x * x) % n
                if x == n - 1:
                    skip = True
                    break
            if skip:
                continue
            return False
        return True

    def prime_factors(n):
        pf = []
        if n % 2 == 0:
            pf.append(2)
            while n % 2 == 0:
                n //= 2
        f = 3
        while f * f <= n:
            if n % f == 0:
                pf.append(f)
                while n % f == 0:
                    n //= f
            f += 2
        if n > 1:
            pf.append(n)
        return pf

    def egcd(a, b):
        if b == 0:
            return (a, 1, 0)
        g, x1, y1 = egcd(b, a % b)
        return (g, y1, x1 - (a // b) * y1)

    def inv_mod(a, m):
        g, x, _ = egcd(a, m)
        if g != 1:
            return None
        return x % m

    def find_prime_with_v2_gt(s):
        step = 1 << (s + 1)
        t = 1
        while True:
            p = t * step + 1
            if is_prime(p):
                return p
            t += 1

    def primitive_root_mod_p2(p):
        # find primitive root modulo p
        pf = prime_factors(p - 1)
        g = None
        a = 2
        while a < p:
            ok = True
            for q in pf:
                if pow(a, (p - 1) // q, p) == 1:
                    ok = False
                    break
            if ok:
                # check lift to p^2
                if pow(a, p - 1, p * p) != 1:
                    g = a
                    break
            a += 1
        if g is None:
            # fallback (should rarely happen): search directly for order p(p-1)
            M = p * p
            T = p * (p - 1)
            pf_T = set(pf + [p])
            a = 2
            while True:
                if a % p != 0:
                    ok = True
                    for r in pf_T:
                        if pow(a, T // r, M) == 1:
                            ok = False
                            break
                    if ok:
                        g = a
                        break
                a += 1
        return g

    k = power
    if k <= 0:
        return None  # undefined for non-positive power in this context

    # If k is odd, p=2 works and minimal m is 3 (since 3^k + 1 ≡ 0 mod 4 for odd k)
    if k % 2 == 1:
        return 3

    # k even: find least odd prime p with v2(p-1) > v2(k)
    s = v2(k)
    p = find_prime_with_v2_gt(s)

    M = p * p
    T = p * (p - 1)

    # Find a primitive root modulo p^2
    g = primitive_root_mod_p2(p)

    # Solve k * a ≡ T/2 (mod T)
    d = gcd(k, T)
    # Existence guaranteed by choice of p, but guard anyway
    if (T // d) % 2 == 1:
        return None

    N = T // d
    b = T // 2
    k1 = k // d
    b1 = b // d
    inv_k1 = inv_mod(k1 % N, N)
    a0 = (b1 * inv_k1) % N

    # Enumerate all d solutions and select minimal residue
    best = None
    for t in range(d):
        a_exp = a0 + t * N
        x = pow(g, a_exp, M)
        if best is None or x < best:
            best = x

    return best

# 调用 solve
result = solve(inputs['power'])
print(result)