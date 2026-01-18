inputs = {'total_sum': 30}

def solve(total_sum):
    S = total_sum

    def make_side_solver(values, max_per_value):
        vals = tuple(values)
        nvals = len(vals)

        from functools import lru_cache

        @lru_cache(maxsize=None)
        def rec(i, cnt_needed, sum_needed):
            if i == nvals:
                if cnt_needed == 0 and sum_needed == 0:
                    return ()
                return None
            v = vals[i]
            # Bound k by available count and sum
            k_max = min(max_per_value, cnt_needed, sum_needed // v if v > 0 else 0)
            # Remaining value bounds
            if i + 1 < nvals:
                min_rem = vals[i + 1]
                max_rem = vals[-1]
            else:
                min_rem = None
                max_rem = None
            for k in range(k_max, -1, -1):
                rem_cnt = cnt_needed - k
                rem_sum = sum_needed - k * v
                if rem_cnt == 0:
                    if rem_sum == 0:
                        rest = ()
                        return (k,) + rest
                    continue
                if rem_sum < 0:
                    continue
                if i + 1 == nvals:
                    continue
                # Prune by coarse bounds
                if rem_sum < rem_cnt * min_rem:
                    continue
                if rem_sum > rem_cnt * max_rem:
                    continue
                rest = rec(i + 1, rem_cnt, rem_sum)
                if rest is not None:
                    return (k,) + rest
            return None

        def solve_counts(cnt_needed, sum_needed):
            return rec(0, cnt_needed, sum_needed)

        def counts_sq(counts):
            if counts is None:
                return None
            total = 0
            for v, k in zip(vals, counts):
                if k:
                    total += k * (v * v)
            return total

        return solve_counts, counts_sq

    # Try both scenarios: 9 on right (s <= 9) and 9 on left (t >= 9)
    for c9 in range(2, S // 9 + 1):
        max_per_value = c9 - 1

        # Scenario B: 9 on right, so s <= 9
        for s in range(2, min(9, S) + 1):
            for t in range(s - 2, 0, -2):
                h_max = (S - c9 * (9 - s)) // (s + 1)
                if h_max < c9:
                    continue
                left_vals = tuple(range(1, t + 1))
                right_vals = tuple(v for v in range(s, S + 1) if v != 9)
                capL = len(left_vals) * max_per_value
                capR = len(right_vals) * max_per_value
                solve_left, left_sq = make_side_solver(left_vals, max_per_value)
                solve_right, right_sq = make_side_solver(right_vals, max_per_value)
                S_rem = S - 9 * c9
                for h in range(c9, h_max + 1):
                    L_need = h
                    R_need = h - c9
                    if L_need > capL or R_need > capR:
                        continue
                    if left_vals:
                        L_min_coarse = L_need * left_vals[0]
                        L_max_coarse = L_need * left_vals[-1]
                    else:
                        if L_need != 0:
                            continue
                        L_min_coarse = 0
                        L_max_coarse = 0
                    if right_vals:
                        R_min_coarse = R_need * s
                        R_max_coarse = R_need * right_vals[-1]
                    else:
                        if R_need != 0:
                            continue
                        R_min_coarse = 0
                        R_max_coarse = 0
                    L_low = max(L_min_coarse, S_rem - R_max_coarse)
                    L_high = min(L_max_coarse, S_rem - R_min_coarse)
                    if L_low > L_high:
                        continue
                    # Try feasible left sums
                    for L_sum in range(L_low, L_high + 1):
                        left_counts = solve_left(L_need, L_sum)
                        if left_counts is None:
                            continue
                        R_sum = S_rem - L_sum
                        right_counts = solve_right(R_need, R_sum)
                        if right_counts is None:
                            continue
                        # Build sum of squares
                        total_sq = c9 * (9 * 9)
                        total_sq += left_sq(left_counts)
                        total_sq += right_sq(right_counts)
                        return total_sq

        # Scenario A: 9 on left, so t >= 9
        for t in range(9, S - 1):
            for s in range(t + 2, S + 1, 2):
                h_max = (S - 8 * c9) // (s + 1)
                if h_max < c9:
                    continue
                left_vals = tuple(v for v in range(1, t + 1) if v != 9)
                right_vals = tuple(range(s, S + 1))
                capL = len(left_vals) * max_per_value
                capR = len(right_vals) * max_per_value
                solve_left, left_sq = make_side_solver(left_vals, max_per_value)
                solve_right, right_sq = make_side_solver(right_vals, max_per_value)
                S_rem = S - 9 * c9
                for h in range(c9, h_max + 1):
                    L_need = h - c9
                    R_need = h
                    if L_need < 0:
                        continue
                    if L_need > capL or R_need > capR:
                        continue
                    if left_vals:
                        L_min_coarse = L_need * left_vals[0]
                        L_max_coarse = L_need * left_vals[-1]
                    else:
                        if L_need != 0:
                            continue
                        L_min_coarse = 0
                        L_max_coarse = 0
                    if right_vals:
                        R_min_coarse = R_need * s
                        R_max_coarse = R_need * right_vals[-1]
                    else:
                        if R_need != 0:
                            continue
                        R_min_coarse = 0
                        R_max_coarse = 0
                    # We need L_sum + R_sum = S_rem, R_sum in [R_min_coarse, R_max_coarse]
                    L_low = max(L_min_coarse, S_rem - R_max_coarse)
                    L_high = min(L_max_coarse, S_rem - R_min_coarse)
                    if L_low > L_high:
                        continue
                    for L_sum in range(L_low, L_high + 1):
                        left_counts = solve_left(L_need, L_sum)
                        if left_counts is None:
                            continue
                        R_sum = S_rem - L_sum
                        right_counts = solve_right(R_need, R_sum)
                        if right_counts is None:
                            continue
                        total_sq = c9 * (9 * 9)
                        total_sq += left_sq(left_counts)
                        total_sq += right_sq(right_counts)
                        return total_sq
    return None

solve(total_sum)

# 调用 solve
result = solve(inputs['total_sum'])
print(result)