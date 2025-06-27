import os
import re
import csv
import time
import openai
import argparse
from openai import OpenAI
from mistralai import Mistral
from volcenginesdkarkruntime import Ark
from fractions import Fraction
from sympy import sympify, simplify, SympifyError, N
def parse_mixed_number(s):
    """
    将带分数如 '3 1/2'、'3 \frac{1}{2}'、'3\frac{1}{2}' 转换为 '7/2'
    """
    s = s.strip()
    # 支持 3 1/2
    match = re.match(r'^(-?\d+)\s+(\d+)/(\d+)$', s)
    if match:
        integer, num, denom = match.groups()
        frac = Fraction(int(num), int(denom))
        total = int(integer) + (frac if int(integer) >= 0 else -frac)
        return str(total)
    
    # 支持 3\frac{1}{2} 或 3 \frac{1}{2}（中间可有空格）
    match = re.match(r'^(-?\d+)\s*\\frac\s*{\s*(\d+)\s*}\s*{\s*(\d+)\s*}$', s)
    if match:
        integer, num, denom = match.groups()
        frac = Fraction(int(num), int(denom))
        total = int(integer) + (frac if int(integer) >= 0 else -frac)
        return str(total)
    
    # 其他情况原样返回
    return s

def normalize_for_compare(ans):
    """
    归一化答案：去空格，处理带分数，统一分数小数，括号等
    """
    ans = ans.strip()
    if ans == '':
        return ''
    # 去除 逗号和类似{,}、,\!、,\thinspace、\,等常用千位分隔
    # 1. 5,\!040 以及 5,040
    ans = re.sub(r'\s*,\s*\\!\s*','', ans)
    # 2. 14{,}916 这种
    ans = re.sub(r'\{,\}', '', ans)
    
    # 把 $0.50、\$0.50、$0.5、\$0.5 都变成 0.50 或 0.5
    ans = re.sub(r'\\?\$\s*([0-9]+(?:\.[0-9]+)?)', r'\1', ans)
    
    # 如果包含等号，去掉等号及其左边，只保留等号右边（去掉右边开头的空格）
    if '=' in ans:
        ans = ans.split('=', 1)[1].lstrip()
    
    # 去除 ^{\circ}、 \circ 和 ^\circ
    ans = re.sub(r'\^\s*{\\circ}', '', ans)
    ans = re.sub(r'(\\circ|\^\\circ)$', '', ans, flags=re.IGNORECASE)

    # 处理 \mbox{单位}^2 及 \mbox{单位}
    ans = re.sub(r'\\mbox\s*{[a-zA-Z\s]+}(\^\s*[\w\d\+\-\(\)]+)?', '', ans)
    
    # 特殊处理 \text{} 环境
    # 1. 纯数字，保留内容
    ans = re.sub(r'\\text\s*{\s*(\d+)\s*}', r'\1', ans)
    # 2. 纯英文，删除整个 \text{英文}或 \text{英文}^2
    ans = re.sub(r'\\text\s*{[a-zA-Z\s]+}(\^\s*[\w\d\+\-\(\)]+)?', '', ans)
    
    # 标准化带分数
    ans = parse_mixed_number(ans)
    
    # 1. \frac 后跟空格和两个数字，如 \frac 13
    ans = re.sub(r'\\frac\s+(\d)(\d)(?!\d)', r'\1/\2', ans)
    # 2. \frac 后跟大括号和一位数字，如 \frac{35}7
    ans = re.sub(r'\\frac\s*{\s*(\d+)\s*}(\d)', r'\1/\2', ans)
    # 3. \frac 后跟空格、一位数字和大括号，如 \frac 4{33}
    ans = re.sub(r'\\frac\s+(\d)\s*{\s*(\d+)\s*}', r'\1/\2', ans) 
    
    # 去空格
    ans = ans.replace(' ', '')
    
    # 处理 √3 -> sqrt(3)
    ans = re.sub(r'√\s*([0-9a-zA-Z]+)', r'sqrt(\1)', ans)
    # 处理 \sqrt{3} -> sqrt(3)
    ans = re.sub(r'\\sqrt\s*{\s*([^{}]+)\s*}', r'sqrt(\1)', ans)
    # 统一小数点前无0的写法
    ans = re.sub(r'(?<!\d)\.(\d+)', r'0.\1', ans)
    # 统一括号写法
    ans = ans.replace('\\left(', '(').replace('\\right)', ')')
    
    # 分数归一化，例如：\frac{1}{2} → 1/2
    ans = re.sub(r'\\frac\s*{\s*([^{}]+)\s*}{\s*([^{}]+)\s*}', r'\1/\2', ans)
    ans = re.sub(r'\\dfrac\s*{\s*([^{}]+)\s*}{\s*([^{}]+)\s*}', r'\1/\2', ans)

    # 处理 \pi -> pi、π -> pi
    ans = ans.replace('\\pi', 'pi')
    ans = ans.replace('π', 'pi')
    
    # 关键：数字与字母之间加 *
    ans = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', ans)
    # 去掉单位
    ans = re.sub(r'(cm|mm|kg|g|m|radian|degree|°|%|\\%|\\circ|\^\\circ)$', '', ans, flags=re.IGNORECASE)
    return ans

