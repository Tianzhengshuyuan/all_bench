inputs = {'k': 5}

def solve(k):
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

    def inv_mod(a, m):
        a %= m
        if a == 0:
            return None
        t0, t1 = 0, 1
        r0, r1 = m, a
        while r1:
            q = r0 // r1
            t0, t1 = t1, t0 - q * t1
            r0, r1 = r1, r0 - q * r1
        if r0 != 1:
            return None
        return t0 % m

    p = 2
    while True:
        if p == 2:
            mod = 4
            candidates = []
            for x in range(1, mod):
                if pow(x, k, mod) == mod - 1:
                    candidates.append(x)
            if candidates:
                return min(candidates)
        else:
            pp = p * p
            if gcd(k, p) == 1:
                # -1 is a k-th power modulo p iff ((p-1)/gcd(k,p-1)) is even
                if ((p - 1) // gcd(k, p - 1)) % 2 == 0:
                    roots = []
                    for x in range(1, p):
                        if pow(x, k, p) == p - 1:
                            roots.append(x)
                    if roots:
                        lifts = []
                        for r in roots:
                            # Hensel lift r (mod p) to r2 (mod p^2) for f(x)=x^k+1
                            f_r = (pow(r, k, pp) + 1) % pp
                            A = (f_r // p) % p
                            fp = (k % p) * pow(r % p, k - 1, p) % p
                            inv = inv_mod(fp, p)
                            if inv is None:
                                continue
                            t = (-A * inv) % p
                            r2 = (r + t * p) % pp
                            if r2 == 0:
                                r2 = pp
                            lifts.append(r2)
                        if lifts:
                            return min(lifts)
            else:
                # Rare case: p | k, try direct search modulo p^2
                if ((p - 1) // gcd(k, p - 1)) % 2 == 0:
                    for r in range(1, p):
                        if pow(r, k, pp) == pp - 1:
                            return r
        # next prime
        n = p + 1
        while not is_prime(n):
            n += 1
        p = n

solve(4)

# 调用 solve
result = solve(inputs['k'])
print(result)