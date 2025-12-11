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

doubao_client = Ark(api_key="196b33be-8abb-4af3-9fba-6e266b2dd942")
deepseek_client = OpenAI(api_key="sk-09da13b2c97948628523d042d6a02f06", base_url="https://api.deepseek.com")
kimi_client = OpenAI(api_key="sk-ODuizMlUC22phanBhvYz6dBjx2yrz7vhKhcjKnoIrYssThQo", base_url="https://api.moonshot.cn/v1")
qwen_client = OpenAI(api_key="sk-341becd932d743f2a750495a0f9f3ede", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

    
def call_doubao_api(question, temperature=0):
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
        print(f"调用 豆包 API 时出错: {e}")
        return "❌"
    
def call_deepseek_api(question, temperature=0):
    try:
        response = doubao_client.chat.completions.create(
            model="deepseek-v3-250324",
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
    
def   call_qwen_api(question, temperature=0):
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
    output_path = os.path.join(args.out_csv, get_output_filename(args.input, args.language))
    total_count = 0
    success_count = 0
    start_time = time.time()

    # 读取 original 文件内容并缓存到列表中
    with open(args.original, 'r', encoding='utf-8') as orifile:
        ori_reader = csv.reader(orifile)
        ori_rows = [row for row in ori_reader if row]  # 去除空行

    # 读取输入文件并翻译
    with open(args.input, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        for row in reader:
            if not row:
                continue
            total_count += 1
            question_text = row[0]          # 拼接题目
            answer_text = row[1] if len(row) > 1 else ""
            source_info = row[2] if len(row) > 2 else ""  # 形如 "2→3" 的来源信息

            # 从 "2→3" 提取题号
            match = re.match(r"(\d+)\s*→\s*(\d+)", source_info)
            if match:
                q1_id, q2_id = int(match.group(1)), int(match.group(2))
            else:
                print(f"⚠️ 无法从 '{source_info}' 提取题号，跳过该行。")
                continue

            # 获取原文中对应题目的内容
            try:
                q1_original = ori_rows[q1_id - 1][0]  # 文件中第 n 题，对应索引 n-1
                q2_original = ori_rows[q2_id - 1][0]
            except IndexError:
                print(f"⚠️ 题号 {q1_id} 或 {q2_id} 超出 original 文件范围，跳过。")
                continue

            # 构造提示词（Prompt）
            prompt = (
                f"{question_text}\n"
                f"把上面的内容翻译为 {args.language}，保留下面的翻译中翻译好的部分，最后得到上面这段话的完整{args.language}翻译，不要忘了翻译“Let the answer be $k$”：\n"
                f"{q1_original}"
                f"{q2_original}\n"
                f"只翻译，不解题，不要返回任何其他信息。"
            )

            # 调用模型
            if args.model == "qwen":
                print(f"🛰 调用 Qwen 模型翻译第 {total_count} 行：...")
                translation = call_qwen_api(prompt, temperature=args.temperature)
            elif args.model == "deepseek":
                print(f"🛰 调用 DeepSeek 模型翻译第 {total_count} 行：...")
                translation = call_deepseek_api(prompt, temperature=args.temperature)
            elif args.model == "kimi":
                print(f"🛰 调用 Kimi 模型翻译第 {total_count} 行：...")
                translation = call_kimi_api(prompt, temperature=args.temperature)
            elif args.model == "gpt":
                print(f"🛰 调用 GPT 模型翻译第 {total_count} 行：...")
                translation = call_gpt_api(prompt, temperature=args.temperature)
            elif args.model == "doubao":    
                print(f"🛰 调用 豆包 模型翻译第 {total_count} 行：...")
                translation = call_doubao_api(prompt, temperature=args.temperature)
            else:
                print(f"❌ 未知模型: {args.model}")
                translation = "❌"

            print(f"==== 第 {total_count} 行翻译结果 ====\n{translation}\n")
            success_count += 1

            # 写入输出文件
            writer.writerow([translation, answer_text, source_info])

    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / total_count if total_count > 0 else 0

    print(f"✅ 翻译结果保存到: {output_path}")
    print(f"总行数: {total_count}，成功翻译: {success_count}，平均耗时: {avg_time:.2f} 秒/行")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量调用 DeepSeek 翻译")
    parser.add_argument('--input', required=True, help="输入 CSV 文件名")
    parser.add_argument('--original', required=True, help="对应的MES文件")
    parser.add_argument('--out_csv', default='./csv', help="输出CSV 文件所在文件夹")
    parser.add_argument('--language', required=True, help="目标语言，如 French, German, Japanese 等")
    parser.add_argument('--temperature', type=float, default=0.2, help="API 回答多样性，默认 0.2")
    parser.add_argument('--model', type=str, default="deepseek", help="使用的模型，如gpt、deepseek、kimi、qwen")
    args = parser.parse_args()

    translate(args)