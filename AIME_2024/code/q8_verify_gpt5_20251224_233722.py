inputs = {'number_of_triples': 601}

def solve(number_of_triples):
    N = number_of_triples
    num = (N - 1) ** 3
    den = 36
    if num % den == 0:
        return num // den
    else:
        from fractions import Fraction
        return Fraction(num, den)

number_of_triples = 601
solve(number_of_triples)

# 调用 solve
result = solve(inputs['number_of_triples'])
print(result)