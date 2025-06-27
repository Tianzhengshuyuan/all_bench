import csv
import argparse
import os
import re
import time
import openai
from openai import OpenAI
from fractions import Fraction
from sympy import sympify, E
from sympy.core.sympify import SympifyError

deepseek_client = OpenAI(api_key="sk-09da13b2c97948628523d042d6a02f06", base_url="https://api.deepseek.com")
kimi_client = OpenAI(api_key="sk-ODuizMlUC22phanBhvYz6dBjx2yrz7vhKhcjKnoIrYssThQo", base_url="https://api.moonshot.cn/v1")
qwen_client = OpenAI(api_key="sk-341becd932d743f2a750495a0f9f3ede", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

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
    
def call_qwen_api(question, temperature=0):
    try:
        response = qwen_client.chat.completions.create(
            model="qwen-plus", 
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': question},
            ],
            temperature=temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 Qwen API 时出错: {e}")
        return "❌"
    
def get_output_filename(input_name, language):
    # 获取不带扩展名的文件主名
    base = os.path.splitext(os.path.basename(input_name))[0]
    # 语言全部小写，空格换成下划线
    lang = language.strip().replace(" ", "_").lower()
    return f"{base}_{lang}.csv"
    
def translate(args):
    output_filename = get_output_filename(args.input, args.language)
    total_count = 0
    success_count = 0
    start_time = time.time()  # 记录开始时间
    # 读取输入 CSV
    with open(args.input, 'r', encoding='utf-8') as infile, \
         open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            total_count += 1            
            if not row:  # 跳过空行
                continue

            prompt = f"Please translate the following content into {args.language}. Only translate, do not return anything else: \n{row[0]}"
            print(f"原文:\n{row[0]}\n")
            if args.model == "deepseek":
                print("调用 deepseek API 进行翻译...")
                translation = call_deepseek_api(prompt, temperature=args.temperature)
            elif args.model == "gpt":
                print("调用 gpt API 进行翻译...")
                translation = call_gpt_api(prompt, temperature=args.temperature)
            elif args.model == "kimi":
                print("调用 Kimi API 进行翻译...")
                translation = call_kimi_api(prompt, temperature=args.temperature)
            elif args.model == "qwen":
                print("调用 Qwen API 进行翻译...")
                translation = call_qwen_api(prompt, temperature=args.temperature)
            print(f"翻译:\n{translation}\n")
            success_count += 1
            writer.writerow([translation, row[1]])
    end_time = time.time()  # 记录结束时间
    total_time = end_time - start_time
    avg_time = total_time / total_count if total_count > 0 else 0
            
    print(f"翻译结果已保存到: {output_filename}，总共 {total_count} 行，成功翻译 {success_count} 行，平均每行耗时 {avg_time:.2f} 秒")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量调用 DeepSeek 翻译")
    parser.add_argument('--input', required=True, help="输入 CSV 文件名")
    parser.add_argument('--language', required=True, help="目标语言，如 French, German, Japanese 等")
    parser.add_argument('--temperature', type=float, default=0.2, help="API 回答多样性，默认 0.2")
    parser.add_argument('--model', type=str, default="deepseek", help="使用的模型，如gpt、deepseek、kimi、qwen")
    args = parser.parse_args()

    translate(args)