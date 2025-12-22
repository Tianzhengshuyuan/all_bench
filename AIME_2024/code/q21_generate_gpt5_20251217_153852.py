inputs = {'example_base': 912}

def solve(example_base):
    def count_beautiful(b):
        B = b - 1
        cnt = 0
        for z in range(2, b):
            s = z * (z - 1)
            if s % B != 0:
                continue
            x = s // B
            if 1 <= x <= b - 1 and x <= z:
                y = z - x
                if 0 <= y <= b - 1:
                    cnt += 1
        return cnt

    b = 2
    while True:
        if count_beautiful(b) > 10:
            return b
        b += 1

# 调用 solve
result = solve(inputs['example_base'])
print(result)