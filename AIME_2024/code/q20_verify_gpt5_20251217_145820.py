inputs = {'size': 5}

def solve(size: int) -> int:
    n = size
    if n <= 0:
        return 0

    # Enumerate all choices of white-row set (rw) and white-column set (cw).
    # Fill exactly the cells where row-color == column-color:
    # - white at RW x CW
    # - black at (complement RW) x (complement CW)
    #
    # Then enforce:
    # - every row and every column is nonempty (else we could add a chip)
    # - maximality: for every empty cell, adding a chip of either color would
    #   break row or column uniformity (so no empty equality cells remain).
    #
    # Deduplicate by the actual colored board pattern to be safe.
    seen = set()
    total = 0

    for rw in range(1 << n):
        for cw in range(1 << n):
            # Build board: -1 empty, 1 white, 0 black
            board = [[-1] * n for _ in range(n)]
            for i in range(n):
                r_white = (rw >> i) & 1
                for j in range(n):
                    c_white = (cw >> j) & 1
                    if r_white == c_white:
                        board[i][j] = 1 if r_white == 1 else 0

            # Check each row/column nonempty and uniform; record their colors
            row_color = [-1] * n
            col_color = [-1] * n

            ok = True
            for i in range(n):
                colors = {board[i][j] for j in range(n) if board[i][j] != -1}
                if not colors or len(colors) > 1:
                    ok = False
                    break
                row_color[i] = next(iter(colors))
            if not ok:
                continue

            for j in range(n):
                colors = {board[i][j] for i in range(n) if board[i][j] != -1}
                if not colors or len(colors) > 1:
                    ok = False
                    break
                col_color[j] = next(iter(colors))
            if not ok:
                continue

            # Maximality: no empty cell can accept a chip without violating uniformity
            maximal = True
            for i in range(n):
                for j in range(n):
                    if board[i][j] == -1:
                        can_white = (row_color[i] == 1) and (col_color[j] == 1)
                        can_black = (row_color[i] == 0) and (col_color[j] == 0)
                        if can_white or can_black:
                            maximal = False
                            break
                if not maximal:
                    break
            if not maximal:
                continue

            key = tuple(tuple(row) for row in board)
            if key not in seen:
                seen.add(key)
                total += 1

    return total

# 调用 solve
result = solve(inputs['size'])
print(result)