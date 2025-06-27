import os
import json
import csv
import re
import argparse

def extract_boxed(text):
    start = text.find(r'\boxed{')
    if start == -1:
        return ""
    i = start + len(r'\boxed{')
    brace_count = 1
    boxed_content = []
    while i < len(text):
        if text[i] == '{':
            brace_count += 1
            boxed_content.append('{')
        elif text[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                return ''.join(boxed_content)
            boxed_content.append('}')
        else:
            boxed_content.append(text[i])
        i += 1
    return ""

def process_dir(dir_path, out_dir):
    dir_name = os.path.basename(dir_path.rstrip("/\\"))
    csv_path = os.path.join(out_dir, f"{dir_name}.csv")

    rows = []
    for fname in os.listdir(dir_path):
        if fname.endswith(".json"):
            json_path = os.path.join(dir_path, fname)
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            problem = data.get("problem", "")
            solution = data.get("solution", "")
            boxed = extract_boxed(solution)
            rows.append([problem, boxed])

    if rows:
        with open(csv_path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        print(f"Saved {csv_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract problems and boxed answers from all subdirectories.")
    parser.add_argument("--dir", type=str, required=True, help="Root directory containing subdirectories with .json files.")
    parser.add_argument("--out_dir", type=str, default="test_clean", help="Directory to save csv files.")
    args = parser.parse_args()

    root_dir = args.dir
    out_dir = args.out_dir

    # 新建输出目录
    os.makedirs(out_dir, exist_ok=True)

    for subdir in os.listdir(root_dir):
        subdir_path = os.path.join(root_dir, subdir)
        if os.path.isdir(subdir_path):
            process_dir(subdir_path, out_dir)