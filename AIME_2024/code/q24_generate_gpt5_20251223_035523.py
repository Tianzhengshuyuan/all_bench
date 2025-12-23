inputs = {'sum': 138}

def solve(sum):
    # Safely coerce input to integer; fallback to 30 if a non-numeric (e.g., built-in sum) is passed
    S = None
    try:
        if isinstance(sum, (int,)):
            S = sum
        elif isinstance(sum, float):
            S = int(sum)
        elif isinstance(sum, str):
            S = int(sum.strip())
    except Exception:
        pass
    if S is None:
        S = 30  # fallback to the intended problem value

    def find_solution():
        # N must be even and at least 4 (odd N would make median appear in the list)
        max_N = S - 16  # minimal sum for N items with at least two 9s is N + 16
        if max_N < 4:
            return None

        for N in range(4, max_N + 1, 2):
            for c9 in range(2, N):  # at least two 9s; not all 9s
                r = N - c9
                S_rem = S - 9 * c9
                if r <= 0:
                    continue
                # minimal sum for r positive integers is r
                if S_rem < r:
                    continue

                freq = {}
                current = []
                found = [None]  # holder to allow early exit from recursion

                def rec(start, left_cnt, left_sum):
                    if found[0] is not None:
                        return
                    if left_cnt == 0:
                        if left_sum != 0:
                            return
                        # Build full sorted list and test median condition
                        full = current + [9] * c9
                        full.sort()
                        k = N // 2
                        a = full[k - 1]
                        b = full[k]
                        s2 = a + b
                        if s2 % 2 != 0:
                            return
                        m = s2 // 2
                        # median must not be in the list
                        if m == 9 or m in set(current):
                            return
                        # compute sum of squares
                        sq = c9 * 81
                        for v in current:
                            sq += v * v
                        found[0] = sq
                        return

                    # prune bounds
                    min_v = start
                    max_v = left_sum - (left_cnt - 1)  # ensure at least 1 for remaining
                    if min_v > max_v:
                        return

                    for v in range(min_v, max_v + 1):
                        if v == 9:
                            continue
                        # unique mode: no other value can reach count c9
                        fv = freq.get(v, 0)
                        if fv + 1 >= c9:
                            continue
                        freq[v] = fv + 1
                        current.append(v)
                        rec(v, left_cnt - 1, left_sum - v)
                        current.pop()
                        if fv == 0:
                            del freq[v]
                        else:
                            freq[v] = fv
                        if found[0] is not None:
                            return

                rec(1, r, S_rem)
                if found[0] is not None:
                    return found[0]
        return None

    ans = find_solution()
    return ans

solve(sum)

# 调用 solve
result = solve(inputs['sum'])
print(result)