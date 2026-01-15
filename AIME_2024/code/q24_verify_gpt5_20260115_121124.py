inputs = {'total_sum': 30}

def solve(total_sum):
    results = set()

    # Iterate over possible counts of 9's (k >= 2 for unique mode)
    max_k = total_sum // 9
    for k in range(2, max_k + 1):
        S_rest = total_sum - 9 * k
        if S_rest <= 0:
            continue  # Need at least one non-9 positive integer

        # Number of non-9 items is m (must be <= S_rest since all >= 1)
        for m in range(1, S_rest + 1):
            n = k + m
            if n % 2 == 1:
                continue  # median condition implies even length
            if S_rest < m:
                continue  # not enough sum to assign at least 1 to each

            # Generate nondecreasing sequences of length m summing to S_rest,
            # values are positive integers not equal to 9, and multiplicity <= k-1
            def backtrack(pos, remaining_sum, last_v, run_len, arr):
                remain_len = m - pos
                if remain_len == 0:
                    if remaining_sum != 0:
                        return
                    L = arr + [9] * k
                    L.sort()
                    i1 = len(L) // 2 - 1
                    i2 = len(L) // 2
                    a, b = L[i1], L[i2]
                    s = a + b
                    if s % 2 != 0:
                        return
                    med = s // 2
                    if med in set(L):
                        return
                    # Verify unique mode is 9
                    from collections import Counter
                    cnt = Counter(L)
                    c9 = cnt.get(9, 0)
                    if c9 == 0:
                        return
                    if any(c >= c9 for v, c in cnt.items() if v != 9):
                        return
                    results.add(sum(x * x for x in L))
                    return

                min_v = last_v
                max_v = remaining_sum - (remain_len - 1)  # leave at least 1 for each remaining
                if max_v < min_v:
                    return
                for v in range(min_v, max_v + 1):
                    if v == 9 or v < 1:
                        continue
                    new_run = run_len + 1 if v == last_v else 1
                    if new_run > k - 1:
                        continue
                    arr.append(v)
                    backtrack(pos + 1, remaining_sum - v, v, new_run, arr)
                    arr.pop()

            backtrack(0, S_rest, 1, 0, [])

    if len(results) == 1:
        return next(iter(results))
    elif len(results) == 0:
        return None
    else:
        return sorted(results)

solve(30)

# 调用 solve
result = solve(inputs['total_sum'])
print(result)