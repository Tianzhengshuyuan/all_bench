inputs = {'p_power': 2}

def solve(p_power):
    e = int(p_power)

    def is_prime(n):
        if n < 2:
            return False
        if n % 2 == 0:
            return n == 2
        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i += 2
        return True

    def egcd(a, b):
        if b == 0:
            return (abs(a), 1 if a >= 0 else -1, 0)
        g, x1, y1 = egcd(b, a % b)
        return (g, y1, x1 - (a // b) * y1)

    def modinv(a, m):
        a %= m
        g, x, _ = egcd(a, m)
        if g != 1:
            raise ValueError("Inverse does not exist")
        return x % m

    def roots_mod_p(p):
        target = (p - 1) % p
        roots = []
        for x in range(p):
            if pow(x, 4, p) == target:
                roots.append(x)
        return roots

    def lift_root(p, e, r0):
        if e == 1:
            return r0 % p
        r = r0 % p
        modulus = p
        for _ in range(1, e):
            modulus_next = modulus * p
            f_mod = (pow(r, 4, modulus_next) + 1) % modulus_next
            w = f_mod // modulus
            g_mod_p = (4 * pow(r, 3, p)) % p
            inv = modinv(g_mod_p, p)
            t = (-w * inv) % p
            r = (r + t * modulus) % modulus_next
            modulus = modulus_next
        return r % modulus

    def least_prime_with_solution(e):
        p = 2
        while True:
            if is_prime(p):
                if p == 2:
                    if e == 1:
                        return 2
                else:
                    if roots_mod_p(p):
                        return p
            p += 1

    if e <= 0:
        return 1

    p = least_prime_with_solution(e)

    if p == 2:
        return 1

    base_roots = roots_mod_p(p)
    candidates = []
    for r0 in base_roots:
        r = lift_root(p, e, r0)
        if r != 0:
            candidates.append(r)
    if not candidates:
        mod = pow(p, e)
        m = 1
        while True:
            if (pow(m, 4, mod) + 1) % mod == 0:
                return m
            m += 1
    return min(candidates)

solve(2)

# 调用 solve
result = solve(inputs['p_power'])
print(result)