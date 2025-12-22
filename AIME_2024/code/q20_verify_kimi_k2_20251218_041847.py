inputs = {'n': 25}

from math import comb

def solve(n):
    # n is the side length of the square grid (here n=5)
    # We have n white and n black chips, but we may not use all.
    # We need to count the number of valid placements on an n×n grid satisfying:
    # 1. At most one chip per cell.
    # 2. All chips in the same row have the same color.
    # 3. All chips in the same column have the same color.
    # 4. The placement is maximal: no more chip can be added without violating 1 or 2 or 3.

    # Key insight:
    # Let R be the set of rows that have at least one chip.
    # Let C be the set of columns that have at least one chip.
    # Then every cell in R×C must be filled (otherwise we could add a chip there without violating row/column color constraints).
    # Also, due to row color constraint, all chips in a row of R must be same color.
    # Similarly for columns in C.
    # But then for any row i in R and column j in C, the chip at (i,j) must have the color of row i and also the color of column j.
    # So the color of row i must equal the color of column j for every i in R, j in C.
    # This implies: all rows in R must have the same color, say c_R, and all columns in C must have the same color, say c_C, and we must have c_R = c_C.
    # So the entire subgrid R×C is monochromatic.

    # Moreover, maximality implies:
    # - Every row not in R must be empty (otherwise we could extend R).
    # - Every column not in C must be empty.
    # - Also, we cannot add any chip outside R×C: so for any row i not in R, we cannot add a chip in any column j (even if j in C), because that would force row i to have a color, but then it would conflict with column j's color unless same, but we can't mix.
    # Actually, maximality implies that the occupied cells are exactly R×C, and we cannot add any more.
    # But since rows outside R are empty, and columns outside C are empty, the only possible additions are in (i,j) with i not in R or j not in C.
    # But if we try to add a chip in (i,j) with i not in R, j in C: then row i would have to get a color, but it must match column j's color. But we could do that? However, the problem is: we are to count maximal configurations.
    # But actually, the above reasoning shows that the only possible maximal configurations are:
    #   Choose a non-empty set of rows R (size r), non-empty set of columns C (size c), fill the r×c subgrid, all same color.
    #   But is that maximal? Yes, because:
    #     - Any cell in R×C is full.
    #     - Any cell in row i not in R: if we try to add in column j in C, then row i would have to be assigned color = color of column j, which is okay, but then we could add it — so to prevent that, we must ensure that such an addition would violate? But the condition is: any additional chip would violate.
    #     So to be maximal, we must ensure that we cannot add any chip anywhere.
    #   But we *can* add a chip in (i,j) for i not in R, j in C, *unless* we don't have that color chip available? But the problem allows us to have up to n white and n black, but we are not required to use all.
    #   However, the maximality is about *violating the rules*, not about running out of chips.
    #   So: can we add a chip in (i,j) with i not in R, j in C?
    #     - Cell is empty: okay.
    #     - After adding: row i has one chip, so its color is set to that chip's color.
    #     - Column j already has a color (from the filled subgrid), so the new chip must have that color.
    #     - So we *can* add such a chip, *if* we have one of that color available.
    #   Therefore, to prevent this, we must ensure that we *cannot* add — but the condition is about *would violate*, not about *we don't have chips*.
    #   So: unless such an addition would violate the row/column color constraint, it is allowed — so our configuration is **not** maximal.
    #   Hence, to be maximal, we must ensure that **no such addition is possible without violating the color constraints**.
    #   But the color constraint is only that in a row/column all chips have same color.
    #   So the only way that adding a chip is impossible is if:
    #     - The cell is already occupied (but it's not), or
    #     - The chip we would add has a color that conflicts with the existing row/column color — but since the row is currently empty, it has no color, so no conflict.
    #   Therefore, we **can** always add a chip in any cell (i,j) with i not in R, j in C, as long as we pick the color to match column j's color (and row i gets that color).
    #   Similarly, we can add in (i,j) with i in R, j not in C? No: because row i is already nonempty, so has a color, and column j is empty, so no conflict — we can add a chip of row i's color.
    #   And in (i,j) with i not in R, j not in C: we can add any color, and it sets both.

    # So the **only** way a configuration is maximal is if there are **no empty cells at all**?
    # But that contradicts the "some" in the problem.

    # Wait: but we just saw that **any** configuration that leaves a cell empty and does not have a conflicting color constraint can be extended.
    # The only extension-blockers are:
    #   - Cell occupied → can't extend.
    #   - Row has color A, column has color B, A≠B → can't place any chip in that cell.
    # So: a configuration is **maximal** iff **every empty cell lies in a row and column that already have conflicting colors**.
    # That is: for every empty cell (i,j), either:
    #   - row i is nonempty and has color A
    #   - column j is nonempty and has color B
    #   - A ≠ B
    # Then we cannot place any chip there (because no color works).

    # So we can have empty cells! But only if they are "blocked" by color conflict.

    # Therefore, the general maximal configuration is determined by:
    #   Let R0 = rows that are nonempty → each has a color c_i
    #   Let C0 = columns that are nonempty → each has a color d_j
    #   Then for every cell (i,j) that is empty: we must have c_i ≠ d_j  (if both i,j nonempty)
    #   But also: if row i is nonempty and column j is empty → then we could add a chip of color c_i in (i,j), unless we don't have chips? But again, the rule is about *violating*, not about supply.
    #   So: to block extension in (i,j) with i in R0, j not in C0: we would need that placing a chip of color c_i is impossible — but it's not, because column j is empty, so no conflict.
    #   Hence, we **can** add such a chip → so configuration is **not** maximal.

    # Therefore, to have maximality, we must **have no such extendable cells**.
    # So:
    #   - Every row is either: empty, or has a color
    #   - Every column is either: empty, or has a color
    #   - The occupied cells are exactly those (i,j) such that: row i nonempty, column j nonempty, and row_color[i] == col_color[j]
    #   - And for every other cell (i,j): either occupied, or **cannot be occupied** → which only happens if row i nonempty and column j nonempty and row_color[i] ≠ col_color[j]
    #   - But cells with i not in R0, j in C0: we **can** add (just use color of column j) → so unless we block it, we can extend.
    #   Similarly, i in R0, j not in C0: we can add (use row color).
    #   i not in R0, j not in C0: we can add (any color).

    # So the **only** way to have maximality is to have **no empty cells at all**?
    # But that can't be — because then the answer would just be the number of ways to fill the entire grid with the row-color = column-color consistency — but we have only 25 white and 25 black, and total cells is 25, so we could fill all — but we are allowed to use **some**.

    # But wait: we just proved that **any configuration that leaves a cell empty in a "extendable" region is not maximal**.
    # So: the only maximal configurations are those where **every empty cell is blocked by a color conflict**.
    # But:
    #   - A cell (i,j) with row i nonempty and column j empty: is **not blocked** → we can add.
    #   - Similarly for row empty, column nonempty.
    #   - For both empty: not blocked.
    # So: **there is no way to block extensions in cells that have at least one of row or column empty**.
    # Therefore, to have maximality, we must have **no such cells** → so **every row and every column must be nonempty**.
    # Then the entire grid has colors: each row has a color, each column has a color.
    # And the occupied cells are exactly those (i,j) with row_color[i] == col_color[j].
    # And the empty cells are those with row_color[i] ≠ col_color[j] → and these **are** blocked (because any chip would have to satisfy both row and column color → impossible).
    # So: maximality is achieved **if and only if**:
    #   - Every row is nonempty
    #   - Every column is nonempty
    #   - The occupied cells are exactly the (i,j) with row_color[i] == col_color[j]
    #   - And we have placed chips in **all** such cells (otherwise we could add one more there)
    #   - And we have enough chips of each color.

    # But also: we are not required to use all chips — but we **must** fill **all** the "agreeing" cells, otherwise we could add one more → violates maximality.

    # So: steps:
    #   1. Choose a color for each row: 2^n ways
    #   2. Choose a color for each column: 2^n ways
    #   3. Then the set of cells that must be filled is: { (i,j) : row_color[i] == col_color[j] }
    #   4. Let:
    #        w = number of white cells in this set
    #        b = number of black cells in this set
    #      But note: each such cell gets a color: if row_color[i]=W, col_color[j]=W → then we place a white chip.
    #      Similarly for black.
    #      So:
    #        Let rW = number of white rows
    #        rB = number of black rows = n - rW
    #        cW = number of white columns
    #        cB = n - cW
    #        Then:
    #          white chips needed = rW * cW + rB * cB ? 
    #        No: only the **agreeing** cells are filled.
    #        And:
    #          # of white chips = number of cells (i,j) with row[i]=W and col[j]=W → rW * cW
    #          # of black chips = number of cells (i,j) with row[i]=B and col[j]=B → rB * cB
    #        So total white used = rW * cW
    #        total black used = rB * cB
    #   5. We must have:
    #        rW * cW <= n   (we have n white chips)
    #        rB * cB <= n   (we have n black chips)
    #   6. And we **do** fill them all → so we must have enough chips.
    #   7. Then this configuration is valid and maximal.

    # But: is every such configuration maximal? Yes — because:
    #   - All rows and columns are nonempty → so every empty cell has both row and column colored, and they differ → so blocked.
    #   - All non-blocked cells are filled → so cannot add more.
    # So: yes.

    # Therefore, the total number is:
    #   Sum over rW in [0,n], cW in [0,n]:
    #       number of ways to choose rW white rows: C(n, rW)
    #       number of ways to choose cW white columns: C(n, cW)
    #       if rW*cW <= n and (n-rW)*(n-cW) <= n:
    #           add C(n,rW)*C(n,cW)
    #   But note: we are **not** summing over colors of individual rows — we are summing over **counts**.
    #   And for each such choice of rW, cW, we get exactly C(n,rW)*C(n,cW) configurations.

    # However: note that **all rows must be nonempty** → but we are **assigning colors** → so they **are** nonempty → so no problem.
    # Similarly for columns.

    # So we just sum over rW=0 to n, cW=0 to n:
    total = 0
    for rW in range(n+1):
        for cW in range(n+1):
            white_needed = rW * cW
            black_needed = (n - rW) * (n - cW)
            if white_needed <= n and black_needed <= n:
                total += comb(n, rW) * comb(n, cW)
    return total

# But note: n=25 → this loop is 26*26=676 iterations → very fast.

# So we write solve(n) as above.

# Test: n=1 → expected?
#   rW,cW in {0,1}
#   (0,0): white=0, black=1*1=1 → okay → add C(1,0)*C(1,0)=1
#   (0,1): white=0, black=1*0=0 → okay → add C(1,0)*C(1,1)=1
#   (1,0): white=0, black=0 → okay → add C(1,1)*C(1,0)=1
#   (1,1): white=1, black=0 → okay → add 1*1=1
#   total=4 → all 4 color assignments are okay → makes sense.

print(solve(1))  # should be 4
print(solve(2))  # let's not worry — just run

# So final code:

def solve(n):
    total = 0
    for rW in range(n+1):
        for cW in range(n+1):
            w = rW * cW
            b = (n - rW) * (n - cW)
            if w <= n and b <= n:
                total += comb(n, rW) * comb(n, cW)
    return total

# 调用 solve
result = solve(inputs['n'])
print(result)