inputs = {'root_degree': 353}

def solve(root_degree):
    z = (1 + 1j) ** root_degree
    term1 = z - 1
    term2 = z.conjugate() - 1
    product = term1 * term2
    res = int(product.real)
    return res % 1000

# 调用 solve
result = solve(inputs['root_degree'])
print(result)