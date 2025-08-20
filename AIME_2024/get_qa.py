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

def get_output_filename(input_name, language):
    # 获取不带扩展名的文件主名
    base = os.path.splitext(os.path.basename(input_name))[0]
    # 语言全部小写，空格换成下划线
    lang = language.strip().replace(" ", "_").lower()
    return f"{base}_{lang}.csv"
    
def select_and_merge(args):
    output_filename = get_output_filename(args.input, "english")

    # 读取输入 CSV
    with open(args.input, 'r', encoding='utf-8') as infile, \
         open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            writer.writerow([row[1], row[3]])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help="输入 CSV 文件名")
    args = parser.parse_args()

    select_and_merge(args)