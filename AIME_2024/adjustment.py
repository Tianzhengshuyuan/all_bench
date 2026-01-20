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
from volcenginesdkarkruntime import Ark

deepseek_client = OpenAI(api_key="sk-09da13b2c97948628523d042d6a02f06", base_url="https://api.deepseek.com")
qwen_client = OpenAI(api_key="sk-e6cfbb89c5f642aa9c0342974158fb96", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
doubao_client = Ark(api_key="196b33be-8abb-4af3-9fba-6e266b2dd942")

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
    
def call_doubao_api(question, temperature=0):
    """
    调用 doubao API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    try:
        response = doubao_client.chat.completions.create(
            model="doubao-1.5-pro-32k-250115",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 doubao API 时出错: {e}")
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
    return f"{lang}_{base}.csv"
    
def adjust(args):
    output_path = os.path.join(args.out_csv, get_output_filename(args.input, "adjusted"))
    
    # 如果设置了 --line 参数，处理单行更新逻辑
    if args.line is not None:
        # 读取输出文件（如果存在）的所有行
        output_rows = []
        if os.path.exists(output_path):
            with open(output_path, 'r', encoding='utf-8') as outfile:
                reader = csv.reader(outfile)
                output_rows = list(reader)
        
        # 读取输入文件，找到对应行的原始内容
        input_row = None
        with open(args.input, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            rows = list(reader)
            if args.line <= 0 or args.line > len(rows):
                print(f"错误: 行号 {args.line} 超出范围（文件共有 {len(rows)} 行）")
                return
            input_row = rows[args.line - 1]  # line 是 1-based
            
        if not input_row:
            print(f"错误: 第 {args.line} 行为空")
            return
        
        # 调用 API 调整该行
        prompt = f"请把下面的题目换一种说法表述，保持题目的答案不变，不要改变题目意思，不要改变数字，不要改变语言，只返回修改后的题目，不要返回任何其他内容：\n{input_row[0]}"
        print(f"原文:\n{input_row[0]}\n")
        if args.model == "deepseek":
            print("调用 deepseek API 进行转换...")
            adjustment = call_deepseek_api(prompt, temperature=args.temperature)
        elif args.model == "gpt":
            print("调用 gpt API 进行转换...")
            adjustment = call_gpt_api(prompt, temperature=args.temperature)
        elif args.model == "doubao":
            print("调用 doubao API 进行转换...")
            adjustment = call_doubao_api(prompt, temperature=args.temperature)
        elif args.model == "qwen":
            print("调用 Qwen API 进行转换...")
            adjustment = call_qwen_api(prompt, temperature=args.temperature)
        print(f"转换后的题目:\n{adjustment}\n")
        
        # 更新输出文件中对应行的内容
        # 确保 output_rows 有足够的行数
        while len(output_rows) < args.line:
            output_rows.append([])
        
        # 更新指定行（line 是 1-based，所以减 1）
        output_rows[args.line - 1] = [adjustment, input_row[1]]
        
        # 写回输出文件
        with open(output_path, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            for row in output_rows:
                writer.writerow(row)
        
        print(f"已更新第 {args.line} 行，结果已保存到: {output_path}")
        return
    
    # 原有的批量处理逻辑
    total_count = 0
    success_count = 0
    start_time = time.time()  # 记录开始时间
    # 读取输入 CSV
    with open(args.input, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:

            total_count += 1            
            if not row:  # 跳过空行
                continue
            if row[0] == "x":
                writer.writerow([row[0], row[1]])
                continue
            prompt = f"请把下面的题目换一种说法表述，保持题目的答案不变，不要改变题目意思，不要改变数字，不要改变语言，只返回修改后的题目，不要返回任何其他内容：\n{row[0]}"
            print(f"原文:\n{row[0]}\n")
            if args.model == "deepseek":
                print("调用 deepseek API 进行转换...")
                adjustment = call_deepseek_api(prompt, temperature=args.temperature)
            elif args.model == "gpt":
                print("调用 gpt API 进行转换...")
                adjustment = call_gpt_api(prompt, temperature=args.temperature)
            elif args.model == "doubao":
                print("调用 doubao API 进行转换...")
                adjustment = call_doubao_api(prompt, temperature=args.temperature)
            elif args.model == "qwen":
                print("调用 Qwen API 进行转换...")
                adjustment = call_qwen_api(prompt, temperature=args.temperature)
            print(f"转换后的题目:\n{adjustment}\n")
            success_count += 1
            writer.writerow([adjustment, row[1]])
    end_time = time.time()  # 记录结束时间
    total_time = end_time - start_time
    avg_time = total_time / total_count if total_count > 0 else 0
            
    print(f"转换结果已保存到: {output_path}，总共 {total_count} 行，成功转换 {success_count} 行，平均每行耗时 {avg_time:.2f} 秒")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量调用 DeepSeek 翻译")
    parser.add_argument('--input', required=True, help="输入 CSV 文件名")
    parser.add_argument('--out_csv', default='./csv', help="输出CSV 文件所在文件夹")
    parser.add_argument('--temperature', type=float, default=0.2, help="API 回答多样性，默认 0.2")
    parser.add_argument('--model', type=str, default="deepseek", help="使用的模型，如gpt、deepseek、kimi、qwen")
    parser.add_argument('--line', type=int, default=None, help="处理第几行")
    args = parser.parse_args()

    adjust(args)