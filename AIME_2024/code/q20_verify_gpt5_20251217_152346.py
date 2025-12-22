inputs = {'size': 5}

def solve(size: int) -> int:
    n = size
    if n <= 0:
        return 0

    total = 0

    # Enumerate all assignments of colors to rows and columns: 0 = black, 1 = white
    # Build the maximal candidate board by filling exactly equal-color intersections.
    # Then verify maximality directly: no empty cell can accept any chip color without
    # violating row/column uniformity. Also ensure no row/column is empty (else not maximal).
    from itertools import product

    for rows in product((0, 1), repeat=n):
        for cols in product((0, 1), repeat=n):
            # Build board: -1 empty, 0 black, 1 white
            board = [[-1] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    if rows[i] == cols[j]:
                        board[i][j] = rows[i]

            # Check that every row and column is nonempty (else we could add a chip)
            ok = True
            for i in range(n):
                if all(board[i][j] == -1 for j in range(n)):
                    ok = False
                    break
            if not ok:
                continue
            for j in range(n):
                if all(board[i][j] == -1 for i in range(n)):
                    ok = False
                    break
            if not ok:
                continue

            # Determine row/column colors (since nonempty, they are well-defined)
            row_color = [None] * n
            col_color = [None] * n
            for i in range(n):
                for j in range(n):
                    if board[i][j] != -1:
                        row_color[i] = board[i][j]
                        break
            for j in range(n):
                for i in range(n):
                    if board[i][j] != -1:
                        col_color[j] = board[i][j]
                        break

            # Maximality: no empty cell admits any chip without breaking uniformity
            maximal = True
            for i in range(n):
                for j in range(n):
                    if board[i][j] == -1:
                        allowed = {0, 1}
                        if row_color[i] is not None:
                            allowed &= {row_color[i]}
                        if col_color[j] is not None:
                            allowed &= {col_color[j]}
                        if allowed:
                            maximal = False
                            break
                if not maximal:
                    break
            if not maximal:
                continue

            total += 1

    return total

# 调用 solve
result = solve(inputs['size'])
print(result)