inputs = {'white_chips': 25}

def solve(white_chips):
    from itertools import combinations

    n = 5
    black_chips = 25  # fixed by problem statement

    rows = list(range(n))
    cols = list(range(n))

    def is_maximal(Rw, Cw):
        # Build grid states: 'W' white, 'B' black, None empty
        grid = [[None] * n for _ in range(n)]
        Rw_set = set(Rw)
        Cw_set = set(Cw)
        for i in range(n):
            for j in range(n):
                if i in Rw_set and j in Cw_set:
                    grid[i][j] = 'W'
                elif i not in Rw_set and j not in Cw_set:
                    grid[i][j] = 'B'
                else:
                    grid[i][j] = None

        # Maximality: no empty cell can accept a chip of any color
        for i in range(n):
            for j in range(n):
                if grid[i][j] is None:
                    # Check if we can place a white chip
                    can_white = True
                    for jj in range(n):
                        if grid[i][jj] == 'B':
                            can_white = False
                            break
                    if can_white:
                        for ii in range(n):
                            if grid[ii][j] == 'B':
                                can_white = False
                                break

                    # Check if we can place a black chip
                    can_black = True
                    for jj in range(n):
                        if grid[i][jj] == 'W':
                            can_black = False
                            break
                    if can_black:
                        for ii in range(n):
                            if grid[ii][j] == 'W':
                                can_black = False
                                break

                    if can_white or can_black:
                        return False
        return True

    ans = 0
    # Enumerate all subsets of rows and columns marked white; others implicitly black
    for r in range(n + 1):
        for Rw in combinations(rows, r):
            for c in range(n + 1):
                for Cw in combinations(cols, c):
                    whites = r * c
                    blacks = (n - r) * (n - c)
                    if whites > white_chips or blacks > black_chips:
                        continue
                    if is_maximal(Rw, Cw):
                        ans += 1
    return ans

solve(25)

# 调用 solve
result = solve(inputs['white_chips'])
print(result)