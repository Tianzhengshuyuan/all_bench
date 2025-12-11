import csv
import argparse
import os
import re
import time
import openai
from volcenginesdkarkruntime import Ark
from openai import OpenAI
from fractions import Fraction
from sympy import sympify, E
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

# == API 调用 ==
def call_doubao_api(question, temperature=0):
    try:
        response = doubao_client.chat.completions.create(
            model="doubao-1-5-pro-32k-250115",  # 注意模型名称拼写
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=args.temperature,
            stream=False,
        )
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"调用 豆包 API 时出错: {e}", file=sys.stderr)
        return "API 调用失败"
    
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
   
def parse_response(translation):
    # 匹配每一部分
    # pattern = re.compile(
    #     r"question\s*[:：]\s*(.*?)\s*\nA\s*[:：]\s*(.*?)\s*\nB\s*[:：]\s*(.*?)\s*\nC\s*[:：]\s*(.*?)\s*\nD\s*[:：]\s*(.*)",
    #     re.DOTALL | re.IGNORECASE
    # )
    pattern = re.compile(
        r"^(.*?)\s*\nA\s*[:：]\s*(.*?)\s*\nB\s*[:：]\s*(.*?)\s*\nC\s*[:：]\s*(.*?)\s*\nD\s*[:：]\s*(.*)$",
        re.DOTALL
    )
    m = pattern.match(translation.strip())
    if m:
        return [m.group(i).strip() for i in range(1, 6)]
    else:
        print("解析翻译结果时出错")
        return None
 
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
    start_time = time.time()  # 记录开始时间
    # 读取输入 CSV
    with open(args.input, 'r', encoding='utf-8') as infile, \
         open(args.original, 'r', encoding='utf-8') as orifile, \
         open(output_path, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        ori_reader = csv.reader(orifile)
        writer = csv.writer(outfile)

        for row, ori_row in zip(reader, ori_reader): 
            total_count += 1            
            if not row:  # 跳过空行
                continue
            text = (
                f"{row[0]}\n"
                f"A: {row[1]}\n"
                f"B: {row[2]}\n"
                f"C: {row[3]}\n"
                f"D: {row[4]}"
            )
            
            prompt = f"请把下面的内容翻译为 {args.language}. 四个选项的内容都要翻译，但是每个选项的标志如“A:”不用翻译，但是要保留其原来的英文形式。只翻译，不要返回任何其他内容 \n{text}"

            if args.model == "qwen":
                print("调用 Qwen API 进行翻译...")
                translation = call_qwen_api(prompt, temperature=args.temperature)
            elif args.model == "doubao":
                print("调用 豆包 API 进行翻译...")
                translation = call_doubao_api(prompt, temperature=args.temperature)
            print(f"问题翻译:\n{translation}\n")
            parsed = parse_response(translation)
            parsed.append(row[5])   # 答案不用翻译

            success_count += 1
            writer.writerow(parsed)

    end_time = time.time()  # 记录结束时间
    total_time = end_time - start_time
    avg_time = total_time / total_count if total_count > 0 else 0
            
    print(f"翻译结果已保存到: {output_path}，总共 {total_count} 行，成功翻译 {success_count} 行，平均每行耗时 {avg_time:.2f} 秒")

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