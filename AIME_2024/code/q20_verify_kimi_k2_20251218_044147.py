inputs = {'n': 25}

from math import comb

def solve(n):
    # n is 25, but we only use it to confirm we have enough chips; the grid is 5x5=25 cells.
    # We interpret the problem as: 5x5 grid, each cell at most one chip,
    # all chips in a row same colour, all chips in a column same colour,
    # and the placement is maximal (no more chip can be added without violating).
    # Chips are indistinguishable within colour, and we have 25 white and 25 black available.
    
    # Key insight: 
    # Because every row must be monochromatic and every column must be monochromatic,
    # the entire pattern is determined by:
    #   - which rows are "active" (have at least one chip),
    #   - which columns are "active",
    #   - and the colour of each active row and each active column.
    # But additionally, at every intersection of an active row and active column,
    # the row-colour and column-colour must agree if we are to place a chip there.
    # 
    # Moreover, maximality implies that we cannot add any chip anywhere.
    # That means: every empty cell (i,j) must be such that
    #   - either row i is inactive, or column j is inactive, or
    #   - if both are active, then the colour of row i differs from the colour of column j
    #      (so we cannot place a chip there because it would violate the row or column colour).
    # But maximality also implies that we cannot "activate" a new row or column easily.
    # 
    # However, a simpler view is possible:
    # Let R be the set of active rows, C the set of active columns.
    # Let f: R -> {W,B} be the colour of each active row,
    # and g: C -> {W,B} the colour of each active column.
    # We place a chip at (i,j) iff i in R, j in C, and f(i) == g(j).
    # 
    # Maximality then implies:
    #   - For every inactive row i, we cannot activate it: 
    #        if we tried to activate it and assign it a colour, we would have to place chips
    #        in all columns j in C with that colour, but then we might conflict or run out?
    #   - But actually maximality is only about *placement* violating the rules,
    #     not about running out of chips.  The rules are only:
    #        (1) at most one chip per cell,
    #        (2) each active row monochromatic, each active column monochromatic.
    # 
    # So maximality means: for every empty cell (i,j), placing a chip there would violate (1) or (2).
    # Since cells are empty, (1) is not violated.  So it must violate (2):
    #   - either row i is active and the new chip would have a different colour from the row,
    #   - or column j is active and the new chip would have a different colour from the column,
    #   - or both.
    # 
    # Therefore, for every empty cell (i,j):
    #   - if row i is active and column j is active, then we must have f(i) != g(j)
    #        (because otherwise we would have placed a chip there already).
    #   - if row i is inactive and column j is inactive, then we *could* place a chip there
    #        without immediately violating colour constraints, but we don't.
    #        However, if we placed a chip there, we would have to assign colours to row i and column j.
    #        But maximality implies we *cannot* place it, so it must be that *any* such placement
    #        would violate the rules.  But we can always place a chip in an inactive row/inactive column cell
    #        and assign both the row and the column to, say, white, and place a white chip.
    #        That would not violate any rule.  So to prevent that, we must have *no* such cell.
    # 
    # Hence, we cannot have any cell (i,j) with row i inactive and column j inactive.
    # That means: the set of inactive rows and inactive columns cannot both be non-empty.
    # In other words, either all rows are active, or all columns are active (or both).
    # 
    # So we have two main cases:
    #   Case 1: all rows are active (|R|=5), columns arbitrary
    #   Case 2: all columns are active (|C|=5), rows arbitrary (but avoid double-counting the case where both are full)
    # 
    # But also, within the active block, we only place chips where row-colour == column-colour.
    # And maximality implies that we have placed *all* such possible chips.
    # 
    # So we proceed by:
    #   - choosing a set C of active columns (subset of {1..5}), and similarly for rows,
    #   - but with the constraint: either |R|=5 or |C|=5 (or both).
    # 
    # However, we can split into:
    #   Case A: |R|=5, |C| arbitrary (0<=|C|<=5)
    #   Case B: |C|=5, |R|<5   (to avoid double-counting the |R|=5,|C|=5 case)
    # 
    # For each such choice, we assign colours to rows and columns,
    # and then the chip placement is forced: chip at (i,j) iff i in R, j in C, f(i)==g(j).
    # 
    # But we must also ensure that we do not exceed the available chips (25 white, 25 black).
    # Since n=25, and we have 25 of each colour, we just need to check that the total white chips <=25
    # and black chips <=25.
    # 
    # Let's implement this enumeration.
    
    total = 0
    
    # Precompute: for each possible (r,c) with r=5 or c=5, and for each colouring,
    # compute the number of white and black chips used.
    
    # We'll iterate over:
    #   r in {0,1,2,3,4,5}, c in {0,1,2,3,4,5}, but require r==5 or c==5.
    
    for r in range(6):   # number of active rows
        for c in range(6):   # number of active columns
            if r != 5 and c != 5:
                continue
            # Choose the set of active rows: C(5, r)
            ways_rows = comb(5, r)
            ways_cols = comb(5, c)
            
            # Assign colours to rows: each active row can be W or B -> 2^r ways
            # Similarly for columns: 2^c ways
            # But we must sum over all colour assignments, and for each, compute white and black chips.
            
            # For a fixed assignment:
            #   Let wrow = number of white rows, brow = r - wrow
            #   Let wcol = number of white columns, bcol = c - wcol
            #   Then white chips = wrow * wcol + brow * bcol
            #        black chips = wrow * bcol + brow * wcol
            # 
            # But we can iterate over wrow and wcol.
            
            for wrow in range(r+1):
                brow = r - wrow
                # number of ways to choose which rows are white: C(r, wrow)
                # but we already chose the set of rows, so we choose subset of those: C(r, wrow)
                ways_row_col = comb(r, wrow)
                
                for wcol in range(c+1):
                    bcol = c - wcol
                    ways_col_col = comb(c, wcol)
                    
                    white = wrow * wcol + brow * bcol
                    black = wrow * bcol + brow * wcol
                    
                    if white <= 25 and black <= 25:
                        # This colouring is feasible
                        total += ways_rows * ways_cols * ways_row_col * ways_col_col
    
    return total

# The problem states n=25, but we ignore n as a size parameter beyond chip supply.
# We call solve(25) to get the answer.

# 调用 solve
result = solve(inputs['n'])
print(result)