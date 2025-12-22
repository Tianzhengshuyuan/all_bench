inputs = {'size': 5}

def solve(size: int) -> int:
    from math import comb

    n = size
    if n <= 0:
        return 0

    max_each_color = 25  # fixed by the problem statement

    total = 0
    for a in range(n + 1):  # number of white rows
        for b in range(n + 1):  # number of white columns
            has_white_row = a > 0
            has_black_row = a < n
            has_white_col = b > 0
            has_black_col = b < n

            # Valid-maximal iff the presence of colors matches between rows and columns
            if (has_white_row != has_white_col) or (has_black_row != has_black_col):
                continue

            # Chips used
            white = a * b
            black = (n - a) * (n - b)

            # Respect chip availability: at most 25 of each color
            if white <= max_each_color and black <= max_each_color:
                total += comb(n, a) * comb(n, b)

    return total

# 调用 solve
result = solve(inputs['size'])
print(result)