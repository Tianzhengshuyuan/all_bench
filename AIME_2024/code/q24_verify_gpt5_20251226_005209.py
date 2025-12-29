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
        if n % 2 == 1:
            return None
        m1 = items[n // 2 - 1]
        m2 = items[n // 2]
        s = m1 + m2
        if s % 2 != 0:
            return None
        m = s // 2
        # median must not appear in the list
        present_vals = set(items)
        if m in present_vals:
            return None
        # unique mode is 9 already enforced by construction (counts_other[v] <= f9-1)
        return sum(items)

    for f9 in range(2, max_f9 + 1):
        S_rem = S - f9 * 81
        if S_rem <= 0:
            continue
        vmax = int(math.isqrt(S_rem))
        values = [v for v in range(1, vmax + 1) if v != 9]
        squares = {v: v * v for v in values}
        max_count_other = f9 - 1

        # DFS to find counts for other values such that sum of squares equals S_rem
        values_sorted = sorted(values)

        def dfs(idx, rem, counts):
            if rem == 0:
                # Check result
                res = check_and_sum(counts, f9)
                if res is not None:
                    return res
                return None
            if idx == len(values_sorted):
                return None
            v = values_sorted[idx]
            sq = squares[v]
            maxc = min(max_count_other, rem // sq)
            # try larger counts first to reduce branching depth
            for c in range(maxc, -1, -1):
                if c > 0:
                    counts[v] = c
                else:
                    counts.pop(v, None)
                ans = dfs(idx + 1, rem - c * sq, counts)
                if ans is not None:
                    return ans
            # cleanup
            counts.pop(v, None)
            return None

        ans = dfs(0, S_rem, {})
        if ans is not None:
            return ans

    return None

solve(sum_of_squares)

# 调用 solve
result = solve(inputs['sum_of_squares'])
print(result)