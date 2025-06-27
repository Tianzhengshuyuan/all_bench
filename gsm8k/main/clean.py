import argparse
import csv
import os
import re

def extract_answer(text):
    # 先尝试匹配 #### 后的内容直到引号或结尾或换行
    match = re.search(r'####\s*([^\n"]+)', text)
    if match:
        return match.group(1).strip()
    return ""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract answer from csv.")
    parser.add_argument("--input", required=True, help="Input csv file")
    args = parser.parse_args()

    input_file = args.input
    base, ext = os.path.splitext(input_file)
    output_file = f"{base}-clean{ext}"

    with open(input_file, "r", encoding="utf-8") as fin, \
         open(output_file, "w", encoding="utf-8", newline='') as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        header = next(reader)

        for row in reader:
            q = row[0]
            a = row[1]
            clean_a = extract_answer(a)
            writer.writerow([q, clean_a])