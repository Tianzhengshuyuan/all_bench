from fractions import Fraction
import math
from math import comb
import sympy as sp
from math import gcd, isqrt

# === 5 ===
def tangent_circles_inradius(R1: int, R2: int, N1: int, N2: int) -> int:
    r_fraction = Fraction(R1 * R2 * (N1 - N2), N1 * R1 - N2 * R2 + R2 - R1)
    return r_fraction.numerator + r_fraction.denominator

if __name__ == "__main__":
    print(tangent_circles_inradius(34, 1, 8, 2134))
