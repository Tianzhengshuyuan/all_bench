inputs = {'p_power': 4}

def solve(p_power):
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

    e = int(p_power)
    if e <= 0:
        return 1

    p = None
    roots_mod_p = []
    cand = 2
    while True:
        if is_prime(cand):
            if cand == 2:
                if e == 1:
                    p = 2
                    break
            else:
                roots = [a for a in range(cand) if (pow(a, 4, cand) + 1) % cand == 0]
                if roots:
                    p = cand
                    roots_mod_p = roots
                    break
        cand += 1

    if p == 2:
        return 1

    def lift_root(r, p, e):
        x = r % p
        if e == 1:
            return x
        for k in range(1, e):
            mod_k = p ** k
            fx_mod = (pow(x, 4, mod_k * p) + 1) % (mod_k * p)
            b = (fx_mod // mod_k) % p
            d_mod_p = (4 * pow(x % p, 3, p)) % p
            inv_d = pow(d_mod_p, p - 2, p)
            t = (-b * inv_d) % p
            x = x + t * mod_k
        return x % (p ** e)

    lifts = [lift_root(r, p, e) for r in roots_mod_p]
    candidates = [x for x in lifts if x > 0]
    return min(candidates) if candidates else 0

solve(2)

# 调用 solve
result = solve(inputs['p_power'])
print(result)