inputs = {}

def solve(_):
    def property_holds(n):
        s = list(f"{n:04d}")
        for i in range(4):
            t = s.copy()
            t[i] = '1'
            m = int(''.join(t))
            if m % 7 != 0:
                return False
        return True

    for n in range(9999, 999, -1):
        if property_holds(n):
            q = n // 1000
            r = n % 1000
            return q + r
    return None

# 调用 solve
result = solve(inputs)
print(result)