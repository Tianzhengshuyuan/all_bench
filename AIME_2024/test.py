from fractions import Fraction
import sympy as sp
import re
from math import comb
import math
import argparse


def lattice_paths_four_turns(S: int) -> int:
    return 2 * math.comb(S - 1, 2) * math.comb(S - 1, 1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=int, default=7)
    args = parser.parse_args()
    print(lattice_paths_four_turns(args.input))  