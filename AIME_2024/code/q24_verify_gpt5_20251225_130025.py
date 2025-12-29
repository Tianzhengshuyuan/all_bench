inputs = {'sum_of_squares': 236}

def solve(sum_of_squares):
    from collections import Counter

    T = sum_of_squares
    results = set()

    # count of 9s must be at least 2 for 9 to be unique mode
    max_k = T // 81
    for k in range(2, max_k + 1):
        rem = T - 81 * k
        if rem < 0:
            break

        other = []

        def dfs(val, rem_sq):
            if rem_sq == 0:
                L = other + [9] * k
                L.sort()
                n = len(L)
                if n % 2 == 1:
                    return
                m1 = L[n // 2 - 1]
                m2 = L[n // 2]
                if (m1 + m2) % 2 != 0:
                    return
                m = (m1 + m2) // 2
                cnt = Counter(L)
                # 9 must be unique mode
                if cnt[9] <= max((c for v, c in cnt.items() if v != 9), default=0):
                    return
                # median must not appear in the list
                if m in cnt:
                    return
                results.add(sum(L))
                return

            max_v = int(rem_sq ** 0.5)
            if val > max_v:
                return

            if val == 9:
                dfs(val + 1, rem_sq)
                return

            max_mult = min(k - 1, rem_sq // (val * val))
            for mult in range(0, max_mult + 1):
                if mult > 0:
                    other.extend([val] * mult)
                dfs(val + 1, rem_sq - mult * (val * val))
                if mult > 0:
                    del other[-mult:]

        dfs(1, rem)

    if len(results) == 1:
        return results.pop()
    elif len(results) > 1:
        return min(results)
    else:
        return None

solve(236)

# 调用 solve
result = solve(inputs['sum_of_squares'])
print(result)