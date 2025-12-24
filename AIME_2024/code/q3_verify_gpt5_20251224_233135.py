inputs = {'m_plus_n': 116}

def solve(m_plus_n):
    from math import comb, gcd
    # Compute counts of outcomes based on number of matches with Jen's 4 numbers
    ways4 = comb(4, 4) * comb(6, 0)  # all 4 match
    ways3 = comb(4, 3) * comb(6, 1)  # exactly 3 match
    ways2 = comb(4, 2) * comb(6, 2)  # exactly 2 match

    total_win_ways = ways2 + ways3 + ways4
    m, n = ways4, total_win_ways  # P(grand | prize) = m/n
    g = gcd(m, n)
    m //= g
    n //= g

    # Given m + n = m_plus_n, return m (which is m_plus_n - n)
    return m_plus_n - n

solve(116)

# 调用 solve
result = solve(inputs['m_plus_n'])
print(result)