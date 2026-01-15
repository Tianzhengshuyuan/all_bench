inputs = {'sum': 30}

def solve(sum):
    S = sum
    min_ssq = None

    for n in range(2, S + 1, 2):
        for c9 in range(2, n):
            m = n - c9
            R = S - 9 * c9
            if m <= 0:
                continue
            if R <= 0:
                continue
            if R < m:
                continue

            others = []

            def backtrack(start_val, remaining_positions, remaining_sum, last_val, last_count):
                nonlocal min_ssq
                if remaining_positions == 0:
                    if remaining_sum == 0:
                        all_values = others + [9] * c9
                        all_values.sort()
                        nn = len(all_values)
                        if nn != n:
                            return
                        mid1 = all_values[nn // 2 - 1]
                        mid2 = all_values[nn // 2]
                        s_mid = mid1 + mid2
                        if s_mid % 2 != 0:
                            return
                        median = s_mid // 2
                        if median in set(all_values):
                            return
                        count_map = {}
                        for v in all_values:
                            count_map[v] = count_map.get(v, 0) + 1
                        max_freq = 0
                        max_freq_values = []
                        for v, c in count_map.items():
                            if c > max_freq:
                                max_freq = c
                                max_freq_values = [v]
                            elif c == max_freq:
                                max_freq_values.append(v)
                        if not (max_freq == c9 and max_freq_values == [9]):
                            return
                        ssq = 0
                        for v in all_values:
                            ssq += v * v
                        if (min_ssq is None) or (ssq < min_ssq):
                            min_ssq = ssq
                    return
                if remaining_sum < remaining_positions:
                    return
                max_v = remaining_sum - (remaining_positions - 1) * 1
                v = max(1, start_val)
                while v <= max_v:
                    if v == 9:
                        v += 1
                        continue
                    if v == last_val:
                        if last_count + 1 >= c9:
                            v += 1
                            continue
                        new_last_count = last_count + 1
                    else:
                        new_last_count = 1
                    others.append(v)
                    backtrack(v, remaining_positions - 1, remaining_sum - v, v, new_last_count)
                    others.pop()
                    v += 1

            backtrack(1, m, R, None, 0)
    return min_ssq

solve(30)

# 调用 solve
result = solve(inputs['sum'])
print(result)