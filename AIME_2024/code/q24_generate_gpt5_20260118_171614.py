inputs = {'total_sum': 27}

def solve(total_sum):
    S = int(total_sum)

    solutions = []

    def enumerate_b(m, k, S_prime):
        # Enumerate nondecreasing sequences b of length m, sum S_prime, excluding 9,
        # and with any value's count <= k-1 (to ensure 9 is unique mode)
        b = []

        def backtrack(i, prev, remaining, last_val, last_count):
            if i == m:
                if remaining != 0:
                    return
                # Evaluate median condition after merging b with k copies of 9
                n = m + k
                p, q = n // 2 - 1, n // 2

                # Determine count of elements < 9 in b (since b excludes 9 and is nondecreasing)
                L = 0
                while L < m and b[L] < 9:
                    L += 1

                def get_val_at(idx):
                    if idx < L:
                        return b[idx]
                    elif idx < L + k:
                        return 9
                    else:
                        return b[idx - (L + k)]

                a_p = get_val_at(p)
                a_q = get_val_at(q)
                M2 = a_p + a_q
                if M2 % 2 != 0:
                    return
                M = M2 // 2
                if M == 9:
                    return
                # M must not be in the list
                # Check against b's values (9 already checked)
                for v in b:
                    if v == M:
                        return

                # Passed all checks; record full list
                full_list = b[:L] + [9] * k + b[L:]
                solutions.append(full_list)
                return

            r = m - i - 1
            max_x = remaining // (r + 1)
            min_x = prev
            if max_x < min_x:
                return

            for x in range(min_x, max_x + 1):
                if x == 9:
                    continue
                if i == 0:
                    new_last_val, new_last_count = x, 1
                else:
                    if x == last_val:
                        if last_count + 1 >= k:  # ensure count(x) <= k-1
                            continue
                        new_last_val, new_last_count = x, last_count + 1
                    else:
                        new_last_val, new_last_count = x, 1
                b.append(x)
                backtrack(i + 1, x, remaining - x, new_last_val, new_last_count)
                b.pop()

        backtrack(0, 1, S_prime, None, 0)

    # Enumerate even lengths n and counts k of 9s
    for n in range(4, S + 1, 2):
        for k in range(2, n + 1):
            m = n - k
            if m <= 0:
                continue
            S_prime = S - 9 * k
            if S_prime < m:  # minimal sum for m positive integers is m
                continue
            enumerate_b(m, k, S_prime)

    if not solutions:
        return None

    # Deduplicate and pick a canonical answer (lexicographically smallest list)
    uniq = []
    seen = set()
    for lst in solutions:
        t = tuple(lst)
        if t not in seen:
            seen.add(t)
            uniq.append(lst)

    uniq.sort()
    chosen = uniq[0]
    return sum(x * x for x in chosen)

# 调用 solve
result = solve(inputs['total_sum'])
print(result)