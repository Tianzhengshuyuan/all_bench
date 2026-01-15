inputs = {'num_triples': 601}

def solve(num_triples):
    S = 6000000

    # Fast path: if solutions count matches the T=0 pattern (2N+1) and T=0 holds, return N
    if (num_triples - 1) % 2 == 0:
        N_candidate = (num_triples - 1) // 2
        if 2 * (N_candidate ** 3) == 9 * S:
            return N_candidate

    import math

    def count_solutions_for_N(N):
        cnt = 0
        for a in range(N + 1):
            A = 3 * a - N
            B = N * N - 4 * a * N + 3 * a * a
            C = N * N * a - N * a * a - S

            if A == 0:
                if B == 0:
                    if C == 0:
                        # Any b in [0, N - a] works
                        cnt += (N - a + 1)
                else:
                    num = -C
                    den = B
                    if den != 0 and num % den == 0:
                        b = num // den
                        if 0 <= b <= N - a:
                            cnt += 1
                continue

            D = B * B - 4 * A * C
            if D < 0:
                continue
            d = math.isqrt(D)
            if d * d != D:
                continue

            if D == 0:
                num = -B
                den = 2 * A
                if den != 0 and num % den == 0:
                    b = num // den
                    if 0 <= b <= N - a:
                        cnt += 1
            else:
                for sign in (1, -1):
                    num = -B + sign * d
                    den = 2 * A
                    if den != 0 and num % den == 0:
                        b = num // den
                        if 0 <= b <= N - a:
                            cnt += 1
        return cnt

    # Fallback search around the natural scale N0 ~ cube_root(9S/2)
    N0 = int(round(((9 * S) / 2) ** (1 / 3)))
    R = 2000
    low = max(0, N0 - R)
    high = N0 + R
    for N in range(low, high + 1):
        if count_solutions_for_N(N) == num_triples:
            return N

    # If not found, broaden search progressively (safety net)
    step = 2000
    for k in range(1, 6):
        low = max(0, N0 - R - k * step)
        high = N0 + R + k * step
        for N in range(low, high + 1):
            if count_solutions_for_N(N) == num_triples:
                return N

    return None

solve(num_triples)

# 调用 solve
result = solve(inputs['num_triples'])
print(result)