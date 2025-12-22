inputs = {'n': 25}

from math import comb

def solve(n):
    # n is 25, but we only use it to know the grid is 5x5
    # We do casework on how many rows are "active" (have at least one chip)
    # and how many columns are active, and their colors.
    
    # Let r = number of active rows, c = number of active columns.
    # Each active row must be monochromatic, each active column must be monochromatic.
    # Also, the subgrid of active rows × active columns must be consistent:
    #   if a cell (i,j) is occupied, then row i color == column j color.
    # So we cannot have two active rows of different colors meeting two active columns of different colors.
    # Hence, either:
    #   - all active rows same color AND all active columns same color, OR
    #   - all active rows same color AND all active columns opposite color, but then no cell can be occupied
    #     unless row color == column color, so only monochromatic blocks.
    
    # Actually, the only way to have any chip is to have:
    #   - all active rows same color, all active columns same color, and that color matches.
    # But we can also have:
    #   - all active rows white, all active columns black -> then no cell can be occupied (conflict), so only empty.
    # So we must have:
    #   - all active rows same color, all active columns same color, and row_color == col_color.
    
    # Furthermore, the "maximal" condition: we cannot add any more chip.
    # That means:
    #   - every inactive row: if we try to add a chip in any cell of that row, it would violate.
    #     But since the row is inactive, we can only add if we assign a color to that row.
    #     However, if we add a chip in column j, then that column must have the same color as the new row.
    #     So to block adding to an inactive row, we need that for every column j:
    #       either column j is active and its color != the color we would assign to the row,
    #       or column j is inactive but then we could potentially add, but we must ensure that
    #       adding *any* chip in that row would break column consistency.
    #     Actually, simpler: we cannot add a chip in any inactive row i and any column j:
    #       - if column j is active, then to add a chip at (i,j), we must assign row i the color of column j.
    #         But then row i would be active with that color. So to block this, we must have that
    #         for every inactive row i, and for every active column j, the color of column j is already
    #         "blocked" for row i?  No — we can always choose to activate the row with that color.
    #     So the only way we cannot add a chip in an inactive row is if **every cell in that row**
    #     is either:
    #       - in a column whose active color (if column active) is opposite to the color we would assign,
    #       but we can choose the row color to match any column.
    #     Hence, we **can** always add a chip in an inactive row by choosing the row color to match
    #     the color of an active column (or arbitrary if column inactive).
    
    # Therefore, to be maximal, we must have **no inactive row** and **no inactive column**?
    # No — we can have inactive rows, but we must ensure that we cannot add **any** chip
    # in any inactive row or inactive column.
    
    # Key insight:
    #   - We cannot add a chip in an inactive row i: 
    #       for every column j, placing a chip at (i,j) would violate.
    #       Violation means: either cell occupied (but it's not), or 
    #       after placing, the row i must be monochromatic and column j must be monochromatic.
    #       Since row i is inactive, we can assign it a color when we place the first chip.
    #       So the only way we **cannot** place a chip at (i,j) is if:
    #         - column j is active, and we would be forced to assign row i the color of column j,
    #           but that would be fine — no violation.
    #       Actually, **there is no violation** possible by placing one chip — we can always do it.
    #       So to block adding **any** chip in an inactive row, we must have that **every cell**
    #       in that row is "unplaceable" — but we can always place at least one chip.
    
    # Hence, the only way the configuration is **maximal** is if:
    #   - **every row is active**, and **every column is active**.
    # Because if any row is inactive, we can place a chip in that row (in any column),
    # and similarly for any inactive column.
    
    # So the grid must be fully active: all 5 rows active, all 5 columns active.
    # Then each row has a color, each column has a color, and a cell (i,j) can be occupied
    # only if row_i_color == col_j_color.
    # Also, we must have **all chips** in those positions, and we cannot add any more —
    # but since all rows and columns are active, we cannot add a chip in a new row/col,
    # and in existing rows/cols, we can only add in cells where colors match — but those
    # cells might be empty or occupied.  We can add **only** in empty cells where row color == col color.
    # So to be maximal, we must have **all such cells occupied**.
    
    # Therefore, the configuration is:
    #   - all rows active, all columns active
    #   - each row color: white or black
    #   - each column color: white or black
    #   - a cell (i,j) is occupied iff row_i_color == col_j_color
    #   - and we use only the available chips: 25 white, 25 black, but we don't have to use all.
    
    # But note: we are **not required to use all chips**, only "some", and the configuration
    # must be maximal — cannot add any more.
    
    # So we sum over all color assignments to rows and columns:
    #   Let R be the set of row colors (each row: W/B)
    #   Let C be the set of column colors (each col: W/B)
    #   Then the occupied cells are those where row_i_color == col_j_color.
    #   Let:
    #       rW = number of white rows
    #       rB = number of black rows = 5 - rW
    #       cW = number of white columns
    #       cB = number of black columns = 5 - cW
    #   Then:
    #       white chips placed = rW * cW
    #       black chips placed = rB * cB
    #   We require:
    #       white chips <= 25, black chips <= 25
    #   but since max(rW*cW) = 25, max(rB*cB)=25, and we have exactly 25 of each, this is always satisfied.
    
    # And for each such color assignment, we get a valid maximal configuration.
    # Also, chips are indistinguishable, so we only care about the counts.
    
    # How many such color assignments?
    #   - Choose rW: 0 to 5
    #   - Choose which rW rows are white: C(5, rW)
    #   - Choose cW: 0 to 5
    #   - Choose which cW columns are white: C(5, cW)
    #   - Then black rows: 5-rW, black cols: 5-cW
    #   - Each gives a unique configuration (occupied cells determined)
    
    # But note: we are counting **configurations on the grid**, i.e., which cells are occupied
    # and what color is in each occupied cell (but row/col force colors).
    # Since row colors determine chip colors in rows, and we’ve fixed the pattern,
    # each (row coloring, column coloring) gives a unique placement.
    
    total = 0
    for rW in range(6):
        for cW in range(6):
            # white chips: rW * cW
            # black chips: (5 - rW) * (5 - cW)
            if rW * cW <= 25 and (5 - rW) * (5 - cW) <= 25:
                ways = comb(5, rW) * comb(5, cW)
                total += ways
    return total

# 调用 solve
result = solve(inputs['n'])
print(result)