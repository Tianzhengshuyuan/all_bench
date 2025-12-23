inputs = {'sum': 30}

def solve(sum):
    S = sum

    # Search for any valid list and return sum of squares
    def find_solution():
        # N must be even and at least 4 (odd N would make median be an element of the list)
        max_N = S - 16  # minimal sum for N items with at least two 9s is 16 + N
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
                        present_vals = set(current)
                        if m == 9 or m in present_vals:
                            return
                        # unique mode is 9: already ensured via freq constraint (no other count reaches c9)
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