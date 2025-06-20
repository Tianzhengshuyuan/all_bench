import csv
import argparse
import os
import re
import openai
from openai import OpenAI
from fractions import Fraction
from sympy import sympify, E
from sympy.core.sympify import SympifyError

deepseek_client = OpenAI(api_key="sk-09da13b2c97948628523d042d6a02f06", base_url="https://api.deepseek.com")
kimi_client = OpenAI(api_key="sk-ODuizMlUC22phanBhvYz6dBjx2yrz7vhKhcjKnoIrYssThQo", base_url="https://api.moonshot.cn/v1")

def is_number(s):
    try:
        # 先尝试 float
        float(s)
        return True
    except ValueError:
        pass
    try:
        # 再尝试分数
        Fraction(s)
        return True
    except ValueError:
        pass
    try:
        # 再尝试表达式（支持e, pi等）
        expr = sympify(s, locals={"e": E})
        if isinstance(expr, tuple):
            return False
        return expr.is_number
    except (SympifyError, TypeError):
        return False
    
def call_deepseek_api(question, temperature=0):
    """
    调用 DeepSeek API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 DeepSeek API 时出错: {e}")
        return "❌"

def call_gpt_api(question, temperature=0):
    """
    调用 gpt API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
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
            temperature=temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 gpt API 时出错: {e}")
        return "❌" 
    
def call_kimi_api(question, temperature=0):
    """
    调用 Kimi API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    try:
        response = kimi_client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 Kimi API 时出错: {e}")
        return "❌"
def get_output_filename(input_name, language):
    # 获取不带扩展名的文件主名
    base = os.path.splitext(os.path.basename(input_name))[0]
    # 语言全部小写，空格换成下划线
    lang = language.strip().replace(" ", "_").lower()
    return f"{base}_{lang}.csv"

def parse_response(translation):
    # 匹配每一部分
    pattern = re.compile(
        r"question\s*[:：]\s*(.*?)\s*\nA\s*[:：]\s*(.*?)\s*\nB\s*[:：]\s*(.*?)\s*\nC\s*[:：]\s*(.*?)\s*\nD\s*[:：]\s*(.*)",
        re.DOTALL | re.IGNORECASE
    )
    m = pattern.match(translation.strip())
    if m:
        return [m.group(i).strip() for i in range(1, 6)]
    else:
        print("解析翻译结果时出错")
        return None
    
def translate(args):
    output_filename = get_output_filename(args.input, args.language)
    # 读取输入 CSV
    with open(args.input, 'r', encoding='utf-8') as infile, \
         open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            if not row:  # 跳过空行
                continue
            # 拼接待翻译文本
            text = (
                f"question: {row[1]}\n"
                f"A: {row[2]}\n"
                f"B: {row[3]}\n"
                f"C: {row[4]}\n"
                f"D: {row[5]}"
            )

            prompt = f"Please translate the following content into {args.language}. Do not translate the word 'question' at the beginning, and do not translate the four options A, B, C, D; keep them in English. Only translate, do not return anything else: \n{text}"
            print(f"原文:\n{text}\n")
            if args.model == "deepseek":
                translation = call_deepseek_api(prompt, temperature=args.temperature)
            elif args.model == "gpt":
                translation = call_gpt_api(prompt, temperature=args.temperature)
            elif args.model == "kimi":
                print("调用 Kimi API 进行翻译...")
                translation = call_kimi_api(prompt, temperature=args.temperature)
            print(f"翻译:\n{translation}\n")
            parsed = parse_response(translation)
            if parsed is None:
                print(f"解析失败，跳过该行\n")
                continue
            parsed.append(row[6])   # 答案不用翻译
            writer.writerow(parsed)
            
    print(f"翻译结果已保存到: {output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量调用 DeepSeek 翻译")
    parser.add_argument('--input', required=True, help="输入 CSV 文件名")
    parser.add_argument('--language', required=True, help="目标语言，如 French, German, Japanese 等")
    parser.add_argument('--temperature', type=float, default=0.2, help="API 回答多样性，默认 0.2")
    parser.add_argument('--model', type=str, default="deepseek", help="使用的模型，如gpt、deepseek")
    args = parser.parse_args()

    translate(args)