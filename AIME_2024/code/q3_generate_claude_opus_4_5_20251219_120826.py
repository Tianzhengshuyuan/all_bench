inputs = {'set_size': 539}

from math import comb, gcd

def solve(set_size):
    # Jen picks 4 distinct numbers from S = {1, 2, ..., set_size}
    # 4 numbers are randomly chosen from S
    # She wins a prize if at least 2 of her numbers match
    # She wins grand prize if all 4 match
    # We need P(grand prize | won a prize) = m/n, find m+n
    
    pick_count = 4  # Jen picks 4 numbers
    chosen_count = 4  # 4 numbers are randomly chosen
    
    # Total ways to choose 4 numbers from set_size
    total_ways = comb(set_size, chosen_count)
    
    # Ways to get exactly k matches (k of Jen's numbers are in the chosen 4)
    # Choose k from Jen's 4 numbers: C(4, k)
    # Choose (4-k) from the remaining (set_size - 4) numbers: C(set_size - 4, 4 - k)
    
    remaining = set_size - pick_count  # numbers not picked by Jen
    
    # Ways to match exactly k numbers
    def ways_match_exactly(k):
        return comb(pick_count, k) * comb(remaining, chosen_count - k)
    
    # Grand prize: all 4 match
    grand_prize_ways = ways_match_exactly(4)
    
    # Win a prize: at least 2 match (2, 3, or 4 matches)
    prize_ways = ways_match_exactly(2) + ways_match_exactly(3) + ways_match_exactly(4)
    
    # P(grand prize | won a prize) = grand_prize_ways / prize_ways
    m = grand_prize_ways
    n = prize_ways
    
    # Simplify the fraction
    g = gcd(m, n)
    m = m // g
    n = n // g
    
    return m + n

result = solve(10)

# 调用 solve
result = solve(inputs['set_size'])
print(result)