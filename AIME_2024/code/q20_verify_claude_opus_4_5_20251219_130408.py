inputs = {'grid_size': 5}

from itertools import product

def solve(grid_size):
    n = grid_size
    
    # We need to place chips such that:
    # 1. Each cell contains at most one chip
    # 2. All chips in same row have same color
    # 3. All chips in same column have same color
    # 4. Grid is maximal - no additional chip can be placed without violating conditions
    
    # For each row, we can assign: 0 = no chips, 1 = white chips, 2 = black chips
    # For each column, we can assign: 0 = no chips, 1 = white chips, 2 = black chips
    # A cell (i,j) has a chip if and only if row[i] != 0 and col[j] != 0 and row[i] == col[j]
    
    # Maximality condition:
    # - If row i has no chips (row[i]=0), then for every column j with col[j]!=0, 
    #   we must not be able to add a chip. This means for each such column j,
    #   there must be some row i' with row[i']=col[j] that already has a chip in column j.
    #   Actually, if row[i]=0, we could potentially add a white or black chip to any cell in row i.
    #   For this to be blocked, every column must either be empty OR have both colors blocked somehow.
    #   
    # Let me reconsider: If row[i]=0 and col[j]=1 (white), then cell (i,j) is empty.
    # Can we place a white chip there? Row i would become white, column j is already white. OK so far.
    # But we need to check if this violates anything. It doesn't directly.
    # So for maximality, if row[i]=0, then for each column j:
    #   - If col[j]=1, placing white in (i,j) must be blocked by some other constraint
    #   - If col[j]=2, placing black in (i,j) must be blocked
    # 
    # The only way placing a chip is blocked is if it would conflict with existing chips.
    # If row i is empty and we try to place white in (i,j) where col[j]=1, 
    # this is only blocked if... actually it's not blocked by the rules.
    # 
    # So for maximality: if row[i]=0, then all columns must be 0 as well? No, that's too restrictive.
    # 
    # Wait, let me re-read. If row i has no chips currently, and col j has white chips,
    # then placing a white chip at (i,j) would make row i have white chips and column j already has white.
    # This is consistent! So it's not blocked.
    # 
    # For maximality with row[i]=0: we need that for every column j and every color c,
    # placing color c at (i,j) is blocked. 
    # - If col[j]=0: placing any color works (row becomes that color, col becomes that color)
    # - If col[j]=c: placing color c works
    # 
    # So if row[i]=0, for maximality we need: for all j, col[j] != 0 AND there exist both colors in columns.
    # Actually no - if col[j]=1, we can place white. If col[j]=2, we can place black.
    # For row i to be maximal with 0 chips, we need that for every j:
    #   - We cannot place white: either col[j]=2 (conflict) or col[j]=0 but then we could place white
    #   - We cannot place black: either col[j]=1 (conflict) or col[j]=0 but then we could place black
    # So we need col[j] != 0 for all j, AND for each j, both colors are blocked.
    # But col[j] is either 1 or 2, so one color is always allowed!
    # 
    # Unless... we need BOTH colors to be blocked for each cell. 
    # For cell (i,j): white blocked if col[j]=2, black blocked if col[j]=1.
    # Both blocked only if col[j] is both 1 and 2, impossible.
    # 
    # So if row[i]=0, there's always some cell where we can add a chip. 
    # Therefore, for maximality, every row must have at least one chip (row[i] != 0).
    # Similarly, every column must have at least one chip (col[j] != 0).
    
    count = 0
    
    # Iterate over all assignments of colors to rows and columns
    # row_colors[i] in {1, 2} for white or black
    # col_colors[j] in {1, 2} for white or black
    
    for row_colors in product([1, 2], repeat=n):
        for col_colors in product([1, 2], repeat=n):
            # Check maximality: can we add any chip?
            # A chip can be added at (i,j) with color c if:
            # - Cell (i,j) is currently empty: row_colors[i] != col_colors[j]
            # - Adding color c is consistent: row_colors[i] would need to be c, col_colors[j] would need to be c
            # 
            # Wait, I need to reconsider. The current state has chips at (i,j) where row_colors[i] == col_colors[j].
            # 
            # For an empty cell (i,j) where row_colors[i] != col_colors[j]:
            # Can we add a white chip? This requires all chips in row i to be white and all in col j to be white.
            # Current row i has chips of color row_colors[i], current col j has chips of color col_colors[j].
            # So we can add white only if row_colors[i]=1 and col_colors[j]=1. But then cell already has chip!
            # So if row_colors[i] != col_colors[j], we cannot add any chip. Good!
            
            # So the configuration is automatically maximal as long as every row and column has at least one chip.
            # Every row has a chip iff there exists j with row_colors[i] == col_colors[j].
            # Every column has a chip iff there exists i with row_colors[i] == col_colors[j].
            
            valid = True
            
            # Check each row has at least one chip
            for i in range(n):
                has_chip = any(row_colors[i] == col_colors[j] for j in range(n))
                if not has_chip:
                    valid = False
                    break
            
            if not valid:
                continue
                
            # Check each column has at least one chip
            for j in range(n):
                has_chip = any(row_colors[i] == col_colors[j] for i in range(n))
                if not has_chip:
                    valid = False
                    break
            
            if valid:
                count += 1
    
    return count

result = solve(5)

# 调用 solve
result = solve(inputs['grid_size'])
print(result)