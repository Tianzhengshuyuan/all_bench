import csv
import argparse
import os
import re
import time
import random
import openai
from openai import OpenAI
from fractions import Fraction
from sympy import sympify, E
from volcenginesdkarkruntime import Ark
from sympy.core.sympify import SympifyError

deepseek_client = OpenAI(api_key="sk-09da13b2c97948628523d042d6a02f06", base_url="https://api.deepseek.com")
kimi_client = OpenAI(api_key="sk-ODuizMlUC22phanBhvYz6dBjx2yrz7vhKhcjKnoIrYssThQo", base_url="https://api.moonshot.cn/v1")
qwen_client = OpenAI(api_key="sk-341becd932d743f2a750495a0f9f3ede", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
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
    
def call_doubao_api(question):
    """
    调用 豆包 API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
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
            
def extract_distractors(response, correct_answer):
    """
    用一个正则表达式一次性提取连续的三个干扰项，形如####干扰1####干扰2####干扰3####。
    """
    # 支持跨行，允许中间有空白
    match = re.search(r'####\s*(.*?)\s*####\s*(.*?)\s*####\s*(.*?)\s*####', response, re.DOTALL)
    distractors = []
    if match:
        # 提取三个分组
        for i in range(1, 4):
            d = match.group(i).strip()
            # 过滤非法和重复、和正确答案相同的项
            if is_number(d) and d != str(correct_answer).strip() and d not in distractors:
                distractors.append(d)
    return distractors

def translate(args):
    total_count = 0
    success_count = 0
    start_time = time.time()
    
    # 新增：准备输出文件名
    output_filename = os.path.splitext(args.input)[0] + f"_choice.csv"
    outfile = open(output_filename, 'w', encoding='utf-8', newline='')
    writer = csv.writer(outfile)
    
    # 读取输入 CSV
    with open(args.input, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        for row in reader:
            total_count += 1            
            if not row or len(row) < 2:  # 跳过空行或无答案行
                continue

            question = row[0]
            correct_answer = str(row[1]).strip()
            prompt = f"下面是一个数学填空题，问题是：{question}，答案是：{correct_answer}。我想将其变为一道选择题，还需要三个干扰答案，请帮我生成三个干扰答案，并且用####将其包围和分隔，例如：####干扰答案1####干扰答案2####干扰答案3####。请注意，干扰答案必须是数字，且不能与正确答案相同。"
            print(f"原题:\n{question}\n答案:\n{correct_answer}\n")
            if args.model == "deepseek":
                print("调用 deepseek API 进行转换...")
                translation = call_deepseek_api(prompt, temperature=args.temperature)
            elif args.model == "gpt":
                print("调用 gpt API 进行转换...")
                translation = call_gpt_api(prompt, temperature=args.temperature)
            elif args.model == "kimi":
                print("调用 Kimi API 进行转换...")
                translation = call_kimi_api(prompt, temperature=args.temperature)
            elif args.model == "qwen":
                print("调用 Qwen API 进行转换...")
                translation = call_qwen_api(prompt, temperature=args.temperature)
            elif args.model == "doubao":
                print("调用 豆包 API 进行转换...")
                translation = call_doubao_api(prompt)
            else:
                print("未知API模型类型")
                translation = ""
            print(f"转换结果:\n{translation}\n")
            
            # 提取干扰答案
            distractors = extract_distractors(translation, correct_answer)
            if len(distractors) < 3:
                print(f"❌ 干扰项不足3个，跳过本题（干扰项为：{distractors}）")
                continue

            # 合并正确答案与干扰项 & 打乱顺序
            options = distractors + [correct_answer]
            random.shuffle(options)
            # 答案位置（A/B/C/D）
            answer_index = options.index(correct_answer)
            answer_letter = ['A', 'B', 'C', 'D'][answer_index]
            # 写入文件
            writer.writerow([question] + options + [answer_letter])
            success_count += 1
    
    outfile.close()
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / total_count if total_count > 0 else 0
            
    print(f"转换结果已保存到: {output_filename}，总共 {total_count} 行，成功转换 {success_count} 行，平均每行耗时 {avg_time:.2f} 秒")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help="输入 CSV 文件名")
    parser.add_argument('--temperature', type=float, default=0.2, help="API 回答多样性，默认 0.2")
    parser.add_argument('--model', type=str, default="deepseek", help="使用的模型，如gpt、deepseek、kimi、qwen")
    args = parser.parse_args()

    translate(args)