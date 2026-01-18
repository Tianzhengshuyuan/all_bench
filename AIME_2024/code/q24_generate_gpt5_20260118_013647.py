inputs = {'total_sum': 36}

def solve(total_sum):
    S = total_sum

    for c9 in range(2, S // 9 + 1):
        rem_sum = S - 9 * c9
        if rem_sum < 0:
            break
        max_per = c9 - 1
        result = None
        arr = []

        def rec(v, rem):
            nonlocal result
            if result is not None:
                return
            if rem == 0:
                final_list = sorted(arr + [9] * c9)
                n = len(final_list)
                if n % 2 == 1:
                    return
                a = final_list[n // 2 - 1]
                b = final_list[n // 2]
                if (a + b) % 2 != 0:
                    return
                m = (a + b) // 2
                # median must not be in the list
                for x in final_list:
                    if x == m:
                        return
                result = sum(x * x for x in final_list)
                return
            if v > rem:
                return
            if v == 9:
                rec(v + 1, rem)
                return
            k_max = min(max_per, rem // v)
            for k in range(k_max, -1, -1):
                if result is not None:
                    return
                if k > 0:
                    arr.extend([v] * k)
                    rec(v + 1, rem - k * v)
                    del arr[-k:]
                else:
                    rec(v + 1, rem)

        rec(1, rem_sum)
        if result is not None:
            return result
    return None

total_sum = 30
solve(total_sum)

# 调用 solve
result = solve(inputs['total_sum'])
print(result)