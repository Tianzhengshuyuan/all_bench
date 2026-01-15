inputs = {'white_count': 25}

def solve(white_count):
    from math import comb
    n = 5
    black_count = 25
    total = 0
    for rW in range(n + 1):
        for cW in range(n + 1):
            # Structural validity for maximality (no empty rows/columns)
            if not ((rW == 0 and cW == 0) or (rW == n and cW == n) or (0 < rW < n and 0 < cW < n)):
                continue
            white_needed = rW * cW
            black_needed = (n - rW) * (n - cW)
            if white_needed <= white_count and black_needed <= black_count:
                total += comb(n, rW) * comb(n, cW)
    return total

solve(white_count)

# 调用 solve
result = solve(inputs['white_count'])
print(result)