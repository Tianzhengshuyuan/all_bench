inputs = {'freq': 1}

def solve(freq):
    # Count intersections between y = 4 g(f(sin(2π x))) and x = 4 g(f(cos(freq π y)))
    # where f(x) = ||x| - 1/2| and g(x) = ||x| - 1/4|.
    #
    # h(u) = 4 g(f(u)) has:
    # - zeros when |u| in {1/4, 3/4}  -> u in {±1/4, ±3/4}
    # - ones  when |u| in {0, 1/2, 1} -> u in {0, ±1/2, ±1}
    #
    # For y = h(sin(2π x)) over x in [0,1]:
    #   - sin crosses each interior value twice per period; 0 thrice (including endpoints); ±1 once.
    # For x = h(cos(m π y)) over y in [0,1], where m = |freq|:
    #   - cos(mπ y) runs over m half-periods; each interior value occurs exactly m times;
    #     value +1 occurs floor(m/2)+1 times; value -1 occurs ceil(m/2) times.
    #
    # The number of monotone "waves" of y(x) is Nx = #(hits of 0) + #(hits of 1) - 1.
    # Similarly for x(y): Ny = #(hits of 0) + #(hits of 1) - 1.
    # Each horizontal wave crosses each vertical wave once in the interior, giving Nx*Ny intersections.
    # There is exactly one boundary intersection at (1,1), so add +1.
    m = int(abs(int(round(freq))))
    zeros_vals = [-0.75, -0.25, 0.25, 0.75]
    ones_vals = [-1.0, -0.5, 0.0, 0.5, 1.0]

    def count_sin_hits_in_01(t):
        if t == 0.0:
            return 3
        if t == 1.0 or t == -1.0:
            return 1
        return 2

    def count_cos_hits_in_01(t):
        if t == 1.0:
            return m // 2 + 1
        if t == -1.0:
            return (m + 1) // 2
        # |t| < 1 (interior)
        return m

    # Waves for y = h(sin(2π x))
    px0 = sum(count_sin_hits_in_01(t) for t in zeros_vals)
    px1 = sum(count_sin_hits_in_01(t) for t in ones_vals)
    Nx = px0 + px1 - 1

    # Waves for x = h(cos(m π y))
    qy0 = sum(count_cos_hits_in_01(t) for t in zeros_vals)
    qy1 = sum(count_cos_hits_in_01(t) for t in ones_vals)
    Ny = qy0 + qy1 - 1

    total_intersections = Nx * Ny + 1
    return total_intersections

# 调用 solve
result = solve(inputs['freq'])
print(result)