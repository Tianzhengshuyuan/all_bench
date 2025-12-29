inputs = {'sum_of_squares': 236}

def solve(sum_of_squares):
    import math
    S = sum_of_squares

    # 9 must be present as unique mode, at least twice
    max_f9 = S // 81
    if max_f9 < 2:
        return None

    def check_and_sum(counts_other, f9):
        # Build list
        items = []
        for v, c in counts_other.items():
            if c > 0:
                items.extend([v] * c)
        items.extend([9] * f9)
        items.sort()
        n = len(items)
        # Median must be an integer not in the list => n must be even and (m1+m2) even; also median not present
        if n % 2 == 1:
            return None
        m1 = items[n // 2 - 1]
        m2 = items[n // 2]
        s = m1 + m2
        if s % 2 != 0:
            return None
        m = s // 2
        if m in set(items):
            return None

        # Verify unique mode is 9
        freq = {}
        for x in items:
            freq[x] = freq.get(x, 0) + 1
        f9_actual = freq.get(9, 0)
        if f9_actual < 2:
            return None
        for v, c in freq.items():
            if v != 9 and c >= f9_actual:
                return None

        # Verify sum of squares matches S (safety)
        if sum(x * x for x in items) != S:
            return None

        return sum(items)

    # Try possible counts of 9
    for f9 in range(2, max_f9 + 1):
        S_rem = S - f9 * 81
        if S_rem <= 0:
            continue

        vmax = int(math.isqrt(S_rem))
        values = [v for v in range(1, vmax + 1) if v != 9]
        squares = {v: v * v for v in values}
        # To keep 9 as unique mode, each other value can appear at most f9-1 times
        max_count_other = f9 - 1

        values_sorted = sorted(values)

        def dfs(idx, rem, counts, total_count_other):
            # pruning: if we already have an odd total length together with f9, we need even -> parity constraint
            # However, parity depends on total_count_other + f9 being even. We'll check at the end anyway.

            if rem == 0:
                # Check result only if total length even
                res = check_and_sum(counts, f9)
                if res is not None:
                    return res
                return None
            if idx == len(values_sorted):
                return None

            v = values_sorted[idx]
            sq = squares[v]
            maxc = min(max_count_other, rem // sq)

            for c in range(maxc, -1, -1):
                if c > 0:
                    counts[v] = c
                else:
                    counts.pop(v, None)
                ans = dfs(idx + 1, rem - c * sq, counts, total_count_other + c)
                if ans is not None:
                    return ans
            counts.pop(v, None)
            return None

        ans = dfs(0, S_rem, {}, 0)
        if ans is not None:
            return ans

    return None

sum_of_squares = 236
solve(sum_of_squares)

# 调用 solve
result = solve(inputs['sum_of_squares'])
print(result)