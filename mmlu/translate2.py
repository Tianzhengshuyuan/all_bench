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

def call_gpt_api(question, temperature=0.2):
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
        return "API 调用失败" 
    
def get_output_filename(input_name, language):
    # 获取不带扩展名的文件主名
    base = os.path.splitext(os.path.basename(input_name))[0]
    # 语言全部小写，空格换成下划线
    lang = language.strip().replace(" ", "_").lower()
    return f"{base}_{lang}.csv"

def parse_translation(translation):
    # 匹配每一部分
    question_keywords = {
        "chinese": r"问题",
        "spanish": r"pregunta",
        "hindi": r"प्रश्न",
        "arabic": r"سؤال",
        "bengali": r"প্রশ্ন",
        "portuguese": r"pergunta",
        "russian": r"вопрос",
        "japanese": r"問題",
        "french": r"question",
    }
    q_kw = question_keywords.get(args.language, r"question")
    pattern = re.compile(
        rf"{q_kw}\s*[:：]\s*(.*?)\s*\nA\s*[:：]\s*(.*?)\s*\nB\s*[:：]\s*(.*?)\s*\nC\s*[:：]\s*(.*?)\s*\nD\s*[:：]\s*(.*)",
        re.DOTALL | re.IGNORECASE
    )
    m = pattern.match(translation.strip())
    if m:
        return [m.group(i).strip() for i in range(1, 6)]
    
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
                f"question: {row[0]}\n"
                f"A: {row[1]}\n"
                f"B: {row[2]}\n"
                f"C: {row[3]}\n"
                f"D: {row[4]}"
            )

            prompt = f"Please translate the following content into {args.language}. Do not translate the word 'question' at the beginning. Only translate, do not return anything else: \n{text}"
            translation = call_gpt_api(prompt, temperature=args.temperature)
            print(f"原文:\n{text}\n翻译:\n{translation}\n")
            parsed = parse_translation(translation)
            parsed.append(row[5])   # 答案原样
            writer.writerow(parsed)
    print(f"翻译结果已保存到: {output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量调用 DeepSeek 翻译")
    parser.add_argument('--input', required=True, help="输入 CSV 文件名")
    parser.add_argument('--language', required=True, help="目标语言，如 French, German, Japanese 等")
    parser.add_argument('--temperature', type=float, default=0.2, help="API 回答多样性，默认 0.2")
    args = parser.parse_args()

    translate(args)