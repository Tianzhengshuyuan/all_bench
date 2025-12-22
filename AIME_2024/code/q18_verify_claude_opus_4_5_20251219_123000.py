inputs = {'n_sides': 12}

import math
from itertools import combinations

def solve(n_sides):
    """
    Count rectangles that can be formed inside a regular n-gon
    where each side of the rectangle lies on either a side or a diagonal.
    """
    n = n_sides
    
    # Place vertices on unit circle
    # Vertex k is at angle 2*pi*k/n from positive x-axis
    vertices = []
    for k in range(n):
        angle = 2 * math.pi * k / n
        x = math.cos(angle)
        y = math.sin(angle)
        vertices.append((x, y))
    
    # Generate all lines (sides and diagonals)
    # A line is defined by two vertices
    lines = []
    for i in range(n):
        for j in range(i + 1, n):
            lines.append((i, j))
    
    # For each line, compute its direction (normalized)
    def get_direction(line):
        i, j = line
        dx = vertices[j][0] - vertices[i][0]
        dy = vertices[j][1] - vertices[i][1]
        length = math.sqrt(dx*dx + dy*dy)
        return (dx/length, dy/length)
    
    # Group lines by their direction (parallel lines have same or opposite direction)
    # Use angle as key
    def get_angle(line):
        dx, dy = get_direction(line)
        angle = math.atan2(dy, dx)
        # Normalize to [0, pi) since opposite directions are same for parallelism
        if angle < 0:
            angle += math.pi
        if angle >= math.pi - 1e-9:
            angle = 0
        return angle
    
    # Group parallel lines
    eps = 1e-9
    line_groups = {}
    for line in lines:
        angle = get_angle(line)
        found = False
        for key in line_groups:
            if abs(key - angle) < eps or abs(key - angle - math.pi) < eps or abs(key - angle + math.pi) < eps:
                line_groups[key].append(line)
                found = True
                break
        if not found:
            line_groups[angle] = [line]
    
    # For a rectangle, we need two pairs of parallel lines that are perpendicular
    # Find pairs of perpendicular direction groups
    angles = list(line_groups.keys())
    perpendicular_pairs = []
    for i in range(len(angles)):
        for j in range(i + 1, len(angles)):
            diff = abs(angles[i] - angles[j])
            if abs(diff - math.pi/2) < eps or abs(diff - 3*math.pi/2) < eps:
                perpendicular_pairs.append((angles[i], angles[j]))
    
    # Function to check if four lines form a rectangle
    def line_equation(line):
        """Return (a, b, c) such that ax + by + c = 0"""
        i, j = line
        x1, y1 = vertices[i]
        x2, y2 = vertices[j]
        a = y2 - y1
        b = x1 - x2
        c = (x2 - x1) * y1 - (y2 - y1) * x1
        return (a, b, c)
    
    def line_intersection(line1, line2):
        """Find intersection point of two lines"""
        a1, b1, c1 = line_equation(line1)
        a2, b2, c2 = line_equation(line2)
        det = a1 * b2 - a2 * b1
        if abs(det) < eps:
            return None
        x = (b1 * c2 - b2 * c1) / det
        y = (a2 * c1 - a1 * c2) / det
        return (x, y)
    
    def point_on_segment(px, py, line):
        """Check if point (px, py) lies on the segment defined by line"""
        i, j = line
        x1, y1 = vertices[i]
        x2, y2 = vertices[j]
        # Check if point is between endpoints
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        return (min_x - eps <= px <= max_x + eps) and (min_y - eps <= py <= max_y + eps)
    
    def lines_are_parallel(line1, line2):
        a1, b1, c1 = line_equation(line1)
        a2, b2, c2 = line_equation(line2)
        return abs(a1 * b2 - a2 * b1) < eps
    
    # Count rectangles
    count = 0
    
    for angle1, angle2 in perpendicular_pairs:
        group1 = line_groups[angle1]
        group2 = line_groups[angle2]
        
        # Choose 2 lines from group1 and 2 lines from group2
        for l1a, l1b in combinations(group1, 2):
            for l2a, l2b in combinations(group2, 2):
                # These 4 lines should form a rectangle
                # Check all 4 intersection points exist and lie on segments
                corners = []
                valid = True
                for la in [l1a, l1b]:
                    for lb in [l2a, l2b]:
                        pt = line_intersection(la, lb)
                        if pt is None:
                            valid = False
                            break
                        px, py = pt
                        if not (point_on_segment(px, py, la) and point_on_segment(px, py, lb)):
                            valid = False
                            break
                        corners.append(pt)
                    if not valid:
                        break
                
                if valid and len(corners) == 4:
                    count += 1
    
    return count

result = solve(12)

# 调用 solve
result = solve(inputs['n_sides'])
print(result)