def match_ratio(n, other):
    ratio_pattern = r'^(-?\d+(?:\.\d+)?):(-?\d+(?:\.\d+)?)$'
    m = re.match(ratio_pattern, n)
    if m:
        a, b = m.groups()
        # 如果 b == 1，且 other == a 或 other == a/1 或 other == float(a)
        if float(b) == 1:
            try:
                if other == a or other == f"{a}/1":
                    return True
                # 允许 3:1 和 3.0 等价
                if abs(float(a) - float(other)) < 1e-8:
                    return True
            except Exception:
                pass
    return False
    
def is_equivalent(ans1, ans2):
    n1 = normalize_for_compare(ans1)
    n2 = normalize_for_compare(ans2)
    if n1 == n2:
        return True
    # 解析 n1 或 n2 是否为 "a:b" 形式，另一方为 "a" 或 "a/1"，例如3:1和3
    if match_ratio(n1, n2) or match_ratio(n2, n1):
        return True
    
    # 用 sympy.N 直接数值化表达式进行比较，比如\frac{\sqrt{3}}{3}和0.5773502691896257
    try:
        v1 = float(N(n1))
        v2 = float(N(n2))
        if abs(v1 - v2) < 1e-8:
            return True
    except Exception:
        pass
    
    try:
    # Fraction是Python fractions模块里的一个类，可以用来精确表达分数。
    # float(...)：把分数转换为浮点数（小数）
        v1 = float(Fraction(n1))
        v2 = float(Fraction(n2))
        if abs(v1 - v2) < 1e-8:
            return True
    except Exception:
        pass
    try:
    # SymPy的sympify函数将字符串或数字n1转换为SymPy的符号表达式（Symbolic Expression）。例如：sympify("1/2 + x") 会变成 Rational(1, 2) + x
    # simplify会对表达式进行化简，比如合并同类项、约分、展开等。例如：simplify("2*x + 3*x") 会变成 5*x
        print(n1, n2)

        expr1 = simplify(sympify(n1))
        expr2 = simplify(sympify(n2))
        print(expr1, expr2)
        if expr1.equals(expr2):
            return True
        if simplify(expr1 - expr2) == 0:
            return True
    except SympifyError as e:
        print(f"SymPy error: {e}")
        
    except Exception as e:
        print(f"SymPy error: {e}")
    try:
        if abs(float(n1) - float(n2)) < 1e-8:
            return True
    except Exception:
        pass
    return False

result = is_equivalent(r"111, \! 111, \! 111", r"111111111")
print(result)  # True


# "\left(1,\frac{9}{2}\right)","(1,4.5)"
# \!\sqrt{33},33\sqrt{33}
# "x \in [-2,7]","(-2, 8]"
# \frac{\sqrt{3}}{9},\frac{8}{3\sqrt{3}+ 7\sqrt{27}} = \frac{8}{3\sqrt{3}+ 7\cdot 3\sqrt{3}} = \frac{8}{24\sqrt{3}} = \frac{1}{3\sqrt{3}} = \frac{\sqrt{3}}{9},✘
# "[6,\infty)","[4, +∞)"
# 4(3-x)(3+x),(6-2x)(6+2x
# \frac{\sqrt6}3,\frac{2\sqrt{6}}{6}
# 13,4+5+1+3,✔
# "[0,\infty)","[0, +\infty)"
# "(-\infty, 2) \cup (3, \infty)","(2,3)∪(3,+∞)"
# \dfrac{5}{7},0.7143
# \frac14,1/4,
# "98,\!770",\frac{85!}{82!3!},
# 25 \pi,78.54
# "\left( \frac{2}{5}, \frac{1}{2} \right)","(1, 1/4)"
# "(-\infty,3)\cup(3,\infty)","(-∞,3)∪(3,∞)"
# \tfrac{8\pi}5,7.5,
# \text{neither},neither
# y = -\frac{1}{2} x^2 + 4x - 6,y = -\frac{1}{4}x^2 + \frac{9}{4}x - 2
# 7x(x-1)(x-2),7x(x-2)(x-1),
# \frac{1}{2004!},1,
# "3, -\frac{1}{3}","x=1,x=-\frac{1}{3}"
# 2x^2 + 5x - 1,x^2 + 2x + 2,