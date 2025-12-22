inputs = {'grid_size': 5}

from itertools import product

def solve(grid_size):
    n = grid_size
    
    # We need to count valid configurations where:
    # 1. Each cell has at most one chip
    # 2. All chips in same row have same color
    # 3. All chips in same column have same color
    # 4. The configuration is maximal (can't add any more chips)
    
    # Key insight: For maximality, every empty cell must be blocked.
    # An empty cell (i,j) is blocked only if row i has one color and column j has the other.
    
    # Each row can be: empty (0), white (1), or black (2)
    # Each column can be: empty (0), white (1), or black (2)
    # Cell (i,j) has a chip iff row[i] and col[j] are both non-empty AND same color
    
    # For maximality:
    # - If row i is empty and col j is empty: can place any chip -> NOT blocked
    # - If row i is empty and col j has color c: can place color c -> NOT blocked
    # - If row i has color c and col j is empty: can place color c -> NOT blocked
    # - If row i has color c1 and col j has color c2 (c1 != c2, both non-zero): BLOCKED
    # - If row i has color c and col j has color c: cell has chip (not empty)
    
    # So for maximality, every empty cell needs row and column to have opposite non-zero colors.
    # This means: no empty rows, no empty columns.
    
    # Additionally, for a row/column to have a color, it must have at least one chip.
    # Row i with color c has a chip iff there exists column j with color c.
    # Column j with color c has a chip iff there exists row i with color c.
    
    # Valid configurations:
    # - All rows have color (1 or 2), all columns have color (1 or 2)
    # - For each color present in rows, that color must be present in columns (and vice versa)
    
    count = 0
    
    for row_colors in product([1, 2], repeat=n):
        for col_colors in product([1, 2], repeat=n):
            # Check that each row has at least one chip
            # Row i (color c) has a chip iff some column has color c
            valid = True
            
            # Check rows
            for i in range(n):
                row_color = row_colors[i]
                has_chip = any(col_colors[j] == row_color for j in range(n))
                if not has_chip:
                    valid = False
                    break
            
            if not valid:
                continue
            
            # Check columns
            for j in range(n):
                col_color = col_colors[j]
                has_chip = any(row_colors[i] == col_color for i in range(n))
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