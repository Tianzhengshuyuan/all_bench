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

# 配置 DeepSeek API 客户端
deepseek_client = OpenAI(api_key="sk-09da13b2c97948628523d042d6a02f06", base_url="https://api.deepseek.com")
kimi_client = OpenAI(api_key="sk-ODuizMlUC22phanBhvYz6dBjx2yrz7vhKhcjKnoIrYssThQo", base_url="https://api.moonshot.cn/v1")
doubao_client = Ark(api_key="196b33be-8abb-4af3-9fba-6e266b2dd942")
mistral_client = Mistral(api_key="zWUDyBGqEIdJAtJoxnsr6ACcLTgz1auH")
qwen_client = OpenAI(api_key="sk-341becd932d743f2a750495a0f9f3ede", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

def call_deepseek_api(question):
    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 DeepSeek API 时出错: {e}")
        return "API 调用失败"
   
def call_gpt_api(question):
    os.environ["HTTP_PROXY"] = "http://localhost:7890"
    os.environ["HTTPS_PROXY"] = "http://localhost:7890"
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 gpt API 时出错: {e}")
        return "API 调用失败" 

def call_kimi_api(question):
    try:
        response = kimi_client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 Kimi API 时出错: {e}")
        return "API 调用失败"
    
def call_doubao_api(question):
    try:
        response = doubao_client.chat.completions.create(
            model="doubao-1.5-pro-32k-250115",
            # model="doubao-1.5-thinking-pro-250415",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 豆包 API 时出错: {e}")
        return "API 调用失败"
    
def call_mistral_api(question):
    try:
        response = mistral_client.chat.complete(
            model="mistral-large-2407",
            # model="mistral-medium-latest",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 Mistral API 时出错: {e}")
        return "API 调用失败"
   
def call_qwen_api(question):
    try:
        response = qwen_client.chat.completions.create(
            model="qwen-plus", 
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': question},
            ],
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 Qwen API 时出错: {e}")
        return "❌"
     
def extract_answer_from_response(response):
    """
    从回答中提取被####包裹的答案（允许任意内容）
    """
    match = re.search(r'####(.*?)####', response, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return "无匹配"


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

def test_gap_filling_on_file(filepath, output_filepath):
    # 读取输入 CSV
    with open(filepath, 'r', encoding='utf-8') as infile, \
        open(output_filepath, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        question_count = 0
        right_count = 0
        start_time = time.time()  # 记录开始时间

        for row in reader:
            if not row:
                continue
            question_count += 1
            prompt = f"What is the answer to the following question? Just tell me the final result, don’t return anything else. Please enclose the answer with two pairs of ####, for example: ####6####.\n{row[0]}"
            print(f"题目:\n{row[0]}\n")
            if args.model == "deepseek":
                response = call_deepseek_api(prompt)
            elif args.model == "gpt":
                response = call_gpt_api(prompt)
            elif args.model == "kimi":
                response = call_kimi_api(prompt)
            elif args.model == "doubao":
                response = call_doubao_api(prompt)
            elif args.model == "mistral":
                response = call_mistral_api(prompt)
            elif args.model == "qwen":
                response = call_qwen_api(prompt)

            print(f"{args.model}回答:\n{response}， 正确答案是: {row[1]}\n")
            answer = extract_answer_from_response(response)
            is_right = is_equivalent(answer, row[1])
            if is_right:
                right_count += 1
            writer.writerow([row[1], answer, "✔" if is_right else "✘"])
        end_time = time.time()  # 记录结束时间
        total_time = end_time - start_time
    if question_count != 0:
        print(f"总题数: {question_count}, 正确答案数: {right_count}, 正确率: {right_count / question_count:.2%}, 耗时: {total_time:.2f}秒")    
    return question_count, right_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量调用 DeepSeek 翻译")
    parser.add_argument('--dir', required=True, help="输入文件夹名，包含多个CSV文件")
    parser.add_argument('--temperature', type=float, default=0.2, help="API 回答多样性，默认 0.2")
    parser.add_argument('--model', type=str, default="deepseek", help="使用的模型，如gpt、deepseek")
    args = parser.parse_args()

    total_questions = 0
    total_right = 0
    # 创建输出目录
    output_dir = args.dir.rstrip('/') + '_with_answer'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(args.dir):
        filepath = os.path.join(args.dir, filename)
        output_filepath = os.path.join(output_dir, filename)
        if os.path.isfile(filepath) and filepath.endswith(".csv"):
            q, r = test_gap_filling_on_file(filepath, output_filepath)
            total_questions += q
            total_right += r

    if total_questions != 0:
        print(f"\n全部统计: 总题数: {total_questions}, 正确答案数: {total_right}, 正确率: {total_right / total_questions:.2%}")
        
#3:1、\mbox
# "\left(1,\frac{9}{2}\right)","(1,4.5)"
# \cup
# \infty