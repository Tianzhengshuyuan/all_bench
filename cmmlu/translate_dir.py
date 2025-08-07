import os
import subprocess
import shutil
import argparse

languages = [
    # ("英语", "english"),
    # ("西班牙语", "spanish"),
    # ("印地语", "hindi"),
    ("阿拉伯语", "arabic"),
    # ("孟加拉语", "bengali"),
    # ("葡萄牙语", "portuguese"),
    ("俄语", "russian"),
    ("日语", "japanese"),
    ("法语", "french")
]

parser = argparse.ArgumentParser()
parser.add_argument('--dir', required=True, help="输入文件夹名")
parser.add_argument('--model', type=str, default="gpt", help="使用的模型，如gpt、deepseek")
parser.add_argument('--language', type=str, default=None, help="只翻译成某种语言（英文小写，如chinese, spanish, ...）")

args = parser.parse_args()

input_dir = f"./{args.dir}"

# 根据参数决定翻译哪些语言
if args.language:
    # 查找指定语言
    found = False
    for lang_cn, lang_en in languages:
        if lang_en == args.language.lower():
            target_languages = [(lang_cn, lang_en)]
            found = True
            break
    if not found:
        raise ValueError(f"指定的语言 {args.language} 不在支持列表中: {[l[1] for l in languages]}")
else:
    target_languages = languages

for lang_cn, lang_en in target_languages:
    output_dir = f"{args.dir}_{lang_en}"
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        if not os.path.isfile(filepath):
            continue
        print(f"Translating {filename} to {lang_cn} ({lang_en})...")
        # 调用翻译脚本
        subprocess.run([
            "python", "translate.py",
            "--input", filepath,
            "--language", lang_en,
            "--model", args.model
        ])
        # 假设translate.py输出文件名为：原文件名_语言名.csv
        base = os.path.splitext(os.path.basename(filename))[0]
        output_name = f"{base}_{lang_en}.csv"
        # 移动到目标文件夹
        if os.path.exists(output_name):
            shutil.move(output_name, os.path.join(output_dir, output_name))
        else:
            print(f"Warning: {output_name} not found!")