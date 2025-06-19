import csv
import argparse
import os
from openai import OpenAI
from fractions import Fraction
from sympy import sympify, E
from sympy.core.sympify import SympifyError

deepseek_client = OpenAI(api_key="sk-09da13b2c97948628523d042d6a02f06", base_url="https://api.deepseek.com")
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
    
def call_deepseek_api(question, temperature=0.2):
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
        return "API 调用失败"

def get_output_filename(input_name, language):
    # 获取不带扩展名的文件主名
    base = os.path.splitext(os.path.basename(input_name))[0]
    # 语言全部小写，空格换成下划线
    lang = language.strip().replace(" ", "_").lower()
    return f"{base}_{lang}.csv"

def translate(args):
    output_filename = get_output_filename(args.input, args.language)
    # 读取输入 CSV
    with open(args.input, 'r', encoding='utf-8') as infile, \
         open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        writer.writerow(['原文', f'翻译（{args.language}）'])  # 写表头

        for row in reader:
            if not row:  # 跳过空行
                continue
            translated_row = []
            for i in range(5):  # 前5列
                cell = row[i]
                if is_number(cell):
                    translated_row.append(cell)
                else:
                    prompt = f"请将以下内容翻译成{args.language}。只翻译，不要返回任何其他内容：\n{cell}"
                    translation = call_deepseek_api(prompt, temperature=args.temperature)
                    print(f"原文: {cell}\n翻译: {translation}\n")
                    translated_row.append(translation)
            # 保留第6列（答案）原样
            translated_row.append(row[5])
            writer.writerow(translated_row)
    print(f"翻译结果已保存到: {output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量调用 DeepSeek 翻译")
    parser.add_argument('--input', required=True, help="输入 CSV 文件名")
    parser.add_argument('--language', required=True, help="目标语言，如 French, German, Japanese 等")
    parser.add_argument('--temperature', type=float, default=0.2, help="API 回答多样性，默认 0.2")
    args = parser.parse_args()

    translate(args)