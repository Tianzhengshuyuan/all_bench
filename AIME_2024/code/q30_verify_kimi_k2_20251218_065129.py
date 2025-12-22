inputs = {'root_order': 13}

import cmath

def solve(root_order):
    # Let w be a primitive root_order-th root of unity
    # We want to compute prod_{k=0}^{root_order-1} (2 - 2*w^k + w^{2k})
    # Rewrite as prod_{k=0}^{root_order-1} ( (1 - w^k)^2 + 1 )
    # = prod_{k=0}^{root_order-1} ( (1 + i - w^k)(1 - i - w^k) )
    # = [prod_{k=0}^{root_order-1} ( (1+i) - w^k )] * [prod_{k=0}^{root_order-1} ( (1-i) - w^k )]
    # = [ (1+i)^{root_order} - 1 ] * [ (1-i)^{root_order} - 1 ]
    # because prod_{k=0}^{n-1} (z - w^k) = z^n - 1 for any n-th root of unity w

    z1 = 1 + 1j
    z2 = 1 - 1j
    n = root_order

    left = z1**n - 1
    right = z2**n - 1
    product = left * right

    # product is real, take real part and convert to int
    result = int(round(product.real))
    return result % 1000

# 调用 solve
result = solve(inputs['root_order'])
print(result)