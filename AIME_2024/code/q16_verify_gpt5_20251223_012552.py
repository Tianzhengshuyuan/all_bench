inputs = {'power': 4}

def solve(power):
    def is_prime(n):
        if n < 2:
            return False
        if n % 2 == 0:
            return n == 2
        d = 3
        while d * d <= n:
            if n % d == 0:
                return False
            d += 2
        return True

    def prime_generator():
        yield 2
        p = 3
        while True:
            if is_prime(p):
                yield p
            p += 2

    def invmod(a, m):
        a %= m
        if a == 0:
            return None
        r0, r1 = m, a
        s0, s1 = 0, 1
        while r1:
            q = r0 // r1
            r0, r1 = r1, r0 - q * r1
            s0, s1 = s1, s0 - q * s1
        if r0 != 1:
            return None
        return s0 % m

    k = int(power)
    if k <= 0:
        return None

    for p in prime_generator():
        p2 = p * p
        target_mod_p = (p - 1) % p  # -1 mod p
        roots_mod_p = []
        for a in range(p):
            if pow(a, k, p) == target_mod_p:
                roots_mod_p.append(a)
        if not roots_mod_p:
            continue

        solutions = []
        for a in roots_mod_p:
            r = pow(a, k, p2)
            s = ((r + 1) // p) % p  # (r+1)/p modulo p
            coef = (k * pow(a, k - 1, p)) % p if k >= 1 else 0
            if coef % p != 0:
                inv = invmod(coef, p)
                if inv is None:
                    continue
                t = (-s * inv) % p
                b = (a + t * p) % p2
                if b != 0 and pow(b, k, p2) == p2 - 1:
                    solutions.append(b)
            else:
                if (r + 1) % p2 == 0:
                    b = a % p2
                    if b != 0:
                        solutions.append(b)

        if solutions:
            return min(solutions)

    return None

solve(4)

# 调用 solve
result = solve(inputs['power'])
print(result)