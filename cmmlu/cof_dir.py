import os
import subprocess
import shutil
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dir', required=True, help="输入文件夹名")

args = parser.parse_args()
 
input_dir = f"./{args.dir}"

output_dir = f"{args.dir}_filling"
os.makedirs(output_dir, exist_ok=True)
for filename in os.listdir(input_dir):
    filepath = os.path.join(input_dir, filename)
    if not os.path.isfile(filepath):
        continue
    print(f"Translating {filename} to gap filling...")
    # 调用翻译脚本
    subprocess.run([
        "python", "choice_to_filling.py",
        "--input", filepath,
    ])
    base = os.path.splitext(os.path.basename(filename))[0]
    output_name = f"{base}_filling.csv"
    # 移动到目标文件夹
    if os.path.exists(output_name):
        shutil.move(output_name, os.path.join(output_dir, output_name))
    else:
        print(f"Warning: {output_name} not found!")