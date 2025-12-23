inputs = {'white_chips': 25}

def solve(white_chips):
    from math import comb
    n = 5
    supply_white = white_chips
    supply_black = white_chips
    total = 0
    for r in range(n + 1):
        for c in range(n + 1):
            # Maximality forces: r>0 iff c>0 and r<n iff c<n
            if (r == 0) != (c == 0):
                continue
            if (r == n) != (c == n):
                continue
            white_need = r * c
            black_need = (n - r) * (n - c)
            if white_need > supply_white or black_need > supply_black:
                continue
            total += comb(n, r) * comb(n, c)
    return total

solve(white_chips)

# 调用 solve
result = solve(inputs['white_chips'])
print(result)