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
   
def parse_translation(translation: str):
    if not isinstance(translation, str):
        return str(translation), ""

    text = translation.strip()

    # 按 '####' 分割
    parts = text.split("####")
    # 例如 "####题目####答案####" -> ["", "题目", "答案", ""]
    # 过滤掉纯空白部分
    parts = [p.strip() for p in parts if p.strip() != ""]

    if len(parts) >= 2:
        question = parts[0]
        answer = parts[1]
        return question, answer
    elif len(parts) == 1:
        # 只有一个内容，认为是题目
        return parts[0], ""
    else:
        # 完全无法解析
        return text, ""
 
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

            # prompt = f"{row[0]}\n请把上面的内容翻译为 {args.language}。保留下面这个部分翻译版本中的全部内容，只新增下面这个翻译中不存在的部分到相应位置：\n{ori_row[0]}\n只翻译，不要返回任何其他信息"
            # prompt = f"{row[0]}\n请把上面的内容转换为 {args.language}。保留下面这个翻译版本中的全部内容，只改变与之不同的数字：\n{ori_row[0]}\n只转换，不要返回任何其他信息"
            # prompt = f"{row[0]}\n请把上面的内容转换为 {args.language}。只转换，不要返回任何其他信息"
            prompt = f"Question:{row[0]}\nAnswer:{row[1]}\n请把上面的题目和答案的内容均翻译为 {args.language}，不要忘记翻译答案，翻译后的版本不要包含“问题”、“答案”字样。只翻译，不要返回任何其他信息。如果题目是填空题，不要用正确答案填充题目，保留题目原来的形式。最终结果使用####隔开，例如：####指数函数 $ y = a^x $ 与对数函数 $ y = \log_a x $ 的图像关于哪条直线对称？####y=x####"
            if args.model == "qwen":
                print("调用 Qwen API 进行翻译...")
                translation = call_qwen_api(prompt, temperature=args.temperature)
            elif args.model == "doubao":
                print("调用 豆包 API 进行翻译...")
                translation = call_doubao_api(prompt, temperature=args.temperature)
            print(f"问题翻译:\n{translation}\n")
            question_parsed, answer_parsed = parse_translation(translation)
            success_count += 1
            # writer.writerow([translation, row[1]])
            writer.writerow([question_parsed, answer_parsed])
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