#!/usr/bin/env python3
import argparse
import pandas as pd
import glob
import os
import re

VARIABLES = [
    "question_type", "cot", "max_tokens", "top_p", "few", "mul",
    "presence_penalty", "Temperature",
    "lang_ey", "lang_zw", "lang_alby", "lang_fy", "lang_yy", "lang_ry",
    "question_tran"
]

def parse_anova_file(filepath, variables=VARIABLES):
    """解析单个 ANOVA 普通文本文件，返回变量 F 值加总排序表"""
    rows = []
    header_found = False
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # 跳过空行、分隔线
            if not line or line.startswith("=") or line.startswith("-"):
                continue
            # 找到表头
            if not header_found and "sum_sq" in line and "df" in line and "F" in line:
                header = re.split(r"\s+", line)
                header_found = True
                continue
            if header_found:
                parts = re.split(r"\s+", line)
                if len(parts) >= 4:  # 至少要有 effect, sum_sq, df, F
                    rows.append(parts)
    
    if not rows:
        print(f"[WARN] {filepath} 没有有效数据行")
        return None
    
    # 构建 dataframe
    df = pd.DataFrame(rows, columns=["effect", "sum_sq", "df", "F", "PR"])
    # 转换数值列
    for col in ["sum_sq", "df", "F", "PR"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    
    # 累加指定变量的 F 值
    results = {}
    for var in variables:
        mask = df["effect"].str.contains(rf"\b{var}\b", regex=True, na=False)
        results[var] = df.loc[mask, "F"].sum()
    
    out_df = pd.DataFrame(
        sorted(results.items(), key=lambda x: x[1], reverse=True),
        columns=["Variable", "F_sum"]
    )
    return out_df

def main():
    parser = argparse.ArgumentParser(description="批处理 ANOVA .log 文件，输出变量重要性排序（F 值求和）")
    parser.add_argument("--folder", type=str, help="包含 ANOVA 结果文件的文件夹路径 (例如 anova_result)")
    args = parser.parse_args()

    folder = args.folder
    if not os.path.isdir(folder):
        print(f"[ERROR] {folder} 不是有效目录")
        return

    files = glob.glob(os.path.join(folder, "*.log"))
    if not files:
        print(f"[WARN] 没有找到 .log 文件在 {folder}")
        return

    for filepath in files:
        print("="*80)
        print(f"File: {os.path.basename(filepath)}")
        result = parse_anova_file(filepath)
        if result is not None:
            print(result.to_string(index=False))
        else:
            print("[ERROR] 无法解析此文件")

if __name__ == "__main__":
    main()