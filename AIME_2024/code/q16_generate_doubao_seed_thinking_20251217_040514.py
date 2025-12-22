inputs = {'exponent_n': 867}

def solve(exponent_n):
    def is_prime(p):
        if p < 2:
            return False
        for i in range(2, int(p**0.5) + 1):
            if p % i == 0:
                return False
        return True

    def find_smallest_prime_1_mod_m(m):
        p = m + 1
        while True:
            if is_prime(p):
                return p
            p += m

    m_val = 2 * exponent_n
    p = find_smallest_prime_1_mod_m(m_val)
    residues = []
    for r in range(p):
        if pow(r, exponent_n, p) == p - 1:
            residues.append(r)
    min_candidate = float('inf')
    p_squared = p * p
    for r in residues:
        s = pow(r, exponent_n, p_squared)
        numerator = s + 1
        c_mod_p = (numerator // p) % p
        A = (exponent_n * pow(r, exponent_n - 1, p)) % p
        inv_A = pow(A, p - 2, p)
        t = (-c_mod_p * inv_A) % p
        candidate = r + t * p
        if candidate < min_candidate:
            min_candidate = candidate
    return min_candidate

# 调用 solve
result = solve(inputs['exponent_n'])
print(result)