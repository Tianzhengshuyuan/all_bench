inputs = {'sum_total': 54}

def solve(sum_total):
    def find_solution():
        # Try even lengths n
        for n in range(2, sum_total + 1, 2):
            # number of 9s is k (unique mode requires k >= 2)
            for k in range(2, n + 1):
                m = n - k  # number of non-9 elements
                if m <= 0:
                    continue
                S = sum_total - 9 * k
                if S < m:  # at least 1 for each non-9 element
                    continue

                ans = [None]
                arr = []
                counts = {}

                def backtrack(idx, rem, last):
                    if ans[0] is not None:
                        return
                    if idx == m:
                        if rem != 0:
                            return
                        L = arr + [9] * k
                        L.sort()
                        mid1 = n // 2 - 1
                        mid2 = n // 2
                        s2 = L[mid1] + L[mid2]
                        if s2 % 2 != 0:
                            return
                        M = s2 // 2
                        if M in L:
                            return
                        # Ensure 9 is the unique mode
                        max_other = 0
                        for v, c in counts.items():
                            if c > max_other:
                                max_other = c
                        if k <= max_other:
                            return
                        ans[0] = sum(x * x for x in L)
                        return

                    remaining_slots = m - idx
                    min_val = last
                    max_val = rem - (remaining_slots - 1) * 1
                    if max_val < min_val:
                        return
                    v = min_val
                    while v <= max_val:
                        if v == 9:
                            v += 1
                            continue
                        c = counts.get(v, 0)
                        if c >= k - 1:
                            v += 1
                            continue
                        arr.append(v)
                        counts[v] = c + 1
                        backtrack(idx + 1, rem - v, v)
                        arr.pop()
                        if c == 0:
                            del counts[v]
                        else:
                            counts[v] = c
                        if ans[0] is not None:
                            return
                        v += 1

                backtrack(0, S, 1)
                if ans[0] is not None:
                    return ans[0]
        return None

    return find_solution()

solve(30)

# 调用 solve
result = solve(inputs['sum_total'])
print(result)