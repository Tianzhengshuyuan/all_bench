from fractions import Fraction
import math
from math import comb
import sympy as sp
from math import gcd, isqrt

def solve(total_residents):
    # Given data
    diamond = 195
    golf = 367
    spade = 562
    candy = total_residents  # every resident owns candy hearts
    
    # Number of residents owning exactly 2 and exactly 3 items
    exactly_two = 437
    exactly_three = 234
    
    # Let w = exactly one item, z = all four items
    # Total residents: w + exactly_two + exactly_three + z = total_residents
    # So: w + z = total_residents - exactly_two - exactly_three
    w_plus_z = total_residents - exactly_two - exactly_three
    
    # Total items counted by ownership:
    # w*1 + exactly_two*2 + exactly_three*3 + z*4 = diamond + golf + spade + candy
    total_items = diamond + golf + spade + candy
    w_plus_4z = total_items - 2*exactly_two - 3*exactly_three
    
    # Solve the system:
    # w + z = w_plus_z
    # w + 4z = w_plus_4z
    # Subtract: 3z = w_plus_4z - w_plus_z
    z = (w_plus_4z - w_plus_z) // 3
    return z

if __name__ == "__main__":
    print(solve(900))

