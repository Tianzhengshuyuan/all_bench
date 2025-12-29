inputs = {'m': 20}

def solve(m):
    # In an isosceles (disphenoid) tetrahedron, all faces are congruent.
    # For an inscribed sphere with inradius r, the height from a vertex to the opposite face is h = 4r.
    # Given r = (m*sqrt(21))/63 and h = (H*sqrt(21))/63, we deduce H = 4m.
    return 4 * m

H = solve(20)

# 调用 solve
result = solve(inputs['m'])
print(result)