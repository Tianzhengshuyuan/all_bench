inputs = {'exponent': 2}

def solve(exponent):
    e = exponent

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

    def primes():
        yield 2
        n = 3
        while True:
            if is_prime(n):
                yield n
            n += 2

    def hensel_lift_root(r, p, e):
        # Lift a root r mod p to a root mod p^e for f(x) = x^4 + 1
        if e == 1:
            return r % p
        x = r % p
        M = p
        for _ in range(1, e):
            modulus_next = M * p
            # Compute (f(x) mod modulus_next), then divide by M to get quotient mod p
            val_mod = (pow(x, 4, modulus_next) + 1) % modulus_next
            q = val_mod // M  # equals (f(x)/M) mod p
            fp = (4 * pow(x % p, 3, p)) % p
            inv_fp = pow(fp, -1, p)
            t = (-q * inv_fp) % p
            x = x + t * M
            M = modulus_next
        return x % M

    # Find the least prime p such that there exists n with p^e | n^4 + 1
    chosen_p = None
    for p in primes():
        if p == 2:
            if e == 1:
                chosen_p = 2
                break
            else:
                continue  # no solutions mod 2^e for e >= 2
        # Check existence of solution modulo p
        has_root = False
        for x in range(1, p):
            if pow(x, 4, p) == (p - 1) % p:
                has_root = True
                break
        if has_root:
            chosen_p = p
            break

    # Now find the least positive integer m such that chosen_p^e | m^4 + 1
    if chosen_p == 2:
        # e == 1 here
        return 1

    p = chosen_p
    residues = [x for x in range(1, p) if pow(x, 4, p) == (p - 1) % p]
    if e == 1:
        return min(residues)
    lifts = [hensel_lift_root(r, p, e) for r in residues]
    return min(lifts)

# 调用 solve
result = solve(inputs['exponent'])
print(result)