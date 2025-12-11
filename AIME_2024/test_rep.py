from fractions import Fraction
import math

def greatest_4digit_digit_toN_divisible_byM(rep_digit: int, divisor: int) -> int:
    # 参数检查（符合 relations 限制）
    rep_new = rep_digit
    if not (0 <= rep_new <= 9):
        raise ValueError("rep_new must be between 0 and 9.")
    if divisor not in (3, 7, 9):
        raise ValueError("divisor must be one of {3, 7, 9}.")

    # 从最大 4 位数开始向下遍历
    for N in range(9999, 999, -1):
        digits = list(str(N))
        ok = True
        for i in range(4):
            original = digits[i]
            digits[i] = str(rep_new)
            modified = int(''.join(digits))
            digits[i] = original
            if modified % divisor != 0:
                ok = False
                break
        if ok:
            Q, R = divmod(N, 1000)
            return Q + R

    raise ValueError(f"No valid 4-digit integer satisfies the given condition rep_digit={rep_digit}, divisor={divisor}.")

if __name__ == "__main__":
    no_result = []  # 记录没有结果的组合
    results = []    # 记录有结果的组合

    for rep in range(0, 10):
        for div in [3, 7, 9]:
            try:
                result = greatest_4digit_digit_toN_divisible_byM(rep, div)
                results.append((rep, div, result))
                print(f"✅ rep_digit: {rep}, divisor: {div} => Result: {result}")
            except ValueError as e:
                no_result.append((rep, div))
                print(f"⚠️ rep_digit: {rep}, divisor: {div} => No result found")

    # 打印没有结果的组合
    print("\n=== 无结果的组合 ===")
    if no_result:
        for rep, div in no_result:
            print(f"rep_digit={rep}, divisor={div}")
    else:
        print("全部组合均有结果。")

    # 示例特例
    try:
        result = greatest_4digit_digit_toN_divisible_byM(0, 7)
        print(f"\n特例 (rep_digit=0, divisor=7) => Result: {result}")
    except ValueError:
        print("\n特例 (rep_digit=0, divisor=7) => 无结果")