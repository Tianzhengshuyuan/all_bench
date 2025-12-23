inputs = {'exponent': 4}

def solve(exponent):
    def is_prime(n):
        if n < 2:
            return False
        if n % 2 == 0:
            return n == 2
        i = 3
        r = int(n**0.5)
        while i <= r:
            if n % i == 0:
                return False
            i += 2
        return True

    def prime_iter():
        n = 2
        while True:
            if is_prime(n):
                yield n
            n += 1 if n == 2 else 2

    def inv_mod(a, m):
        a %= m
        if a == 0:
            return None
        t, newt = 0, 1
        r, newr = m, a
        while newr != 0:
            q = r // newr
            t, newt = newt, t - q * newt
            r, newr = newr, r - q * newr
        if r != 1:
            return None
        return t % m

    e = exponent
    for p in prime_iter():
        p2 = p * p
        target_mod_p = (p - 1) % p
        roots_mod_p = [r for r in range(p) if pow(r, e, p) == target_mod_p]
        if not roots_mod_p:
            continue

        best = None
        if e % p != 0:
            for r in roots_mod_p:
                d = (e % p) * pow(r % p, e - 1, p) % p
                if d == 0:
                    # Fallback to brute lift if derivative vanishes unexpectedly
                    for k in range(p):
                        x = r + k * p
                        if pow(x, e, p2) == p2 - 1:
                            if best is None or x < best:
                                best = x
                            break
                    continue
                f_mod_p2 = (pow(r, e, p2) + 1) % p2
                a = (f_mod_p2 // p) % p
                invd = inv_mod(d, p)
                if invd is None:
                    continue
                t = (-a * invd) % p
                x = (r + t * p) % p2
                if pow(x, e, p2) == p2 - 1:
                    if best is None or x < best:
                        best = x
        else:
            # p | e, use brute-force lift over k in [0, p-1]
            for r in roots_mod_p:
                for k in range(p):
                    x = r + k * p
                    if pow(x, e, p2) == p2 - 1:
                        if best is None or x < best:
                            best = x
                        break

        if best is not None and best != 0:
            return best

solve(4)

# 调用 solve
result = solve(inputs['exponent'])
print(result)