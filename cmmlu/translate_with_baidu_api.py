import csv
import argparse
import os
import re
from fractions import Fraction
from sympy import sympify, E
from sympy.core.sympify import SympifyError
import requests
import random
import json
from hashlib import md5

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
    
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

def call_baidu_api(query):
    # Set your own appid/appkey.
    appid = '20250620002386418'
    appkey = 'oWPnWhFG_caLFgZxwaSk'

    # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
    from_lang = 'zh'
    to_lang =  'spa' #en、jp、pt、fra、ara、spa

    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()

    # Show response
    print(json.dumps(result, indent=4, ensure_ascii=False))
    return 

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
                f"{row[1]}, "
                f"A: {row[2]}, "
                f"B: {row[3]}, "
                f"C: {row[4]}, "
                f"D: {row[5]}"
            )

            print(f"原文:\n{text}\n")
            translation = call_baidu_api(text)
            # print(f"翻译:\n{translation}\n")
            # parsed = parse_response(translation)
            # if parsed is None:
            #     print(f"解析失败，跳过该行\n")
            #     continue
            # parsed.append(row[6])   # 答案不用翻译
            # writer.writerow(parsed)
            
    print(f"翻译结果已保存到: {output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量调用 DeepSeek 翻译")
    parser.add_argument('--input', required=True, help="输入 CSV 文件名")
    parser.add_argument('--language', required=True, help="目标语言，如 French, German, Japanese 等")
    args = parser.parse_args()

    translate(args)