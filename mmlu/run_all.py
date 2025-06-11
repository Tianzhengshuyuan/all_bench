import os
import subprocess
import shutil
import argparse

languages = [
    # ("中文", "chinese"),
    # ("西班牙语", "spanish"),
    # ("印地语", "hindi"),
    # ("阿拉伯语", "arabic"),
    # ("孟加拉语", "bengali"),
    # ("葡萄牙语", "portuguese"),
    # ("俄语", "russian"),
    ("日语", "japanese"),
    ("法语", "french")
]

parser = argparse.ArgumentParser()
parser.add_argument('--dir', required=True, help="输入文件夹名")
args = parser.parse_args()

 
input_dir = f"./{args.dir}"

for lang_cn, lang_en in languages:
    output_dir = f"{args.dir}_{lang_en}"
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        if not os.path.isfile(filepath):
            continue
        print(f"Translating {filename} to {lang_cn} ({lang_en})...")
        # 调用翻译脚本
        subprocess.run([
            "python", "translate2.py",
            "--input", filepath,
            "--language", lang_en
        ])
        # 假设translate2.py输出文件名为：原文件名_语言名.csv
        base = os.path.splitext(os.path.basename(filename))[0]
        output_name = f"{base}_{lang_en}.csv"
        # 移动到目标文件夹
        if os.path.exists(output_name):
            shutil.move(output_name, os.path.join(output_dir, output_name))
        else:
            print(f"Warning: {output_name} not found!")