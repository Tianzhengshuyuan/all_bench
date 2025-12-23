inputs = {'white_chips': 25}

from itertools import product

def solve(white_chips):
    n = 5
    black_chips = 25  # fixed by problem statement

    def is_maximal(Rw, Cw):
        # Build grid: 'W' at Rw∩Cw, 'B' at Rc∩Cc, None elsewhere
        grid = [[None]*n for _ in range(n)]
        Rw_set, Cw_set = set(Rw), set(Cw)
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
                    # Check placing white at (i,j)
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
                    # Check placing black at (i,j)
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
    rows = range(n)
    cols = range(n)
    # Enumerate all choices of white-rows and white-columns
    for row_mask in range(1 << n):
        Rw = [i for i in rows if (row_mask >> i) & 1]
        for col_mask in range(1 << n):
            Cw = [j for j in cols if (col_mask >> j) & 1]
            whites = len(Rw) * len(Cw)
            blacks = (n - len(Rw)) * (n - len(Cw))
            if whites > white_chips or blacks > black_chips:
                continue
            if is_maximal(Rw, Cw):
                ans += 1
    return ans

solve(25)

# 调用 solve
result = solve(inputs['white_chips'])
print(result)