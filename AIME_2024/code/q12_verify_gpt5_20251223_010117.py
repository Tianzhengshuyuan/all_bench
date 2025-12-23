inputs = {'row_sum': 999}

def solve(row_sum):
    S = int(row_sum)
    if S < 0 or S > 1998:
        return 0
    s0 = S % 10
    s1 = (S // 10) % 10
    s2 = (S // 100) % 10
    s3 = (S // 1000) % 10
    if s3 not in (0, 1):
        return 0
    s012 = s0 + s1 + s2
    if s012 % 9 != 0:
        return 0
    E = (99 - s012) // 9
    total = 0
    for k1 in (0, 1):
        T0 = s0 + 10 * k1
        if T0 > 18:
            continue
        for k2 in (0, 1):
            T1 = s1 + 10 * k2 - k1
            if T1 < 0 or T1 > 18:
                continue
            k3 = s3
            T2 = s2 + 10 * k3 - k2
            if T2 < 0 or T2 > 18:
                continue
            C = k1 + k2 + k3
            x1 = E - C
            Tsum = T0 + T1 + T2
            x2 = Tsum - x1
            if not (0 <= x1 <= 27 and 0 <= x2 <= 27):
                continue
            L0, U0 = max(0, T0 - 9), min(9, T0)
            L1, U1 = max(0, T1 - 9), min(9, T1)
            L2, U2 = max(0, T2 - 9), min(9, T2)
            cnt = 0
            for a in range(L2, U2 + 1):
                for b in range(L1, U1 + 1):
                    c = x1 - a - b
                    if L0 <= c <= U0:
                        cnt += 1
            total += cnt
    return total

if 'row_sum' in globals():
    solve(row_sum)

# 调用 solve
result = solve(inputs['row_sum'])
print(result)