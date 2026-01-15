inputs = {'total_sum': 30}

def solve(total_sum):
    def find_solution():
        # iterate over even lengths
        for n in range(2, total_sum + 1, 2):
            # number of 9s (unique mode count >= 2)
            max_c9 = min(n, total_sum // 9)
            for c9 in range(2, max_c9 + 1):
                k = n - c9  # number of non-9 elements
                sum_remaining = total_sum - 9 * c9
                if k == 0:
                    continue  # all 9s -> median would be 9 (appears), invalid
                if sum_remaining < k:
                    continue  # cannot fill k positive integers
                # backtrack to build nondecreasing sequence of non-9 positives summing to sum_remaining
                res = []

                counts = {}
                limit_count = c9 - 1  # any other value count cannot reach c9

                found = [None]  # mutable holder to break out early

                def backtrack(idx, last, s_left):
                    if found[0] is not None:
                        return
                    if idx == k:
                        if s_left == 0:
                            # build full list and check median condition
                            arr = res + [9] * c9
                            arr.sort()
                            m1 = arr[n // 2 - 1]
                            m2 = arr[n // 2]
                            if (m1 + m2) % 2 != 0:
                                return
                            median_val = (m1 + m2) // 2
                            if median_val <= 0:
                                return
                            if median_val in arr:
                                return
                            # passed all checks -> compute sum of squares and store
                            found[0] = sum(x * x for x in arr)
                        return
                    # choose next value v >= last, v != 9
                    max_v = s_left // (k - idx)
                    v = last
                    while v <= max_v:
                        if v != 9:
                            cnt = counts.get(v, 0)
                            if cnt + 1 <= limit_count:
                                res.append(v)
                                counts[v] = cnt + 1
                                backtrack(idx + 1, v, s_left - v)
                                res.pop()
                                if counts[v] == 1:
                                    del counts[v]
                                else:
                                    counts[v] -= 1
                        v += 1

                backtrack(0, 1, sum_remaining)
                if found[0] is not None:
                    return found[0]
        return None

    return find_solution()

total_sum = 30
solve(total_sum)

# 调用 solve
result = solve(inputs['total_sum'])
print(result)